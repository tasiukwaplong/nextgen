
const ALL_BRIEFS = JSON.parse(document.getElementById('briefs-data').textContent);
const DATA_SOURCES = JSON.parse(document.getElementById('sources-data').textContent);

let currentTrack = 'ALL';
let currentSearch = '';
let currentDiff = 'ALL';
let currentSort = 'id_asc';
let viewMode = 'grid';
let bookmarks = new Set(JSON.parse(localStorage.getItem('brief_bookmarks') || '[]'));
let activeModalBriefId = null;

const trackColors = {
    'AI - Machine Learning': { bg: 'rgba(16, 185, 129, 0.15)', text: '#34D399', border: 'rgba(16, 185, 129, 0.4)', icon: '🤖' },
    'Animation': { bg: 'rgba(139, 92, 246, 0.15)', text: '#A78BFA', border: 'rgba(139, 92, 246, 0.4)', icon: '🎬' },
    'Cloud Computing': { bg: 'rgba(6, 182, 212, 0.15)', text: '#22D3EE', border: 'rgba(6, 182, 212, 0.4)', icon: '☁️' },
    'UI-UX Design': { bg: 'rgba(236, 72, 153, 0.15)', text: '#F472B6', border: 'rgba(236, 72, 153, 0.4)', icon: '🎨' },
    'Data Analysis and Visualization': { bg: 'rgba(20, 184, 166, 0.15)', text: '#2DD4BF', border: 'rgba(20, 184, 166, 0.4)', icon: '📊' },
    'Data Science': { bg: 'rgba(99, 102, 241, 0.15)', text: '#818CF8', border: 'rgba(99, 102, 241, 0.4)', icon: '🔬' },
    'DevOps': { bg: 'rgba(245, 158, 11, 0.15)', text: '#FBBF24', border: 'rgba(245, 158, 11, 0.4)', icon: '⚙️' },
    'Game Development': { bg: 'rgba(217, 70, 239, 0.15)', text: '#E879F9', border: 'rgba(217, 70, 239, 0.4)', icon: '🎮' },
    'Product Management': { bg: 'rgba(132, 204, 22, 0.15)', text: '#A3E635', border: 'rgba(132, 204, 22, 0.4)', icon: '📋' },
    'Quality Assurance': { bg: 'rgba(239, 68, 68, 0.15)', text: '#F87171', border: 'rgba(239, 68, 68, 0.4)', icon: '🧪' },
    'Software Development': { bg: 'rgba(59, 130, 246, 0.15)', text: '#60A5FA', border: 'rgba(59, 130, 246, 0.4)', icon: '💻' },
    'Cybersecurity': { bg: 'rgba(234, 179, 8, 0.15)', text: '#FACC15', border: 'rgba(234, 179, 8, 0.4)', icon: '🛡️' }
};

const criteriaList = [
    { key: 'c1', name: 'Adherence to Brief & Completeness', weight: 20 },
    { key: 'c2', name: 'Functionality / Effectiveness', weight: 25 },
    { key: 'c3', name: 'Technical Quality / Craft', weight: 15 },
    { key: 'c4', name: 'User Experience / Clarity', weight: 15 },
    { key: 'c5', name: 'Innovation & Nigerian-Context Fit', weight: 10 },
    { key: 'c6', name: 'Documentation & Demo Video', weight: 15 }
];

let ratings = { c1: 3, c2: 3, c3: 3, c4: 3, c5: 3, c6: 3 };

document.addEventListener('DOMContentLoaded', () => {
    renderTrackPills();
    renderFilteredBriefs();
    renderDataSources();
    initCalculator();
    updateBookmarkBadge();

    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            document.getElementById('search-input').focus();
        }
    });
});

