#!/usr/bin/env python3
"""
Beatbook News App Generator
Creates a comprehensive news beatbook application using master data files.
Generates HTML, CSS, and JavaScript files for an interactive dashboard.
"""

import json
import os
from pathlib import Path
from datetime import datetime


class BeatbookGenerator:
    """Generates a news beatbook dashboard from master data files."""
    
    def __init__(self, master_data_dir, output_dir):
        self.master_data_dir = Path(master_data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load all data
        self.budget_data = self.load_json('budget.json')
        self.profiles = self.load_json('beatbook_profiles.json')
        self.quotes = self.load_json('master_quotes.json')
        self.stories = self.load_json('refined_beatbook_stories.json')
        
        # Load county student data
        self.counties = {}
        for county in ['caroline', 'dorchester', 'kent', 'queen_annes', 'talbot']:
            filename = f"{county}_master_student_data.json"
            data = self.load_json(filename)
            if data:
                self.counties[county] = data
    
    def load_json(self, filename):
        """Load a JSON file from master_data directory."""
        filepath = self.master_data_dir / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_html(self):
        """Generate the main HTML file."""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Eastern Shore Education Beatbook</title>

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700;900&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- Styles -->
    <link rel="stylesheet" href="style.css" />
</head>

<body>
    <!-- ===========================
         HEADER
    ============================ -->
    <header id="main-header">
        <div class="header-content">
            <h1>Eastern Shore Education Beatbook</h1>
            <div class="subtitle">Caroline • Dorchester • Kent • Queen Anne's • Talbot</div>
        </div>
    </header>

    <!-- ===========================
         MAIN NAVIGATION TABS
    ============================ -->
    <nav id="main-nav">
        <div class="nav-container">
            <button class="nav-tab active" data-tab="dashboard">Overview Dashboard</button>
            <button class="nav-tab" data-tab="counties">County Profiles</button>
            <button class="nav-tab" data-tab="stories">Recent Stories</button>
            <button class="nav-tab" data-tab="sources">Key Sources</button>
            <button class="nav-tab" data-tab="quotes">Quote Database</button>
        </div>
    </nav>

    <!-- ===========================
         MAIN CONTENT WRAPPER
    ============================ -->
    <main id="content">

        <!-- ===========================
             TAB 1: DASHBOARD
        ============================ -->
        <section id="dashboard" class="tab-section active">
            <div class="container">
                <h2>Overview Dashboard</h2>

                <!-- Chart Row -->
                <div class="dashboard-grid">
                    <div class="chart-card">
                        <h3>Enrollment by County</h3>
                        <canvas id="enrollmentChart"></canvas>
                    </div>

                    <div class="chart-card">
                        <h3>Total Education Budgets</h3>
                        <canvas id="budgetChart"></canvas>
                    </div>

                    <div class="chart-card">
                        <h3>Per-Pupil Spending</h3>
                        <canvas id="ppChart"></canvas>
                    </div>
                </div>

                <!-- Summary narrative -->
                <div class="narrative-box">
                    <h3>Topline Summary</h3>
                    <p id="dashboard-summary">
                        The Eastern Shore region exhibits profound differences in local revenue capacity, 
                        student demographics, and per-pupil spending. Queen Anne's leads in local contributions, 
                        while Caroline and Dorchester depend heavily on Blueprint state aid. Enrollment trends 
                        diverge sharply, as do capital needs and staffing pressures.
                    </p>
                </div>
            </div>
        </section>

        <!-- ===========================
             TAB 2: COUNTY PROFILES
        ============================ -->
        <section id="counties" class="tab-section">
            <div class="container">
                <h2>County Profiles</h2>
                <p class="section-intro">
                    Explore county-by-county conditions across Maryland's Mid–Shore region.
                </p>

                <div class="accordion" id="countyAccordion">
                    <!-- JS will inject county accordions here -->
                </div>
            </div>
        </section>

        <!-- ===========================
             TAB 3: RECENT STORIES
        ============================ -->
        <section id="stories" class="tab-section">
            <div class="container">
                <h2>Recent Stories</h2>
                <p class="section-intro">
                    Browse the latest education coverage from across the Eastern Shore.
                </p>

                <!-- Story Filters -->
                <div class="filter-bar">
                    <div class="filter-group">
                        <label for="story-county-filter">County:</label>
                        <select id="story-county-filter">
                            <option value="">All Counties</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="story-topic-filter">Topic:</label>
                        <select id="story-topic-filter">
                            <option value="">All Topics</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <input type="text" id="story-search" placeholder="Search stories..." />
                    </div>
                </div>

                <!-- Story Grid -->
                <div id="story-grid" class="story-grid">
                    <!-- JS will inject stories here -->
                </div>
            </div>
        </section>

        <!-- ===========================
             TAB 4: KEY SOURCES
        ============================ -->
        <section id="sources" class="tab-section">
            <div class="container">
                <h2>Key Sources</h2>
                <p class="section-intro">
                    Comprehensive profiles of education leaders across the Eastern Shore.
                </p>

                <!-- Source Search -->
                <div class="filter-bar">
                    <input type="text" id="source-search" placeholder="Search sources by name, title, or topic..." />
                </div>

                <!-- Source Grid -->
                <div id="source-grid" class="source-grid">
                    <!-- JS will inject source profiles here -->
                </div>
            </div>
        </section>

        <!-- ===========================
             TAB 5: QUOTE DATABASE
        ============================ -->
        <section id="quotes" class="tab-section">
            <div class="container">
                <h2>Quote Database</h2>
                <p class="section-intro">
                    Search through thousands of quotes from education leaders.
                </p>

                <!-- Quote Filters -->
                <div class="filter-bar">
                    <div class="filter-group">
                        <label for="quote-speaker-filter">Speaker:</label>
                        <select id="quote-speaker-filter">
                            <option value="">All Speakers</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="quote-topic-filter">Topic:</label>
                        <select id="quote-topic-filter">
                            <option value="">All Topics</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <input type="text" id="quote-search" placeholder="Search quotes..." />
                    </div>
                </div>

                <!-- Quote Results -->
                <div id="quote-results" class="quote-results">
                    <!-- JS will inject quotes here -->
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>Eastern Shore Education Beatbook | Generated """ + datetime.now().strftime("%B %d, %Y") + """</p>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="script.js"></script>
</body>
</html>"""
        
        with open(self.output_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✓ Generated index.html")
    
    def generate_css(self):
        """Generate the CSS stylesheet."""
        css_content = """/* ============================================
   GLOBAL RESETS & VARIABLES
============================================ */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --paper: #f5f3ed;
    --white: #ffffff;
    --ink: #1a111a;
    --gray: #5d5d5d;
    --light-gray: #ddd7cb;

    --accent: #2c5f8d;

    /* County accent colors */
    --talbot: #2c5f8d;
    --caroline: #a3333d;
    --dorchester: #d4880f;
    --kent: #3a7d7c;
    --queen-annes: #7b5d8c;

    --shadow: 0 4px 14px rgba(0,0,0,0.15);
}

