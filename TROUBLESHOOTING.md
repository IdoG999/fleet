# Troubleshooting Guide

## 403 Forbidden Error

If you're seeing a **403 Forbidden** error when loading the fleet list, here are the steps to resolve it:

### Solution 1: Ensure Both Servers Are Running

1. **Stop any running processes** (Press Ctrl+C in the terminal)

2. **Start the application again:**
   ```bash
   npm start
   ```

3. **Verify both servers are running:**
   - You should see output like:
     ```
     Server running on port 5000
     webpack compiled successfully
     ```
   - Backend should be on http://localhost:5000
   - Frontend should be on http://localhost:3000

### Solution 2: Start Servers Manually (If npm start doesn't work)

**Terminal 1 - Start Backend:**
```bash
cd server
npm start
```

You should see: `Server running on port 5000`

**Terminal 2 - Start Frontend:**
```bash
cd client
npm start
```

This will open http://localhost:3000 in your browser.

### Solution 3: Check if Ports Are Available

**Check if port 5000 is already in use:**
```bash
# On macOS/Linux:
lsof -i :5000

# On Windows:
netstat -ano | findstr :5000
```

If port 5000 is in use, you can either:
- Kill the process using that port
- Change the port in `server/server.js` (line 6):
  ```javascript
  const PORT = process.env.PORT || 5001; // Change to 5001
  ```
  Then update `client/src/config.js`:
  ```javascript
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';
  ```

### Solution 4: Verify Server Is Working

Test the backend directly in your browser or with curl:
```bash
curl http://localhost:5000/api/health
```

You should see:
```json
{"status":"ok","vessels":95,"fleets":8,"locations":95}
```

If this doesn't work, the server isn't running or there's a problem with the data files.

### Solution 5: Check Data Files

Ensure these files exist in the root directory:
- `vessels.json`
- `fleets.json`
- `vesselLocations.json`

The server needs these files to start. If they're missing, the server will exit with an error.

### Solution 6: Reinstall Dependencies

If nothing works, try a clean reinstall:

```bash
# Remove all node_modules
rm -rf node_modules server/node_modules client/node_modules

# Remove all package-lock files
rm -f package-lock.json server/package-lock.json client/package-lock.json

# Reinstall everything
npm run install-all

# Start again
npm start
```

### Solution 7: Check Browser Console

Open your browser's Developer Tools (F12) and check:

1. **Console tab** - Look for any JavaScript errors
2. **Network tab** - Check the failed request:
   - Click on the failed request
   - Check the "Response" tab for error details
   - Verify the request URL is correct: `http://localhost:5000/api/fleets`

### Common Issues

**Issue: "Cannot GET /api/fleets"**
- Backend server is not running
- Run `cd server && npm start` in a separate terminal

**Issue: "Network Error"**
- Backend server is not accessible
- Check if backend is running on port 5000
- Check firewall settings

**Issue: "CORS Error"**
- Should not happen with our setup, but if it does:
- Verify `cors` is installed in server/package.json
- Check that server.js has `app.use(cors());`

**Issue: Frontend won't start**
- Port 3000 might be in use
- Create a `.env` file in the `client` folder with:
  ```
  PORT=3001
  ```

## Still Having Issues?

1. Check that you're in the correct directory (the `ido` folder)
2. Make sure Node.js is installed: `node --version` (should be v14 or higher)
3. Make sure npm is installed: `npm --version`
4. Try running the servers manually in separate terminals (see Solution 2)

## Quick Test Checklist

- [ ] Node.js installed (v14+)
- [ ] All dependencies installed (`npm run install-all`)
- [ ] Data files (vessels.json, fleets.json, vesselLocations.json) exist
- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] No firewall blocking localhost connections
- [ ] Browser accessing http://localhost:3000

