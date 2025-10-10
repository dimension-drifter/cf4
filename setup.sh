#!/bin/bash

echo "🏨 Setting up The Pink Pearl Hotel Admin Dashboard"
echo "================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js v18 or higher."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd hotel-admin-dashboard
npm install

if [ $? -eq 0 ]; then
    echo "✅ Frontend dependencies installed successfully"
else
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

# Create environment file for frontend
if [ ! -f .env ]; then
    echo "📄 Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your actual API keys and configuration"
fi

# Go back to root and install Python dependencies
cd ..
echo "🐍 Installing Python backend dependencies..."

# Check if pip is available
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
else
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

# Install Python dependencies
$PIP_CMD install flask flask-cors python-dotenv livekit

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Create backend environment file
if [ ! -f .env ]; then
    echo "📄 Creating backend environment file..."
    cat > .env << EOL
# LiveKit Configuration
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your_api_key_here
LIVEKIT_API_SECRET=your_api_secret_here

# Add your actual LiveKit credentials above
EOL
    echo "⚠️  Please update the backend .env file with your LiveKit credentials"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Update the backend .env file with your LiveKit credentials"
echo "2. Update hotel-admin-dashboard/.env with your configuration"
echo "3. Start the backend server: python enhanced_server.py"
echo "4. Start the dashboard: cd hotel-admin-dashboard && npm run dev"
echo ""
echo "🚀 Your dashboard will be available at: http://localhost:3000"
echo "🔧 Backend API will be available at: http://localhost:5000"