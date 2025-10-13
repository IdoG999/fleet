import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import 'mapbox-gl/dist/mapbox-gl.css';
import App from './App';

// start the react app
const root = ReactDOM.createRoot(document.getElementById('root'));
// render the app
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

