# Quick Start Scripts

## Windows PowerShell Quick Start

```powershell
# Start backend server
python enhanced_server.py

# In a new terminal - Start frontend
cd hotel-admin-dashboard
npm run dev
```

## Individual Commands

### Backend Setup
```bash
pip install flask flask-cors python-dotenv livekit
python enhanced_server.py
```

### Frontend Setup
```bash
cd hotel-admin-dashboard
npm install
npm run dev
```

## Environment Variables Required

### Backend (.env)
```
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your_api_key_here
LIVEKIT_API_SECRET=your_api_secret_here
```

### Frontend (hotel-admin-dashboard/.env)
```
VITE_API_URL=http://localhost:5000
VITE_LIVEKIT_URL=wss://your-livekit-server.com
```

## Default Access
- **Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## Troubleshooting

### Port Issues
If ports are busy, you can change them:
- Backend: Edit `enhanced_server.py` line with `app.run(port=5000)`
- Frontend: Use `npm run dev -- --port 3001`

### Dependency Issues
Make sure you have:
- Node.js v18+ 
- Python 3.8+
- npm or yarn
- pip