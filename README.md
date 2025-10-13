# Fleet Management App

This is a simple web app I built to track and visualize fleet vessels. It shows vessel locations on a map and lets you search through different fleets.

## What it does

The app has two main pages:
- **Fleet List**: Shows all fleets in a table. You can sort by name or vessel count, and click any fleet to see its details.
- **Fleet Details**: Shows all vessels in a selected fleet. There's a search bar to filter vessels, a sortable table, and a map showing where each vessel is located.

## Tech stuff

**Backend**: Node.js + Express server that serves vessel data from JSON files
**Frontend**: React app with Material-UI components and Mapbox for the map

## Getting started

First, install everything:
```bash
npm run install-all
```

Then start the app:
```bash
npm start
```

This runs both the backend (port 5000) and frontend (port 3000). Your browser should open automatically.

## Mapbox setup

The map won't work without a Mapbox token. Get a free one at mapbox.com, then update the token in `client/src/components/VesselMap.js`:

```javascript
const MAPBOX_TOKEN = 'your-actual-token-here';
```

## API

The server has these endpoints:
- `/api/fleets` - get all fleets
- `/api/fleets/:id/vessels` - get vessels for a specific fleet  
- `/api/vessels/search` - search vessels by name, MMSI, or flag
- `/api/health` - check if server is running

## Files

```
fleet/
├── server/           # Backend code
├── client/           # React frontend
├── vessels.json      # Vessel data
├── fleets.json       # Fleet data  
├── vesselLocations.json  # Location data
└── package.json      # Root package file
```

That's about it. The data is stored in memory for fast lookups, and everything should work smoothly once you add your Mapbox token.