html, body {
    background: var(--paper);
    font-family: "Merriweather", serif;
    color: var(--ink);
    line-height: 1.7;
    font-size: 17px;
}

/* ============================================
   HEADER
============================================ */
#main-header {
    background: var(--ink);
    color: var(--white);
    padding: 2rem 0;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 4px 18px rgba(0,0,0,0.3);
}

.header-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
}

#main-header h1 {
    font-size: 2.3rem;
    font-weight: 900;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-family: "Work Sans", sans-serif;
    font-size: 0.95rem;
    opacity: 0.8;
    letter-spacing: 3px;
    text-transform: uppercase;
}

/* ============================================
   NAVIGATION
============================================ */
#main-nav {
    background: var(--white);
    border-bottom: 3px solid var(--ink);
    position: sticky;
    top: 84px;
    z-index: 900;
}

.nav-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    overflow-x: auto;
}

.nav-tab {
    padding: 1rem 1.4rem;
    cursor: pointer;
    border: none;
    font-family: "Work Sans", sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--gray);
    background: transparent;
    border-bottom: 3px solid transparent;
    transition: 0.25s ease;
    white-space: nowrap;
}

.nav-tab:hover {
    color: var(--ink);
    background: rgba(0,0,0,0.03);
}

.nav-tab.active {
    color: var(--ink);
    border-bottom-color: var(--accent);
}

