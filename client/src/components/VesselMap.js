import React, { useState, useMemo } from 'react';
import Map, { Marker, Popup } from 'react-map-gl';
import { Box, Typography, Divider } from '@mui/material';
import DirectionsBoatIcon from '@mui/icons-material/DirectionsBoat';

// Mapbox access token - You'll need to add your own token
const MAPBOX_TOKEN = 'pk.eyJ1IjoiZXhhbXBsZSIsImEiOiJjbGV4YW1wbGUifQ.example'; // Replace with your token

function VesselMap({ vessels }) {
  const [selectedVessel, setSelectedVessel] = useState(null);
  const [viewState, setViewState] = useState({
    longitude: 0,
    latitude: 20,
    zoom: 2
  });

  // Calculate bounds to fit all vessels
  const vesselsWithLocation = useMemo(() => {
    return vessels.filter(v => v.location?.geometry?.coordinates);
  }, [vessels]);

  // Set initial view based on vessels
  useMemo(() => {
    if (vesselsWithLocation.length > 0) {
      const lngs = vesselsWithLocation.map(v => v.location.geometry.coordinates[0]);
      const lats = vesselsWithLocation.map(v => v.location.geometry.coordinates[1]);
      
      const avgLng = lngs.reduce((a, b) => a + b, 0) / lngs.length;
      const avgLat = lats.reduce((a, b) => a + b, 0) / lats.length;
      
      setViewState(prev => ({
        ...prev,
        longitude: avgLng,
        latitude: avgLat,
        zoom: 3
      }));
    }
  }, [vesselsWithLocation.length]);

  return (
    <Box sx={{ height: 600, width: '100%', position: 'relative' }}>
      <Map
        {...viewState}
        onMove={evt => setViewState(evt.viewState)}
        mapStyle="mapbox://styles/mapbox/streets-v12"
        mapboxAccessToken={MAPBOX_TOKEN}
        style={{ width: '100%', height: '100%' }}
      >
        {vesselsWithLocation.map((vessel) => {
          const [lng, lat] = vessel.location.geometry.coordinates;
          return (
            <Marker
              key={vessel._id}
              longitude={lng}
              latitude={lat}
              anchor="bottom"
              onClick={(e) => {
                e.originalEvent.stopPropagation();
                setSelectedVessel(vessel);
              }}
            >
              <DirectionsBoatIcon
                sx={{
                  fontSize: 30,
                  color: 'primary.main',
                  cursor: 'pointer',
                  '&:hover': {
                    color: 'secondary.main',
                    transform: 'scale(1.2)',
                  },
                  transition: 'all 0.2s'
                }}
              />
            </Marker>
          );
        })}

        {selectedVessel && selectedVessel.location?.geometry?.coordinates && (
          <Popup
            longitude={selectedVessel.location.geometry.coordinates[0]}
            latitude={selectedVessel.location.geometry.coordinates[1]}
            anchor="top"
            onClose={() => setSelectedVessel(null)}
            closeOnClick={false}
          >
            <Box sx={{ p: 1, minWidth: 200 }}>
              <Typography variant="h6" gutterBottom>
                {selectedVessel.name || 'Unknown Vessel'}
              </Typography>
              <Divider sx={{ my: 1 }} />
              <Typography variant="body2" gutterBottom>
                <strong>MMSI:</strong> {selectedVessel.mmsi || 'N/A'}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Flag:</strong> {selectedVessel.flag || 'N/A'}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Class:</strong> {selectedVessel.vessel_class || 'Unknown'}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Type:</strong> {selectedVessel.vessel_type || 'Unknown'}
              </Typography>
              <Divider sx={{ my: 1 }} />
              <Typography variant="caption" color="text.secondary">
                <strong>Coordinates:</strong><br />
                Lat: {selectedVessel.location.geometry.coordinates[1].toFixed(4)}<br />
                Lng: {selectedVessel.location.geometry.coordinates[0].toFixed(4)}
              </Typography>
              {selectedVessel.location.sog !== undefined && (
                <Typography variant="caption" display="block" color="text.secondary">
                  <strong>Speed:</strong> {selectedVessel.location.sog} knots
                </Typography>
              )}
              {selectedVessel.location.course !== undefined && (
                <Typography variant="caption" display="block" color="text.secondary">
                  <strong>Course:</strong> {selectedVessel.location.course}°
                </Typography>
              )}
            </Box>
          </Popup>
        )}
      </Map>
      
      {vesselsWithLocation.length === 0 && (
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            p: 3,
            borderRadius: 2,
            textAlign: 'center'
          }}
        >
          <Typography variant="h6" color="text.secondary">
            No vessel locations available
          </Typography>
        </Box>
      )}
    </Box>
  );
}

export default VesselMap;

