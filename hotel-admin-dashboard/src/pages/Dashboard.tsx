import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Calendar,
  Phone,
  TrendingUp,
  Users,
  DollarSign,
  Clock,
  UserCheck,
  UtensilsCrossed,
  Zap,
  Activity,
} from 'lucide-react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { getDashboardStats } from '../services/api';
import { DashboardStats } from '../types';

// Mock data - In real app, this would come from your backend
const revenueData = [
  { name: 'Jan', revenue: 45000, bookings: 120 },
  { name: 'Feb', revenue: 52000, bookings: 135 },
  { name: 'Mar', revenue: 48000, bookings: 128 },
  { name: 'Apr', revenue: 61000, bookings: 155 },
  { name: 'May', revenue: 55000, bookings: 142 },
  { name: 'Jun', revenue: 67000, bookings: 168 },
];

const callAnalyticsData = [
  { name: 'Mon', calls: 24, bookings: 8 },
  { name: 'Tue', calls: 32, bookings: 12 },
  { name: 'Wed', calls: 28, bookings: 9 },
  { name: 'Thu', calls: 35, bookings: 15 },
  { name: 'Fri', calls: 41, bookings: 18 },
  { name: 'Sat', calls: 38, bookings: 16 },
  { name: 'Sun', calls: 29, bookings: 11 },
];

const sentimentData = [
  { name: 'Positive', value: 65, color: '#10B981' },
  { name: 'Neutral', value: 25, color: '#6B7280' },
  { name: 'Negative', value: 10, color: '#EF4444' },
];

