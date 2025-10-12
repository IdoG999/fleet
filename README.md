# Fleet Management System

A full-stack web application for managing and visualizing fleet vessels with real-time location tracking.

## Features

### Phase 1 - Fleet List
- Display all fleets in a sortable table
- Show fleet name and vessel count
- Click on fleet to view details

### Phase 2 - Fleet Details
- View detailed information about vessels in a fleet
- Sortable vessel table with multiple columns (Name, MMSI, Flag, Class, Location)
- Interactive map showing vessel locations with markers
- Click vessel markers to view detailed information in popups

### Phase 3 - Search & Filter
- Search vessels by name, MMSI, and flag
- Multiple filters work together with AND logic
- Real-time results displayed in both table and map

## Technology Stack

### Backend
- Node.js with Express
- Efficient in-memory data storage with Map-based indexing
- RESTful API endpoints
- CORS enabled for cross-origin requests

### Frontend
- React 18 with React Router for navigation
- Material-UI (MUI) for beautiful, modern UI components
- Mapbox GL JS for interactive maps
- Axios for API calls

## Installation

1. Install all dependencies:
```bash
npm run install-all
```

## Running the Application

Start both server and client with a single command:
```bash
npm start
```

This will:
- Start the Node.js backend on port 5000
- Start the React frontend on port 3000
- Automatically open your browser to http://localhost:3000

## API Endpoints

- `GET /api/fleets` - Get all fleets with basic info
- `GET /api/fleets/:fleetId/vessels` - Get vessels for a specific fleet
- `GET /api/vessels/search` - Search vessels (query params: name, mmsi, flag, fleetId)
- `GET /api/health` - Health check endpoint

## Project Structure

```
ido/
├── server/
│   ├── server.js           # Backend server with API routes
│   └── package.json        # Backend dependencies
├── client/
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── FleetList.js    # Main fleet list page
│   │   │   ├── FleetDetail.js  # Fleet detail page
│   │   │   └── VesselMap.js    # Map component
│   │   ├── App.js          # Main app component with routing
│   │   ├── index.js        # React entry point
│   │   └── index.css       # Global styles
│   └── package.json        # Frontend dependencies
├── vessels.json            # Vessel data
├── fleets.json             # Fleet data
├── vesselLocations.json    # Vessel location data
├── package.json            # Root package with start script
└── README.md               # This file
```

## Configuration

### Mapbox Token
To use the map functionality, you need to add your Mapbox access token:

1. Sign up for a free account at https://www.mapbox.com/
2. Get your access token from your account dashboard
3. Replace the token in `client/src/components/VesselMap.js`:
```javascript
const MAPBOX_TOKEN = 'your-token-here';
```

## Features Implemented

✅ Smart data loading with efficient Map-based indexing (O(1) lookups)  
✅ Sortable fleet table on main page  
✅ Fleet detail page with vessel information  
✅ Interactive Mapbox map with vessel markers  
✅ Clickable markers with detailed popup information  
✅ Search functionality with multiple filters (AND logic)  
✅ Responsive design with Material-UI  
✅ Single command startup  
✅ Clean, modern UI with smooth interactions  

## Notes

- The application uses in-memory data storage for fast access
- All vessel and location data is indexed for O(1) lookup performance
- The map requires a Mapbox token to function properly
- Search filters work together with AND logic
- Tables are fully sortable by clicking column headers

# fleet
