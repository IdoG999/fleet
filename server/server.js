const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = 5003;

app.use(cors());
app.use(express.json());

// keeping all the data in memory for fast access
let vessels = [];
let fleets = [];
let vesselLocations = [];
let vesselMap = new Map(); // quick vessel lookup by ID
let locationMap = new Map(); // quick location lookup by vessel ID

// load all the data when server starts
function loadData() {
  try {
    // grab vessel data
    const vesselsData = fs.readFileSync(path.join(__dirname, '../vessels.json'), 'utf8');
    vessels = JSON.parse(vesselsData);
    
    // build lookup map for vessels
    vessels.forEach(vessel => {
      vesselMap.set(vessel._id, vessel);
    });
    
    // grab fleet data
    const fleetsData = fs.readFileSync(path.join(__dirname, '../fleets.json'), 'utf8');
    fleets = JSON.parse(fleetsData);
    
    // grab location data
    const locationsData = fs.readFileSync(path.join(__dirname, '../vesselLocations.json'), 'utf8');
    vesselLocations = JSON.parse(locationsData);
    
    // build lookup map for locations
    vesselLocations.forEach(location => {
      locationMap.set(location._id, location);
    });
    
    console.log(`Loaded ${vessels.length} vessels, ${fleets.length} fleets, ${vesselLocations.length} locations`);
  } catch (error) {
    console.error('Error loading data:', error);
    process.exit(1);
  }
}

// start loading data
loadData();

// add location info to vessel data
function enrichVesselWithLocation(vessel) {
  const location = locationMap.get(vessel._id);
  return {
    ...vessel,
    location: location ? location.lastpos : null
  };
}

// get all fleets
app.get('/api/fleets', (req, res) => {
  try {
    const fleetsBasicInfo = fleets.map(fleet => ({
      _id: fleet._id,
      name: fleet.name,
      vesselsCount: fleet.vessels ? fleet.vessels.length : 0
    }));
    
    res.json(fleetsBasicInfo);
  } catch (error) {
    console.error('Error fetching fleets:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// get vessels for one fleet
app.get('/api/fleets/:fleetId/vessels', (req, res) => {
  try {
    const { fleetId } = req.params;
    const fleet = fleets.find(f => f._id === fleetId);
    
    if (!fleet) {
      return res.status(404).json({ error: 'Fleet not found' });
    }
    
    // get all vessel details including locations
    const fleetVessels = fleet.vessels.map(fleetVessel => {
      const vessel = vesselMap.get(fleetVessel._id);
      if (vessel) {
        const location = locationMap.get(vessel._id);
        return {
          ...vessel,
          fleetValue: fleetVessel.value,
          location: location ? location.lastpos : null
        };
      }
      return null;
    }).filter(v => v !== null);
    
    res.json({
      fleet: {
        _id: fleet._id,
        name: fleet.name,
        vesselsCount: fleet.vessels.length
      },
      vessels: fleetVessels
    });
  } catch (error) {
    console.error('Error fetching fleet vessels:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// search through vessels
app.get('/api/vessels/search', (req, res) => {
  try {
    const { name, mmsi, flag, fleetId } = req.query;
    
    // figure out which vessels to search
    let vesselsToSearch = [];
    
    if (fleetId) {
      // only search this fleet
      const fleet = fleets.find(f => f._id === fleetId);
      if (fleet) {
        vesselsToSearch = fleet.vessels.map(fv => vesselMap.get(fv._id)).filter(v => v);
      }
    } else {
      // search everything
      vesselsToSearch = vessels;
    }
    
    // filter results
    let results = vesselsToSearch;
    
    if (name) {
      const nameLower = name.toLowerCase();
      results = results.filter(vessel => 
        vessel.name && vessel.name.toLowerCase().includes(nameLower)
      );
    }
    
    if (mmsi) {
      results = results.filter(vessel => 
        vessel.mmsi && vessel.mmsi.toString().includes(mmsi.toString())
      );
    }
    
    if (flag) {
      const flagLower = flag.toLowerCase();
      results = results.filter(vessel => 
        vessel.flag && vessel.flag.toLowerCase().includes(flagLower)
      );
    }
    
    // add location info to results
    const enrichedResults = results.map(vessel => {
      const location = locationMap.get(vessel._id);
      return {
        ...vessel,
        location: location ? location.lastpos : null
      };
    });
    
    res.json(enrichedResults);
  } catch (error) {
    console.error('Error searching vessels:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// check if server is working
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok',
    vessels: vessels.length,
    fleets: fleets.length,
    locations: vesselLocations.length
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`API endpoints:`);
  console.log(`  GET /api/fleets - Get all fleets`);
  console.log(`  GET /api/fleets/:fleetId/vessels - Get vessels for a fleet`);
  console.log(`  GET /api/vessels/search - Search vessels`);
});

