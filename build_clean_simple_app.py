import json

with open('app_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

briefs_json_str = json.dumps(data['briefs'], ensure_ascii=False)

with open('app_simple.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3MTT NextGen Project Brief Bank</title>
    <meta name="description" content="Search, filter, category, and sort 240 capstone project briefs for 3MTT NextGen Cohort.">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-body: #0F172A;
            --bg-card: #1E293B;
            --bg-card-hover: #334155;
            --bg-input: #334155;
            --bg-modal: #1E293B;
            
            --border-color: rgba(255, 255, 255, 0.1);
            --border-active: #10B981;
            
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --text-dim: #64748B;
            
            --accent-primary: #10B981;
            --accent-secondary: #3B82F6;
            
            --radius-lg: 12px;
            --radius-md: 8px;
            --radius-sm: 6px;
        }}

        [data-theme="light"] {{
            --bg-body: #F8FAFC;
            --bg-card: #FFFFFF;
            --bg-card-hover: #F1F5F9;
            --bg-input: #E2E8F0;
            --bg-modal: #FFFFFF;
            
            --border-color: rgba(0, 0, 0, 0.1);
            --border-active: #059669;
            
            --text-main: #0F172A;
            --text-muted: #475569;
            --text-dim: #64748B;
            
            --accent-primary: #059669;
            --accent-secondary: #2563EB;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.5;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.5rem 1.5rem 3rem;
        }}

        /* Header */
        header {{
            background: var(--bg-card);
            border-bottom: 1px solid var(--border-color);
            padding: 1.25rem 0;
            margin-bottom: 1.5rem;
        }}

        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .brand-title h1 {{
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -0.01em;
        }}

        .brand-subtitle {{
            font-size: 0.85rem;
            color: var(--accent-primary);
            font-weight: 600;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .btn {{
            padding: 0.5rem 1rem;
            border-radius: var(--radius-sm);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid var(--border-color);
            background: transparent;
            color: var(--text-main);
            transition: all 0.15s ease;
        }}

        .btn:hover {{
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }}

        .btn-primary {{
            background: var(--accent-primary);
            color: #000;
            border-color: var(--accent-primary);
            font-weight: 700;
        }}

        .btn-primary:hover {{
            opacity: 0.9;
            color: #000;
        }}

        /* Controls Section */
        .controls-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .search-box {{
            position: relative;
            flex: 1;
        }}

        .search-input {{
            width: 100%;
            padding: 0.75rem 1rem;
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            color: var(--text-main);
            font-size: 0.95rem;
            font-family: inherit;
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--accent-primary);
        }}

        .clear-search-btn {{
            position: absolute;
            right: 0.85rem;
            top: 50%;
            transform: translateY(-50%);
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            font-size: 1.2rem;
            display: none;
        }}

        .clear-search-btn.visible {{
            display: block;
        }}

        /* Track Category Pills */
        .track-pills-container {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            overflow-x: auto;
            padding-bottom: 0.25rem;
        }}

        .track-pill {{
            padding: 0.4rem 0.8rem;
            border-radius: var(--radius-md);
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
        }}

        .track-pill:hover {{
            color: var(--text-main);
            border-color: rgba(255, 255, 255, 0.2);
        }}

        .track-pill.active {{
            background: var(--accent-primary);
            color: #000;
            border-color: var(--accent-primary);
            font-weight: 700;
        }}

        .filter-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .filter-group {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
        }}

        .select-input {{
            padding: 0.5rem 2rem 0.5rem 0.75rem;
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            color: var(--text-main);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
        }}

        .view-toggle {{
            display: flex;
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            padding: 2px;
        }}

        .view-btn {{
            padding: 0.35rem 0.65rem;
            background: transparent;
            border: none;
            color: var(--text-muted);
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8rem;
            font-weight: 600;
        }}

        .view-btn.active {{
            background: rgba(255, 255, 255, 0.15);
            color: var(--text-main);
        }}

        .results-meta {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-bottom: 1rem;
        }}

        /* Brief Cards */
        .briefs-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.25rem;
        }}

        .brief-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            transition: all 0.15s ease;
            cursor: pointer;
        }}

        .brief-card:hover {{
            border-color: var(--border-active);
            background: var(--bg-card-hover);
        }}

        .card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brief-id-badge {{
            font-weight: 800;
            font-size: 0.85rem;
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-primary);
            padding: 0.2rem 0.5rem;
            border-radius: var(--radius-sm);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        .brief-id-badge-sm {{
            font-weight: 700;
            color: var(--accent-primary);
        }}

        .diff-badge {{
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.15rem 0.5rem;
            border-radius: 99px;
        }}

        .diff-beginner {{
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
        }}

        .diff-beginner-intermediate {{
            background: rgba(59, 130, 246, 0.15);
            color: #60A5FA;
        }}

        .diff-intermediate {{
            background: rgba(245, 158, 11, 0.15);
            color: #FBBF24;
        }}

        .brief-track-name {{
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }}

        .brief-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.3;
        }}

        .brief-problem {{
            font-size: 0.85rem;
            color: var(--text-muted);
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .brief-solution {{
            font-size: 0.85rem;
            color: var(--text-main);
        }}

        .card-features-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            margin-top: auto;
        }}

        .feature-chip {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.72rem;
            color: var(--text-muted);
        }}

        /* Table View */
        .table-wrapper {{
            overflow-x: auto;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
        }}

        .briefs-table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.875rem;
        }}

        .briefs-table th {{
            background: rgba(0, 0, 0, 0.2);
            padding: 0.85rem 1rem;
            font-weight: 700;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }}

        .briefs-table td {{
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--border-color);
            vertical-align: top;
        }}

        .briefs-table tr:hover {{
            background: rgba(255, 255, 255, 0.03);
            cursor: pointer;
        }}

        /* Detail Modal */
        .modal-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(4px);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }}

        .modal-backdrop.active {{
            opacity: 1;
            pointer-events: auto;
        }}

        .modal-box {{
            background: var(--bg-modal);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 750px;
            max-height: 90vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }}

        .modal-header {{
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
        }}

        .modal-close-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 1.5rem;
            cursor: pointer;
            line-height: 1;
        }}

        .modal-body {{
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}

        .detail-section {{
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }}

        .detail-label {{
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--accent-primary);
            letter-spacing: 0.05em;
        }}

        .detail-content {{
            background: rgba(0, 0, 0, 0.15);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 0.85rem 1rem;
            font-size: 0.9rem;
            color: var(--text-main);
            line-height: 1.5;
        }}

        .modal-footer {{
            padding: 1rem 1.5rem;
            border-top: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }}

        .toast-container {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 2000;
        }}

        .toast {{
            background: #1E293B;
            border: 1px solid var(--accent-primary);
            color: var(--text-main);
            padding: 0.75rem 1rem;
            border-radius: var(--radius-md);
            font-size: 0.85rem;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}

        .highlight-text {{
            background: rgba(16, 185, 129, 0.25);
            color: #6EE7B7;
            padding: 0 2px;
            border-radius: 2px;
        }}

        .empty-state {{
            text-align: center;
            padding: 4rem 2rem;
            background: var(--bg-card);
            border: 1px dashed var(--border-color);
            border-radius: var(--radius-lg);
            color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-content">
            <div>
                <div class="brand-title">
                    <h1>3MTT NextGen Project Brief Bank</h1>
                </div>
                <div class="brand-subtitle">Project & Portfolio Phase • 240 Project Briefs</div>
            </div>

            <div class="header-actions">
                <button class="btn" onclick="exportFilteredCSV()">
                    Export CSV
                </button>
                <button class="btn" onclick="toggleTheme()" id="theme-btn">
                    Theme: Dark
                </button>
            </div>
        </div>
    </header>

    <div class="container">

        <!-- Controls Card -->
        <div class="controls-card">
            <!-- Search Bar -->
            <div class="search-box">
                <input type="text" id="search-input" class="search-input" placeholder="Search brief ID, title, problem, tools, deliverables..." oninput="handleSearchInput()">
                <button class="clear-search-btn" id="clear-search-btn" onclick="clearSearch()">×</button>
            </div>

            <!-- Track Pills -->
            <div class="track-pills-container" id="track-pills"></div>

            <!-- Filters & Sort -->
            <div class="filter-row">
                <div class="filter-group">
                    <select id="diff-filter" class="select-input" onchange="renderFilteredBriefs()">
                        <option value="ALL">All Difficulties</option>
                        <option value="Beginner">Beginner</option>
                        <option value="Beginner-Intermediate">Beginner-Intermediate</option>
                        <option value="Intermediate">Intermediate</option>
                    </select>

                    <select id="sort-select" class="select-input" onchange="renderFilteredBriefs()">
                        <option value="id_asc">Sort: ID (Ascending)</option>
                        <option value="id_desc">Sort: ID (Descending)</option>
                        <option value="title_asc">Sort: Title (A-Z)</option>
                        <option value="title_desc">Sort: Title (Z-A)</option>
                        <option value="track_asc">Sort: Track</option>
                        <option value="diff">Sort: Difficulty Level</option>
                    </select>

                    <button class="btn" style="padding: 0.45rem 0.75rem; font-size:0.8rem;" onclick="resetFilters()">
                        Reset Filters
                    </button>
                </div>

                <div class="filter-group">
                    <div class="view-toggle">
                        <button class="view-btn active" id="view-grid-btn" onclick="setViewMode('grid')">
                            Card View
                        </button>
                        <button class="view-btn" id="view-table-btn" onclick="setViewMode('table')">
                            Table View
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Meta Results -->
        <div class="results-meta">
            <span id="results-count">Showing 240 briefs</span>
            <span id="active-track-name" style="font-weight: 600; color: var(--accent-primary);">All Tracks</span>
        </div>

        <!-- Briefs Container -->
        <div id="briefs-grid" class="briefs-grid"></div>

        <div id="briefs-table-container" class="table-wrapper" style="display: none;">
            <table class="briefs-table">
                <thead>
                    <tr>
                        <th>Brief ID</th>
                        <th>Track</th>
                        <th>Title</th>
                        <th>Problem Context</th>
                        <th>What to Build (MVP)</th>
                        <th>Difficulty</th>
                    </tr>
                </thead>
                <tbody id="briefs-table-body"></tbody>
            </table>
        </div>

        <div id="empty-state" class="empty-state" style="display: none;">
            <h3>No briefs match your search</h3>
            <p style="margin-top: 0.5rem;">Try adjusting your search terms or clearing track filters.</p>
            <button class="btn btn-primary" style="margin-top: 1rem;" onclick="resetFilters()">Reset All Filters</button>
        </div>

    </div>

    <!-- Brief Detail Modal -->
    <div class="modal-backdrop" id="brief-modal" onclick="closeModalOnBackdrop(event)">
        <div class="modal-box">
            <div class="modal-header">
                <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.3rem;">
                        <span id="modal-brief-id" class="brief-id-badge">SD-01</span>
                        <span id="modal-track" class="brief-track-name">Software Development</span>
                        <span id="modal-diff" class="diff-badge diff-beginner">Beginner</span>
                    </div>
                    <h2 id="modal-title" class="brief-title" style="font-size: 1.25rem;">POS Transaction Web App</h2>
                </div>
                <button class="modal-close-btn" onclick="closeModal()">×</button>
            </div>
            <div class="modal-body">
                <div class="detail-section">
                    <div class="detail-label">Problem Context</div>
                    <div id="modal-problem" class="detail-content"></div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">What to Build (MVP Scope)</div>
                    <div id="modal-solution" class="detail-content"></div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">Core MVP Features</div>
                    <div id="modal-features" class="detail-content"></div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">Expected Deliverables</div>
                    <div id="modal-deliverables" class="detail-content"></div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">Suggested Tools & Tech Stack</div>
                    <div id="modal-tools" class="detail-content"></div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn" onclick="copyBriefLink()">
                    Copy Brief Text
                </button>
                <button class="btn btn-primary" onclick="closeModal()">
                    Close
                </button>
            </div>
        </div>
    </div>

    <!-- Toast Notifications -->
    <div class="toast-container" id="toast-container"></div>

    <!-- DATA -->
    <script id="briefs-data" type="application/json">
{briefs_json_str}
    </script>

    <!-- LOGIC -->
    <script>
{js_content}
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('3MTT_NextGen_Project_Brief_Bank.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Simple HTML updated successfully!")