function renderTrackPills() {
    const container = document.getElementById('track-pills');
    const tracks = Object.keys(trackColors);
    
    let html = `<button class="track-pill active" onclick="selectTrack('ALL')">🚀 All Tracks (240)</button>`;
    
    tracks.forEach(track => {
        const count = ALL_BRIEFS.filter(b => b.track === track).length;
        const icon = trackColors[track]?.icon || '📁';
        html += `<button class="track-pill" data-track="${track}" onclick="selectTrack('${track}')">${icon} ${track} (${count})</button>`;
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
        const style = trackColors[b.track] || { bg: 'rgba(255,255,255,0.1)', text: '#FFF', border: 'transparent' };
        const isBookmarked = bookmarks.has(b.id);
        const diffClass = b.difficulty === 'Beginner' ? 'diff-beginner' : (b.difficulty === 'Intermediate' ? 'diff-intermediate' : 'diff-beginner-intermediate');
        
        const featureList = (b.features || '').split(';').slice(0, 3);
        const chipsHtml = featureList.map(f => `<span class="feature-chip">${highlightText(f.trim(), currentSearch)}</span>`).join('');

        html += `
        <div class="brief-card" onclick="openModal('${b.id}')">
            <div class="card-header">
                <span class="brief-id-badge" style="background:${style.bg}; color:${style.text}; border:1px solid ${style.border};">${highlightText(b.id, currentSearch)}</span>
                <div class="card-meta-right">
                    <span class="diff-badge ${diffClass}">${b.difficulty}</span>
                    <button class="bookmark-star-btn ${isBookmarked ? 'bookmarked' : ''}" onclick="event.stopPropagation(); toggleBookmark('${b.id}')">
                        ${isBookmarked ? '★' : '☆'}
                    </button>
                </div>
            </div>

            <div>
                <div class="brief-track-name" style="color:${style.text}">${b.track}</div>
                <h3 class="brief-title">${highlightText(b.title, currentSearch)}</h3>
            </div>

            <div class="brief-problem">
                🇳🇬 <strong>Problem:</strong> ${highlightText(b.problem, currentSearch)}
            </div>

            <div class="brief-solution">
                🚀 ${highlightText(b.solution, currentSearch)}
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
        const style = trackColors[b.track] || { text: '#FFF' };
        const diffClass = b.difficulty === 'Beginner' ? 'diff-beginner' : (b.difficulty === 'Intermediate' ? 'diff-intermediate' : 'diff-beginner-intermediate');
        const isBookmarked = bookmarks.has(b.id);

        html += `
        <tr onclick="openModal('${b.id}')">
            <td><strong style="color:var(--accent-emerald);">${b.id}</strong></td>
            <td style="color:${style.text}; font-weight:600;">${b.track}</td>
            <td><strong>${b.title}</strong></td>
            <td style="max-width: 250px; color:var(--text-muted);">${b.problem}</td>
            <td style="max-width: 250px;">${b.solution}</td>
            <td><span class="diff-badge ${diffClass}">${b.difficulty}</span></td>
            <td>
                <button class="bookmark-star-btn ${isBookmarked ? 'bookmarked' : ''}" onclick="event.stopPropagation(); toggleBookmark('${b.id}')">
                    ${isBookmarked ? '★' : '☆'}
                </button>
            </td>
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

    const isBookmarked = bookmarks.has(brief.id);
    const bmBtn = document.getElementById('modal-bookmark-btn');
    bmBtn.innerText = isBookmarked ? '★ Bookmarked' : '☆ Bookmark';

    document.getElementById('brief-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('brief-modal').classList.remove('active');
}

function closeModalOnBackdrop(e) {
    if (e.target.id === 'brief-modal') closeModal();
}

function toggleModalBookmark() {
    if (activeModalBriefId) {
        toggleBookmark(activeModalBriefId);
        const isBookmarked = bookmarks.has(activeModalBriefId);
        document.getElementById('modal-bookmark-btn').innerText = isBookmarked ? '★ Bookmarked' : '☆ Bookmark';
    }
}

function toggleBookmark(id) {
    if (bookmarks.has(id)) {
        bookmarks.delete(id);
        showToast(`Removed ${id} from bookmarks`);
    } else {
        bookmarks.add(id);
        showToast(`Saved ${id} to bookmarks ⭐`);
    }
    localStorage.setItem('brief_bookmarks', JSON.stringify(Array.from(bookmarks)));
    updateBookmarkBadge();
    renderFilteredBriefs();
    renderBookmarksPage();
}

function updateBookmarkBadge() {
    document.getElementById('bookmark-count-badge').innerText = bookmarks.size;
}

function renderBookmarksPage() {
    const container = document.getElementById('bookmarks-grid');
    const empty = document.getElementById('bookmarks-empty');
    const bookmarkedBriefs = ALL_BRIEFS.filter(b => bookmarks.has(b.id));

    if (bookmarkedBriefs.length === 0) {
        container.style.display = 'none';
        empty.style.display = 'block';
        return;
    }

    empty.style.display = 'none';
    container.style.display = 'grid';

    let html = '';
    bookmarkedBriefs.forEach(b => {
        const style = trackColors[b.track] || { bg: 'rgba(255,255,255,0.1)', text: '#FFF' };
        const diffClass = b.difficulty === 'Beginner' ? 'diff-beginner' : (b.difficulty === 'Intermediate' ? 'diff-intermediate' : 'diff-beginner-intermediate');

        html += `
        <div class="brief-card" onclick="openModal('${b.id}')">
            <div class="card-header">
                <span class="brief-id-badge" style="background:${style.bg}; color:${style.text};">${b.id}</span>
                <div class="card-meta-right">
                    <span class="diff-badge ${diffClass}">${b.difficulty}</span>
                    <button class="bookmark-star-btn bookmarked" onclick="event.stopPropagation(); toggleBookmark('${b.id}')">★</button>
                </div>
            </div>
            <div>
                <div class="brief-track-name" style="color:${style.text}">${b.track}</div>
                <h3 class="brief-title">${b.title}</h3>
            </div>
            <div class="brief-solution">🚀 ${b.solution}</div>
        </div>
        `;
    });
    container.innerHTML = html;
}

function copyBriefLink() {
    if (!activeModalBriefId) return;
    const brief = ALL_BRIEFS.find(b => b.id === activeModalBriefId);
    const text = `3MTT Brief [${brief.id}]: ${brief.title}\nTrack: ${brief.track}\nScope: ${brief.solution}\nDeliverables: ${brief.deliverables}`;
    navigator.clipboard.writeText(text);
    showToast('Brief summary copied to clipboard!');
}

function switchTab(tabId) {
    document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.content-tab-page').forEach(page => page.classList.remove('active'));

    const targetBtn = Array.from(document.querySelectorAll('.nav-tab')).find(b => b.getAttribute('onclick').includes(tabId));
    if (targetBtn) targetBtn.classList.add('active');

    const page = document.getElementById(`tab-${tabId}`);
    if (page) page.classList.add('active');

    if (tabId === 'bookmarks') renderBookmarksPage();
}

function initCalculator() {
    const trackSelect = document.getElementById('calc-track');
    trackSelect.innerHTML = Object.keys(trackColors).map(t => `<option value="${t}">${t}</option>`).join('');

    document.getElementById('calc-date').valueAsDate = new Date();

    const container = document.getElementById('rating-criteria-list');
    let html = '';

    criteriaList.forEach(c => {
        html += `
        <div class="calc-form-group" style="margin-bottom: 1.2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <label style="font-size:0.9rem; color:var(--text-main); font-weight:700;">${c.name} (${c.weight}%)</label>
                <span id="score-val-${c.key}" style="color:var(--accent-emerald); font-weight:800; font-size:0.9rem;">Rating: 3/5</span>
            </div>
            <div class="rating-selector">
                ${[1,2,3,4,5].map(rating => `
                    <button class="rating-btn ${rating === 3 ? 'active' : ''}" data-key="${c.key}" data-rating="${rating}" onclick="setRating('${c.key}', ${rating})">
                        ${rating}
                    </button>
                `).join('')}
            </div>
        </div>
        `;
    });
    container.innerHTML = html;
    calculateTotalScore();
}

function setRating(key, rating) {
    ratings[key] = rating;
    document.querySelectorAll(`button[data-key="${key}"]`).forEach(btn => {
        btn.classList.toggle('active', parseInt(btn.getAttribute('data-rating')) === rating);
    });
    document.getElementById(`score-val-${key}`).innerText = `Rating: ${rating}/5`;
    calculateTotalScore();
}

function calculateTotalScore() {
    let total = 0;
    criteriaList.forEach(c => {
        const rating = ratings[c.key] || 3;
        const score = (rating / 5) * c.weight;
        total += score;
    });

    const totalScoreRounded = Math.round(total);
    document.getElementById('calc-total-score').innerText = totalScoreRounded;

    const badge = document.getElementById('calc-result-badge');
    if (totalScoreRounded >= 80) {
        badge.innerText = 'DISTINCTION';
        badge.style.background = 'rgba(16, 185, 129, 0.2)';
        badge.style.color = '#34D399';
    } else if (totalScoreRounded >= 60) {
        badge.innerText = 'PASS - CERTIFIED';
        badge.style.background = 'rgba(99, 102, 241, 0.2)';
        badge.style.color = '#818CF8';
    } else if (totalScoreRounded >= 40) {
        badge.innerText = 'REVISE & RESUBMIT';
        badge.style.background = 'rgba(245, 158, 11, 0.2)';
        badge.style.color = '#FBBF24';
    } else {
        badge.innerText = 'NOT YET MET';
        badge.style.background = 'rgba(244, 63, 94, 0.2)';
        badge.style.color = '#F87171';
    }
}

function openBriefInCalculator() {
    if (!activeModalBriefId) return;
    const brief = ALL_BRIEFS.find(b => b.id === activeModalBriefId);
    closeModal();
    switchTab('calculator');
    document.getElementById('calc-brief-id').value = brief.id;
    document.getElementById('calc-track').value = brief.track;
    showToast(`Loaded ${brief.id} into Score Calculator`);
}

function copyEvaluationSummary() {
    const name = document.getElementById('calc-fellow-name').value || 'N/A';
    const fId = document.getElementById('calc-fellow-id').value || 'N/A';
    const track = document.getElementById('calc-track').value;
    const bId = document.getElementById('calc-brief-id').value || 'N/A';
    const reviewer = document.getElementById('calc-reviewer').value || 'N/A';
    const date = document.getElementById('calc-date').value || 'N/A';
    const score = document.getElementById('calc-total-score').innerText;
    const result = document.getElementById('calc-result-badge').innerText;
    const comments = document.getElementById('calc-comments').value || 'None';

    const text = `====================================\n3MTT NEXTGEN FELLOW EVALUATION SCORECARD\n====================================\nFellow Name: ${name}\nFellow ID: ${fId}\nTrack: ${track}\nBrief ID: ${bId}\nReviewer: ${reviewer}\nDate: ${date}\n\nRubric Score: ${score} / 100\nFinal Result: ${result}\n\nReviewer Comments:\n${comments}\n====================================`;

    navigator.clipboard.writeText(text);
    showToast('Evaluation report copied to clipboard!');
}

function resetCalculator() {
    document.getElementById('calc-fellow-name').value = '';
    document.getElementById('calc-fellow-id').value = '';
    document.getElementById('calc-brief-id').value = '';
    document.getElementById('calc-reviewer').value = '';
    document.getElementById('calc-comments').value = '';
    ratings = { c1: 3, c2: 3, c3: 3, c4: 3, c5: 3, c6: 3 };
    initCalculator();
    showToast('Calculator reset');
}

function renderDataSources() {
    const tbody = document.getElementById('data-sources-table-body');
    let html = '';

    DATA_SOURCES.forEach(ds => {
        if (ds.name.includes('KEY OPEN-DATA') || ds.name.includes('THREE WAYS') || ds.name.includes('Source') || !ds.url) return;

        html += `
        <tr>
            <td><strong>${ds.name}</strong></td>
            <td>${ds.description}</td>
            <td><a href="https://${ds.url.split('/')[0]}" target="_blank" style="color:var(--accent-teal); font-weight:600; text-decoration:none;">${ds.url} ↗</a></td>
        </tr>
        `;
    });
    tbody.innerHTML = html;
}

function exportFilteredCSV() {
    let filtered = ALL_BRIEFS.filter(b => {
        const matchTrack = (currentTrack === 'ALL' || b.track === currentTrack);
        const matchDiff = (currentDiff === 'ALL' || b.difficulty === currentDiff);
        return matchTrack && matchDiff;
    });

    let csv = 'Brief ID,Track,Title,Difficulty,Nigerian Problem Context,What to Build (MVP),Core MVP Features,Expected Deliverables,Suggested Tools\n';
    
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
    showToast('Exported briefs to CSV!');
}

function toggleTheme() {
    const isLight = document.body.getAttribute('data-theme') === 'light';
    if (isLight) {
        document.body.removeAttribute('data-theme');
        document.getElementById('theme-btn').innerText = '🌙';
    } else {
        document.body.setAttribute('data-theme', 'light');
        document.getElementById('theme-btn').innerText = '☀️';
    }
}

function showToast(msg) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerText = msg;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

