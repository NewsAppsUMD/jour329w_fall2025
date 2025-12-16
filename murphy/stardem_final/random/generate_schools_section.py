#!/usr/bin/env python3
"""
Generate new schools section HTML with filters and modal popup
"""
import json

with open('schools_data.json', 'r') as f:
    schools = json.load(f)

# County display names
county_names = {
    'caroline': 'Caroline',
    'dorchester': 'Dorchester',
    'kent': 'Kent',
    'queen-annes': "Queen Anne's",
    'talbot': 'Talbot'
}

html = '''        <!-- SCHOOLS TAB -->
        <section id="schools" class="section">
            <h2>Schools Dashboard</h2>

            <p>Complete school-level directory for all 47 schools across the five-county region. Use the filters below to find schools by type, county, or sort by different metrics. Click any school card to view detailed enrollment, demographics, student groups (FARMS, Title I, Students with Disabilities), and MCAP performance data.</p>

            <div class="narrative-box">
                <p><strong>School-level data reveals significant within-school and between-school disparities.</strong> At Chapel District Elementary in Talbot County, white students score 67.5% proficient in 5th grade ELA while Black students in the same building score just 18.2%—a 49.3-point gap. These within-school achievement gaps demonstrate that equity challenges persist even in well-funded, high-performing schools.</p>
                
                <p><strong>Between-school differences are equally stark.</strong> Elementary schools across the region serve significantly different populations. Some schools have Free and Reduced Meals (FARMS) rates below 20%, while others exceed 70%. These demographic differences correlate with achievement outcomes, creating opportunity gaps within individual counties that mirror the cross-county disparities documented in the Five Key Issues section.</p>
            </div>

            <!-- School Filters -->
            <div class="school-filters">
                <div class="filter-row">
                    <div class="filter-group">
                        <label>School Type</label>
                        <div class="filter-tabs">
                            <button class="filter-tab active" data-filter-type="type" data-value="all">All Schools</button>
                            <button class="filter-tab" data-filter-type="type" data-value="Elementary">Elementary</button>
                            <button class="filter-tab" data-filter-type="type" data-value="Middle">Middle Schools</button>
                            <button class="filter-tab" data-filter-type="type" data-value="High">High Schools</button>
                        </div>
                    </div>
                </div>
                <div class="filter-row">
                    <div class="filter-group">
                        <label>County</label>
                        <div class="filter-tabs">
                            <button class="filter-tab active" data-filter-type="county" data-value="all">All Counties</button>
                            <button class="filter-tab" data-filter-type="county" data-value="caroline">Caroline</button>
                            <button class="filter-tab" data-filter-type="county" data-value="dorchester">Dorchester</button>
                            <button class="filter-tab" data-filter-type="county" data-value="kent">Kent</button>
                            <button class="filter-tab" data-filter-type="county" data-value="queen-annes">Queen Anne's</button>
                            <button class="filter-tab" data-filter-type="county" data-value="talbot">Talbot</button>
                        </div>
                    </div>
                </div>
                <div class="filter-row">
                    <div class="filter-group">
                        <label>Sort By</label>
                        <select class="filter-select" id="schoolSortSelect">
                            <option value="name">School Name (A-Z)</option>
                            <option value="enrollment-desc">Enrollment (High to Low)</option>
                            <option value="enrollment-asc">Enrollment (Low to High)</option>
                            <option value="farms-desc">FARMS Rate (High to Low)</option>
                            <option value="farms-asc">FARMS Rate (Low to High)</option>
                            <option value="econ-desc">Economically Disadvantaged (High to Low)</option>
                            <option value="econ-asc">Economically Disadvantaged (Low to High)</option>
                            <option value="white-desc">% White (High to Low)</option>
                            <option value="black-desc">% Black (High to Low)</option>
                            <option value="hispanic-desc">% Hispanic (High to Low)</option>
                            <option value="ela-desc">ELA Proficiency (High to Low)</option>
                            <option value="math-desc">Math Proficiency (High to Low)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Schools Grid -->
            <div class="schools-card-grid" id="schoolsGrid">
'''

