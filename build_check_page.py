import csv
import json

csv_file_path = "02Innovations_Lab_Fellows.csv"
html_file_path = "check.html"

fellows = []
with open(csv_file_path, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader, 1):
        first = row.get('First Name', '').strip()
        last = row.get('Last Name', '').strip()
        name = row.get('name', '').strip() or f"{first} {last}".strip()
        email = row.get('Email', '').strip()
        phone_raw = row.get('PHONENUMBER', '').strip()
        
        # Clean phone
        phone_clean = phone_raw
        if phone_clean.endswith('.0'):
            phone_clean = phone_clean[:-2]
            
        if phone_clean.startswith('+234'):
            phone_display = '0' + phone_clean[4:]
        elif len(phone_clean) == 10 and not phone_clean.startswith('0'):
            phone_display = '0' + phone_clean
        else:
            phone_display = phone_clean
            
        fellow_id = row.get('FELLOW ID', '').strip()
        cohort = row.get('Cohort', '').strip() or row.get('course', '').strip()
        state = row.get('STATE', '').strip()
        provider = row.get('PROVIDER NAME', '').strip()
        topic = row.get('ASSIGNED TOPIC', '').strip() or row.get('topic', '').strip()
        
        fellows.append({
            'id': idx,
            'firstName': first,
            'lastName': last,
            'name': name,
            'email': email,
            'phoneRaw': phone_raw,
            'phone': phone_display,
            'fellowId': fellow_id,
            'cohort': cohort,
            'state': state,
            'provider': provider,
            'topic': topic
        })

