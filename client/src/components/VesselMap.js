import React, { useState, useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { Box, Typography, Divider } from '@mui/material';
import DirectionsBoatIcon from '@mui/icons-material/DirectionsBoat';

// custom simple boat icon using MUI color
const boatIcon = new L.DivIcon({
  className: 'custom-boat-icon',
  html: '<div style="color:#1976d2;font-size:24px;">⛵️</div>',
  iconSize: [24, 24],
  iconAnchor: [12, 24]
});

// map component to show vessel locations
function VesselMap({ vessels }) {
  // which vessel is selected for popup
  const [selectedVessel, setSelectedVessel] = useState(null);
  // map view settings
  const [viewState, setViewState] = useState({
    lng: 0,
    lat: 20,
    zoom: 2
  });
  // error state for map tiles
  const [mapError, setMapError] = useState(null);

  // figure out which vessels have location data
  const vesselsWithLocation = useMemo(() => {
    return vessels.filter(v => v.location?.geometry?.coordinates);
  }, [vessels]);

  // center the map on the vessels
  useMemo(() => {
    if (vesselsWithLocation.length > 0) {
      const lngs = vesselsWithLocation.map(v => v.location.geometry.coordinates[0]);
      const lats = vesselsWithLocation.map(v => v.location.geometry.coordinates[1]);
      
      const avgLng = lngs.reduce((a, b) => a + b, 0) / lngs.length;
      const avgLat = lats.reduce((a, b) => a + b, 0) / lats.length;
      
      setViewState(prev => ({ ...prev, lng: avgLng, lat: avgLat, zoom: 3 }));
    }
  }, [vesselsWithLocation.length]);

  // helper to fly the map to center once computed
  function MapFlyTo({ center, zoom }) {
    const map = useMap();
    useMemo(() => {
      map.setView([center.lat, center.lng], zoom);
    }, [center.lat, center.lng, zoom]);
    return null;
  }

  return (
    <Box sx={{ height: 600, width: '100%', position: 'relative' }}>
      <MapContainer
        center={[viewState.lat, viewState.lng]}
        zoom={viewState.zoom}
        style={{ width: '100%', height: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          eventHandlers={{
            tileerror: (e) => {
              console.error('Tile loading error:', e);
              setMapError('Map tiles failed to load. This may be due to rate limiting.');
            }
          }}
        />
        <MapFlyTo center={{ lat: viewState.lat, lng: viewState.lng }} zoom={viewState.zoom} />
        {vesselsWithLocation.map((vessel) => {
          const [lng, lat] = vessel.location.geometry.coordinates;
          return (
            <Marker key={vessel._id} position={[lat, lng]} icon={boatIcon} eventHandlers={{ click: () => setSelectedVessel(vessel) }} />
          );
        })}

        {selectedVessel && selectedVessel.location?.geometry?.coordinates && (
          <Popup position={[selectedVessel.location.geometry.coordinates[1], selectedVessel.location.geometry.coordinates[0]]} onClose={() => setSelectedVessel(null)}>
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
      </MapContainer>
      
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
      
      {mapError && (
        <Box
          sx={{
            position: 'absolute',
            top: 10,
            left: 10,
            right: 10,
            backgroundColor: 'rgba(255, 0, 0, 0.8)',
            color: 'white',
            p: 2,
            borderRadius: 1,
            textAlign: 'center'
          }}
        >
          <Typography variant="body2">
            {mapError}
          </Typography>
        </Box>
      )}
    </Box>
  );
}

export default VesselMap;

