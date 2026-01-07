# Eastern Shore Education Beatbook - GitHub Pages Setup

## Status
✅ **Ready for GitHub Pages**

Your beatbook application files have been set up in the `/docs` folder of your repository and are ready to be published via GitHub Pages.

## Files Included

- `index.html` - Main beatbook application interface
- `script.js` - JavaScript application logic (fixed regex issue)
- `style.css` - Complete styling
- `data.json` - Beatbook data (embed this from the source folder)

## Quick Setup Instructions

1. **Enable GitHub Pages:**
   - Go to: https://github.com/NewsAppsUMD/jour329w_fall2025/settings/pages
   - Under "Build and deployment":
     - Source: **Deploy from a branch**
     - Branch: **main** 
     - Folder: **/docs**
   - Click **Save**

2. **Add the data.json file:**
   - Copy from: `murphy/stardem_final/beatbook_outputs/data.json`
   - Paste to: `docs/data.json`
   - Commit and push

3. **View your live site:**
   - Once deployed, access it at: `https://NewsAppsUMD.github.io/jour329w_fall2025/`

## About This Setup

GitHub Pages will automatically serve your `index.html` as the homepage when someone visits the site. The JavaScript file loads `data.json` asynchronously, so make sure to include that file in the `/docs` folder.

## Features

- **Dashboard**: Charts and statistics for all 5 counties
- **County Profiles**: Detailed fiscal and demographic data
- **Story Archive**: Searchable database of education news
- **Key Sources**: Profiles of education leaders
- **Quote Database**: Thousands of searchable quotes

## Troubleshooting

If the data doesn't load:
1. Check that `data.json` is in the `/docs` folder
2. Check browser console (F12) for errors
3. Ensure all JSON is valid (use https://jsonlint.com/ to validate)

## Next Steps

1. Commit and push the `docs/` folder to GitHub
2. Enable GitHub Pages in repository settings
3. Wait 1-2 minutes for the site to deploy
4. Share the link with your team!