/* ============================================
   MAIN CONTENT
============================================ */
main {
    max-width: 1400px;
    margin: 0 auto;
    padding: 3rem 2rem;
}

.tab-section {
    display: none;
}

.tab-section.active {
    display: block;
}

.container h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: var(--ink);
}

.section-intro {
    margin-bottom: 2rem;
    color: var(--gray);
    font-size: 1.1rem;
}

/* ============================================
   DASHBOARD
============================================ */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.chart-card {
    background: var(--white);
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: var(--shadow);
}

.chart-card h3 {
    margin-bottom: 1rem;
    font-size: 1.2rem;
    color: var(--ink);
}

.narrative-box {
    background: var(--white);
    padding: 2rem;
    border-radius: 8px;
    box-shadow: var(--shadow);
}

.narrative-box h3 {
    margin-bottom: 1rem;
    color: var(--accent);
}

/* ============================================
   ACCORDION (COUNTY PROFILES)
============================================ */
.accordion {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.accordion-item {
    background: var(--white);
    border-radius: 8px;
    box-shadow: var(--shadow);
    overflow: hidden;
}

.accordion-header {
    padding: 1.5rem;
    cursor: pointer;
    border-left: 6px solid var(--accent);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 700;
    font-size: 1.2rem;
    transition: background 0.25s;
}

.accordion-header:hover {
    background: rgba(0,0,0,0.03);
}

.accordion-header.open .accordion-arrow {
    transform: rotate(180deg);
}

.accordion-arrow {
    transition: transform 0.25s;
}

.accordion-content {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
}

.accordion-inner {
    padding: 2rem;
    border-top: 1px solid var(--light-gray);
}

.accordion-inner h3 {
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    color: var(--accent);
}

.accordion-inner h3:first-child {
    margin-top: 0;
}

/* ============================================
   FILTER BAR
============================================ */
.filter-bar {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.filter-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.filter-group label {
    font-weight: 600;
    font-family: "Work Sans", sans-serif;
}

.filter-bar select,
.filter-bar input[type="text"] {
    padding: 0.75rem;
    border: 2px solid var(--light-gray);
    border-radius: 6px;
    font-family: "Work Sans", sans-serif;
    font-size: 1rem;
    min-width: 200px;
}

.filter-bar input[type="text"] {
    flex: 1;
}

/* ============================================
   STORY GRID
============================================ */
.story-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
}

.story-card {
    background: var(--white);
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: var(--shadow);
    border-left: 6px solid var(--accent);
    transition: transform 0.2s;
}

.story-card:hover {
    transform: translateY(-4px);
}

.story-card h3 {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
    color: var(--ink);
}

.story-meta {
    font-family: "Work Sans", sans-serif;
    font-size: 0.9rem;
    color: var(--gray);
    margin-bottom: 1rem;
}

.story-excerpt {
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1rem;
}

.story-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.story-tag {
    background: var(--light-gray);
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.85rem;
    font-family: "Work Sans", sans-serif;
}

/* ============================================
   SOURCE GRID
============================================ */
.source-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 2rem;
}

.source-card {
    background: var(--white);
    padding: 2rem;
    border-radius: 8px;
    box-shadow: var(--shadow);
    border-left: 6px solid var(--accent);
}

.source-card h3 {
    font-size: 1.3rem;
    margin-bottom: 0.25rem;
    color: var(--ink);
}

.source-title {
    font-family: "Work Sans", sans-serif;
    font-size: 1rem;
    color: var(--gray);
    margin-bottom: 1rem;
}

.source-stats {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    font-family: "Work Sans", sans-serif;
    font-size: 0.9rem;
}

.source-stat {
    background: var(--light-gray);
    padding: 0.5rem 1rem;
    border-radius: 6px;
}

.source-topics {
    margin-bottom: 1rem;
}

.source-topics h4 {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    color: var(--accent);
}

.topic-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.topic-tag {
    background: var(--light-gray);
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.85rem;
    font-family: "Work Sans", sans-serif;
}

.source-summary {
    font-size: 0.95rem;
    line-height: 1.6;
}

.source-summary details {
    margin-top: 0.5rem;
}

.source-summary summary {
    cursor: pointer;
    font-weight: 600;
    color: var(--accent);
    font-family: "Work Sans", sans-serif;
}

