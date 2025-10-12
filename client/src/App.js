import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import FleetList from './components/FleetList';
import FleetDetail from './components/FleetDetail';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<FleetList />} />
          <Route path="/fleet/:fleetId" element={<FleetDetail />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;

