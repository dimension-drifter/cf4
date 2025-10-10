@echo off
echo 🏨 Setting up The Pink Pearl Hotel Admin Dashboard
echo =================================================

:: Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js v18 or higher.
    pause
    exit /b 1
)

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

:: Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd hotel-admin-dashboard
call npm install

if %errorlevel% equ 0 (
    echo ✅ Frontend dependencies installed successfully
) else (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

:: Create environment file for frontend
if not exist .env (
    echo 📄 Creating frontend environment file...
    copy .env.example .env >nul 2>&1
    echo ⚠️  Please update the .env file with your actual configuration
)

:: Go back to root and install Python dependencies
cd ..
echo 🐍 Installing Python backend dependencies...

:: Install Python dependencies
pip install flask flask-cors python-dotenv livekit

if %errorlevel% equ 0 (
    echo ✅ Python dependencies installed successfully
) else (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

:: Create backend environment file
if not exist .env (
    echo 📄 Creating backend environment file...
    echo # LiveKit Configuration > .env
    echo LIVEKIT_URL=wss://your-livekit-server.com >> .env
    echo LIVEKIT_API_KEY=your_api_key_here >> .env
    echo LIVEKIT_API_SECRET=your_api_secret_here >> .env
    echo. >> .env
    echo # Add your actual LiveKit credentials above >> .env
    echo ⚠️  Please update the backend .env file with your LiveKit credentials
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo Next steps:
echo 1. Update the backend .env file with your LiveKit credentials
echo 2. Update hotel-admin-dashboard/.env with your configuration
echo 3. Start the backend server: python enhanced_server.py
echo 4. Start the dashboard: cd hotel-admin-dashboard ^&^& npm run dev
echo.
echo 🚀 Your dashboard will be available at: http://localhost:3000
echo 🔧 Backend API will be available at: http://localhost:5000
echo.
pause