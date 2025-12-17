#!/usr/bin/env python3
import re

def convert_markdown_to_html(md_text):
    """Convert markdown to HTML using regex patterns."""
    html = md_text
    
    # Remove "Updated December XX" timestamps
    html = re.sub(r'\*Updated December \d+\*\n*', '', html)
    
    # Convert headers
    html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Convert code blocks
    html = re.sub(r'```(.*?)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # Convert bold and italic
    html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Convert inline code
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # Convert lists
    lines = html.split('\n')
    in_ul = False
    in_ol = False
    result = []
    
    for line in lines:
        # Unordered lists
        if re.match(r'^\s*[-*]\s+', line):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            item = re.sub(r'^\s*[-*]\s+', '', line)
            result.append(f'<li>{item}</li>')
        # Ordered lists
        elif re.match(r'^\s*\d+\.\s+', line):
            if not in_ol:
                result.append('<ol>')
                in_ol = True
            item = re.sub(r'^\s*\d+\.\s+', '', line)
            result.append(f'<li>{item}</li>')
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append(line)
    
    if in_ul:
        result.append('</ul>')
    if in_ol:
        result.append('</ol>')
    
    html = '\n'.join(result)
    
    # Convert paragraphs (lines that aren't tags)
    lines = html.split('\n')
    result = []
    for line in lines:
        if line.strip() and not line.strip().startswith('<') and not line.strip().endswith('>'):
            result.append(f'<p>{line}</p>')
        else:
            result.append(line)
    
    html = '\n'.join(result)
    
    # Convert horizontal rules
    html = re.sub(r'^---$', '<hr>', html, flags=re.MULTILINE)
    
    return html

# Read markdown files
with open('beatbook_guide.md', 'r') as f:
    guide_md = f.read()

with open('beatbook_journey.md', 'r') as f:
    journey_md = f.read()

# Convert to HTML
guide_html = convert_markdown_to_html(guide_md)
journey_html = convert_markdown_to_html(journey_md)

# Create complete HTML document
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>How to Build a Beat Book</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700;900&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --paper: #f5f3ed;
            --white: #ffffff;
            --ink: #1a1a1a;
            --gray: #6b6b6b;
            --light-gray: #d4d2c8;
            --accent: #2c5f8d;
            --shadow: rgba(0, 0, 0, 0.12);
        }
        body {
            font-family: 'Merriweather', serif;
            background: var(--paper);
            color: var(--ink);
            line-height: 1.7;
            font-size: 17px;
        }
        
        header {
            background: var(--ink);
            color: var(--white);
            padding: 1.25rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        header h1 {
            font-size: 1.75rem;
            font-weight: 700;
            margin: 0;
        }
        
        nav {
            background: var(--white);
            border-bottom: 3px solid var(--ink);
            position: sticky;
            top: 60px;
            z-index: 99;
        }
        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        .nav-tabs {
            display: flex;
            gap: 0;
            overflow-x: auto;
        }
        .nav-tab {
            padding: 1rem 1.5rem;
            background: transparent;
            border: none;
            border-bottom: 3px solid transparent;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-family: 'Work Sans', sans-serif;
            color: var(--gray);
            transition: all 0.3s;
            white-space: nowrap;
        }
        .nav-tab:hover {
            color: var(--ink);
            background: rgba(0,0,0,0.02);
        }
        .nav-tab.active {
            color: var(--ink);
            border-bottom-color: var(--accent);
            background: rgba(44, 95, 141, 0.05);
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }
        .section {
            display: none;
        }
        .section.active {
            display: block;
            animation: fadeIn 0.4s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        h1 { font-size: 2.5rem; font-weight: 900; margin: 2rem 0 1rem; }
        h2 { font-size: 2rem; font-weight: 900; margin: 2.5rem 0 1.5rem; border-bottom: 4px solid var(--ink); padding-bottom: 0.75rem; }
        h3 { font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem; }
        h4 { font-size: 1.2rem; font-weight: 600; margin: 1.5rem 0 0.75rem; }
        p { margin-bottom: 1.25rem; }
        ul, ol { margin: 1rem 0 1rem 2rem; }
        li { margin-bottom: 0.5rem; }
        strong { font-weight: 700; }
        em { font-style: italic; }
        hr { border: none; border-top: 2px solid var(--light-gray); margin: 2rem 0; }
        
        code {
            background: #2a2a2a;
            color: #e8e8e8;
            padding: 0.2rem 0.5rem;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.875rem;
        }
        pre {
            background: #2a2a2a;
            color: #e8e8e8;
            padding: 1.5rem;
            margin: 1.5rem 0;
            font-family: 'Courier New', monospace;
            font-size: 0.875rem;
            border-radius: 4px;
            overflow-x: auto;
            border-left: 4px solid var(--accent);
        }
        pre code {
            background: none;
            padding: 0;
        }
        
        @media (max-width: 768px) {
            header h1 { font-size: 1.5rem; }
            h1 { font-size: 1.875rem; }
            h2 { font-size: 1.625rem; }
            h3 { font-size: 1.375rem; }
            .container { padding: 2rem 1.5rem; }
            .nav-tab { font-size: 0.75rem; padding: 0.875rem 1rem; }
        }
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>How to Build a Beat Book</h1>
        </div>
    </header>
    
    <nav>
        <div class="nav-container">
            <div class="nav-tabs">
                <button class="nav-tab active" onclick="showTab('guide')">Beatbook for Dummies</button>
                <button class="nav-tab" onclick="showTab('journey')">My Journey from the Trenches</button>
            </div>
        </div>
    </nav>
    
    <div class="container">
        <div id="guide" class="section active">
            {guide_content}
        </div>
        
        <div id="journey" class="section">
            {journey_content}
        </div>
    </div>
    
    <script>
        function showTab(tabName) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            // Remove active from all tabs
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            
            // Show selected section
            document.getElementById(tabName).classList.add('active');
            // Activate clicked tab
            event.target.classList.add('active');
            
            // Scroll to top
            window.scrollTo(0, 0);
        }
    </script>
</body>
</html>'''

# Fill in content (using replace to avoid CSS {} conflicts with format())
final_html = html_template.replace('{guide_content}', guide_html).replace('{journey_content}', journey_html)

# Write output
with open('index.html', 'w') as f:
    f.write(final_html)

print(f"✓ Created index.html with two tabs")
print(f"  - Tab 1 (Guide): {len(guide_html)} chars")
print(f"  - Tab 2 (Journey): {len(journey_html)} chars")
