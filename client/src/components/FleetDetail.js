import React, { useState, useEffect, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Button,
  Grid,
  TextField,
  Card,
  CardContent
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import SearchIcon from '@mui/icons-material/Search';
import axios from 'axios';
import API_BASE_URL from '../config';
import VesselMap from './VesselMap';

// fleet detail page with vessels and map
function FleetDetail() {
  // get fleet id from url
  const { fleetId } = useParams();
  // navigation hook
  const navigate = useNavigate();
  // fleet info
  const [fleetData, setFleetData] = useState(null);
  // all vessels in fleet
  const [vessels, setVessels] = useState([]);
  // filtered vessels after search
  const [filteredVessels, setFilteredVessels] = useState([]);
  // loading state
  const [loading, setLoading] = useState(true);
  // error handling
  const [error, setError] = useState(null);
  // sorting state
  const [orderBy, setOrderBy] = useState('name');
  // sort direction
  const [order, setOrder] = useState('asc');
  
  // search filters
  const [searchName, setSearchName] = useState('');
  const [searchMmsi, setSearchMmsi] = useState('');
  const [searchFlag, setSearchFlag] = useState('');

  // load vessels when fleet changes
  useEffect(() => {
    fetchFleetVessels();
  }, [fleetId]);

  // get vessels for this fleet
  const fetchFleetVessels = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/fleets/${fleetId}/vessels`);
      setFleetData(response.data.fleet);
      setVessels(response.data.vessels);
      setFilteredVessels(response.data.vessels);
      setError(null);
    } catch (err) {
      setError(`Failed to fetch fleet vessels. Please ensure the server is running. Error: ${err.message}`);
      console.error('Error fetching fleet vessels:', err);
    } finally {
      setLoading(false);
    }
  };

  // search through vessels
  const handleSearch = async () => {
    try {
      const params = new URLSearchParams();
      params.append('fleetId', fleetId);
      if (searchName) params.append('name', searchName);
      if (searchMmsi) params.append('mmsi', searchMmsi);
      if (searchFlag) params.append('flag', searchFlag);

      const response = await axios.get(`${API_BASE_URL}/api/vessels/search?${params.toString()}`);
      setFilteredVessels(response.data);
    } catch (err) {
      setError(`Failed to search vessels. Error: ${err.message}`);
      console.error('Error searching vessels:', err);
    }
  };

  // clear search and show all vessels
  const handleClearSearch = () => {
    setSearchName('');
    setSearchMmsi('');
    setSearchFlag('');
    setFilteredVessels(vessels);
  };

  // handle column sorting
  const handleSort = (property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  // sort vessels based on current settings
  const sortedVessels = useMemo(() => {
    return [...filteredVessels].sort((a, b) => {
      let aValue = a[orderBy];
      let bValue = b[orderBy];

      // handle missing values
      if (aValue == null) return order === 'asc' ? 1 : -1;
      if (bValue == null) return order === 'asc' ? -1 : 1;

      // make sure strings compare properly
      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue?.toLowerCase() || '';
      }

      if (order === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
      }
    });
  }, [filteredVessels, order, orderBy]);

  // show loading spinner
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  // fleet not found
  if (!fleetData) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">Fleet not found</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/')}
          variant="outlined"
          sx={{ mb: 2 }}
        >
          Back to Fleets
        </Button>
        <Typography variant="h3" component="h1" fontWeight="bold">
          {fleetData.name}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          {fleetData.vesselsCount} vessels in fleet
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* search section */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <SearchIcon /> Search Vessels
          </Typography>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Vessel Name"
                value={searchName}
                onChange={(e) => setSearchName(e.target.value)}
                size="small"
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="MMSI"
                value={searchMmsi}
                onChange={(e) => setSearchMmsi(e.target.value)}
                size="small"
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Flag"
                value={searchFlag}
                onChange={(e) => setSearchFlag(e.target.value)}
                size="small"
              />
            </Grid>
            <Grid item xs={12} md={3} sx={{ display: 'flex', gap: 1 }}>
              <Button
                variant="contained"
                onClick={handleSearch}
                fullWidth
              >
                Search
              </Button>
              <Button
                variant="outlined"
                onClick={handleClearSearch}
                fullWidth
              >
                Clear
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* vessels table */}
      <Paper elevation={3} sx={{ mb: 3 }}>
        <TableContainer sx={{ maxHeight: 500 }}>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell sx={{ backgroundColor: 'primary.main' }}>
                  <TableSortLabel
                    active={orderBy === 'name'}
                    direction={orderBy === 'name' ? order : 'asc'}
                    onClick={() => handleSort('name')}
                    sx={{ 
                      color: 'white !important',
                      '&.Mui-active': { color: 'white !important' },
                      '& .MuiTableSortLabel-icon': { color: 'white !important' }
                    }}
                  >
                    <Typography variant="subtitle2" color="white" fontWeight="bold">
                      Name
                    </Typography>
                  </TableSortLabel>
                </TableCell>
                <TableCell sx={{ backgroundColor: 'primary.main' }}>
                  <TableSortLabel
                    active={orderBy === 'mmsi'}
                    direction={orderBy === 'mmsi' ? order : 'asc'}
                    onClick={() => handleSort('mmsi')}
                    sx={{ 
                      color: 'white !important',
                      '&.Mui-active': { color: 'white !important' },
                      '& .MuiTableSortLabel-icon': { color: 'white !important' }
                    }}
                  >
                    <Typography variant="subtitle2" color="white" fontWeight="bold">
                      MMSI
                    </Typography>
                  </TableSortLabel>
                </TableCell>
                <TableCell sx={{ backgroundColor: 'primary.main' }}>
                  <TableSortLabel
                    active={orderBy === 'flag'}
                    direction={orderBy === 'flag' ? order : 'asc'}
                    onClick={() => handleSort('flag')}
                    sx={{ 
                      color: 'white !important',
                      '&.Mui-active': { color: 'white !important' },
                      '& .MuiTableSortLabel-icon': { color: 'white !important' }
                    }}
                  >
                    <Typography variant="subtitle2" color="white" fontWeight="bold">
                      Flag
                    </Typography>
                  </TableSortLabel>
                </TableCell>
                <TableCell sx={{ backgroundColor: 'primary.main' }}>
                  <TableSortLabel
                    active={orderBy === 'vessel_class'}
                    direction={orderBy === 'vessel_class' ? order : 'asc'}
                    onClick={() => handleSort('vessel_class')}
                    sx={{ 
                      color: 'white !important',
                      '&.Mui-active': { color: 'white !important' },
                      '& .MuiTableSortLabel-icon': { color: 'white !important' }
                    }}
                  >
                    <Typography variant="subtitle2" color="white" fontWeight="bold">
                      Class
                    </Typography>
                  </TableSortLabel>
                </TableCell>
                <TableCell sx={{ backgroundColor: 'primary.main' }}>
                  <Typography variant="subtitle2" color="white" fontWeight="bold">
                    Location
                  </Typography>
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sortedVessels.map((vessel) => (
                <TableRow key={vessel._id} hover>
                  <TableCell>{vessel.name || 'N/A'}</TableCell>
                  <TableCell>{vessel.mmsi || 'N/A'}</TableCell>
                  <TableCell>{vessel.flag || 'N/A'}</TableCell>
                  <TableCell>{vessel.vessel_class || 'Unknown'}</TableCell>
                  <TableCell>
                    {vessel.location?.geometry?.coordinates ? (
                      <Typography variant="body2" sx={{ fontSize: '0.75rem' }}>
                        {vessel.location.geometry.coordinates[1].toFixed(4)}, {vessel.location.geometry.coordinates[0].toFixed(4)}
                      </Typography>
                    ) : (
                      'No location'
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* map section */}
      <Paper elevation={3}>
        <Box sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Vessel Locations
          </Typography>
        </Box>
        <VesselMap vessels={sortedVessels} />
      </Paper>

      {sortedVessels.length === 0 && !loading && (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="h6" color="text.secondary">
            No vessels found matching the search criteria
          </Typography>
        </Box>
      )}
    </Container>
  );
}

export default FleetDetail;

