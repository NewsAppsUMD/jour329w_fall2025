
// Global data storage
let countyData = {};
let currentCounty = 'caroline';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, starting initialization...');
    
    // Set a timeout to detect if loading hangs
    const timeoutId = setTimeout(() => {
        console.error('Loading timed out after 10 seconds');
        document.getElementById('content').innerHTML = '<div class="container"><div class="card"><h2>Loading Timeout</h2><p>Data loading is taking too long. This might be a network issue or the data files are too large.</p><p>Try refreshing the page.</p></div></div>';
    }, 10000);
    
    loadAllData().then(() => {
        clearTimeout(timeoutId);
        console.log('Initialization complete');
    }).catch(err => {
        clearTimeout(timeoutId);
        console.error('Initialization failed:', err);
    });
    
    setupEventListeners();
});

// Load all data files
async function loadAllData() {
    const content = document.getElementById('content');
    
    try {
        content.innerHTML = '<div class="container"><div class="card"><h2>Loading data...</h2><p>Loading county information...</p></div></div>';
        
        console.log('Starting to load county data...');
        
        // Load county data
        for (const county of ['caroline', 'dorchester', 'kent', 'queen_annes', 'talbot']) {
            console.log(`Fetching ${county}_data.json...`);
            const response = await fetch(`data/${county}_data.json`);
            
            if (!response.ok) {
                throw new Error(`Failed to load ${county}: ${response.status}`);
            }
            
            countyData[county] = await response.json();
            console.log(`${county} loaded successfully`);
        }
        
        console.log('All data loaded successfully!');
        renderOverview();
    } catch (error) {
        console.error('Error loading data:', error);
        content.innerHTML = '<div class="container"><div class="card"><h2>Error Loading Data</h2><p>Error: ' + error.message + '</p><p>Check the browser console (F12) for more details.</p></div></div>';
    }
}

// Setup event listeners
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            const county = this.getAttribute('data-county');
            
            // Update active nav
            document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
            this.classList.add('active');
            
            // Render appropriate page
            if (page === 'overview') {
                renderOverview();
            } else if (county) {
                currentCounty = county;
                renderCountyPage(county);
            }
        });
    });
}

// Render overview page
function renderOverview() {
    const content = document.getElementById('content');
    
    let html = '<div class="container">';
    html += '<h1 class="mb-3">Five-County Overview</h1>';
    
    // Stats grid
    html += '<div class="grid grid-3 mb-3">';
    html += `<div class="stat-box"><div class="number">5</div><div class="label">Counties</div></div>`;
    
    // Calculate total population
    let totalPop = 0;
    Object.values(countyData).forEach(county => {
        if (county.census && typeof county.census.total_population === 'number') {
            totalPop += county.census.total_population;
        }
    });
    
    html += `<div class="stat-box"><div class="number">${totalPop.toLocaleString()}</div><div class="label">Total Population</div></div>`;
    html += `<div class="stat-box"><div class="number">${Object.keys(countyData).length}</div><div class="label">Counties Loaded</div></div>`;
    html += '</div>';
    
    // County quick links
    html += '<div class="card">';
    html += '<h2>Select a County to Explore</h2>';
    html += '<div class="grid grid-2">';
    
    for (const [key, name] of Object.entries({
        'caroline': 'Caroline County',
        'dorchester': 'Dorchester County',
        'kent': 'Kent County',
        'queen_annes': "Queen Anne's County",
        'talbot': 'Talbot County'
    })) {
        const data = countyData[key];
        const pop = data?.census?.total_population || 'N/A';
        const income = data?.census?.median_household_income || 'N/A';
        html += `<div class="card" onclick="navigateToCounty('${key}')" style="cursor: pointer;">`;
        html += `<h3>${name}</h3>`;
        html += `<p class="text-muted">Population: ${typeof pop === 'number' ? pop.toLocaleString() : pop}</p>`;
        html += `<p class="text-muted">Median Income: ${typeof income === 'number' ? '$' + income.toLocaleString() : income}</p>`;
        html += `<p class="text-small mt-2">Click to explore demographics, government, schools, budget & elections →</p>`;
        html += `</div>`;
    }
    
    html += '</div>';
    html += '</div>';
    
    html += '</div>';
    content.innerHTML = html;
}

// Navigate to county
function navigateToCounty(county) {
    document.querySelector(`nav a[data-county="${county}"]`).click();
}