# Generate school cards
for school in schools:
    county = school['county']
    name = school['name']
    school_type = school['type']
    
    # Extract numeric values for data attributes
    enrollment = school.get('enrollment', '0')
    
    # Extract FARMS percentage
    farms = school.get('student_groups', {}).get('Free and Reduced Meals Students', '0%')
    farms_pct = farms.split('%')[0] if '%' in farms else '0'
    
    # Extract race percentages
    white_pct = school.get('race', {}).get('White', '0%').split('%')[0]
    black_pct = school.get('race', {}).get('African Am.', '0%').split('%')[0]
    hispanic_pct = school.get('race', {}).get('Hispanic', '0%').split('%')[0]
    
    # Extract economically disadvantaged percentage
    econ_disadv = school.get('student_groups', {}).get('Economically Disadvantaged', '0%')
    econ_pct = econ_disadv.split('%')[0] if '%' in econ_disadv else '0'
    
    # Extract MCAP percentages
    ela_mcap = school.get('mcap', {}).get('ELA', '0% Proficient').split('%')[0]
    math_mcap = school.get('mcap', {}).get('Math', '0% Proficient').split('%')[0]
    
    # Build all data attributes from school data
    data_attrs = f'data-school-type="{school_type}" data-county="{county}" data-enrollment="{enrollment}" data-farms="{farms_pct}" data-econ="{econ_pct}" data-white="{white_pct}" data-black="{black_pct}" data-hispanic="{hispanic_pct}" data-ela="{ela_mcap}" data-math="{math_mcap}"'
    
    # Add all school details as data attributes
    data_attrs += f' data-name="{name}"'
    data_attrs += f' data-male="{school.get("male_pct", "N/A")}"'
    data_attrs += f' data-female="{school.get("female_pct", "N/A")}"'
    
    # Race data - remove (number) patterns
    race = school.get('race', {})
    import re
    for race_key, race_val in race.items():
        safe_key = race_key.replace(' ', '-').replace('.', '').lower()
        # Remove (number) patterns like (291), (128), etc.
        clean_val = re.sub(r'\s*\(\d+\)', '', race_val)
        data_attrs += f' data-race-{safe_key}="{clean_val}"'
    
    # Student groups - remove (n=XX) patterns
    groups = school.get('student_groups', {})
    import re
    for group_key, group_val in groups.items():
        # Remove (n=XX) or (n=*) patterns
        clean_val = re.sub(r'\s*\(n=.*?\)', '', group_val)
        if 'Free and Reduced' in group_key:
            data_attrs += f' data-farms-full="{clean_val}"'
        elif 'Economically Disadvantaged' in group_key:
            data_attrs += f' data-econ-disadv="{clean_val}"'
        elif 'Disabilities' in group_key:
            data_attrs += f' data-swd="{clean_val}"'
        elif 'Multilingual' in group_key:
            data_attrs += f' data-ml="{clean_val}"'
    
    # MCAP data
    mcap = school.get('mcap', {})
    for subj, val in mcap.items():
        safe_subj = subj.replace(' ', '-').lower()
        data_attrs += f' data-mcap-{safe_subj}="{val}"'
    
    html += f'''                <div class="school-card {county}" {data_attrs} onclick="openSchoolModal(this)">
                    <h4>{name}</h4>
                    <span class="school-type">{school_type}</span>
                    <div class="school-card-county">{county_names[county]} County</div>
                </div>
'''

html += '''            </div>
        </section>

        <!-- School Modal -->
        <div id="schoolModal" class="school-modal" onclick="closeSchoolModal(event)">
            <div class="school-modal-content" onclick="event.stopPropagation()">
                <div class="school-modal-header">
                    <button class="school-modal-close" onclick="closeSchoolModal()">&times;</button>
                    <h3 id="modalSchoolName">School Name</h3>
                    <div class="school-info" id="modalSchoolInfo">County • Type</div>
                </div>
                <div class="school-modal-body" id="modalSchoolBody">
                    <!-- Content populated by JavaScript -->
                </div>
            </div>
        </div>
'''

with open('schools_section.html', 'w') as f:
    f.write(html)

print(f"Generated schools section with {len(schools)} schools")
