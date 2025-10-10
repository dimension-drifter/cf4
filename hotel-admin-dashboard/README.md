# The Pink Pearl Hotel - Admin Dashboard

A modern, interactive admin dashboard for managing hotel operations, built with React, TypeScript, Vite, and Tailwind CSS. This dashboard integrates with a LiveKit-powered voice call assistant backend for seamless hotel management.

## 🏨 Features

### 📊 Dashboard Overview
- Real-time statistics and KPIs
- Live call monitoring with animated indicators
- Revenue tracking and trend analysis
- Quick action buttons for common tasks
- Recent activity feed

### 🏠 Booking Management
- Complete reservation management system
- Guest information tracking
- Room allocation and status updates
- Payment status monitoring
- Advanced filtering and search capabilities

### 🍽️ Restaurant Management
- Order tracking and management
- Kitchen workflow optimization
- Table and room service coordination
- Real-time order status updates
- Billing and payment processing

### 📞 Voice Call Analytics
- Comprehensive call performance metrics
- Sentiment analysis and trending
- Conversion rate tracking
- Call volume analytics by time
- Customer satisfaction monitoring

### 🔴 Live Call Monitoring
- Real-time active call tracking
- Live transcription and sentiment analysis
- Agent performance monitoring
- Call routing and management
- Interactive call controls

### ⚙️ Settings & Configuration
- System preferences management
- Voice agent configuration
- Notification settings
- Security and authentication
- API integration settings

## 🚀 Technology Stack

- **Frontend**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: React Query for server state
- **Routing**: React Router DOM
- **Charts**: Recharts
- **Icons**: Lucide React
- **Notifications**: Sonner
- **HTTP Client**: Axios

## 🛠️ Installation & Setup

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn

### Installation Steps

1. **Clone and navigate to the project**
   ```bash
   cd hotel-admin-dashboard
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   VITE_API_BASE_URL=http://localhost:5000
   VITE_LIVEKIT_URL=wss://your-livekit-server.com
   VITE_LIVEKIT_API_KEY=your_api_key
   VITE_LIVEKIT_API_SECRET=your_api_secret
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

5. **Access the dashboard**
   Open [http://localhost:3000](http://localhost:3000) in your browser

## 🔧 Backend Integration

This dashboard is designed to work with the LiveKit voice call assistant backend. Make sure your backend server is running on `http://localhost:5000` (or update the API base URL in your environment variables).

### Backend Endpoints Expected
- `POST /create_token` - Create LiveKit tokens for voice sessions
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/bookings` - Booking data
- `GET /api/restaurant/orders` - Restaurant orders
- `GET /api/calls/logs` - Call analytics data
- `GET /api/calls/live` - Live call monitoring

## 📱 Responsive Design

The dashboard is fully responsive and optimized for:
- Desktop computers (1920px+)
- Laptops (1024px+)
- Tablets (768px+)
- Mobile devices (320px+)

## 🎨 Key Design Features

- **Modern UI**: Clean, professional interface with gradient accents
- **Real-time Updates**: Live data updates with smooth animations
- **Interactive Charts**: Dynamic data visualization with Recharts
- **Responsive Layout**: Optimized for all device sizes
- **Intuitive Navigation**: Sidebar navigation with active state indicators
- **Loading States**: Shimmer loading effects for better UX
- **Error Handling**: Graceful error handling with user-friendly messages

## 📊 Dashboard Sections

### 1. Main Dashboard
- Key performance indicators
- Revenue trends
- Call volume analytics
- Live call status
- Quick action buttons

### 2. Booking Management
- Guest information forms
- Room availability calendar
- Booking status tracking
- Payment management
- Search and filter options

### 3. Restaurant Operations
- Order management system
- Kitchen display board
- Table management
- Menu item tracking
- Billing integration

### 4. Call Analytics
- Performance metrics
- Sentiment analysis
- Conversion tracking
- Historical data views
- Export capabilities

### 5. Live Call Monitor
- Active call dashboard
- Real-time transcription
- Agent performance
- Call quality metrics
- Transfer and routing

## 🔒 Security Features

- Secure API communication
- Environment variable protection
- Input validation and sanitization
- CORS configuration
- Session management

## 🔧 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏨 About The Pink Pearl Hotel

The Pink Pearl Hotel is a modern hospitality solution that combines traditional hotel management with cutting-edge voice AI technology to provide exceptional guest experiences and streamlined operations.

---

Built with ❤️ for modern hotel management