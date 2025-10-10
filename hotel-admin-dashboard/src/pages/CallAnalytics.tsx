import React, { useState } from 'react';
import { 
  Phone, 
  TrendingUp, 
  Clock, 
  MessageSquare, 
  Calendar,
  BarChart3,
  Users,
  Star,
  Filter,
  Download
} from 'lucide-react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

// Mock data for call analytics
const callVolumeData = [
  { name: '00:00', calls: 2 }, { name: '01:00', calls: 1 }, { name: '02:00', calls: 0 }, { name: '03:00', calls: 1 },
  { name: '04:00', calls: 0 }, { name: '05:00', calls: 2 }, { name: '06:00', calls: 5 }, { name: '07:00', calls: 8 },
  { name: '08:00', calls: 12 }, { name: '09:00', calls: 18 }, { name: '10:00', calls: 25 }, { name: '11:00', calls: 22 },
  { name: '12:00', calls: 28 }, { name: '13:00', calls: 24 }, { name: '14:00', calls: 30 }, { name: '15:00', calls: 26 },
  { name: '16:00', calls: 32 }, { name: '17:00', calls: 29 }, { name: '18:00', calls: 35 }, { name: '19:00', calls: 31 },
  { name: '20:00', calls: 27 }, { name: '21:00', calls: 20 }, { name: '22:00', calls: 15 }, { name: '23:00', calls: 8 },
];

const sentimentTrendData = [
  { name: 'Mon', positive: 85, neutral: 12, negative: 3 },
  { name: 'Tue', positive: 78, neutral: 18, negative: 4 },
  { name: 'Wed', positive: 92, neutral: 6, negative: 2 },
  { name: 'Thu', positive: 88, neutral: 10, negative: 2 },
  { name: 'Fri', positive: 90, neutral: 8, negative: 2 },
  { name: 'Sat', positive: 82, neutral: 15, negative: 3 },
  { name: 'Sun', positive: 86, neutral: 11, negative: 3 },
];

const conversionData = [
  { name: 'Booking Inquiry', calls: 145, conversions: 89, rate: 61 },
  { name: 'Room Service', calls: 67, conversions: 67, rate: 100 },
  { name: 'Restaurant', calls: 34, conversions: 32, rate: 94 },
  { name: 'Complaint', calls: 12, conversions: 11, rate: 92 },
  { name: 'General Info', calls: 89, conversions: 23, rate: 26 },
];

const recentCalls = [
  {
    id: '1',
    callerNumber: '+91 98765 43210',
    callerName: 'Rahul Sharma',
    intent: 'Booking Inquiry',
    sentiment: 'positive',
    duration: 245,
    startTime: '2024-10-10T18:30:00Z',
    outcome: 'booking_made',
    transcript: 'Customer inquired about availability for weekend stay...'
  },
  {
    id: '2',
    callerNumber: '+91 98765 43211',
    callerName: 'Priya Singh',
    intent: 'Room Service',
    sentiment: 'neutral',
    duration: 120,
    startTime: '2024-10-10T18:15:00Z',
    outcome: 'completed',
    transcript: 'Requested extra towels and room cleaning...'
  },
  {
    id: '3',
    callerNumber: '+91 98765 43212',
    callerName: 'Vikash Patel',
    intent: 'Complaint',
    sentiment: 'negative',
    duration: 380,
    startTime: '2024-10-10T17:45:00Z',
    outcome: 'resolved',
    transcript: 'Complained about noisy neighbors...'
  },
];

const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
};

const getSentimentColor = (sentiment: string) => {
  const colors = {
    positive: 'bg-green-100 text-green-800',
    neutral: 'bg-gray-100 text-gray-800',
    negative: 'bg-red-100 text-red-800',
  };
  return colors[sentiment as keyof typeof colors] || 'bg-gray-100 text-gray-800';
};

const CallAnalytics: React.FC = () => {
  const [timeFilter, setTimeFilter] = useState('today');
  const [selectedMetric, setSelectedMetric] = useState('volume');

  const stats = {
    totalCalls: 347,
    avgDuration: '3:45',
    conversionRate: 68,
    customerSatisfaction: 4.2,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Call Analytics</h1>
          <p className="text-gray-600">Monitor call performance and customer interactions</p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <select
            className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={timeFilter}
            onChange={(e) => setTimeFilter(e.target.value)}
          >
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="quarter">This Quarter</option>
          </select>
          <button 
            onClick={() => alert('Analytics report exported successfully!')}
            className="btn-secondary flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export Report</span>
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Calls</p>
              <p className="text-3xl font-bold text-gray-900">{stats.totalCalls}</p>
              <p className="text-sm text-green-600">+12% from yesterday</p>
            </div>
            <Phone className="w-8 h-8 text-blue-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg Duration</p>
              <p className="text-3xl font-bold text-gray-900">{stats.avgDuration}</p>
              <p className="text-sm text-green-600">-8% from yesterday</p>
            </div>
            <Clock className="w-8 h-8 text-green-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Conversion Rate</p>
              <p className="text-3xl font-bold text-gray-900">{stats.conversionRate}%</p>
              <p className="text-sm text-green-600">+5% from yesterday</p>
            </div>
            <TrendingUp className="w-8 h-8 text-purple-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Satisfaction</p>
              <p className="text-3xl font-bold text-gray-900">{stats.customerSatisfaction}</p>
              <div className="flex items-center">
                <Star className="w-4 h-4 text-yellow-400 fill-current" />
                <span className="text-sm text-gray-600 ml-1">out of 5</span>
              </div>
            </div>
            <Users className="w-8 h-8 text-orange-600" />
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Call Volume Chart */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Call Volume (24h)</h3>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Calls per hour</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={callVolumeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey="calls" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Sentiment Trend */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Sentiment Trend</h3>
            <div className="flex items-center space-x-4 text-sm">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span>Positive</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-gray-400 rounded-full"></div>
                <span>Neutral</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <span>Negative</span>
              </div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={sentimentTrendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="positive" stroke="#10B981" strokeWidth={2} />
              <Line type="monotone" dataKey="neutral" stroke="#6B7280" strokeWidth={2} />
              <Line type="monotone" dataKey="negative" stroke="#EF4444" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Conversion Analysis */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Conversion Analysis by Intent</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={conversionData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="calls" fill="#E5E7EB" name="Total Calls" />
            <Bar dataKey="conversions" fill="#3B82F6" name="Conversions" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Calls */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Recent Calls</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Caller
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Intent
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Sentiment
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Duration
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Outcome
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {recentCalls.map((call) => (
                <tr key={call.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{call.callerName}</div>
                      <div className="text-sm text-gray-500">{call.callerNumber}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                      {call.intent}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSentimentColor(call.sentiment)}`}>
                      {call.sentiment}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatDuration(call.duration)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                      {call.outcome.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button 
                      onClick={() => alert('View transcript for call ' + call.id)}
                      className="text-blue-600 hover:text-blue-800 mr-3"
                      title="View Transcript"
                    >
                      <MessageSquare className="w-4 h-4" />
                    </button>
                    <button 
                      onClick={() => alert('View detailed analytics for call ' + call.id)}
                      className="text-gray-600 hover:text-gray-800"
                      title="View Analytics"
                    >
                      <BarChart3 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default CallAnalytics;