/* ============================================
   QUOTE RESULTS
============================================ */
.quote-results {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.quote-card {
    background: var(--white);
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: var(--shadow);
    border-left: 6px solid var(--accent);
}

.quote-text {
    font-size: 1.1rem;
    font-style: italic;
    margin-bottom: 1rem;
    line-height: 1.6;
}

.quote-attribution {
    font-family: "Work Sans", sans-serif;
    font-size: 0.9rem;
    color: var(--gray);
    margin-bottom: 0.5rem;
}

.quote-context {
    font-size: 0.9rem;
    color: var(--gray);
    line-height: 1.5;
    border-top: 1px solid var(--light-gray);
    padding-top: 1rem;
    margin-top: 1rem;
}

/* ============================================
   FOOTER
============================================ */
footer {
    background: var(--ink);
    color: var(--white);
    padding: 2rem 0;
    text-align: center;
    margin-top: 4rem;
}

footer p {
    font-family: "Work Sans", sans-serif;
    font-size: 0.9rem;
}

/* ============================================
   UTILITIES
============================================ */
.mt-2 {
    margin-top: 2rem;
}

.hidden {
    display: none;
}"""
        
        with open(self.output_dir / 'style.css', 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print("✓ Generated style.css")
    
    def prepare_data_json(self):
        """Prepare the data structure for embedding in JavaScript."""
        return {
            'budget': self.budget_data,
            'counties': self.counties,
            'profiles': self.profiles,
            'quotes': self.quotes,
            'stories': self.stories
        }
    
    def generate_data_json(self):
        """Generate a separate JSON file for async loading."""
        data = self.prepare_data_json()
        
        with open(self.output_dir / 'data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print("✓ Generated data.json")
    
    def generate_script_js(self):
        """Generate the main JavaScript application file that loads data async."""
        
        js_content = "/* ============================================================\n"
        js_content += "   EASTERN SHORE EDUCATION BEATBOOK\n"
        js_content += "   Main Application Logic\n"
        js_content += f"   Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}\n"
        js_content += "===============================================================*/\n\n"
        js_content += """/* ============================================================
   GLOBAL STATE
===============================================================*/
const STATE = {
    data: null,
    currentTab: 'dashboard',
    filters: {
        storyCounty: '',
        storyTopic: '',
        storySearch: '',
        sourceSearch: '',
        quoteSpeaker: '',
        quoteTopic: '',
        quoteSearch: ''
    }
};

/* County configuration */
const COUNTY_NAMES = {
    caroline: "Caroline County",
    dorchester: "Dorchester County",
    kent: "Kent County",
    queen_annes: "Queen Anne's County",
    talbot: "Talbot County"
};

const COUNTY_COLORS = {
    caroline: "#a3333d",
    dorchester: "#d4880f",
    kent: "#3a7d7c",
    queen_annes: "#7b5d8c",
    talbot: "#2c5f8d"
};

/* ============================================================
   DATA LOADING
===============================================================*/
async function loadData() {
    try {
        const response = await fetch('data.json');
        if (!response.ok) throw new Error('Failed to load data');
        return await response.json();
    } catch (error) {
        console.error('Error loading data:', error);
        return null;
    }
}

/* ============================================================
   INITIALIZATION
===============================================================*/
document.addEventListener("DOMContentLoaded", async () => {
    console.log("Loading beatbook data...");
    
    // Load data first
    STATE.data = await loadData();
    
    if (!STATE.data) {
        document.body.innerHTML = '<div style="padding: 2rem; text-align: center;"><h2>Error loading data</h2><p>Please refresh the page or check the console for details.</p></div>';
        return;
    }
    
    console.log("Data loaded successfully");
    
    try {
        setupNavigation();
        console.log("✓ Navigation setup");
        
        buildDashboard();
        console.log("✓ Dashboard built");
        
        buildCountyProfiles();
        console.log("✓ County profiles built");
        
        buildStories();
        console.log("✓ Stories built");
        
        buildSources();
        console.log("✓ Sources built");
        
        buildQuotes();
        console.log("✓ Quotes built");
        
        console.log("Beatbook initialization complete!");
    } catch (error) {
        console.error("Error during initialization:", error);
    }
});

/* ============================================================
   TAB NAVIGATION
===============================================================*/
function setupNavigation() {
    const tabs = document.querySelectorAll(".nav-tab");
    const sections = document.querySelectorAll(".tab-section");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");

            const id = tab.dataset.tab;
            STATE.currentTab = id;
            
            sections.forEach(sec => {
                sec.classList.toggle("active", sec.id === id);
            });
        });
    });
}

