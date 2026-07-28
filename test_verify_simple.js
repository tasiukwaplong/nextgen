
const ALL_BRIEFS = JSON.parse(document.getElementById('briefs-data').textContent);

let currentTrack = 'ALL';
let currentSearch = '';
let currentDiff = 'ALL';
let currentSort = 'id_asc';
let viewMode = 'grid';
let activeModalBriefId = null;

const trackList = [
    'AI - Machine Learning',
    'Animation',
    'Cloud Computing',
    'UI-UX Design',
    'Data Analysis and Visualization',
    'Data Science',
    'DevOps',
    'Game Development',
    'Product Management',
    'Quality Assurance',
    'Software Development',
    'Cybersecurity'
];

document.addEventListener('DOMContentLoaded', () => {
    renderTrackPills();
    renderFilteredBriefs();

    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            document.getElementById('search-input').focus();
        }
    });
});

function renderTrackPills() {
    const container = document.getElementById('track-pills');
    
    let html = `<button class="track-pill active" onclick="selectTrack('ALL')">All Tracks (${ALL_BRIEFS.length})</button>`;
    
    trackList.forEach(track => {
        const count = ALL_BRIEFS.filter(b => b.track === track).length;
        html += `<button class="track-pill" data-track="${track}" onclick="selectTrack('${track}')">${track} (${count})</button>`;
    });
    
    container.innerHTML = html;
}

