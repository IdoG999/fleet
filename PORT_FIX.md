# Port 5000 Already in Use - FIXED

## What I Changed

Port 5000 is commonly used by macOS AirPlay Receiver. I've changed the server to use **port 5001** instead.

### Changes Made:
1. ✅ Server now uses port **5001** (changed default in server.js)
2. ✅ Created `server/.env` file with PORT=5001
3. ✅ Updated API config to use port 5001
4. ✅ Added dotenv package for environment variable support

## What You Need to Do

### Step 1: Install the new dependency
```bash
cd server
npm install
cd ..
```

### Step 2: Start the application
```bash
npm start
```

Your server will now run on **http://localhost:5001** instead of 5000.

---

## Alternative: Kill the Process Using Port 5000

If you want to keep using port 5000, you can find and kill the process:

### On macOS/Linux:
```bash
# Find what's using port 5000
lsof -ti:5000

# Kill the process (replace PID with the number from above)
kill -9 $(lsof -ti:5000)
```

### On Windows:
```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with the number from above)
taskkill /PID <PID> /F
```

### Common Culprits for Port 5000:
- **macOS AirPlay Receiver** - Disable in System Preferences → Sharing → AirPlay Receiver
- Another Node.js server you forgot to stop
- Docker container

---

## To Switch Back to Port 5000 Later

If you want to use port 5000 again after freeing it up:

1. Edit `server/.env`:
   ```
   PORT=5000
   ```

2. Edit `client/src/config.js`:
   ```javascript
   const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
   ```

3. Restart the app:
   ```bash
   npm start
   ```

---

## Verification

After starting with `npm start`, you should see:
- ✅ `Server running on port 5001`
- ✅ Frontend connecting successfully at http://localhost:3000

Test the backend directly:
```bash
curl http://localhost:5001/api/health
```

Should return: `{"status":"ok","vessels":95,"fleets":8,"locations":95}`