// Render county page
function renderCountyPage(county) {
    const content = document.getElementById('content');
    const data = countyData[county];
    const countyName = {
        'caroline': 'Caroline County',
        'dorchester': 'Dorchester County',
        'kent': 'Kent County',
        'queen_annes': "Queen Anne's County",
        'talbot': 'Talbot County'
    }[county];
    
    let html = '<div class="container">';
    html += `<h1 class="mb-3">${countyName}</h1>`;
    
    // Tabs
    html += '<div class="tabs">';
    html += '<button class="tab active" onclick="showTab('summary')">Summary</button>';
    html += '<button class="tab" onclick="showTab('government')">Government</button>';
    html += '<button class="tab" onclick="showTab('issues')">Key Issues</button>';
    html += '<button class="tab" onclick="showTab('budget')">Budget</button>';
    html += '<button class="tab" onclick="showTab('schools')">Schools</button>';
    html += '<button class="tab" onclick="showTab('stories')">News Stories</button>';
    html += '</div>';
    
    // Tab contents
    html += renderSummaryTab(county, data, countyName);
    html += renderGovernmentTab(county, data);
    html += renderIssuesTab(county, data, countyName);
    // Tabs
    html += '<div class="tabs">';
    html += '<button class="tab active" onclick="showTab(\'summary\')">Summary</button>';
    html += '<button class="tab" onclick="showTab(\'government\')">Government</button>';
    html += '<button class="tab" onclick="showTab(\'budget\')">Budget</button>';
    html += '<button class="tab" onclick="showTab(\'schools\')">Schools</button>';
    html += '<button class="tab" onclick="showTab(\'elections\')">Elections</button>';
    html += '</div>';
    
    // Tab contents
    html += renderSummaryTab(county, data, countyName);
    html += renderGovernmentTab(county, data);
    html += renderBudgetTab(county, data);
    html += renderSchoolsTab(county, data);
    html += renderElectionsTab(county, data);ld_income;
        const poverty = data.census.poverty_rate;
        
        html += `<div class="stat-box"><div class="number">${typeof pop === 'number' ? pop.toLocaleString() : pop}</div><div class="label">Population</div></div>`;
        html += `<div class="stat-box"><div class="number">$${typeof income === 'number' ? income.toLocaleString() : income}</div><div class="label">Median Income</div></div>`;
        html += `<div class="stat-box"><div class="number">${poverty}%</div><div class="label">Poverty Rate</div></div>`;
    }
    html += '</div>';
    
    // Demographics
    if (data.census) {
        html += '<div class="card">';
        html += '<h2>Demographics</h2>';
        html += '<table><tbody>';
        html += `<tr><td><strong>White (Non-Hispanic)</strong></td><td>${data.census.white_non_hispanic_percentage}%</td></tr>`;
        html += `<tr><td><strong>Black/African American</strong></td><td>${data.census.black_percentage}%</td></tr>`;
        html += `<tr><td><strong>Hispanic/Latino</strong></td><td>${data.census.hispanic_percentage}%</td></tr>`;
        html += `<tr><td><strong>Asian</strong></td><td>${data.census.asian_percentage}%</td></tr>`;
        html += `<tr><td><strong>Bachelor's Degree or Higher</strong></td><td>${data.census.bachelors_or_higher_percentage}%</td></tr>`;
        html += '</tbody></table>';
        html += '</div>';
    }
    
    html += '</div>';
    return html;
}

// Render government tab
function renderGovernmentTab(county, data) {
    let html = '<div class="tab-content" id="government">';
    html += '<div class="card">';
    html += '<h2>County Officials</h2>';
    
    if (data.officials && data.officials.legislative_branch) {
        html += '<h3>Commissioners</h3>';
        html += '<table><thead><tr><th>Name</th><th>Title</th><th>Party</th></tr></thead><tbody>';
        data.officials.legislative_branch.forEach(official => {
            html += `<tr><td>${official.name}</td><td>${official.title || ''}</td><td>${official.party || ''}</td></tr>`;
        });
        html += '</tbody></table>';
    }
    
    if (data.officials && data.officials.other_info) {
        const info = data.officials.other_info;
        html += '<h3 class="mt-3">Contact & Meeting Information</h3>';
        html += '<table><tbody>';
        if (info.meeting_schedule) html += `<tr><td><strong>Meeting Schedule</strong></td><td>${info.meeting_schedule}</td></tr>`;
        if (info.address) html += `<tr><td><strong>Address</strong></td><td>${info.address}</td></tr>`;
        if (info.phone) html += `<tr><td><strong>Phone</strong></td><td>${info.phone}</td></tr>`;
        if (info.website) html += `<tr><td><strong>Website</strong></td><td><a href="${info.website}" target="_blank">${info.website}</a></td></tr>`;
        html += '</tbody></table>';
    }
    
    html += '</div>';
    html += '</div>';
    return html;
}