function selectTrack(track) {
    currentTrack = track;
    document.querySelectorAll('.track-pill').forEach(btn => {
        if (btn.getAttribute('data-track') === track || (track === 'ALL' && btn.innerText.includes('All Tracks'))) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    document.getElementById('active-track-name').innerText = track === 'ALL' ? 'All Tracks' : track;
    renderFilteredBriefs();
}

function renderFilteredBriefs() {
    currentDiff = document.getElementById('diff-filter').value;
    currentSort = document.getElementById('sort-select').value;
    
    let filtered = ALL_BRIEFS.filter(b => {
        const matchTrack = (currentTrack === 'ALL' || b.track === currentTrack);
        const matchDiff = (currentDiff === 'ALL' || b.difficulty === currentDiff);
        
        let matchSearch = true;
        if (currentSearch) {
            const q = currentSearch.toLowerCase();
            matchSearch = (
                b.id.toLowerCase().includes(q) ||
                b.title.toLowerCase().includes(q) ||
                b.problem.toLowerCase().includes(q) ||
                b.solution.toLowerCase().includes(q) ||
                b.features.toLowerCase().includes(q) ||
                b.deliverables.toLowerCase().includes(q) ||
                b.tools.toLowerCase().includes(q) ||
                b.track.toLowerCase().includes(q) ||
                b.difficulty.toLowerCase().includes(q)
            );
        }
        return matchTrack && matchDiff && matchSearch;
    });

    filtered.sort((a, b) => {
        if (currentSort === 'id_asc') return a.id.localeCompare(b.id, undefined, {numeric: true});
        if (currentSort === 'id_desc') return b.id.localeCompare(a.id, undefined, {numeric: true});
        if (currentSort === 'title_asc') return a.title.localeCompare(b.title);
        if (currentSort === 'title_desc') return b.title.localeCompare(a.title);
        if (currentSort === 'track_asc') return a.track.localeCompare(b.track);
        if (currentSort === 'diff') {
            const level = { 'Beginner': 1, 'Beginner-Intermediate': 2, 'Intermediate': 3 };
            return (level[a.difficulty] || 1) - (level[b.difficulty] || 1);
        }
        return 0;
    });

    document.getElementById('results-count').innerText = `Showing ${filtered.length} of ${ALL_BRIEFS.length} briefs`;
    
    if (filtered.length === 0) {
        document.getElementById('briefs-grid').style.display = 'none';
        document.getElementById('briefs-table-container').style.display = 'none';
        document.getElementById('empty-state').style.display = 'block';
        return;
    } else {
        document.getElementById('empty-state').style.display = 'none';
    }

    if (viewMode === 'grid') {
        document.getElementById('briefs-grid').style.display = 'grid';
        document.getElementById('briefs-table-container').style.display = 'none';
        renderGridCards(filtered);
    } else {
        document.getElementById('briefs-grid').style.display = 'none';
        document.getElementById('briefs-table-container').style.display = 'block';
        renderTableRows(filtered);
    }
}

function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function highlightText(text, search) {
    if (!search || !text) return text || '';
    const safeSearch = escapeRegExp(search);
    const regex = new RegExp(`(${safeSearch})`, 'gi');
    return text.replace(regex, '<span class="highlight-text">$1</span>');
}

function renderGridCards(briefs) {
    const container = document.getElementById('briefs-grid');
    let html = '';
    
    briefs.forEach(b => {
        const diffClass = b.difficulty === 'Beginner' ? 'diff-beginner' : (b.difficulty === 'Intermediate' ? 'diff-intermediate' : 'diff-beginner-intermediate');
        const featureList = (b.features || '').split(';').slice(0, 3);
        const chipsHtml = featureList.map(f => `<span class="feature-chip">${highlightText(f.trim(), currentSearch)}</span>`).join('');

        html += `
        <div class="brief-card" onclick="openModal('${b.id}')">
            <div class="card-header">
                <span class="brief-id-badge">${highlightText(b.id, currentSearch)}</span>
                <span class="diff-badge ${diffClass}">${b.difficulty}</span>
            </div>

            <div>
                <div class="brief-track-name">${b.track}</div>
                <h3 class="brief-title">${highlightText(b.title, currentSearch)}</h3>
            </div>

            <div class="brief-problem">
                <strong>Problem:</strong> ${highlightText(b.problem, currentSearch)}
            </div>

            <div class="brief-solution">
                <strong>Scope:</strong> ${highlightText(b.solution, currentSearch)}
            </div>

            <div class="card-features-chips">
                ${chipsHtml}
            </div>
        </div>
        `;
    });
    
    container.innerHTML = html;
}

function renderTableRows(briefs) {
    const tbody = document.getElementById('briefs-table-body');
    let html = '';
    
    briefs.forEach(b => {
        const diffClass = b.difficulty === 'Beginner' ? 'diff-beginner' : (b.difficulty === 'Intermediate' ? 'diff-intermediate' : 'diff-beginner-intermediate');

        html += `
        <tr onclick="openModal('${b.id}')">
            <td><strong class="brief-id-badge-sm">${b.id}</strong></td>
            <td style="font-weight:600;">${b.track}</td>
            <td><strong>${b.title}</strong></td>
            <td style="max-width: 260px; color:var(--text-muted);">${b.problem}</td>
            <td style="max-width: 260px;">${b.solution}</td>
            <td><span class="diff-badge ${diffClass}">${b.difficulty}</span></td>
        </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function handleSearchInput() {
    const val = document.getElementById('search-input').value;
    currentSearch = val;
    const clearBtn = document.getElementById('clear-search-btn');
    if (val) clearBtn.classList.add('visible');
    else clearBtn.classList.remove('visible');
    renderFilteredBriefs();
}

function clearSearch() {
    document.getElementById('search-input').value = '';
    currentSearch = '';
    document.getElementById('clear-search-btn').classList.remove('visible');
    renderFilteredBriefs();
}

function resetFilters() {
    document.getElementById('search-input').value = '';
    currentSearch = '';
    currentDiff = 'ALL';
    currentSort = 'id_asc';
    document.getElementById('diff-filter').value = 'ALL';
    document.getElementById('sort-select').value = 'id_asc';
    selectTrack('ALL');
}

function setViewMode(mode) {
    viewMode = mode;
    document.getElementById('view-grid-btn').classList.toggle('active', mode === 'grid');
    document.getElementById('view-table-btn').classList.toggle('active', mode === 'table');
    renderFilteredBriefs();
}

function openModal(id) {
    const brief = ALL_BRIEFS.find(b => b.id === id);
    if (!brief) return;
    activeModalBriefId = id;

    document.getElementById('modal-brief-id').innerText = brief.id;
    document.getElementById('modal-track').innerText = brief.track;
    document.getElementById('modal-diff').innerText = brief.difficulty;
    document.getElementById('modal-title').innerText = brief.title;
    document.getElementById('modal-problem').innerText = brief.problem;
    document.getElementById('modal-solution').innerText = brief.solution;
    document.getElementById('modal-features').innerText = brief.features;
    document.getElementById('modal-deliverables').innerText = brief.deliverables;
    document.getElementById('modal-tools').innerText = brief.tools;

    document.getElementById('brief-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('brief-modal').classList.remove('active');
}

function closeModalOnBackdrop(e) {
    if (e.target.id === 'brief-modal') closeModal();
}

function copyBriefLink() {
    if (!activeModalBriefId) return;
    const brief = ALL_BRIEFS.find(b => b.id === activeModalBriefId);
    const text = `3MTT Brief [${brief.id}]: ${brief.title}\nTrack: ${brief.track}\nProblem: ${brief.problem}\nScope: ${brief.solution}\nDeliverables: ${brief.deliverables}\nTools: ${brief.tools}`;
    navigator.clipboard.writeText(text);
    showToast('Brief text copied to clipboard.');
}

function exportFilteredCSV() {
    let filtered = ALL_BRIEFS.filter(b => {
        const matchTrack = (currentTrack === 'ALL' || b.track === currentTrack);
        const matchDiff = (currentDiff === 'ALL' || b.difficulty === currentDiff);
        return matchTrack && matchDiff;
    });

    let csv = 'Brief ID,Track,Title,Difficulty,Problem Context,What to Build (MVP),Core MVP Features,Expected Deliverables,Suggested Tools\n';
    
    filtered.forEach(b => {
        const escape = (str) => `"${(str || '').replace(/"/g, '""')}"`;
        csv += `${escape(b.id)},${escape(b.track)},${escape(b.title)},${escape(b.difficulty)},${escape(b.problem)},${escape(b.solution)},${escape(b.features)},${escape(b.deliverables)},${escape(b.tools)}\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `3MTT_Project_Briefs_${currentTrack.replace(/[^a-zA-Z0-9]/g, '_')}.csv`);
    link.click();
    showToast('Exported briefs to CSV.');
}

function toggleTheme() {
    const isLight = document.body.getAttribute('data-theme') === 'light';
    if (isLight) {
        document.body.removeAttribute('data-theme');
        document.getElementById('theme-btn').innerText = 'Theme: Dark';
    } else {
        document.body.setAttribute('data-theme', 'light');
        document.getElementById('theme-btn').innerText = 'Theme: Light';
    }
}

function showToast(msg) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerText = msg;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
}

    