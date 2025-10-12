# Quick Start Guide

## Installation & Running

### 1. Install Dependencies
```bash
npm run install-all
```

This will install dependencies for:
- Root project (concurrently for running both servers)
- Backend server (Express, CORS)
- Frontend client (React, Material-UI, Mapbox)

### 2. Configure Mapbox Token (Important!)

To enable the map functionality, you need a free Mapbox token:

1. Go to https://www.mapbox.com/ and sign up for a free account
2. Get your access token from https://account.mapbox.com/access-tokens/
3. Open `client/src/components/VesselMap.js`
4. Replace the placeholder token on line 8:
   ```javascript
   const MAPBOX_TOKEN = 'your-actual-token-here';
   ```

### 3. Start the Application
```bash
npm start
```

This single command will:
- Start the backend server on http://localhost:5000
- Start the frontend client on http://localhost:3000
- Automatically open your browser

## What You'll See

### Main Page (Fleet List)
- Table showing all fleets with their vessel counts
- Click column headers to sort
- Click any fleet row to view details

### Fleet Detail Page
- Search bar to filter vessels by Name, MMSI, and Flag
- Sortable table of all vessels in the fleet
- Interactive map showing vessel locations
- Click vessel markers on the map to see detailed information

## Features

✅ **Phase 1**: Fleet list with sortable columns  
✅ **Phase 2**: Fleet detail page with vessels table and interactive map  
✅ **Phase 3**: Search/filter vessels with multiple criteria  

## API Endpoints

The backend provides these REST endpoints:

- `GET /api/fleets` - All fleets with basic info
- `GET /api/fleets/:fleetId/vessels` - Vessels in a specific fleet
- `GET /api/vessels/search?name=X&mmsi=Y&flag=Z&fleetId=ID` - Search vessels

## Troubleshooting

**Map not showing?**
- Make sure you've added your Mapbox token (see step 2 above)

**Port already in use?**
- Backend: Change PORT in server/server.js
- Frontend: Create a .env file in client/ with `PORT=3001`

**Dependencies issues?**
- Delete all node_modules folders and package-lock.json files
- Run `npm run install-all` again

## Tech Stack

**Backend**: Node.js, Express, efficient Map-based data indexing  
**Frontend**: React 18, Material-UI, Mapbox GL, React Router  
**Features**: Sortable tables, real-time search, interactive maps

