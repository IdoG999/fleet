import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
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
  Alert
} from '@mui/material';
import DirectionsBoatIcon from '@mui/icons-material/DirectionsBoat';
import axios from 'axios';
import API_BASE_URL from '../config';

// main fleet list page
function FleetList() {
  // state for managing fleets data
  const [fleets, setFleets] = useState([]);
  // loading state
  const [loading, setLoading] = useState(true);
  // error handling
  const [error, setError] = useState(null);
  // sorting state
  const [orderBy, setOrderBy] = useState('name');
  // sort direction
  const [order, setOrder] = useState('asc');
  // navigation hook
  const navigate = useNavigate();

  // load fleets when component mounts
  useEffect(() => {
    fetchFleets();
  }, []);

  // get fleets from the server
  const fetchFleets = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/fleets`);
      setFleets(response.data);
      setError(null);
    } catch (err) {
      setError(`Failed to fetch fleets. Please ensure the server is running on port 5000. Error: ${err.message}`);
      console.error('Error fetching fleets:', err);
    } finally {
      setLoading(false);
    }
  };

  // handle column sorting
  const handleSort = (property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  // sort the fleets based on current settings
  const sortedFleets = useMemo(() => {
    return [...fleets].sort((a, b) => {
      let aValue = a[orderBy];
      let bValue = b[orderBy];

      // make sure strings compare properly
      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }

      if (order === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
      }
    });
  }, [fleets, order, orderBy]);

  // navigate to fleet detail page
  const handleRowClick = (fleetId) => {
    navigate(`/fleet/${fleetId}`);
  };

  // show loading spinner
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 2 }}>
        <DirectionsBoatIcon sx={{ fontSize: 40, color: 'primary.main' }} />
        <Typography variant="h3" component="h1" fontWeight="bold">
          Fleet Management
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Paper elevation={3}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow sx={{ backgroundColor: 'primary.main' }}>
                <TableCell>
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
                    <Typography variant="h6" color="white" fontWeight="bold">
                      Fleet Name
                    </Typography>
                  </TableSortLabel>
                </TableCell>
                <TableCell align="right">
                  <TableSortLabel
                    active={orderBy === 'vesselsCount'}
                    direction={orderBy === 'vesselsCount' ? order : 'asc'}
                    onClick={() => handleSort('vesselsCount')}
                    sx={{ 
                      color: 'white !important',
                      '&.Mui-active': { color: 'white !important' },
                      '& .MuiTableSortLabel-icon': { color: 'white !important' }
                    }}
                  >
                    <Typography variant="h6" color="white" fontWeight="bold">
                      Vessels Count
                    </Typography>
                  </TableSortLabel>
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sortedFleets.map((fleet) => (
                <TableRow
                  key={fleet._id}
                  hover
                  onClick={() => handleRowClick(fleet._id)}
                  sx={{ 
                    cursor: 'pointer',
                    '&:hover': { backgroundColor: 'action.hover' }
                  }}
                >
                  <TableCell>
                    <Typography variant="body1" fontWeight="medium">
                      {fleet.name}
                    </Typography>
                  </TableCell>
                  <TableCell align="right">
                    <Typography variant="body1">
                      {fleet.vesselsCount}
                    </Typography>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {sortedFleets.length === 0 && !loading && !error && (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="h6" color="text.secondary">
            No fleets found
          </Typography>
        </Box>
      )}
    </Container>
  );
}

export default FleetList;

