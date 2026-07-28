import json
import os

# Load data
with open('app_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

briefs_json = json.dumps(data['briefs'], ensure_ascii=False)
data_sources_json = json.dumps(data['data_sources'], ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3MTT NextGen Project Brief Bank & Evaluation Portal</title>
    <meta name="description" content="Interactive Project Brief Bank, Search, Filter, Sort and Evaluation Rubric for 3MTT NextGen Cohort.">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-body: #090D16;
            --bg-card: rgba(17, 24, 39, 0.75);
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --bg-card-solid: #111827;
            --bg-input: #1F2937;
            --bg-modal: #111827;
            
            --border-color: rgba(255, 255, 255, 0.08);
            --border-highlight: rgba(16, 185, 129, 0.3);
            
            --text-main: #F9FAFB;
            --text-muted: #9CA3AF;
            --text-dim: #6B7280;
            
            --accent-emerald: #10B981;
            --accent-teal: #14B8A6;
            --accent-cyan: #06B6D4;
            --accent-indigo: #6366F1;
            --accent-purple: #8B5CF6;
            --accent-pink: #EC4899;
            --accent-amber: #F59E0B;
            --accent-rose: #F43F5E;
            
            --radius-lg: 16px;
            --radius-md: 12px;
            --radius-sm: 8px;
            
            --shadow-glow: 0 0 25px rgba(16, 185, 129, 0.15);
            --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        [data-theme="light"] {{
            --bg-body: #F3F4F6;
            --bg-card: rgba(255, 255, 255, 0.85);
            --bg-card-hover: #FFFFFF;
            --bg-card-solid: #FFFFFF;
            --bg-input: #E5E7EB;
            --bg-modal: #FFFFFF;
            
            --border-color: rgba(0, 0, 0, 0.08);
            --border-highlight: rgba(16, 185, 129, 0.5);
            
            --text-main: #111827;
            --text-muted: #4B5563;
            --text-dim: #6B7280;
            
            --shadow-glow: 0 4px 20px rgba(0, 0, 0, 0.08);
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
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.05) 0%, transparent 40%);
            background-attachment: fixed;
        }}

        .container {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 0 1.5rem 3rem;
        }}

        /* Header */
        header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(9, 13, 22, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 0;
            margin-bottom: 2rem;
        }}

        .header-content {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 0 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .brand-logo {{
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, var(--accent-emerald), var(--accent-teal));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #000;
            font-weight: 800;
            font-size: 1.25rem;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        .brand-title h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.35rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFFFFF, #9CA3AF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }}

        [data-theme="light"] .brand-title h1 {{
            background: linear-gradient(135deg, #111827, #374151);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .brand-subtitle {{
            font-size: 0.8rem;
            color: var(--accent-emerald);
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        /* Navigation Tabs */
        .nav-tabs {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            padding: 4px;
            border-radius: var(--radius-md);
        }}

        .nav-tab {{
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-muted);
            background: transparent;
            border: none;
            border-radius: var(--radius-sm);
            cursor: pointer;
            transition: var(--transition-fast);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .nav-tab:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }}

        .nav-tab.active {{
            color: #FFFFFF;
            background: linear-gradient(135deg, var(--accent-emerald), var(--accent-teal));
            box-shadow: 0 2px 10px rgba(16, 185, 129, 0.25);
        }}

        .nav-tab .badge {{
            background: rgba(255, 255, 255, 0.2);
            padding: 2px 6px;
            border-radius: 99px;
            font-size: 0.75rem;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .btn {{
            padding: 0.55rem 1.1rem;
            border-radius: var(--radius-sm);
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition-fast);
            border: 1px solid transparent;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
        }}

        .btn-outline {{
            background: transparent;
            border-color: var(--border-color);
            color: var(--text-main);
        }}

        .btn-outline:hover {{
            border-color: var(--accent-emerald);
            color: var(--accent-emerald);
            background: rgba(16, 185, 129, 0.05);
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--accent-emerald), var(--accent-teal));
            color: #000;
            font-weight: 700;
        }}

        .btn-primary:hover {{
            opacity: 0.9;
            transform: translateY(-1px);
        }}

        /* Hero Banner Stats */
        .hero-banner {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.75rem 2rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(12px);
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            position: relative;
            overflow: hidden;
        }}

        .hero-banner::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-emerald), var(--accent-cyan), var(--accent-indigo));
        }}

        .stat-card {{
            display: flex;
            align-items: center;
            gap: 1.25rem;
        }}

        .stat-icon {{
            width: 52px;
            height: 52px;
            border-radius: var(--radius-md);
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--accent-emerald);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }}

        .stat-info .stat-value {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--text-main);
            line-height: 1.2;
        }}

        .stat-info .stat-label {{
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        /* Explorer Controls */
        .controls-wrapper {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            margin-bottom: 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .search-bar-container {{
            display: flex;
            gap: 0.75rem;
            align-items: center;
        }}

        .search-input-box {{
            position: relative;
            flex: 1;
        }}

        .search-input-box svg {{
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-dim);
            pointer-events: none;
        }}

        .search-input {{
            width: 100%;
            padding: 0.85rem 1rem 0.85rem 2.8rem;
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            color: var(--text-main);
            font-size: 0.95rem;
            font-family: inherit;
            transition: var(--transition-fast);
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--accent-emerald);
            box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
        }}

        .clear-search-btn {{
            position: absolute;
            right: 0.85rem;
            top: 50%;
            transform: translateY(-50%);
            background: transparent;
            border: none;
            color: var(--text-dim);
            cursor: pointer;
            font-size: 1.2rem;
            display: none;
        }}

        .clear-search-btn.visible {{
            display: block;
        }}

        .shortcut-badge {{
            position: absolute;
            right: 1rem;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--border-color);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.75rem;
            color: var(--text-muted);
        }}

        .filter-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .track-pills-container {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            overflow-x: auto;
            padding-bottom: 0.25rem;
            scroll-behavior: smooth;
            -webkit-overflow-scrolling: touch;
        }}

        .track-pill {{
            padding: 0.45rem 0.85rem;
            border-radius: 99px;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            cursor: pointer;
            white-space: nowrap;
            transition: var(--transition-fast);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .track-pill:hover {{
            color: var(--text-main);
            border-color: rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.08);
        }}

        .track-pill.active {{
            background: var(--accent-emerald);
            color: #000;
            border-color: var(--accent-emerald);
            font-weight: 700;
        }}

        .secondary-filters {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
        }}

        .select-input {{
            padding: 0.55rem 2rem 0.55rem 0.85rem;
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            color: var(--text-main);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%239CA3AF' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
        }}

        .select-input:focus {{
            outline: none;
            border-color: var(--accent-emerald);
        }}

        .view-toggle {{
            display: flex;
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            padding: 2px;
        }}

        .view-btn {{
            padding: 0.4rem 0.6rem;
            background: transparent;
            border: none;
            color: var(--text-muted);
            border-radius: 4px;
            cursor: pointer;
            display: flex;
            align-items: center;
        }}

        .view-btn.active {{
            background: rgba(255, 255, 255, 0.15);
            color: var(--text-main);
        }}

        .results-meta {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 0.5rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }}

        /* Brief Cards Grid */
        .briefs-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 1.25rem;
        }}

        .brief-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.85rem;
            transition: var(--transition-fast);
            cursor: pointer;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }}

        .brief-card:hover {{
            transform: translateY(-3px);
            border-color: var(--border-highlight);
            box-shadow: var(--shadow-glow);
            background: var(--bg-card-hover);
        }}

        .card-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.5rem;
        }}

        .brief-id-badge {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 0.9rem;
            padding: 0.25rem 0.6rem;
            border-radius: var(--radius-sm);
            letter-spacing: 0.03em;
        }}

        .card-meta-right {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .diff-badge {{
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.2rem 0.5rem;
            border-radius: 99px;
            border: 1px solid transparent;
        }}

        .diff-beginner {{
            background: rgba(16, 185, 129, 0.12);
            color: #34D399;
            border-color: rgba(16, 185, 129, 0.3);
        }}

        .diff-beginner-intermediate {{
            background: rgba(99, 102, 241, 0.12);
            color: #818CF8;
            border-color: rgba(99, 102, 241, 0.3);
        }}

        .diff-intermediate {{
            background: rgba(245, 158, 11, 0.12);
            color: #FBBF24;
            border-color: rgba(245, 158, 11, 0.3);
        }}

        .bookmark-star-btn {{
            background: transparent;
            border: none;
            color: var(--text-dim);
            cursor: pointer;
            font-size: 1.1rem;
            transition: var(--transition-fast);
            padding: 2px;
        }}

        .bookmark-star-btn:hover, .bookmark-star-btn.bookmarked {{
            color: var(--accent-amber);
            transform: scale(1.15);
        }}

        .brief-track-name {{
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--accent-teal);
        }}

        .brief-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.35;
        }}

        .brief-problem {{
            font-size: 0.85rem;
            color: var(--text-muted);
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.02);
            padding: 0.5rem 0.75rem;
            border-radius: var(--radius-sm);
            border-left: 3px solid var(--accent-emerald);
        }}

        .brief-solution {{
            font-size: 0.85rem;
            color: var(--text-main);
            font-weight: 500;
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
            padding: 2px 7px;
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
            background: rgba(255, 255, 255, 0.03);
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
            background: rgba(255, 255, 255, 0.04);
            cursor: pointer;
        }}

        /* Modal */
        .modal-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.25s ease;
        }}

        .modal-backdrop.active {{
            opacity: 1;
            pointer-events: auto;
        }}

        .modal-box {{
            background: var(--bg-modal);
            border: 1px solid var(--border-highlight);
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 800px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            transform: translateY(20px);
            transition: transform 0.25s ease;
        }}

        .modal-backdrop.active .modal-box {{
            transform: translateY(0);
        }}

        .modal-header {{
            padding: 1.5rem 1.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
        }}

        .modal-close-btn {{
            background: rgba(255, 255, 255, 0.08);
            border: none;
            color: var(--text-muted);
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }}

        .modal-close-btn:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.15);
        }}

        .modal-body {{
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}

        .detail-section {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .detail-label {{
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--accent-emerald);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .detail-content {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1rem 1.1rem;
            font-size: 0.95rem;
            color: var(--text-main);
            line-height: 1.6;
        }}

        .modal-footer {{
            padding: 1rem 1.75rem;
            border-top: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            background: rgba(0, 0, 0, 0.2);
        }}

        /* Content Views (Guide, Calculator, Data Sources) */
        .content-tab-page {{
            display: none;
        }}

        .content-tab-page.active {{
            display: block;
        }}

        .rubric-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.75rem;
            margin-bottom: 1.5rem;
        }}

        .rubric-card h2 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.35rem;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .rubric-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}

        .rubric-table th, .rubric-table td {{
            padding: 0.85rem 1rem;
            border: 1px solid var(--border-color);
            text-align: left;
        }}

        .rubric-table th {{
            background: rgba(255, 255, 255, 0.04);
            font-weight: 700;
        }}

        /* Calculator Styles */
        .calc-grid {{
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 1.5rem;
        }}

        @media (max-width: 900px) {{
            .calc-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .calc-form-group {{
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
            margin-bottom: 1rem;
        }}

        .calc-form-group label {{
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
        }}

        .calc-input {{
            padding: 0.65rem 0.85rem;
            background: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            color: var(--text-main);
            font-family: inherit;
        }}

        .rating-selector {{
            display: flex;
            gap: 0.4rem;
            margin-top: 0.3rem;
        }}

        .rating-btn {{
            flex: 1;
            padding: 0.5rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            color: var(--text-muted);
            font-weight: 700;
            cursor: pointer;
            transition: var(--transition-fast);
        }}

        .rating-btn:hover {{
            background: rgba(255, 255, 255, 0.15);
            color: var(--text-main);
        }}

        .rating-btn.active {{
            background: var(--accent-emerald);
            color: #000;
            border-color: var(--accent-emerald);
        }}

        .score-summary-box {{
            background: var(--bg-card);
            border: 2px solid var(--accent-emerald);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            text-align: center;
            position: sticky;
            top: 90px;
        }}

        .score-number {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            color: var(--accent-emerald);
            line-height: 1;
            margin: 0.75rem 0;
        }}

        .score-band-badge {{
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 99px;
            font-weight: 800;
            font-size: 0.9rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        /* Toast Notifications */
        .toast-container {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            z-index: 2000;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .toast {{
            background: #1F2937;
            border: 1px solid var(--accent-emerald);
            color: var(--text-main);
            padding: 0.85rem 1.25rem;
            border-radius: var(--radius-md);
            font-size: 0.875rem;
            font-weight: 600;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        @keyframes slideIn {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}

        .highlight-text {{
            background: rgba(16, 185, 129, 0.25);
            color: #6EE7B7;
            padding: 0 3px;
            border-radius: 2px;
        }}

        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 4rem 2rem;
            background: var(--bg-card);
            border: 1px dashed var(--border-color);
            border-radius: var(--radius-lg);
            color: var(--text-muted);
        }}

        .empty-state svg {{
            margin-bottom: 1rem;
            color: var(--text-dim);
        }}

        /* Highlight animations */
        @media print {{
            header, .controls-wrapper, .hero-banner, .modal-footer, .nav-tabs {{
                display: none !important;
            }}
            body {{
                background: #FFF;
                color: #000;
            }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-content">
            <div class="brand">
                <div class="brand-logo">3M</div>
                <div class="brand-title">
                    <h1>3MTT NextGen Brief Bank</h1>
                    <div class="brand-subtitle">Project & Portfolio Phase • 240 Scoped MVPs</div>
                </div>
            </div>

            <!-- Nav Tabs -->
            <nav class="nav-tabs">
                <button class="nav-tab active" onclick="switchTab('explorer')">
                    🔍 Brief Explorer
                </button>
                <button class="nav-tab" onclick="switchTab('scoring-guide')">
                    📊 Scoring Rubric
                </button>
                <button class="nav-tab" onclick="switchTab('calculator')">
                    🧮 Score Calculator
                </button>
                <button class="nav-tab" onclick="switchTab('data-sources')">
                    🌐 Data Sources
                </button>
                <button class="nav-tab" onclick="switchTab('bookmarks')">
                    ⭐ Bookmarks <span class="badge" id="bookmark-count-badge">0</span>
                </button>
            </nav>

            <div class="header-actions">
                <button class="btn btn-outline" onclick="exportFilteredCSV()">
                    📥 Export CSV
                </button>
                <button class="btn btn-outline" onclick="toggleTheme()" id="theme-btn">
                    🌙
                </button>
            </div>
        </div>
    </header>

    <div class="container">

        <!-- HERO BANNER -->
        <div class="hero-banner">
            <div class="stat-card">
                <div class="stat-icon">📋</div>
                <div class="stat-info">
                    <div class="stat-value">240</div>
                    <div class="stat-label">Total Capstone Briefs</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🛠️</div>
                <div class="stat-info">
                    <div class="stat-value">12</div>
                    <div class="stat-label">Specialized Tech Tracks</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🇳🇬</div>
                <div class="stat-info">
                    <div class="stat-value">100%</div>
                    <div class="stat-label">Nigerian Problem Context</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💯</div>
                <div class="stat-info">
                    <div class="stat-value">100 PTS</div>
                    <div class="stat-label">Standard Rubric Rating</div>
                </div>
            </div>
        </div>

        <!-- TAB PAGE 1: EXPLORER -->
        <main id="tab-explorer" class="content-tab-page active">

            <!-- Controls -->
            <div class="controls-wrapper">
                <div class="search-bar-container">
                    <div class="search-input-box">
                        <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                        <input type="text" id="search-input" class="search-input" placeholder="Search by Brief ID, title, problem, deliverables, or tools... (Press '/' to focus)" oninput="handleSearchInput()">
                        <button class="clear-search-btn" id="clear-search-btn" onclick="clearSearch()">×</button>
                        <span class="shortcut-badge">/</span>
                    </div>
                </div>

                <!-- Track Pills -->
                <div class="track-pills-container" id="track-pills">
                    <!-- Dynamic Pills -->
                </div>

                <div class="filter-row">
                    <div class="secondary-filters">
                        <!-- Difficulty Filter -->
                        <select id="diff-filter" class="select-input" onchange="renderFilteredBriefs()">
                            <option value="ALL">All Difficulties</option>
                            <option value="Beginner">Beginner</option>
                            <option value="Beginner-Intermediate">Beginner-Intermediate</option>
                            <option value="Intermediate">Intermediate</option>
                        </select>

                        <!-- Sort Order -->
                        <select id="sort-select" class="select-input" onchange="renderFilteredBriefs()">
                            <option value="id_asc">Sort: ID (Ascending)</option>
                            <option value="id_desc">Sort: ID (Descending)</option>
                            <option value="title_asc">Sort: Title (A-Z)</option>
                            <option value="title_desc">Sort: Title (Z-A)</option>
                            <option value="track_asc">Sort: Track</option>
                            <option value="diff">Sort: Difficulty Level</option>
                        </select>

                        <button class="btn btn-outline" style="padding: 0.45rem 0.75rem; font-size:0.8rem;" onclick="resetFilters()">
                            🔄 Reset
                        </button>
                    </div>

                    <div class="secondary-filters">
                        <div class="view-toggle">
                            <button class="view-btn active" id="view-grid-btn" onclick="setViewMode('grid')" title="Grid View">
                                🔲 Card Grid
                            </button>
                            <button class="view-btn" id="view-table-btn" onclick="setViewMode('table')" title="Table View">
                                ☰ Table View
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Meta Stats -->
            <div class="results-meta" style="margin-bottom: 1rem;">
                <span id="results-count">Showing 240 briefs</span>
                <span id="active-track-name" style="font-weight: 600; color: var(--accent-teal);">All Tracks</span>
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
                            <th>Nigerian Problem Context</th>
                            <th>What to Build (MVP)</th>
                            <th>Difficulty</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody id="briefs-table-body"></tbody>
                </table>
            </div>

            <div id="empty-state" class="empty-state" style="display: none;">
                <svg width="48" height="48" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <h3>No project briefs match your criteria</h3>
                <p style="margin-top: 0.5rem;">Try adjusting your search terms or clearing track filters.</p>
                <button class="btn btn-primary" style="margin-top: 1rem;" onclick="resetFilters()">Reset All Filters</button>
            </div>
        </main>

        <!-- TAB PAGE 2: SCORING GUIDE & RUBRIC -->
        <section id="tab-scoring-guide" class="content-tab-page">
            <div class="rubric-card">
                <h2>📋 Submission Validity Checklist</h2>
                <p style="color: var(--text-muted); margin-bottom: 1rem;">
                    All 5 checks must be <strong>YES</strong> for a submission to count toward a center's milestone payment.
                </p>
                <table class="rubric-table">
                    <thead>
                        <tr>
                            <th style="width: 50px;">#</th>
                            <th>Check</th>
                            <th>Counts if</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>1</strong></td>
                            <td><strong>Registered Fellow</strong></td>
                            <td>Submission is linked to a verified, registered Fellow (one submission per Fellow)</td>
                        </tr>
                        <tr>
                            <td><strong>2</strong></td>
                            <td><strong>Assigned brief</strong></td>
                            <td>Work matches a brief from this bank for the Fellow's track</td>
                        </tr>
                        <tr>
                            <td><strong>3</strong></td>
                            <td><strong>Working deliverable</strong></td>
                            <td>The required deliverable is present and functional (per track)</td>
                        </tr>
                        <tr>
                            <td><strong>4</strong></td>
                            <td><strong>Demo video</strong></td>
                            <td>A 2-3 min video where the Fellow explains their own work is attached</td>
                        </tr>
                        <tr>
                            <td><strong>5</strong></td>
                            <td><strong>Original work</strong></td>
                            <td>Work is the Fellow's own; not a duplicate or plagiarised submission</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="rubric-card">
                <h2>💯 Standard Quality Rubric (100 Points Total)</h2>
                <p style="color: var(--text-muted); margin-bottom: 1rem;">
                    Evaluated by reviewers rating each criterion 1 to 5. The total weighted score determines the Fellow's Certification Result.
                </p>
                <table class="rubric-table">
                    <thead>
                        <tr>
                            <th>Criterion</th>
                            <th style="width: 100px;">Weight %</th>
                            <th>What Good Looks Like</th>
                            <th>Track Application</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Adherence to Brief & Completeness</strong></td>
                            <td><span style="color: var(--accent-emerald); font-weight:800;">20%</span></td>
                            <td>Solves the assigned brief; required scope is complete</td>
                            <td>Did they build what the brief asked for?</td>
                        </tr>
                        <tr>
                            <td><strong>Functionality / Effectiveness</strong></td>
                            <td><span style="color: var(--accent-emerald); font-weight:800;">25%</span></td>
                            <td>The solution works and does its job reliably</td>
                            <td>App runs / dashboard answers Qs / report is sound / design is usable</td>
                        </tr>
                        <tr>
                            <td><strong>Technical Quality / Craft</strong></td>
                            <td><span style="color: var(--accent-emerald); font-weight:800;">15%</span></td>
                            <td>Clean, sensible build; good practices for the level</td>
                            <td>Code / model / design / test / config quality</td>
                        </tr>
                        <tr>
                            <td><strong>User Experience / Clarity</strong></td>
                            <td><span style="color: var(--accent-emerald); font-weight:800;">15%</span></td>
                            <td>Clear, usable, well-presented for the intended user</td>
                            <td>Ease of use, readability, presentation</td>
                        </tr>
                        <tr>
                            <td><strong>Innovation & Nigerian-Context Fit</strong></td>
                            <td><span style="color: var(--accent-emerald); font-weight:800;">10%</span></td>
                            <td>Thoughtful approach; genuinely fits the local problem</td>
                            <td>Relevance and creativity for the Nigerian context</td>
                        </tr>
                        <tr>
                            <td><strong>Documentation & Demo Video</strong></td>
                            <td><span style="color: var(--accent-emerald); font-weight:800;">15%</span></td>
                            <td>Clear README + a demo video explaining their own work</td>
                            <td>Understanding demonstrated; reproducible</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="rubric-card">
                <h2>🏅 Score Bands & Certification Standards</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1rem;">
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: var(--radius-md); padding: 1.25rem;">
                        <div style="color: #34D399; font-size: 1.2rem; font-weight: 800;">80 - 100 PTS</div>
                        <div style="font-weight: 700; margin-top: 0.2rem;">DISTINCTION</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.4rem;">Exceeds expectations; portfolio-ready presentation.</div>
                    </div>
                    <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: var(--radius-md); padding: 1.25rem;">
                        <div style="color: #818CF8; font-size: 1.2rem; font-weight: 800;">60 - 79 PTS</div>
                        <div style="font-weight: 700; margin-top: 0.2rem;">PASS (CERTIFIED)</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.4rem;">Meets standard requirements for 3MTT certification.</div>
                    </div>
                    <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: var(--radius-md); padding: 1.25rem;">
                        <div style="color: #FBBF24; font-size: 1.2rem; font-weight: 800;">40 - 59 PTS</div>
                        <div style="font-weight: 700; margin-top: 0.2rem;">REVISE & RESUBMIT</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.4rem;">Close to pass; return with feedback if time permits.</div>
                    </div>
                    <div style="background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: var(--radius-md); padding: 1.25rem;">
                        <div style="color: #F87171; font-size: 1.2rem; font-weight: 800;">0 - 39 PTS</div>
                        <div style="font-weight: 700; margin-top: 0.2rem;">NOT YET MET</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.4rem;">Does not meet certification standard.</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB PAGE 3: SCORE CALCULATOR -->
        <section id="tab-calculator" class="content-tab-page">
            <div class="calc-grid">
                <div>
                    <div class="rubric-card">
                        <h2>🧮 Interactive Fellow Score Calculator</h2>
                        <p style="color: var(--text-muted); margin-bottom: 1.5rem;">
                            Rate the Fellow from 1 to 5 for each criterion. Scores calculate automatically based on rubric weightings.
                        </p>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div class="calc-form-group">
                                <label>Fellow Full Name</label>
                                <input type="text" id="calc-fellow-name" class="calc-input" placeholder="e.g. Amina Bello">
                            </div>
                            <div class="calc-form-group">
                                <label>Fellow ID</label>
                                <input type="text" id="calc-fellow-id" class="calc-input" placeholder="e.g. FELL-2026-9041">
                            </div>
                            <div class="calc-form-group">
                                <label>Track</label>
                                <select id="calc-track" class="calc-input"></select>
                            </div>
                            <div class="calc-form-group">
                                <label>Brief ID</label>
                                <input type="text" id="calc-brief-id" class="calc-input" placeholder="e.g. SD-01">
                            </div>
                            <div class="calc-form-group">
                                <label>Reviewer Name</label>
                                <input type="text" id="calc-reviewer" class="calc-input" placeholder="Evaluator Name">
                            </div>
                            <div class="calc-form-group">
                                <label>Date</label>
                                <input type="date" id="calc-date" class="calc-input">
                            </div>
                        </div>

                        <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 1.5rem 0;">

                        <!-- Criteria Rating Inputs -->
                        <div id="rating-criteria-list">
                            <!-- JS dynamic rating rows -->
                        </div>

                        <div class="calc-form-group" style="margin-top: 1.5rem;">
                            <label>Reviewer Comments & Feedback</label>
                            <textarea id="calc-comments" class="calc-input" rows="3" placeholder="Provide constructive feedback for the fellow..."></textarea>
                        </div>
                    </div>
                </div>

                <!-- Calculator Output Sticky Box -->
                <div>
                    <div class="score-summary-box">
                        <div style="font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase;">Total Rubric Score</div>
                        <div class="score-number" id="calc-total-score">60</div>
                        <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem;">Out of 100 Points</div>

                        <div id="calc-result-badge" class="score-band-badge" style="background: rgba(99, 102, 241, 0.2); color: #818CF8;">
                            PASS - CERTIFIED
                        </div>

                        <hr style="border: 0; border-top: 1px solid var(--border-color); margin: 1.5rem 0;">

                        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                            <button class="btn btn-primary" style="justify-content: center;" onclick="copyEvaluationSummary()">
                                📋 Copy Evaluation Summary
                            </button>
                            <button class="btn btn-outline" style="justify-content: center;" onclick="window.print()">
                                🖨️ Print Evaluation Card
                            </button>
                            <button class="btn btn-outline" style="justify-content: center; font-size: 0.8rem;" onclick="resetCalculator()">
                                🔄 Reset Form
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB PAGE 4: DATA SOURCES -->
        <section id="tab-data-sources" class="content-tab-page">
            <div class="rubric-card">
                <h2>🌐 Data Sources Guide</h2>
                <p style="color: var(--text-muted); margin-bottom: 1.5rem;">
                    For data-driven briefs (AI/ML, Data Analysis & Visualization, Data Science).
                </p>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin-bottom: 2rem;">
                    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.25rem;">
                        <div style="font-size: 1.25rem; margin-bottom: 0.5rem;">1. 📊 Open Datasets</div>
                        <p style="font-size: 0.875rem; color: var(--text-muted);">
                            Download from public Nigerian or global open-data portals. Best when reliable public data exists (prices, health, power, elections).
                        </p>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.25rem;">
                        <div style="font-size: 1.25rem; margin-bottom: 0.5rem;">2. 📝 Collect Your Own Data</div>
                        <p style="font-size: 0.875rem; color: var(--text-muted);">
                            Gather real data locally — a short survey (Google Forms), local business records (with permission), or observations. Adds strong authenticity.
                        </p>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.25rem;">
                        <div style="font-size: 1.25rem; margin-bottom: 0.5rem;">3. ⚙️ Synthetic Mock Data</div>
                        <p style="font-size: 0.875rem; color: var(--text-muted);">
                            Create realistic mock data where no real data is practical. Clearly document generation methods in the README.
                        </p>
                    </div>
                </div>

                <h3>Key Open-Data Sources (Nigeria & Global)</h3>
                <div class="table-wrapper" style="margin-top: 1rem;">
                    <table class="briefs-table">
                        <thead>
                            <tr>
                                <th>Source</th>
                                <th>What You'll Find</th>
                                <th>Portal Link</th>
                            </tr>
                        </thead>
                        <tbody id="data-sources-table-body"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- TAB PAGE 5: BOOKMARKS -->
        <section id="tab-bookmarks" class="content-tab-page">
            <div class="rubric-card" style="margin-bottom: 1.5rem;">
                <h2>⭐ Saved Bookmarks</h2>
                <p style="color: var(--text-muted);">View your bookmarked capstone briefs for quick access.</p>
            </div>
            <div id="bookmarks-grid" class="briefs-grid"></div>
            <div id="bookmarks-empty" class="empty-state" style="display: none;">
                <h3>No bookmarked briefs yet</h3>
                <p style="margin-top: 0.5rem;">Click the ⭐ icon on any brief card to save it here for quick reference.</p>
            </div>
        </section>

    </div>

    <!-- BRIEF DETAIL MODAL -->
    <div class="modal-backdrop" id="brief-modal" onclick="closeModalOnBackdrop(event)">
        <div class="modal-box">
            <div class="modal-header">
                <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.4rem;">
                        <span id="modal-brief-id" class="brief-id-badge" style="background: var(--accent-emerald); color:#000;">SD-01</span>
                        <span id="modal-track" class="brief-track-name">Software Development</span>
                        <span id="modal-diff" class="diff-badge diff-beginner">Beginner</span>
                    </div>
                    <h2 id="modal-title" class="brief-title" style="font-size: 1.35rem;">POS Transaction Web App</h2>
                </div>
                <button class="modal-close-btn" onclick="closeModal()">×</button>
            </div>
            <div class="modal-body">
                <div class="detail-section">
                    <div class="detail-label">🇳🇬 Nigerian Problem Context</div>
                    <div id="modal-problem" class="detail-content"></div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">🚀 What to Build (MVP Scope)</div>
                    <div id="modal-solution" class="detail-content"></div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">🛠️ Core MVP Features</div>
                    <div id="modal-features" class="detail-content"></div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">📦 Expected Deliverables</div>
                    <div id="modal-deliverables" class="detail-content"></div>
                </div>
                <div class="detail-section">
                    <div class="detail-label">🧰 Suggested Tools & Tech Stack</div>
                    <div id="modal-tools" class="detail-content"></div>
                </div>
            </div>
            <div class="modal-footer">
                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-outline" id="modal-bookmark-btn" onclick="toggleModalBookmark()">
                        ⭐ Bookmark
                    </button>
                    <button class="btn btn-outline" onclick="copyBriefLink()">
                        🔗 Copy Brief Info
                    </button>
                </div>
                <button class="btn btn-primary" onclick="openBriefInCalculator()">
                    🧮 Score in Calculator
                </button>
            </div>
        </div>
    </div>

    <!-- Toast Notifications -->
    <div class="toast-container" id="toast-container"></div>

    <!-- EMBEDDED DATA & APPLICATION LOGIC -->
    <script>
        const ALL_BRIEFS = {briefs_json};
        const DATA_SOURCES = {data_sources_json};

        // State Management
        let currentTrack = 'ALL';
        let currentSearch = '';
        let currentDiff = 'ALL';
        let currentSort = 'id_asc';
        let viewMode = 'grid';
        let bookmarks = new Set(JSON.parse(localStorage.getItem('brief_bookmarks') || '[]'));
        let activeModalBriefId = null;

        // Color palettes per track
        const trackColors = {{
            'AI - Machine Learning': {{ bg: 'rgba(16, 185, 129, 0.15)', text: '#34D399', border: 'rgba(16, 185, 129, 0.4)', icon: '🤖' }},
            'Animation': {{ bg: 'rgba(139, 92, 246, 0.15)', text: '#A78BFA', border: 'rgba(139, 92, 246, 0.4)', icon: '🎬' }},
            'Cloud Computing': {{ bg: 'rgba(6, 182, 212, 0.15)', text: '#22D3EE', border: 'rgba(6, 182, 212, 0.4)', icon: '☁️' }},
            'UI-UX Design': {{ bg: 'rgba(236, 72, 153, 0.15)', text: '#F472B6', border: 'rgba(236, 72, 153, 0.4)', icon: '🎨' }},
            'Data Analysis and Visualization': {{ bg: 'rgba(20, 184, 166, 0.15)', text: '#2DD4BF', border: 'rgba(20, 184, 166, 0.4)', icon: '📊' }},
            'Data Science': {{ bg: 'rgba(99, 102, 241, 0.15)', text: '#818CF8', border: 'rgba(99, 102, 241, 0.4)', icon: '🔬' }},
            'DevOps': {{ bg: 'rgba(245, 158, 11, 0.15)', text: '#FBBF24', border: 'rgba(245, 158, 11, 0.4)', icon: '⚙️' }},
            'Game Development': {{ bg: 'rgba(217, 70, 239, 0.15)', text: '#E879F9', border: 'rgba(217, 70, 239, 0.4)', icon: '🎮' }},
            'Product Management': {{ bg: 'rgba(132, 204, 22, 0.15)', text: '#A3E635', border: 'rgba(132, 204, 22, 0.4)', icon: '📋' }},
            'Quality Assurance': {{ bg: 'rgba(239, 68, 68, 0.15)', text: '#F87171', border: 'rgba(239, 68, 68, 0.4)', icon: '🧪' }},
            'Software Development': {{ bg: 'rgba(59, 130, 246, 0.15)', text: '#60A5FA', border: 'rgba(59, 130, 246, 0.4)', icon: '💻' }},
            'Cybersecurity': {{ bg: 'rgba(234, 179, 8, 0.15)', text: '#FACC15', border: 'rgba(234, 179, 8, 0.4)', icon: '🛡️' }}
        }};

        // Criteria Rubric Setup
        const criteriaList = [
            {{ key: 'c1', name: 'Adherence to Brief & Completeness', weight: 20, maxScore: 20 }},
            {{ key: 'c2', name: 'Functionality / Effectiveness', weight: 25, maxScore: 25 }},
            {{ key: 'c3', name: 'Technical Quality / Craft', weight: 15, maxScore: 15 }},
            {{ key: 'c4', name: 'User Experience / Clarity', weight: 15, maxScore: 15 }},
            {{ key: 'c5', name: 'Innovation & Nigerian-Context Fit', weight: 10, maxScore: 10 }},
            {{ key: 'c6', name: 'Documentation & Demo Video', weight: 15, maxScore: 15 }}
        ];

        let ratings = {{ c1: 3, c2: 3, c3: 3, c4: 3, c5: 3, c6: 3 }};

        // Initialize App
        document.addEventListener('DOMContentLoaded', () => {{
            renderTrackPills();
            renderFilteredBriefs();
            renderDataSources();
            initCalculator();
            updateBookmarkBadge();

            // Keyboard shortcut '/'
            document.addEventListener('keydown', (e) => {{
                if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {{
                    e.preventDefault();
                    document.getElementById('search-input').focus();
                }}
            }});
        }});

        // Render Track Pills
        function renderTrackPills() {{
            const container = document.getElementById('track-pills');
            const tracks = Object.keys(trackColors);
            
            let html = `<button class="track-pill active" onclick="selectTrack('ALL')">🚀 All Tracks (240)</button>`;
            
            tracks.forEach(track => {{
                const count = ALL_BRIEFS.filter(b => b.track === track).length;
                const icon = trackColors[track]?.icon || '📁';
                html += `<button class="track-pill" data-track="${{track}}" onclick="selectTrack('${{track}}')">${{icon}} ${{track}} (${{count}})</button>`;
            }});
            
            container.innerHTML = html;
        }}

        function selectTrack(track) {{
            currentTrack = track;
            document.querySelectorAll('.track-pill').forEach(btn => {{
                if (btn.getAttribute('data-track') === track || (track === 'ALL' && btn.innerText.includes('All Tracks'))) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});
            
            document.getElementById('active-track-name').innerText = track === 'ALL' ? 'All Tracks' : track;
            renderFilteredBriefs();
        }}

        // Filter and Sort Engine
        function renderFilteredBriefs() {{
            currentDiff = document.getElementById('diff-filter').value;
            currentSort = document.getElementById('sort-select').value;
            
            let filtered = ALL_BRIEFS.filter(b => {{
                const matchTrack = (currentTrack === 'ALL' || b.track === currentTrack);
                const matchDiff = (currentDiff === 'ALL' || b.difficulty === currentDiff);
                
                let matchSearch = true;
                if (currentSearch) {{
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
                }}
                return matchTrack && matchDiff && matchSearch;
            }});

            // Sorting logic
            filtered.sort((a, b) => {{
                if (currentSort === 'id_asc') return a.id.localeCompare(b.id, undefined, {{numeric: true}});
                if (currentSort === 'id_desc') return b.id.localeCompare(a.id, undefined, {{numeric: true}});
                if (currentSort === 'title_asc') return a.title.localeCompare(b.title);
                if (currentSort === 'title_desc') return b.title.localeCompare(a.title);
                if (currentSort === 'track_asc') return a.track.localeCompare(b.track);
                if (currentSort === 'diff') {{
                    const level = {{ 'Beginner': 1, 'Beginner-Intermediate': 2, 'Intermediate': 3 }};
                    return (level[a.difficulty] || 1) - (level[b.difficulty] || 1);
                }}
                return 0;
            }});

            // Update UI count
            document.getElementById('results-count').innerText = `Showing ${{filtered.length}} of ${{ALL_BRIEFS.length}} briefs`;
            
            if (filtered.length === 0) {{
                document.getElementById('briefs-grid').style.display = 'none';
                document.getElementById('briefs-table-container').style.display = 'none';
                document.getElementById('empty-state').style.display = 'block';
                return;
            }} else {{
                document.getElementById('empty-state').style.display = 'none';
            }}

            if (viewMode === 'grid') {{
                document.getElementById('briefs-grid').style.display = 'grid';
                document.getElementById('briefs-table-container').style.display = 'none';
                renderGridCards(filtered);
            }} else {{
                document.getElementById('briefs-grid').style.display = 'none';
                document.getElementById('briefs-table-container').style.display = 'block';
                renderTableRows(filtered);
            }}
        }}

        function highlightText(text, search) {{
            if (!search) return text;
            const regex = new RegExp(`(${{search.replace(/[.*+?^${{}}()|[\\]\\]/g, '\\$&')}})`, 'gi');
            return text.replace(regex, '<span class="highlight-text">$1</span>');
        }}

        function renderGridCards(briefs) {{
            const container = document.getElementById('briefs-grid');
            let html = '';
            
            briefs.forEach(b => {{
                const style = trackColors[b.track] || {{ bg: 'rgba(255,255,255,0.1)', text: '#FFF', border: 'transparent' }};
                const isBookmarked = bookmarks.has(b.id);
                const diffClass = b.difficulty === 'Beginner' ? 'diff-beginner' : (b.difficulty === 'Intermediate' ? 'diff-intermediate' : 'diff-beginner-intermediate');
                
                // Feature chips
                const featureList = b.features.split(';').slice(0, 3);
                const chipsHtml = featureList.map(f => `<span class="feature-chip">${{highlightText(f.trim(), currentSearch)}}</span>`).join('');

                html += `
                <div class="brief-card" onclick="openModal('${{b.id}}')">
                    <div class="card-header">
                        <span class="brief-id-badge" style="background:${{style.bg}}; color:${{style.text}}; border:1px solid ${{style.border}};">${{highlightText(b.id, currentSearch)}}</span>
                        <div class="card-meta-right">
                            <span class="diff-badge ${{diffClass}}">${{b.difficulty}}</span>
                            <button class="bookmark-star-btn ${{isBookmarked ? 'bookmarked' : ''}}" onclick="event.stopPropagation(); toggleBookmark('${{b.id}}')">
                                ${{isBookmarked ? '★' : '☆'}}
                            </button>
                        </div>
                    </div>

                    <div>
                        <div class="brief-track-name" style="color:${{style.text}}">${{b.track}}</div>
                        <h3 class="brief-title">${{highlightText(b.title, currentSearch)}}</h3>
                    </div>

                    <div class="brief-problem">
                        🇳🇬 <strong>Problem:</strong> ${{highlightText(b.problem, currentSearch)}}
                    </div>

                    <div class="brief-solution">
                        🚀 ${{highlightText(b.solution, currentSearch)}}
                    </div>

                    <div class="card-features-chips">
                        ${{chipsHtml}}
                    </div>
                </div>
                `;
            }});
            
            container.innerHTML = html;
        }}

        function renderTableRows(briefs) {{
            const tbody = document.getElementById('briefs-table-body');
            let html = '';
            
            briefs.forEach(b => {{
                const style = trackColors[b.track] || {{ text: '#FFF' }};
                const diffClass = b.difficulty === 'Beginner' ? 'diff-beginner' : (b.difficulty === 'Intermediate' ? 'diff-intermediate' : 'diff-beginner-intermediate');
                const isBookmarked = bookmarks.has(b.id);

                html += `
                <tr onclick="openModal('${{b.id}}')">
                    <td><strong style="color:var(--accent-emerald);">${{b.id}}</strong></td>
                    <td style="color:${{style.text}}; font-weight:600;">${{b.track}}</td>
                    <td><strong>${{b.title}}</strong></td>
                    <td style="max-width: 250px; color:var(--text-muted);">${{b.problem}}</td>
                    <td style="max-width: 250px;">${{b.solution}}</td>
                    <td><span class="diff-badge ${{diffClass}}">${{b.difficulty}}</span></td>
                    <td>
                        <button class="bookmark-star-btn ${{isBookmarked ? 'bookmarked' : ''}}" onclick="event.stopPropagation(); toggleBookmark('${{b.id}}')">
                            ${{isBookmarked ? '★' : '☆'}}
                        </button>
                    </td>
                </tr>
                `;
            }});
            
            tbody.innerHTML = html;
        }}

        // Search Controls
        function handleSearchInput() {{
            const val = document.getElementById('search-input').value;
            currentSearch = val;
            const clearBtn = document.getElementById('clear-search-btn');
            if (val) clearBtn.classList.add('visible');
            else clearBtn.classList.remove('visible');
            renderFilteredBriefs();
        }}

        function clearSearch() {{
            document.getElementById('search-input').value = '';
            currentSearch = '';
            document.getElementById('clear-search-btn').classList.remove('visible');
            renderFilteredBriefs();
        }}

        function resetFilters() {{
            document.getElementById('search-input').value = '';
            currentSearch = '';
            currentDiff = 'ALL';
            currentSort = 'id_asc';
            document.getElementById('diff-filter').value = 'ALL';
            document.getElementById('sort-select').value = 'id_asc';
            selectTrack('ALL');
        }}

        function setViewMode(mode) {{
            viewMode = mode;
            document.getElementById('view-grid-btn').classList.toggle('active', mode === 'grid');
            document.getElementById('view-table-btn').classList.toggle('active', mode === 'table');
            renderFilteredBriefs();
        }}

        // Modal Functionality
        function openModal(id) {{
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
        }}

        function closeModal() {{
            document.getElementById('brief-modal').classList.remove('active');
        }}

        function closeModalOnBackdrop(e) {{
            if (e.target.id === 'brief-modal') closeModal();
        }}

        function toggleModalBookmark() {{
            if (activeModalBriefId) {{
                toggleBookmark(activeModalBriefId);
                const isBookmarked = bookmarks.has(activeModalBriefId);
                document.getElementById('modal-bookmark-btn').innerText = isBookmarked ? '★ Bookmarked' : '☆ Bookmark';
            }}
        }}

        function toggleBookmark(id) {{
            if (bookmarks.has(id)) {{
                bookmarks.delete(id);
                showToast(`Removed ${{id}} from bookmarks`);
            }} else {{
                bookmarks.add(id);
                showToast(`Saved ${{id}} to bookmarks ⭐`);
            }}
            localStorage.setItem('brief_bookmarks', JSON.stringify(Array.from(bookmarks)));
            updateBookmarkBadge();
            renderFilteredBriefs();
            renderBookmarksPage();
        }}

        function updateBookmarkBadge() {{
            document.getElementById('bookmark-count-badge').innerText = bookmarks.size;
        }}

        function renderBookmarksPage() {{
            const container = document.getElementById('bookmarks-grid');
            const empty = document.getElementById('bookmarks-empty');
            const bookmarkedBriefs = ALL_BRIEFS.filter(b => bookmarks.has(b.id));

            if (bookmarkedBriefs.length === 0) {{
                container.style.display = 'none';
                empty.style.display = 'block';
                return;
            }}

            empty.style.display = 'none';
            container.style.display = 'grid';

            let html = '';
            bookmarkedBriefs.forEach(b => {{
                const style = trackColors[b.track] || {{ bg: 'rgba(255,255,255,0.1)', text: '#FFF' }};
                const diffClass = b.difficulty === 'Beginner' ? 'diff-beginner' : (b.difficulty === 'Intermediate' ? 'diff-intermediate' : 'diff-beginner-intermediate');

                html += `
                <div class="brief-card" onclick="openModal('${{b.id}}')">
                    <div class="card-header">
                        <span class="brief-id-badge" style="background:${{style.bg}}; color:${{style.text}};">${{b.id}}</span>
                        <div class="card-meta-right">
                            <span class="diff-badge ${{diffClass}}">${{b.difficulty}}</span>
                            <button class="bookmark-star-btn bookmarked" onclick="event.stopPropagation(); toggleBookmark('${{b.id}}')">★</button>
                        </div>
                    </div>
                    <div>
                        <div class="brief-track-name" style="color:${{style.text}}">${{b.track}}</div>
                        <h3 class="brief-title">${{b.title}}</h3>
                    </div>
                    <div class="brief-solution">🚀 ${{b.solution}}</div>
                </div>
                `;
            }});
            container.innerHTML = html;
        }}

        function copyBriefLink() {{
            if (!activeModalBriefId) return;
            const brief = ALL_BRIEFS.find(b => b.id === activeModalBriefId);
            const text = `3MTT Brief [${{brief.id}}]: ${{brief.title}}\nTrack: ${{brief.track}}\nScope: ${{brief.solution}}\nDeliverables: ${{brief.deliverables}}`;
            navigator.clipboard.writeText(text);
            showToast('Brief summary copied to clipboard!');
        }}

        // Switch Navigation Tabs
        function switchTab(tabId) {{
            document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.content-tab-page').forEach(page => page.classList.remove('active'));

            const targetBtn = Array.from(document.querySelectorAll('.nav-tab')).find(b => b.getAttribute('onclick').includes(tabId));
            if (targetBtn) targetBtn.classList.add('active');

            const page = document.getElementById(`tab-${{tabId}}`);
            if (page) page.classList.add('active');

            if (tabId === 'bookmarks') renderBookmarksPage();
        }}

        // Calculator Logic
        function initCalculator() {{
            // Populate tracks select
            const trackSelect = document.getElementById('calc-track');
            trackSelect.innerHTML = Object.keys(trackColors).map(t => `<option value="${{t}}">${{t}}</option>`).join('');

            // Set current date
            document.getElementById('calc-date').valueAsDate = new Date();

            // Render criteria ratings
            const container = document.getElementById('rating-criteria-list');
            let html = '';

            criteriaList.forEach(c => {{
                html += `
                <div class="calc-form-group" style="margin-bottom: 1.2rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <label style="font-size:0.9rem; color:var(--text-main); font-weight:700;">${{c.name}} (${{c.weight}}%)</label>
                        <span id="score-val-${{c.key}}" style="color:var(--accent-emerald); font-weight:800; font-size:0.9rem;">Rating: 3/5</span>
                    </div>
                    <div class="rating-selector">
                        ${{[1,2,3,4,5].map(rating => `
                            <button class="rating-btn ${{rating === 3 ? 'active' : ''}}" data-key="${{c.key}}" data-rating="${{rating}}" onclick="setRating('${{c.key}}', ${{rating}})">
                                ${{rating}}
                            </button>
                        `).join('')}}
                    </div>
                </div>
                `;
            }});
            container.innerHTML = html;
            calculateTotalScore();
        }}

        function setRating(key, rating) {{
            ratings[key] = rating;
            document.querySelectorAll(`button[data-key="${{key}}"]`).forEach(btn => {{
                btn.classList.toggle('active', parseInt(btn.getAttribute('data-rating')) === rating);
            }});
            document.getElementById(`score-val-${{key}}`).innerText = `Rating: ${{rating}}/5`;
            calculateTotalScore();
        }}

        function calculateTotalScore() {{
            let total = 0;
            criteriaList.forEach(c => {{
                const rating = ratings[c.key] || 3;
                const score = (rating / 5) * c.weight;
                total += score;
            }});

            const totalScoreRounded = Math.round(total);
            document.getElementById('calc-total-score').innerText = totalScoreRounded;

            const badge = document.getElementById('calc-result-badge');
            if (totalScoreRounded >= 80) {{
                badge.innerText = 'DISTINCTION';
                badge.style.background = 'rgba(16, 185, 129, 0.2)';
                badge.style.color = '#34D399';
            }} else if (totalScoreRounded >= 60) {{
                badge.innerText = 'PASS - CERTIFIED';
                badge.style.background = 'rgba(99, 102, 241, 0.2)';
                badge.style.color = '#818CF8';
            }} else if (totalScoreRounded >= 40) {{
                badge.innerText = 'REVISE & RESUBMIT';
                badge.style.background = 'rgba(245, 158, 11, 0.2)';
                badge.style.color = '#FBBF24';
            }} else {{
                badge.innerText = 'NOT YET MET';
                badge.style.background = 'rgba(244, 63, 94, 0.2)';
                badge.style.color = '#F87171';
            }}
        }}

        function openBriefInCalculator() {{
            if (!activeModalBriefId) return;
            const brief = ALL_BRIEFS.find(b => b.id === activeModalBriefId);
            closeModal();
            switchTab('calculator');
            document.getElementById('calc-brief-id').value = brief.id;
            document.getElementById('calc-track').value = brief.track;
            showToast(`Loaded ${{brief.id}} into Score Calculator`);
        }}

        function copyEvaluationSummary() {{
            const name = document.getElementById('calc-fellow-name').value || 'N/A';
            const fId = document.getElementById('calc-fellow-id').value || 'N/A';
            const track = document.getElementById('calc-track').value;
            const bId = document.getElementById('calc-brief-id').value || 'N/A';
            const reviewer = document.getElementById('calc-reviewer').value || 'N/A';
            const date = document.getElementById('calc-date').value || 'N/A';
            const score = document.getElementById('calc-total-score').innerText;
            const result = document.getElementById('calc-result-badge').innerText;
            const comments = document.getElementById('calc-comments').value || 'None';

            const text = `====================================\n3MTT NEXTGEN FELLOW EVALUATION SCORECARD\n====================================\nFellow Name: ${{name}}\nFellow ID: ${{fId}}\nTrack: ${{track}}\nBrief ID: ${{bId}}\nReviewer: ${{reviewer}}\nDate: ${{date}}\n\nRubric Score: ${{score}} / 100\nFinal Result: ${{result}}\n\nReviewer Comments:\n${{comments}}\n====================================`;

            navigator.clipboard.writeText(text);
            showToast('Evaluation report copied to clipboard!');
        }}

        function resetCalculator() {{
            document.getElementById('calc-fellow-name').value = '';
            document.getElementById('calc-fellow-id').value = '';
            document.getElementById('calc-brief-id').value = '';
            document.getElementById('calc-reviewer').value = '';
            document.getElementById('calc-comments').value = '';
            ratings = {{ c1: 3, c2: 3, c3: 3, c4: 3, c5: 3, c6: 3 }};
            initCalculator();
            showToast('Calculator reset');
        }}

        // Data Sources Render
        function renderDataSources() {{
            const tbody = document.getElementById('data-sources-table-body');
            let html = '';

            DATA_SOURCES.forEach(ds => {{
                if (ds.name.includes('KEY OPEN-DATA') || ds.name.includes('THREE WAYS') || ds.name.includes('Source') || !ds.url) return;

                html += `
                <tr>
                    <td><strong>${{ds.name}}</strong></td>
                    <td>${{ds.description}}</td>
                    <td><a href="https://${{ds.url.split('/')[0]}}" target="_blank" style="color:var(--accent-teal); font-weight:600; text-decoration:none;">${{ds.url}} ↗</a></td>
                </tr>
                `;
            }});
            tbody.innerHTML = html;
        }}

        // CSV Export
        function exportFilteredCSV() {{
            let filtered = ALL_BRIEFS.filter(b => {{
                const matchTrack = (currentTrack === 'ALL' || b.track === currentTrack);
                const matchDiff = (currentDiff === 'ALL' || b.difficulty === currentDiff);
                return matchTrack && matchDiff;
            }});

            let csv = 'Brief ID,Track,Title,Difficulty,Nigerian Problem Context,What to Build (MVP),Core MVP Features,Expected Deliverables,Suggested Tools\n';
            
            filtered.forEach(b => {{
                const escape = (str) => `"${{(str || '').replace(/"/g, '""')}}"`;
                csv += `${{escape(b.id)}},${{escape(b.track)}},${{escape(b.title)}},${{escape(b.difficulty)}},${{escape(b.problem)}},${{escape(b.solution)}},${{escape(b.features)}},${{escape(b.deliverables)}},${{escape(b.tools)}}\n`;
            }});

            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.setAttribute('href', url);
            link.setAttribute('download', `3MTT_Project_Briefs_${{currentTrack.replace(/[^a-zA-Z0-9]/g, '_')}}.csv`);
            link.click();
            showToast('Exported briefs to CSV!');
        }}

        // Theme Toggle
        function toggleTheme() {{
            const isLight = document.body.getAttribute('data-theme') === 'light';
            if (isLight) {{
                document.body.removeAttribute('data-theme');
                document.getElementById('theme-btn').innerText = '🌙';
            }} else {{
                document.body.setAttribute('data-theme', 'light');
                document.getElementById('theme-btn').innerText = '☀️';
            }}
        }}

        // Toast Helper
        function showToast(msg) {{
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerText = msg;
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }}
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('3MTT_NextGen_Project_Brief_Bank.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("index.html and 3MTT_NextGen_Project_Brief_Bank.html successfully generated!")