const StatCard: React.FC<{
  title: string;
  value: string;
  change: string;
  changeType: 'positive' | 'negative';
  icon: React.ReactNode;
  description?: string;
}> = ({ title, value, change, changeType, icon, description }) => (
  <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-all duration-200">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
        <p className="text-3xl font-bold text-gray-900 mb-2">{value}</p>
        <div className="flex items-center space-x-2">
          <span className={`text-sm font-medium ${
            changeType === 'positive' ? 'text-green-600' : 'text-red-600'
          }`}>
            {change}
          </span>
          {description && (
            <span className="text-xs text-gray-500">{description}</span>
          )}
        </div>
      </div>
      <div className="p-3 bg-primary-50 rounded-xl">
        {icon}
      </div>
    </div>
  </div>
);

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [realtimeStats, setRealtimeStats] = useState({
    activeCalls: 3,
    waitingCalls: 1,
    totalCallsToday: 89,
    averageWaitTime: '2m 15s',
  });

  // Fetch dashboard data from backend
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const data = await getDashboardStats();
        setDashboardData(data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
        // Use mock data as fallback
        setDashboardData({
          totalBookings: 2,
          occupancyRate: 75.5,
          revenue: { today: 25000, month: 750000, growth: 12.5 },
          callMetrics: { totalCalls: 45, avgDuration: 150, satisfactionScore: 4.3, resolutionRate: 92 },
          recentActivity: [
            { type: 'booking', message: 'New booking confirmed - Room 301', time: '2 min ago' },
            { type: 'call', message: 'Call completed - Booking inquiry', time: '5 min ago' },
            { type: 'order', message: 'Room service order delivered', time: '8 min ago' }
          ],
          chartData: {
            revenue: [
              { name: 'Mon', value: 12000 },
              { name: 'Tue', value: 19000 },
              { name: 'Wed', value: 15000 },
              { name: 'Thu', value: 25000 },
              { name: 'Fri', value: 30000 },
              { name: 'Sat', value: 35000 },
              { name: 'Sun', value: 28000 }
            ],
            sentiment: [
              { name: 'Positive', value: 65, color: '#10B981' },
              { name: 'Neutral', value: 25, color: '#F59E0B' },
              { name: 'Negative', value: 10, color: '#EF4444' }
            ]
          }
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setRealtimeStats(prev => ({
        ...prev,
        activeCalls: Math.floor(Math.random() * 5) + 1,
        waitingCalls: Math.floor(Math.random() * 3),
        totalCallsToday: prev.totalCallsToday + (Math.random() > 0.7 ? 1 : 0),
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="loading-shimmer w-full h-32 rounded-lg"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-primary-600 to-purple-600 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">Welcome back, Admin!</h1>
            <p className="text-primary-100">Here's what's happening at The Pink Pearl Hotel today.</p>
          </div>
          <div className="hidden md:flex items-center space-x-4 text-right">
            <div>
              <p className="text-primary-100 text-sm">Today's Date</p>
              <p className="font-semibold">{new Date().toLocaleDateString('en-IN', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
              })}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Key Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Bookings"
          value={dashboardData?.totalBookings?.toString() || "0"}
          change="+12%"
          changeType="positive"
          description="all time"
          icon={<Calendar className="w-6 h-6 text-primary-600" />}
        />
        <StatCard
          title="Revenue Today"
          value={`₹${dashboardData?.revenue?.today?.toLocaleString() || "0"}`}
          change={`+${dashboardData?.revenue?.growth || 0}%`}
          changeType="positive"
          description="vs last month"
          icon={<DollarSign className="w-6 h-6 text-primary-600" />}
        />
        <StatCard
          title="Occupancy Rate"
          value={`${dashboardData?.occupancyRate || 0}%`}
          change="+5%"
          changeType="positive"
          description="of 50 rooms"
          icon={<UserCheck className="w-6 h-6 text-primary-600" />}
        />
        <StatCard
          title="Total Calls"
          value={dashboardData?.callMetrics?.totalCalls?.toString() || "0"}
          change="+15%"
          changeType="positive"
          description="today"
          icon={<Phone className="w-6 h-6 text-primary-600" />}
        />
      </div>

      {/* Live Call Monitoring */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Call Analytics</h3>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">Live</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={dashboardData?.chartData?.revenue || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey="value" stackId="1" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.1} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Live Call Status</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span className="font-medium text-green-800">Active Calls</span>
              </div>
              <span className="text-2xl font-bold text-green-600">{realtimeStats.activeCalls}</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-yellow-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <Clock className="w-4 h-4 text-yellow-600" />
                <span className="font-medium text-yellow-800">Waiting</span>
              </div>
              <span className="text-2xl font-bold text-yellow-600">{realtimeStats.waitingCalls}</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <Activity className="w-4 h-4 text-blue-600" />
                <span className="font-medium text-blue-800">Avg. Response</span>
              </div>
              <span className="text-lg font-bold text-blue-600">{realtimeStats.averageWaitTime}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Revenue & Sentiment Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Revenue Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="revenue" stroke="#3B82F6" strokeWidth={3} dot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Call Sentiment Analysis</h3>
          <div className="flex items-center justify-center">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sentimentData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {sentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Quick Actions & Recent Activities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Quick Actions</h3>
          <div className="grid grid-cols-2 gap-4">
            <button 
              onClick={() => navigate('/bookings')}
              className="p-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 flex flex-col items-center space-y-2 transform hover:scale-105"
            >
              <Calendar className="w-6 h-6" />
              <span className="text-sm font-medium">New Booking</span>
            </button>
            <button 
              onClick={() => navigate('/live-calls')}
              className="p-4 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-200 flex flex-col items-center space-y-2 transform hover:scale-105"
            >
              <Phone className="w-6 h-6" />
              <span className="text-sm font-medium">Call Center</span>
            </button>
            <button 
              onClick={() => navigate('/restaurant')}
              className="p-4 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-200 flex flex-col items-center space-y-2 transform hover:scale-105"
            >
              <UtensilsCrossed className="w-6 h-6" />
              <span className="text-sm font-medium">Restaurant</span>
            </button>
            <button 
              onClick={() => navigate('/analytics')}
              className="p-4 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-lg hover:from-orange-600 hover:to-orange-700 transition-all duration-200 flex flex-col items-center space-y-2 transform hover:scale-105"
            >
              <TrendingUp className="w-6 h-6" />
              <span className="text-sm font-medium">Analytics</span>
            </button>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Recent Activities</h3>
          <div className="space-y-4">
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">New booking confirmed</p>
                <p className="text-xs text-gray-500">Room 205 - John Doe - 2 mins ago</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">Call completed</p>
                <p className="text-xs text-gray-500">Booking inquiry - 5 mins ago</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">Restaurant order</p>
                <p className="text-xs text-gray-500">Table 8 - ₹2,450 - 8 mins ago</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">Room service completed</p>
                <p className="text-xs text-gray-500">Room 312 - 12 mins ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;