// Render elections tab
function renderElectionsTab(county, data) {
    let html = '<div class="tab-content" id="elections">';
    html += '<div class="card">';
    html += '<h2>Election Results</h2>';
    
    if (data.elections && data.elections.results) {
        const results = data.elections.results;
        
        // Presidential results
        if (results.presidential_2024) {
            html += '<h3>2024 Presidential Election</h3>';
            html += '<table><thead><tr><th>Candidate</th><th>Votes</th><th>Percentage</th></tr></thead><tbody>';
            Object.entries(results.presidential_2024).forEach(([candidate, info]) => {
                html += `<tr><td>${candidate}</td><td>${info.votes.toLocaleString()}</td><td>${info.percentage}%</td></tr>`;
            });
            html += '</tbody></table>';
        }
        
        // Governor results
        if (results.governor_2022) {
            html += '<h3 class="mt-3">2022 Governor Election</h3>';
            html += '<table><thead><tr><th>Candidate</th><th>Votes</th><th>Percentage</th></tr></thead><tbody>';
            Object.entries(results.governor_2022).forEach(([candidate, info]) => {
                html += `<tr><td>${candidate}</td><td>${info.votes.toLocaleString()}</td><td>${info.percentage}%</td></tr>`;
            });
            html += '</tbody></table>';
        }
    } else {
        html += '<p class="text-muted">Election data not available.</p>';
    }
    
    html += '</div>';
    html += '</div>';
    return html;
}

// Render budget tab
function renderBudgetTab(county, data) {
    let html = '<div class="tab-content" id="budget">';
    html += '<div class="card">';
    html += '<h2>Budget Overview</h2>';
    
    if (data.budget_summary) {
        html += `<div class="text-muted mb-3">${data.budget_summary}</div>`;
    } else {
        html += '<p class="text-muted">Detailed budget analysis available in source files.</p>';
    }
    
    html += '</div>';
    html += '</div>';
    return html;
}

// Render schools tab
function renderSchoolsTab(county, data) {
    let html = '<div class="tab-content" id="schools">';
    html += '<div class="card">';
    html += '<h2>Schools & Education</h2>';
    
    if (data.schools) {
        if (data.schools.superintendent) {
            html += `<p><strong>Superintendent:</strong> ${data.schools.superintendent}</p>`;
        }
        if (data.schools.board_members && data.schools.board_members.length > 0) {
            html += '<h3 class="mt-2">Board Members</h3><ul>';
            data.schools.board_members.forEach(member => {
                html += `<li>${member}</li>`;
            });
            html += '</ul>';
        }
        if (data.schools.schools) {
            html += `<p class="mt-2"><strong>Total Schools:</strong> ${data.schools.schools.length}</p>`;
        }
    } else {
        html += '<p class="text-muted">School data not available.</p>';
    }
    
    html += '</div>';
    html += '</div>';
    return html;
}



// Show tab
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Filter stories
function filterStories() {
    const searchTerm = document.getElementById('storySearch').value.toLowerCase();
    const countyName = {
        'caroline': 'Caroline County',
        'dorchester': 'Dorchester County',
        'kent': 'Kent County',
        'queen_annes': "Queen Anne's County",
        'talbot': 'Talbot County'
    }[currentCounty];
    
    const countyStories = storiesData.filter(story => 
        story.counties && story.counties.includes(countyName)
    );
    
    const filtered = countyStories.filter(story =>
        story.title.toLowerCase().includes(searchTerm) ||
        (story.author && story.author.toLowerCase().includes(searchTerm)) ||
        (story.beatbook_tag && story.beatbook_tag.toLowerCase().includes(searchTerm))
    );
    
    let html = '';
    filtered.slice(0, 20).forEach(story => {
        html += '<div class="story-item">';
        html += `<h4>${story.title}</h4>`;
        html += `<div class="date">${story.date} | ${story.author || 'Unknown author'}</div>`;
        if (story.beatbook_tag) {
            html += `<div class="mt-1"><span class="tag">${story.beatbook_tag}</span></div>`;
        }
        html += '</div>';
    });
    
    if (filtered.length === 0) {
        html = '<p class="text-muted text-center">No stories found matching your search.</p>';