fellows_json = json.dumps(fellows, indent=2)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fellow Search & Verification Portal | 02Innovations Lab</title>
  <meta name="description" content="Official Fellow Verification Portal for 02Innovations Lab. Search fellow record by Email, Fellow ID, or Phone Number.">
  
  <!-- Google Fonts & Font Awesome Icons -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <style>
    :root {{
      --bg-dark: #090d16;
      --bg-card: rgba(17, 24, 39, 0.75);
      --bg-card-hover: rgba(30, 41, 59, 0.85);
      --bg-input: rgba(15, 23, 42, 0.8);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-glow: rgba(59, 130, 246, 0.4);
      --primary: #3b82f6;
      --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
      --accent-cyan: #06b6d4;
      --accent-indigo: #6366f1;
      --accent-emerald: #10b981;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
      --text-dim: #6b7280;
      --radius-lg: 16px;
      --radius-md: 12px;
      --radius-sm: 8px;
      --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(59, 130, 246, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(99, 102, 241, 0.1) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 60%);
      background-attachment: fixed;
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      line-height: 1.6;
    }}

    /* Container */
    .container {{
      max-width: 1000px;
      margin: 0 auto;
      padding: 0 20px;
      width: 100%;
    }}

    /* Header */
    header {{
      border-bottom: 1px solid var(--border-color);
      backdrop-filter: blur(12px);
      background: rgba(9, 13, 22, 0.8);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 16px 0;
    }}

    .header-content {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 14px;
      text-decoration: none;
      color: inherit;
    }}

    .brand-logo {{
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, #2563eb, #06b6d4);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 20px;
      box-shadow: 0 4px 20px rgba(37, 99, 235, 0.35);
    }}

    .brand-text h1 {{
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(to right, #ffffff, #93c5fd);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .brand-text p {{
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 500;
    }}

    .header-badges {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      border-radius: 20px;
      color: #34d399;
      font-size: 12px;
      font-weight: 600;
    }}

    .status-dot {{
      width: 8px;
      height: 8px;
      background-color: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 10px #10b981;
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0% {{ opacity: 0.6; transform: scale(0.95); }}
      50% {{ opacity: 1; transform: scale(1.15); }}
      100% {{ opacity: 0.6; transform: scale(0.95); }}
    }}

    /* Hero Section */
    .hero {{
      padding: 48px 0 28px;
      text-align: center;
    }}

    .hero-title {{
      font-size: 34px;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin-bottom: 12px;
      line-height: 1.2;
    }}

    .hero-title span {{
      background: linear-gradient(135deg, #60a5fa, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero-subtitle {{
      color: var(--text-muted);
      font-size: 15px;
      max-width: 620px;
      margin: 0 auto 32px;
    }}

    /* Search Container Box */
    .search-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 28px;
      backdrop-filter: blur(16px);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
      margin-bottom: 32px;
    }}

    /* Search Mode Tabs */
    .search-tabs {{
      display: flex;
      justify-content: center;
      gap: 8px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }}

    .tab-btn {{
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 10px 20px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
    }}

    .tab-btn:hover {{
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.04);
      border-color: rgba(255, 255, 255, 0.2);
    }}

    .tab-btn.active {{
      background: rgba(59, 130, 246, 0.15);
      color: #60a5fa;
      border-color: rgba(59, 130, 246, 0.4);
      box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
    }}

    /* Main Search Bar */
    .search-input-wrapper {{
      position: relative;
    }}

    .search-icon {{
      position: absolute;
      left: 20px;
      top: 50%;
      transform: translateY(-50%);
      color: #60a5fa;
      font-size: 20px;
      pointer-events: none;
    }}

    .search-input {{
      width: 100%;
      padding: 20px 54px 20px 56px;
      background: var(--bg-input);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      color: var(--text-main);
      font-size: 16px;
      font-family: inherit;
      transition: var(--transition);
      outline: none;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }}

    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.25);
      background: rgba(15, 23, 42, 0.95);
    }}

    .clear-btn {{
      position: absolute;
      right: 20px;
      top: 50%;
      transform: translateY(-50%);
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: var(--text-muted);
      width: 30px;
      height: 30px;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      align-items: center;
      justify-content: center;
      transition: var(--transition);
    }}

    .clear-btn:hover {{
      background: rgba(255, 255, 255, 0.2);
      color: var(--text-main);
    }}

    /* Results Header / Stats */
    .results-info {{
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 24px;
    }}

    .results-count {{
      font-size: 14px;
      color: var(--text-muted);
      text-align: center;
    }}

    /* Grid Layout - Focused Single Card */
    .fellows-grid {{
      display: flex;
      justify-content: center;
      margin-bottom: 40px;
    }}

    /* Single Result Card Style */
    .fellow-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-glow);
      border-radius: var(--radius-lg);
      padding: 32px;
      transition: var(--transition);
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
      max-width: 580px;
      width: 100%;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(59, 130, 246, 0.15);
      background-image: radial-gradient(circle at top right, rgba(59, 130, 246, 0.1), transparent 60%);
    }}

    .fellow-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 4px;
      background: linear-gradient(90deg, #3b82f6, #06b6d4, #10b981);
    }}

    .card-top {{
      display: flex;
      align-items: flex-start;
      gap: 18px;
      margin-bottom: 22px;
    }}

    .avatar {{
      width: 60px;
      height: 60px;
      border-radius: 16px;
      background: linear-gradient(135deg, #1e293b, #334155);
      border: 1px solid rgba(255, 255, 255, 0.12);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      font-weight: 700;
      color: #60a5fa;
      flex-shrink: 0;
      box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.05);
    }}

    .fellow-name-group {{
      flex-grow: 1;
      overflow: hidden;
    }}

    .fellow-name {{
      font-size: 22px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 6px;
    }}

    .fellow-id-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      background: rgba(59, 130, 246, 0.12);
      color: #93c5fd;
      padding: 4px 12px;
      border-radius: 6px;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }}

    .copy-id-btn {{
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 12px;
      padding: 2px 4px;
      transition: var(--transition);
    }}

    .copy-id-btn:hover {{
      color: #60a5fa;
    }}

    .card-body {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 24px;
    }}

    .info-row {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 14px;
      color: var(--text-muted);
      background: rgba(15, 23, 42, 0.5);
      padding: 10px 14px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.04);
    }}

    .info-row i {{
      width: 20px;
      text-align: center;
      color: #60a5fa;
      font-size: 16px;
      flex-shrink: 0;
    }}

    .info-row span.val {{
      color: var(--text-main);
      font-weight: 600;
      word-break: break-all;
    }}

    .cohort-tag {{
      display: inline-block;
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.02em;
      text-transform: uppercase;
      margin-bottom: 16px;
      align-self: flex-start;
      border: 1px solid transparent;
    }}

    /* Cohort Accent Colors */
    .tag-3d {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border-color: rgba(245, 158, 11, 0.3); }}
    .tag-ai {{ background: rgba(168, 85, 247, 0.15); color: #c084fc; border-color: rgba(168, 85, 247, 0.3); }}
    .tag-cloud {{ background: rgba(14, 165, 233, 0.15); color: #38bdf8; border-color: rgba(14, 165, 233, 0.3); }}
    .tag-cyber {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: rgba(16, 185, 129, 0.3); }}
    .tag-data-an {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border-color: rgba(59, 130, 246, 0.3); }}
    .tag-data-sc {{ background: rgba(20, 184, 166, 0.15); color: #2dd4bf; border-color: rgba(20, 184, 166, 0.3); }}
    .tag-devops {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; border-color: rgba(244, 63, 94, 0.3); }}
    .tag-game {{ background: rgba(236, 72, 153, 0.15); color: #f472b6; border-color: rgba(236, 72, 153, 0.3); }}
    .tag-pm {{ background: rgba(234, 179, 8, 0.15); color: #facc15; border-color: rgba(234, 179, 8, 0.3); }}
    .tag-qa {{ background: rgba(132, 204, 22, 0.15); color: #a3e635; border-color: rgba(132, 204, 22, 0.3); }}
    .tag-soft {{ background: rgba(99, 102, 241, 0.15); color: #818cf8; border-color: rgba(99, 102, 241, 0.3); }}
    .tag-ui {{ background: rgba(192, 132, 252, 0.15); color: #e879f9; border-color: rgba(192, 132, 252, 0.3); }}
    .tag-default {{ background: rgba(156, 163, 175, 0.15); color: #d1d5db; border-color: rgba(156, 163, 175, 0.3); }}

    .card-footer {{
      padding-top: 18px;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .verify-link {{
      color: #60a5fa;
      text-decoration: none;
      font-size: 14px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      transition: var(--transition);
    }}

    .verify-link:hover {{
      color: #93c5fd;
      gap: 10px;
    }}

    .card-actions {{
      display: flex;
      gap: 8px;
    }}

    .action-icon-btn {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: var(--transition);
      text-decoration: none;
      font-size: 14px;
    }}

    .action-icon-btn:hover {{
      background: rgba(59, 130, 246, 0.2);
      color: #60a5fa;
      border-color: rgba(59, 130, 246, 0.4);
    }}

    /* Initial Prompt State */
    .initial-state {{
      text-align: center;
      padding: 64px 20px;
      background: var(--bg-card);
      border: 1px dashed var(--border-color);
      border-radius: var(--radius-lg);
      margin-bottom: 40px;
    }}

    .initial-icon {{
      font-size: 54px;
      background: linear-gradient(135deg, #60a5fa, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 16px;
    }}

    .initial-title {{
      font-size: 22px;
      font-weight: 700;
      margin-bottom: 10px;
    }}

    .initial-desc {{
      color: var(--text-muted);
      font-size: 14px;
      max-width: 480px;
      margin: 0 auto;
    }}

    /* Empty State */
    .empty-state {{
      text-align: center;
      padding: 64px 20px;
      background: var(--bg-card);
      border: 1px dashed var(--border-color);
      border-radius: var(--radius-lg);
      margin-bottom: 40px;
      display: none;
    }}

    .empty-icon {{
      font-size: 48px;
      color: var(--text-dim);
      margin-bottom: 16px;
    }}

    .empty-title {{
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 8px;
    }}

    .empty-desc {{
      color: var(--text-muted);
      font-size: 14px;
      max-width: 420px;
      margin: 0 auto 20px;
    }}

    /* Modal / Certificate View */
    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(8px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      opacity: 0;
      transition: opacity 0.25s ease;
    }}

    .modal-overlay.active {{
      display: flex;
      opacity: 1;
    }}

    .modal-card {{
      background: #0f172a;
      border: 1px solid var(--border-glow);
      border-radius: var(--radius-lg);
      max-width: 640px;
      width: 100%;
      padding: 36px;
      position: relative;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      background-image: radial-gradient(circle at top right, rgba(59, 130, 246, 0.15), transparent 50%);
      transform: scale(0.95);
      transition: transform 0.25s ease;
    }}

    .modal-overlay.active .modal-card {{
      transform: scale(1);
    }}

    .modal-close {{
      position: absolute;
      top: 20px;
      right: 20px;
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: var(--text-muted);
      width: 36px;
      height: 36px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: var(--transition);
    }}

    .modal-close:hover {{
      background: rgba(255, 255, 255, 0.2);
      color: white;
    }}

    .cert-header {{
      text-align: center;
      margin-bottom: 28px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 20px;
    }}

    .cert-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 182, 212, 0.2));
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: #34d399;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 14px;
    }}

    .cert-title {{
      font-size: 24px;
      font-weight: 800;
      color: var(--text-main);
    }}

    .cert-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-bottom: 28px;
    }}

    .cert-item {{
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid var(--border-color);
      padding: 14px 16px;
      border-radius: var(--radius-sm);
    }}

    .cert-item.full-width {{
      grid-column: span 2;
    }}

    .cert-label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 4px;
    }}

    .cert-value {{
      font-size: 15px;
      font-weight: 600;
      color: var(--text-main);
      word-break: break-all;
    }}

    .cert-actions {{
      display: flex;
      gap: 12px;
    }}

    .btn {{
      flex: 1;
      padding: 12px;
      border-radius: var(--radius-sm);
      font-weight: 600;
      font-size: 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: none;
      transition: var(--transition);
    }}

    .btn-primary {{
      background: var(--primary-gradient);
      color: white;
      box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35);
    }}

    .btn-primary:hover {{
      opacity: 0.95;
      transform: translateY(-1px);
    }}

    .btn-secondary {{
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-main);
      border: 1px solid var(--border-color);
    }}

    .btn-secondary:hover {{
      background: rgba(255, 255, 255, 0.15);
    }}

    /* Toast Notification */
    .toast-container {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 2000;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .toast {{
      background: #1e293b;
      border: 1px solid var(--primary);
      color: white;
      padding: 12px 20px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
      animation: slideUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    @keyframes slideUp {{
      from {{ transform: translateY(20px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}

    /* Footer */
    footer {{
      margin-top: auto;
      border-top: 1px solid var(--border-color);
      padding: 24px 0;
      text-align: center;
      font-size: 13px;
      color: var(--text-muted);
      background: rgba(9, 13, 22, 0.9);
    }}

    /* Responsive */
    @media (max-width: 768px) {{
      .hero-title {{ font-size: 26px; }}
      .cert-grid {{ grid-template-columns: 1fr; }}
      .cert-item.full-width {{ grid-column: span 1; }}
    }}
  </style>
</head>
<body>

  <!-- Header Navigation -->
  <header>
    <div class="container header-content">
      <a href="#" class="brand">
        <div class="brand-logo">
          <i class="fa-solid fa-user-check"></i>
        </div>
        <div class="brand-text">
          <h1>02Innovations Lab</h1>
          <p>Fellow Verification Portal</p>
        </div>
      </a>
      <div class="header-badges">
        <div class="status-badge">
          <div class="status-dot"></div>
          <span>Public Verification Portal</span>
        </div>
      </div>
    </div>
  </header>

  <main class="container">
    <!-- Hero Section -->
    <section class="hero">
      <h2 class="hero-title">Verify <span>Fellow Credentials</span></h2>
      <p class="hero-subtitle">Enter a Fellow's Email Address, Fellow ID, or Phone Number to verify their details.</p>
      
      <!-- Search Card -->
      <div class="search-card">
        <!-- Search Mode Tabs -->
        <div class="search-tabs">
          <button class="tab-btn active" data-mode="all" onclick="setSearchMode('all', this)">
            <i class="fa-solid fa-magnifying-glass"></i> All Fields
          </button>
          <button class="tab-btn" data-mode="email" onclick="setSearchMode('email', this)">
            <i class="fa-solid fa-envelope"></i> Email Address
          </button>
          <button class="tab-btn" data-mode="id" onclick="setSearchMode('id', this)">
            <i class="fa-solid fa-id-card"></i> Fellow ID
          </button>
          <button class="tab-btn" data-mode="phone" onclick="setSearchMode('phone', this)">
            <i class="fa-solid fa-phone"></i> Phone Number
          </button>
        </div>

        <!-- Search Input Bar -->
        <div class="search-input-wrapper">
          <i class="fa-solid fa-magnifying-glass search-icon"></i>
          <input 
            type="text" 
            id="searchInput" 
            class="search-input" 
            placeholder="Type Email, Fellow ID, or Phone Number to verify..."
            autocomplete="off"
            spellcheck="false"
            oninput="handleSearch()"
          >
          <button id="clearBtn" class="clear-btn" onclick="clearSearch()" title="Clear search">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- Results Count / Verification Status Bar -->
    <div class="results-info">
      <div class="results-count" id="resultsCount">
        Enter Fellow Email Address, Fellow ID, or Phone Number to verify.
      </div>
    </div>

    <!-- Initial Prompt State (Shown when search bar is empty) -->
    <div id="initialState" class="initial-state">
      <div class="initial-icon">
        <i class="fa-solid fa-shield-halved"></i>
      </div>
      <h3 class="initial-title">Fellow Lookup & Verification</h3>
      <p class="initial-desc">For privacy and public verification, please type the exact Email Address, Fellow ID, or Phone Number in the search field above.</p>
    </div>

    <!-- Results Grid Container (Displays SINGLE Fellow Record when matched) -->
    <div id="fellowsGrid" class="fellows-grid"></div>

    <!-- Empty State (Shown when search produces no record match) -->
    <div id="emptyState" class="empty-state">
      <div class="empty-icon">
        <i class="fa-solid fa-user-slash"></i>
      </div>
      <h3 class="empty-title">No Record Found</h3>
      <p class="empty-desc">No fellow record matched the details entered. Please verify the Email Address, Fellow ID, or Phone Number.</p>
      <button class="btn btn-secondary" onclick="clearSearch()" style="max-width: 200px; margin: 0 auto;">
        <i class="fa-solid fa-arrow-rotate-left"></i> Try Again
      </button>
    </div>
  </main>

  <!-- Fellow Verification Modal / Certificate -->
  <div id="certModal" class="modal-overlay" onclick="closeModalOnOverlay(event)">
    <div class="modal-card">
      <button class="modal-close" onclick="closeModal()" title="Close modal">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <div class="cert-header">
        <div class="cert-badge">
          <i class="fa-solid fa-shield-check"></i> Official Verification Certificate
        </div>
        <h3 class="cert-title" id="modalName">Fellow Name</h3>
        <p style="font-size: 13px; color: var(--text-muted); margin-top: 4px;" id="modalCohort">Cohort Name</p>
      </div>

      <div class="cert-grid">
        <div class="cert-item">
          <div class="cert-label"><i class="fa-solid fa-id-card" style="color:#60a5fa;"></i> Fellow ID</div>
          <div class="cert-value" id="modalId">FE/23/00000</div>
        </div>

        <div class="cert-item">
          <div class="cert-label"><i class="fa-solid fa-location-dot" style="color:#34d399;"></i> State & Provider</div>
          <div class="cert-value" id="modalProvider">Nasarawa - 02Innovations Lab</div>
        </div>

        <div class="cert-item">
          <div class="cert-label"><i class="fa-solid fa-envelope" style="color:#facc15;"></i> Email Address</div>
          <div class="cert-value" id="modalEmail">email@example.com</div>
        </div>

        <div class="cert-item">
          <div class="cert-label"><i class="fa-solid fa-phone" style="color:#f472b6;"></i> Phone Number</div>
          <div class="cert-value" id="modalPhone">08000000000</div>
        </div>

        <div class="cert-item full-width">
          <div class="cert-label"><i class="fa-solid fa-diagram-project" style="color:#c084fc;"></i> Assigned Capstone Project</div>
          <div class="cert-value" id="modalTopic" style="color:#93c5fd;">Project Topic Here</div>
        </div>
      </div>

      <div class="cert-actions">
        <button class="btn btn-primary" onclick="copyCertDetails()">
          <i class="fa-solid fa-copy"></i> Copy Verification Summary
        </button>
        <button class="btn btn-secondary" onclick="window.print()">
          <i class="fa-solid fa-print"></i> Print Certificate
        </button>
      </div>
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div id="toastContainer" class="toast-container"></div>

  <!-- Footer -->
  <footer>
    <div class="container">
      <p>&copy; 2026 02Innovations Lab Nig. Ltd &bull; 3MTT NextGen Fellows Verification System</p>
    </div>
  </footer>

  <!-- Embed Data & Application Logic -->
  <script>
    // Embedded Data Source
    const fellowsData = {fellows_json};

    let currentMode = 'all';
    let activeFellow = null;

    // Cohort Tag Stylers
    function getCohortTagClass(cohort) {{
      const c = (cohort || '').toUpperCase();
      if (c.includes('3D')) return 'tag-3d';
      if (c.includes('AI')) return 'tag-ai';
      if (c.includes('CLOUD')) return 'tag-cloud';
      if (c.includes('CYBER')) return 'tag-cyber';
      if (c.includes('DATA ANALYSIS')) return 'tag-data-an';
      if (c.includes('DATA SCIENCE')) return 'tag-data-sc';
      if (c.includes('DEVOPS')) return 'tag-devops';
      if (c.includes('GAME')) return 'tag-game';
      if (c.includes('PRODUCT MANAGEMENT')) return 'tag-pm';
      if (c.includes('QUALITY ASSURANCE')) return 'tag-qa';
      if (c.includes('SOFTWARE')) return 'tag-soft';
      if (c.includes('UI/UX')) return 'tag-ui';
      return 'tag-default';
    }}

    // Clean Phone Number for Matcher
    function normalizeDigits(str) {{
      return (str || '').replace(/\\D/g, '');
    }}

    // Set Search Tab Mode
    function setSearchMode(mode, element) {{
      currentMode = mode;
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      element.classList.add('active');

      const input = document.getElementById('searchInput');
      if (mode === 'email') input.placeholder = "Enter exact Email Address (e.g. idrisabbaumar7@gmail.com)...";
      else if (mode === 'id') input.placeholder = "Enter exact Fellow ID (e.g. FE/23/52884367)...";
      else if (mode === 'phone') input.placeholder = "Enter Phone Number (e.g. 08103683459)...";
      else input.placeholder = "Type Email, Fellow ID, or Phone Number to verify...";

      input.focus();
      handleSearch();
    }}

    // Clear Search Input
    function clearSearch() {{
      const input = document.getElementById('searchInput');
      input.value = '';
      document.getElementById('clearBtn').style.display = 'none';
      handleSearch();
      input.focus();
    }}

    // Main Public Verification & Search Execution
    function handleSearch() {{
      const input = document.getElementById('searchInput');
      const query = input.value.trim().toLowerCase();
      const clearBtn = document.getElementById('clearBtn');
      const initialState = document.getElementById('initialState');
      const resultsCount = document.getElementById('resultsCount');

      clearBtn.style.display = query.length > 0 ? 'flex' : 'none';

      // IF QUERY IS EMPTY OR TOO SHORT: HIDE ALL RECORDS
      if (!query || query.length < 3) {{
        document.getElementById('fellowsGrid').style.display = 'none';
        document.getElementById('emptyState').style.display = 'none';
        initialState.style.display = 'block';
        resultsCount.innerHTML = "Enter Fellow Email Address, Fellow ID, or Phone Number to verify.";
        return;
      }}

      initialState.style.display = 'none';
      const digitsQuery = normalizeDigits(query);

      // PUBLIC VERIFICATION LOOKUP: Search for exact or direct fellow match
      let match = fellowsData.find(item => {{
        const emailMatch = item.email.toLowerCase() === query || (query.includes('@') && item.email.toLowerCase().includes(query));
        
        // Exact Fellow ID match or digit sequence match (e.g. FE/23/52884367 or 52884367)
        const idMatch = item.fellowId.toLowerCase() === query || 
                        item.fellowId.toLowerCase().replace(/[^a-z0-9]/g, '') === query.replace(/[^a-z0-9]/g, '') ||
                        (digitsQuery.length >= 6 && normalizeDigits(item.fellowId).includes(digitsQuery));
        
        // Phone match requires at least 7 digits to prevent accidental multi-matches
        const phoneDigits = normalizeDigits(item.phone);
        const phoneRawDigits = normalizeDigits(item.phoneRaw);
        const phoneMatch = (digitsQuery.length >= 7) && (phoneDigits.includes(digitsQuery) || phoneRawDigits.includes(digitsQuery));

        if (currentMode === 'email') return emailMatch;
        if (currentMode === 'id') return idMatch;
        if (currentMode === 'phone') return phoneMatch;

        // All fields mode
        return emailMatch || idMatch || phoneMatch;
      }});

      // RENDER PUBLIC VERIFICATION RESULT (SINGLE RECORD ONLY)
      if (match) {{
        resultsCount.innerHTML = '<span style="color:#34d399; font-weight:700;"><i class="fa-solid fa-circle-check"></i> Verification Successful: Verified Record Found</span>';
        renderSingleFellow(match);
      }} else {{
        resultsCount.innerHTML = '<span style="color:#f87171; font-weight:700;"><i class="fa-solid fa-circle-xmark"></i> Verification Failed: No Record Found</span>';
        document.getElementById('fellowsGrid').style.display = 'none';
        document.getElementById('emptyState').style.display = 'block';
      }}
    }}

    // Render SINGLE Fellow Record Card
    function renderSingleFellow(item) {{
      const grid = document.getElementById('fellowsGrid');
      const emptyState = document.getElementById('emptyState');

      emptyState.style.display = 'none';
      grid.style.display = 'flex';

      const initials = item.name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();
      const tagClass = getCohortTagClass(item.cohort);

      grid.innerHTML = `
        <div class="fellow-card">
          <div class="card-top">
            <div class="avatar">${{initials}}</div>
            <div class="fellow-name-group">
              <h4 class="fellow-name">${{item.name}}</h4>
              <div class="fellow-id-badge">
                <i class="fa-solid fa-shield-check" style="color:#34d399;"></i> ${{item.fellowId}}
                <button class="copy-id-btn" onclick="copyToClipboard('${{item.fellowId}}', 'Fellow ID')" title="Copy ID">
                  <i class="fa-regular fa-copy"></i>
                </button>
              </div>
            </div>
          </div>

          <span class="cohort-tag ${{tagClass}}">${{item.cohort}}</span>

          <div class="card-body">
            <div class="info-row">
              <i class="fa-solid fa-envelope"></i>
              <span class="val">${{item.email}}</span>
            </div>
            <div class="info-row">
              <i class="fa-solid fa-phone"></i>
              <span class="val">${{item.phone}}</span>
            </div>
            <div class="info-row">
              <i class="fa-solid fa-location-dot"></i>
              <span class="val">${{item.state}} &bull; ${{item.provider}}</span>
            </div>
            <div class="info-row">
              <i class="fa-solid fa-book-bookmark"></i>
              <span class="val" style="color: #93c5fd;">${{item.topic || 'Capstone Assigned'}}</span>
            </div>
          </div>

          <div class="card-footer">
            <span class="verify-link" onclick="openCertModal(${{item.id}})">
              <i class="fa-solid fa-certificate"></i> View Official Verification
            </span>

            <div class="card-actions">
              <a href="mailto:${{item.email}}" class="action-icon-btn" title="Send Email">
                <i class="fa-solid fa-paper-plane"></i>
              </a>
              <button class="action-icon-btn" onclick="copyToClipboard('${{item.phone}}', 'Phone Number')" title="Copy Phone">
                <i class="fa-solid fa-copy"></i>
              </button>
            </div>
          </div>
        </div>
      `;
    }}

    // Modal Certificate Open
    function openCertModal(id) {{
      const fellow = fellowsData.find(f => f.id === id);
      if (!fellow) return;
      activeFellow = fellow;

      document.getElementById('modalName').textContent = fellow.name;
      document.getElementById('modalCohort').textContent = fellow.cohort;
      document.getElementById('modalId').textContent = fellow.fellowId;
      document.getElementById('modalProvider').textContent = `${{fellow.state}} — ${{fellow.provider}}`;
      document.getElementById('modalEmail').textContent = fellow.email;
      document.getElementById('modalPhone').textContent = fellow.phone;
      document.getElementById('modalTopic').textContent = fellow.topic || 'General Capstone Project';

      const modal = document.getElementById('certModal');
      modal.classList.add('active');
    }}

    function closeModal() {{
      document.getElementById('certModal').classList.remove('active');
    }}

    function closeModalOnOverlay(e) {{
      if (e.target.id === 'certModal') closeModal();
    }}

    // Copy Verification Text
    function copyCertDetails() {{
      if (!activeFellow) return;
      const text = `02INNOVATIONS LAB FELLOW VERIFICATION
Fellow ID: ${{activeFellow.fellowId}}
Name: ${{activeFellow.name}}
Email: ${{activeFellow.email}}
Phone: ${{activeFellow.phone}}
Cohort: ${{activeFellow.cohort}}
State: ${{activeFellow.state}}
Assigned Topic: ${{activeFellow.topic}}
Status: OFFICIALLY VERIFIED FELLOW`;

      copyToClipboard(text, "Verification Certificate Summary");
    }}

    // Copy Utility & Toast
    function copyToClipboard(text, label) {{
      navigator.clipboard.writeText(text).then(() => {{
        showToast(`<i class="fa-solid fa-check-circle" style="color:#10b981;"></i> Copied ${{label}} to clipboard!`);
      }}).catch(() => {{
        showToast(`<i class="fa-solid fa-triangle-exclamation" style="color:#f59e0b;"></i> Could not copy automatically.`);
      }});
    }}

    function showToast(htmlMsg) {{
      const container = document.getElementById('toastContainer');
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.innerHTML = htmlMsg;

      container.appendChild(toast);
      setTimeout(() => {{
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
      }}, 2500);
    }}

    // Keyboard Shortcuts (Press "/" to focus search input)
    document.addEventListener('keydown', (e) => {{
      if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'SELECT') {{
        e.preventDefault();
        document.getElementById('searchInput').focus();
      }}
      if (e.key === 'Escape') {{
        closeModal();
      }}
    }});

    // Initialize Page
    document.addEventListener('DOMContentLoaded', () => {{
      handleSearch();
    }});
  </script>
</body>
</html>
"""

with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated public verification {html_file_path} (single-record lookup mode with total count indicators completely removed)!")
