# Story Archive Feature

## Overview
The Story Archive tab provides comprehensive access to all 211 education stories from the Eastern Shore, with advanced filtering and search capabilities.

## Features

### 1. **Advanced Filtering**
- **County Filter**: View stories from specific counties (Caroline, Dorchester, Kent, Queen Anne's, Talbot)
- **Time Period**: Filter by Last 30/60/90 Days or All Time
- **Author Filter**: Browse stories by specific reporters
- **Search**: Full-text search across titles, summaries, and key people

### 2. **Sorting Options**
- Newest First (default)
- Oldest First
- Quality Score (High to Low) - based on beatbook_evaluation scores

### 3. **Rich Story Cards**
Each story displays:
- **Title** and publication date
- **Author** attribution
- **AI-generated summary** for quick comprehension
- **Quality score** (1-5) indicating story value
- **County tags** for geographic context
- **Key sources** mentioned in the article

### 4. **Visual Design**
- Color-coded quality scores (green = high, orange = medium, gray = low)
- County tags with accent colors
- Hover effects for better interactivity
- Responsive grid layout

## Data Source
Stories are loaded from `refined_beatbook_stories.json` which includes:
- Full article content and metadata
- LLM-generated summaries
- Quality evaluations
- Extracted key people and organizations
- Geographic tagging

## Usage Tips
1. Start with County filter to focus on specific districts
2. Use Date filter to see recent coverage
3. Combine filters to find specific story types
4. Search for specific schools, people, or topics
5. Sort by Quality Score to find most newsworthy stories

## Statistics
- **Total Stories**: 211
- **Date Range**: September - October 2025
- **Counties Covered**: 5
- **Primary Authors**: Konner Metz, Ahmad Garnett, Lily Tierney, Staff Writers