/* ============================================================
   DASHBOARD
===============================================================*/
function buildDashboard() {
    const budget = STATE.data.budget;
    if (!budget) return;

    // Filter out non-county entries
    const counties = Object.keys(budget).filter(c => c !== 'cross_county');
    const enrollment = counties.map(c => budget[c].enrollment_per_pupil.enrollment);
    const budgets = counties.map(c => budget[c].core_fiscal.county_operating_budget);
    const pp = counties.map(c => budget[c].enrollment_per_pupil.total_per_pupil);

    /* Chart 1: Enrollment */
    new Chart(document.getElementById("enrollmentChart"), {
        type: "bar",
        data: {
            labels: counties.map(c => COUNTY_NAMES[c]),
            datasets: [{
                label: "Enrollment",
                data: enrollment,
                backgroundColor: counties.map(c => COUNTY_COLORS[c])
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });

    /* Chart 2: Total Budgets */
    new Chart(document.getElementById("budgetChart"), {
        type: "bar",
        data: {
            labels: counties.map(c => COUNTY_NAMES[c]),
            datasets: [{
                label: "County Operating Budget ($)",
                data: budgets,
                backgroundColor: counties.map(c => COUNTY_COLORS[c])
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });

    /* Chart 3: Per-Pupil Spending */
    new Chart(document.getElementById("ppChart"), {
        type: "bar",
        data: {
            labels: counties.map(c => COUNTY_NAMES[c]),
            datasets: [{
                label: "Per-Pupil Spending ($)",
                data: pp,
                backgroundColor: counties.map(c => COUNTY_COLORS[c])
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}

/* ============================================================
   COUNTY PROFILES
===============================================================*/
function buildCountyProfiles() {
    const container = document.getElementById("countyAccordion");
    container.innerHTML = "";

    const budget = STATE.data.budget;
    const counties = STATE.data.counties;

    // Filter out non-county entries
    const countyKeys = Object.keys(budget).filter(c => c !== 'cross_county');

    countyKeys.forEach(countyKey => {
        const bData = budget[countyKey];
        const cData = counties[countyKey];

        const item = document.createElement("div");
        item.className = "accordion-item";

        /* HEADER */
        const header = document.createElement("div");
        header.className = "accordion-header";
        header.style.borderLeftColor = COUNTY_COLORS[countyKey];
        header.innerHTML = `
            <span>${COUNTY_NAMES[countyKey]}</span>
            <span class="accordion-arrow">▼</span>
        `;
        item.appendChild(header);

        /* CONTENT */
        const content = document.createElement("div");
        content.className = "accordion-content";

        const inner = document.createElement("div");
        inner.className = "accordion-inner";

        const enrollment = bData.enrollment_per_pupil.enrollment;
        const totalBudget = bData.core_fiscal.county_operating_budget;
        const localShare = bData.core_fiscal.local_share_pct;
        const stateShare = bData.core_fiscal.state_share_pct;
        const perPupil = bData.enrollment_per_pupil.total_per_pupil;

        inner.innerHTML = `
            <h3>Fiscal Overview</h3>
            <p><strong>Total County Budget:</strong> $${totalBudget.toLocaleString()}</p>
            <p><strong>Local Share:</strong> ${localShare}%</p>
            <p><strong>State Share:</strong> ${stateShare}%</p>
            <p><strong>Enrollment:</strong> ${enrollment.toLocaleString()}</p>
            <p><strong>Per-Pupil Spending:</strong> $${perPupil.toLocaleString()}</p>

            <h3 class="mt-2">Narrative Summary</h3>
            <p>${bData.narrative}</p>

            <h3 class="mt-2">Blueprint Drivers</h3>
            <ul>
                ${Object.entries(bData.blueprint_drivers).map(([key, value]) => `
                    <li><strong>${key.replace(/_/g, ' ')}:</strong> ${value}</li>
                `).join('')}
            </ul>

            <h3 class="mt-2">Emerging Issues</h3>
            <ul>
                ${bData.emerging_issues.map(issue => `<li>${issue}</li>`).join('')}
            </ul>

            <h3 class="mt-2">Schools</h3>
            <p>${cData ? cData.elementary_schools.length + ' schools in data' : 'School data available'}</p>
        `;

        content.appendChild(inner);
        item.appendChild(content);

        /* Accordion behavior */
        header.addEventListener("click", () => {
            const isOpen = header.classList.contains("open");
            document.querySelectorAll(".accordion-header").forEach(h => h.classList.remove("open"));
            document.querySelectorAll(".accordion-content").forEach(c => c.style.maxHeight = 0);

            if (!isOpen) {
                header.classList.add("open");
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });

        container.appendChild(item);
    });
}

/* ============================================================
   STORIES
===============================================================*/
function buildStories() {
    const stories = STATE.data.stories || [];
    if (!Array.isArray(stories)) return;

    // Populate filters
    populateStoryFilters(stories);

    // Setup filter handlers
    document.getElementById('story-county-filter').addEventListener('change', filterStories);
    document.getElementById('story-topic-filter').addEventListener('change', filterStories);
    document.getElementById('story-search').addEventListener('input', filterStories);

    // Initial render
    renderStories(stories);
}

function populateStoryFilters(stories) {
    const counties = new Set();
    const topics = new Set();

    stories.forEach(story => {
        if (story.counties) {
            story.counties.forEach(c => counties.add(c));
        }
        if (story.llm_classification && story.llm_classification.topic) {
            topics.add(story.llm_classification.topic);
        }
    });

    const countySelect = document.getElementById('story-county-filter');
    Array.from(counties).sort().forEach(county => {
        const opt = document.createElement('option');
        opt.value = county;
        opt.textContent = county;
        countySelect.appendChild(opt);
    });

    const topicSelect = document.getElementById('story-topic-filter');
    Array.from(topics).sort().forEach(topic => {
        const opt = document.createElement('option');
        opt.value = topic;
        opt.textContent = topic;
        topicSelect.appendChild(opt);
    });
}

function filterStories() {
    const countyFilter = document.getElementById('story-county-filter').value;
    const topicFilter = document.getElementById('story-topic-filter').value;
    const searchTerm = document.getElementById('story-search').value.toLowerCase();

    const stories = STATE.data.stories || [];
    
    const filtered = stories.filter(story => {
        // County filter
        if (countyFilter && (!story.counties || !story.counties.includes(countyFilter))) {
            return false;
        }

        // Topic filter
        if (topicFilter && (!story.llm_classification || story.llm_classification.topic !== topicFilter)) {
            return false;
        }

        // Search term
        if (searchTerm) {
            const searchable = `${story.title} ${story.content}`.toLowerCase();
            if (!searchable.includes(searchTerm)) {
                return false;
            }
        }

        return true;
    });

    renderStories(filtered);
}

function renderStories(stories) {
    const grid = document.getElementById('story-grid');
    grid.innerHTML = '';

    if (stories.length === 0) {
        grid.innerHTML = '<p>No stories found matching your criteria.</p>';
        return;
    }

    stories.slice(0, 50).forEach(story => {
        const card = document.createElement('div');
        card.className = 'story-card';
        
        const topic = story.llm_classification ? story.llm_classification.topic : 'General';
        const date = story.date || 'Unknown date';
        const author = story.author || 'Unknown author';
        
        // Extract first 200 chars as excerpt
        const excerpt = story.content ? story.content.substring(0, 200) + '...' : '';

        card.innerHTML = `
            <h3>${story.title}</h3>
            <div class="story-meta">${date} | ${author}</div>
            <div class="story-excerpt">${excerpt}</div>
            <div class="story-tags">
                ${story.counties ? story.counties.map(c => `<span class="story-tag">${c}</span>`).join('') : ''}
                <span class="story-tag">${topic}</span>
            </div>
        `;

        grid.appendChild(card);
    });
}

/* ============================================================
   SOURCES
===============================================================*/
function buildSources() {
    const profiles = STATE.data.profiles;
    if (!profiles || !profiles.profiles) return;

    // Setup search
    document.getElementById('source-search').addEventListener('input', filterSources);

    // Initial render
    renderSources(profiles.profiles);
}

function filterSources() {
    const searchTerm = document.getElementById('source-search').value.toLowerCase();
    const profiles = STATE.data.profiles.profiles;

    const filtered = profiles.filter(profile => {
        const searchable = `${profile.name} ${profile.title} ${profile.topics.join(' ')}`.toLowerCase();
        return searchable.includes(searchTerm);
    });

    renderSources(filtered);
}

function renderSources(profiles) {
    const grid = document.getElementById('source-grid');
    grid.innerHTML = '';

    if (profiles.length === 0) {
        grid.innerHTML = '<p>No sources found matching your search.</p>';
        return;
    }

    profiles.forEach(profile => {
        const card = document.createElement('div');
        card.className = 'source-card';

        card.innerHTML = `
            <h3>${profile.name}</h3>
            <div class="source-title">${profile.title}</div>
            <div class="source-stats">
                <div class="source-stat">${profile.quote_count} quotes</div>
                <div class="source-stat">${profile.direct_quotes} direct</div>
            </div>
            <div class="source-topics">
                <h4>Topics:</h4>
                <div class="topic-list">
                    ${profile.topics.map(t => `<span class="topic-tag">${t}</span>`).join('')}
                </div>
            </div>
            <div class="source-summary">
                <details>
                    <summary>Read Full Profile</summary>
                    <div style="margin-top: 1rem;">
                        ${profile.beatbook_summary.replace(/\n/g, '<br>')}
                    </div>
                </details>
            </div>
        `;

        grid.appendChild(card);
    });
}

/* ============================================================
   QUOTES
===============================================================*/
function buildQuotes() {
    const quotes = STATE.data.quotes;
    if (!quotes || !quotes.quotes_by_topic) return;

    populateQuoteFilters();

    // Setup filter handlers
    document.getElementById('quote-speaker-filter').addEventListener('change', filterQuotes);
    document.getElementById('quote-topic-filter').addEventListener('change', filterQuotes);
    document.getElementById('quote-search').addEventListener('input', filterQuotes);

    // Initial render
    renderQuotes([]);
}

function populateQuoteFilters() {
    const quotes = STATE.data.quotes.quotes_by_topic;
    const speakers = new Set();
    const topics = Object.keys(quotes);

    // Collect all speakers
    topics.forEach(topic => {
        Object.keys(quotes[topic]).forEach(speaker => {
            speakers.add(speaker);
        });
    });

    // Populate speaker dropdown
    const speakerSelect = document.getElementById('quote-speaker-filter');
    Array.from(speakers).sort().forEach(speaker => {
        const opt = document.createElement('option');
        opt.value = speaker;
        opt.textContent = speaker;
        speakerSelect.appendChild(opt);
    });

    // Populate topic dropdown
    const topicSelect = document.getElementById('quote-topic-filter');
    topics.sort().forEach(topic => {
        const opt = document.createElement('option');
        opt.value = topic;
        opt.textContent = topic;
        topicSelect.appendChild(opt);
    });
}

function filterQuotes() {
    const speakerFilter = document.getElementById('quote-speaker-filter').value;
    const topicFilter = document.getElementById('quote-topic-filter').value;
    const searchTerm = document.getElementById('quote-search').value.toLowerCase();

    const quotesData = STATE.data.quotes.quotes_by_topic;
    const results = [];

    // Extract quotes based on filters
    const topics = topicFilter ? [topicFilter] : Object.keys(quotesData);

    topics.forEach(topic => {
        const speakers = speakerFilter ? [speakerFilter] : Object.keys(quotesData[topic]);

        speakers.forEach(speaker => {
            if (!quotesData[topic][speaker]) return;

            const speakerData = quotesData[topic][speaker];
            if (!speakerData.quotes) return;

            speakerData.quotes.forEach(quoteObj => {
                if (searchTerm && !quoteObj.quote.toLowerCase().includes(searchTerm)) {
                    return;
                }

                results.push({
                    speaker: speaker,
                    topic: topic,
                    quote: quoteObj.quote,
                    type: quoteObj.type,
                    context: quoteObj.context,
                    story: quoteObj.story_title,
                    date: quoteObj.story_date
                });
            });
        });
    });

    renderQuotes(results);
}

function renderQuotes(quotes) {
    const container = document.getElementById('quote-results');
    container.innerHTML = '';

    if (quotes.length === 0) {
        container.innerHTML = '<p>Enter search criteria or select filters to find quotes.</p>';
        return;
    }

    // Limit to first 100 results
    quotes.slice(0, 100).forEach(q => {
        const card = document.createElement('div');
        card.className = 'quote-card';

        card.innerHTML = `
            <div class="quote-text">"${q.quote}"</div>
            <div class="quote-attribution">
                <strong>${q.speaker}</strong> | ${q.topic} | ${q.type} quote
            </div>
            <div class="quote-context">
                <strong>From:</strong> ${q.story} (${q.date})
            </div>
        `;

        container.appendChild(card);
    });

    if (quotes.length > 100) {
        const message = document.createElement('p');
        message.textContent = `Showing first 100 of ${quotes.length} results. Refine your search for more specific results.`;
        message.style.textAlign = 'center';
        message.style.marginTop = '2rem';
        message.style.color = 'var(--gray)';
        container.appendChild(message);
    }
}
"""
        
        with open(self.output_dir / 'script.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print("✓ Generated script.js")
    
    def generate_readme(self):
        """Generate a README file for the beatbook."""
        readme_content = f"""# Eastern Shore Education Beatbook

A comprehensive news app beatbook for education coverage across Maryland's Eastern Shore counties.

## Generated
{datetime.now().strftime("%B %d, %Y at %I:%M %p")}

## Features

- **Overview Dashboard**: Visual charts showing enrollment, budgets, and per-pupil spending
- **County Profiles**: Detailed fiscal and demographic information for each county
- **Recent Stories**: Searchable archive of education news stories with filtering
- **Key Sources**: Profiles of education leaders with quote counts and topic expertise
- **Quote Database**: Searchable database of thousands of quotes from officials

## Counties Covered

- Caroline County
- Dorchester County
- Kent County
- Queen Anne's County
- Talbot County

## Data Sources

This beatbook is built from the following master data files:

- `budget.json` - County fiscal data and budget analysis
- `beatbook_profiles.json` - Profiles of key education sources
- `master_quotes.json` - Database of quotes from officials
- `refined_beatbook_stories.json` - Curated news stories
- County-specific student data files for all five counties

## Usage

Open `index.html` in a web browser to view the beatbook. All data is embedded in the application,
so no server is required.

## Technology

- HTML5, CSS3, JavaScript
- Chart.js for data visualization
- Responsive design for mobile and desktop
- No external dependencies beyond Chart.js CDN

## Generator

This beatbook was generated using `generate_beatbook.py`, a Python script that processes
master data files and creates a standalone web application.
"""
        
        with open(self.output_dir / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✓ Generated README.md")
    
    def generate_all(self):
        """Generate all beatbook files."""
        print("\n" + "="*60)
        print("GENERATING EASTERN SHORE EDUCATION BEATBOOK")
        print("="*60 + "\n")
        
        print("Loading data files...")
        print(f"  Budget data: {len(self.budget_data) if self.budget_data else 0} counties")
        print(f"  Profiles: {self.profiles['metadata']['total_profiles'] if self.profiles else 0} sources")
        print(f"  Stories: {len(self.stories) if self.stories else 0} articles")
        print(f"  County data: {len(self.counties)} counties")
        print()
        
        print("Generating files...")
        self.generate_html()
        self.generate_css()
        self.generate_data_json()
        self.generate_script_js()
        self.generate_readme()
        
        print("\n" + "="*60)
        print("BEATBOOK GENERATION COMPLETE!")
        print("="*60)
        print(f"\nOutput directory: {self.output_dir}")
        print("\nTo view the beatbook:")
        print(f"  1. Open {self.output_dir}/index.html in a web browser")
        print("  2. Or run: python -m http.server 8000")
        print("     Then visit: http://localhost:8000")
        print()


def main():
    """Main entry point."""
    import sys
    
    # Default paths
    script_dir = Path(__file__).parent
    master_data_dir = script_dir / "master_data"
    output_dir = script_dir / "beatbook_output"
    
    # Allow command line overrides
    if len(sys.argv) > 1:
        master_data_dir = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_dir = Path(sys.argv[2])
    
    # Generate beatbook
    generator = BeatbookGenerator(master_data_dir, output_dir)
    generator.generate_all()


if __name__ == "__main__":
    main()
