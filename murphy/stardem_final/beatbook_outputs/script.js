/* ============================================================
   EASTERN SHORE EDUCATION BEATBOOK
   Main Application Logic
   Generated: December 07, 2025 03:34 AM
===============================================================*/

/* ============================================================
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
        
        buildArchive();
        console.log("✓ Archive built");
        
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
   STORY ARCHIVE
===============================================================*/
function buildArchive() {
    const stories = STATE.data.stories || [];
    if (!Array.isArray(stories)) return;

    // Populate filters
    populateArchiveFilters(stories);

    // Setup filter handlers
    document.getElementById('archive-county-filter').addEventListener('change', filterArchive);
    document.getElementById('archive-date-filter').addEventListener('change', filterArchive);
    document.getElementById('archive-author-filter').addEventListener('change', filterArchive);
    document.getElementById('archive-search').addEventListener('input', filterArchive);
    document.getElementById('archive-sort').addEventListener('change', filterArchive);

    // Initial render
    renderArchive(stories);
}

function populateArchiveFilters(stories) {
    const counties = new Set();
    const authors = new Set();

    stories.forEach(story => {
        if (story.counties) {
            story.counties.forEach(c => counties.add(c));
        }
        if (story.author) {
            authors.add(story.author);
        }
    });

    const countySelect = document.getElementById('archive-county-filter');
    Array.from(counties).sort().forEach(county => {
        const opt = document.createElement('option');
        opt.value = county;
        opt.textContent = county;
        countySelect.appendChild(opt);
    });

    const authorSelect = document.getElementById('archive-author-filter');
    Array.from(authors).sort().forEach(author => {
        const opt = document.createElement('option');
        opt.value = author;
        opt.textContent = author;
        authorSelect.appendChild(opt);
    });
}

function filterArchive() {
    const countyFilter = document.getElementById('archive-county-filter').value;
    const dateFilter = document.getElementById('archive-date-filter').value;
    const authorFilter = document.getElementById('archive-author-filter').value;
    const searchTerm = document.getElementById('archive-search').value.toLowerCase();
    const sortBy = document.getElementById('archive-sort').value;

    const stories = STATE.data.stories || [];
    
    // Filter
    let filtered = stories.filter(story => {
        // County filter
        if (countyFilter && (!story.counties || !story.counties.includes(countyFilter))) {
            return false;
        }

        // Author filter
        if (authorFilter && story.author !== authorFilter) {
            return false;
        }

        // Date filter
        if (dateFilter && story.date) {
            const storyDate = new Date(story.date);
            const today = new Date();
            const daysAgo = parseInt(dateFilter);
            const cutoffDate = new Date(today.getTime() - daysAgo * 24 * 60 * 60 * 1000);
            if (storyDate < cutoffDate) {
                return false;
            }
        }

        // Search term
        if (searchTerm) {
            const searchable = `${story.title} ${story.summary || story.content || ''} ${(story.key_people || []).join(' ')}`.toLowerCase();
            if (!searchable.includes(searchTerm)) {
                return false;
            }
        }

        return true;
    });

    // Sort
    filtered.sort((a, b) => {
        switch(sortBy) {
            case 'date-desc':
                return new Date(b.date) - new Date(a.date);
            case 'date-asc':
                return new Date(a.date) - new Date(b.date);
            case 'score-desc':
                const scoreA = a.beatbook_evaluation?.score || 0;
                const scoreB = b.beatbook_evaluation?.score || 0;
                return scoreB - scoreA;
            default:
                return 0;
        }
    });

    renderArchive(filtered);
}

function renderArchive(stories) {
    const grid = document.getElementById('archive-grid');
    const countSpan = document.getElementById('archive-count');
    
    countSpan.textContent = `${stories.length} ${stories.length === 1 ? 'story' : 'stories'}`;
    
    grid.innerHTML = '';

    if (stories.length === 0) {
        grid.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--gray);">No stories found matching your criteria.</p>';
        return;
    }

    stories.forEach(story => {
        const item = document.createElement('div');
        item.className = 'archive-item';
        
        // Extract data
        const date = story.date ? new Date(story.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Unknown date';
        const author = story.author || 'Unknown author';
        const summary = story.summary || story.content?.substring(0, 300) + '...' || 'No summary available';
        const score = story.beatbook_evaluation?.score || 0;
        const counties = story.counties || [];
        const people = story.key_people || [];
        
        // Determine score class
        let scoreClass = 'score-low';
        if (score >= 4) scoreClass = 'score-high';
        else if (score >= 3) scoreClass = 'score-medium';
        
        item.innerHTML = `
            <div class="archive-item-header">
                <h3 class="archive-item-title">${story.title}</h3>
            </div>
            
            <div class="archive-item-meta">
                <span>📅 ${date}</span>
                <span>✍️ ${author}</span>
                ${score > 0 ? `<span>⭐ Quality: ${score}/5</span>` : ''}
            </div>
            
            <div class="archive-item-summary">${summary}</div>
            
            <div class="archive-item-tags">
                ${counties.map(c => `<span class="archive-tag county">${c}</span>`).join('')}
                ${score > 0 ? `<span class="archive-tag ${scoreClass}">Score: ${score}/5</span>` : ''}
            </div>
            
            ${people.length > 0 ? `
                <div class="archive-item-footer">
                    <div class="people-list">
                        <strong>Sources:</strong> ${people.slice(0, 3).join(', ')}${people.length > 3 ? ` +${people.length - 3} more` : ''}
                    </div>
                </div>
            ` : ''}
        `;

        grid.appendChild(item);
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
                        ${profile.beatbook_summary.replace(/\\n/g, '<br>')}
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
