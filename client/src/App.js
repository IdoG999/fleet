import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import FleetList from './components/FleetList';
import FleetDetail from './components/FleetDetail';

// main app colors - blue and red theme
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

// main app component - handles routing and theme
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

