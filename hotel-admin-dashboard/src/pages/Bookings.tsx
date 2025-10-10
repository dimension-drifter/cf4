import React, { useState, useEffect } from 'react';
import { 
  Calendar, 
  Search, 
  Filter, 
  Plus, 
  Edit3, 
  Trash2, 
  Eye,
  Download,
  UserCheck,
  Clock,
  DollarSign 
} from 'lucide-react';
import { getBookings, createBooking, updateBooking, deleteBooking } from '../services/api';

// Mock data
const bookings = [
  {
    id: 'BK001',
    guestName: 'Rajesh Sharma',
    email: 'rajesh@example.com',
    phone: '+91 9876543210',
    checkIn: '2024-10-12',
    checkOut: '2024-10-15',
    roomType: 'Deluxe Suite',
    roomNumber: '205',
    guests: 2,
    totalAmount: 15000,
    status: 'confirmed',
    paymentStatus: 'paid',
    createdAt: '2024-10-10T10:30:00Z',
  },
  {
    id: 'BK002',
    guestName: 'Priya Patel',
    email: 'priya@example.com',
    phone: '+91 9876543211',
    checkIn: '2024-10-13',
    checkOut: '2024-10-16',
    roomType: 'Standard Room',
    roomNumber: '108',
    guests: 1,
    totalAmount: 9000,
    status: 'pending',
    paymentStatus: 'pending',
    createdAt: '2024-10-10T14:20:00Z',
  },
  {
    id: 'BK003',
    guestName: 'Amit Kumar',
    email: 'amit@example.com',
    phone: '+91 9876543212',
    checkIn: '2024-10-11',
    checkOut: '2024-10-14',
    roomType: 'Premium Suite',
    roomNumber: '301',
    guests: 3,
    totalAmount: 22500,
    status: 'completed',
    paymentStatus: 'paid',
    createdAt: '2024-10-09T16:45:00Z',
  },
];

const getStatusBadge = (status: string) => {
  const colors = {
    confirmed: 'bg-green-100 text-green-800',
    pending: 'bg-yellow-100 text-yellow-800',
    cancelled: 'bg-red-100 text-red-800',
    completed: 'bg-blue-100 text-blue-800',
  };
  return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
};

const getPaymentBadge = (status: string) => {
  const colors = {
    paid: 'bg-green-100 text-green-800',
    pending: 'bg-yellow-100 text-yellow-800',
    failed: 'bg-red-100 text-red-800',
  };
  return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
};

const Bookings: React.FC = () => {
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [showNewBookingModal, setShowNewBookingModal] = useState(false);
  const [newBookingForm, setNewBookingForm] = useState({
    guestName: '',
    email: '',
    phone: '',
    checkIn: '',
    checkOut: '',
    roomType: 'Standard Room',
    guests: 1,
    totalAmount: 0
  });

  // Fetch bookings from backend
  useEffect(() => {
    const fetchBookings = async () => {
      try {
        setLoading(true);
        const data = await getBookings();
        setBookings(data);
      } catch (error) {
        console.error('Failed to fetch bookings:', error);
        // Use mock data as fallback
        setBookings([
          {
            id: 'BK001',
            guestName: 'Rajesh Sharma',
            email: 'rajesh@example.com',
            phone: '+91 9876543210',
            checkIn: '2024-10-12',
            checkOut: '2024-10-15',
            roomType: 'Deluxe Suite',
            roomNumber: '205',
            guests: 2,
            totalAmount: 15000,
            status: 'confirmed',
            paymentStatus: 'paid',
            createdAt: '2024-10-10T10:30:00Z',
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchBookings();
  }, []);

  // Handle booking creation
  const handleCreateBooking = async () => {
    try {
      if (!newBookingForm.guestName || !newBookingForm.email || !newBookingForm.checkIn || !newBookingForm.checkOut) {
        alert('Please fill in all required fields');
        return;
      }

      const newBooking = {
        ...newBookingForm,
        id: `BK${Date.now()}`,
        roomNumber: `${Math.floor(Math.random() * 300) + 100}`,
        status: 'pending',
        paymentStatus: 'pending',
        createdAt: new Date().toISOString(),
        totalAmount: calculateBookingAmount(newBookingForm.roomType, newBookingForm.checkIn, newBookingForm.checkOut)
      };

      // Try to create via API
      try {
        const createdBooking = await createBooking(newBooking);
        setBookings(prev => [createdBooking, ...prev]);
      } catch (apiError) {
        // Fallback to local state if API fails
        setBookings(prev => [newBooking, ...prev]);
      }

      // Reset form and close modal
      setNewBookingForm({
        guestName: '',
        email: '',
        phone: '',
        checkIn: '',
        checkOut: '',
        roomType: 'Standard Room',
        guests: 1,
        totalAmount: 0
      });
      setShowNewBookingModal(false);
      alert('Booking created successfully!');
    } catch (error) {
      console.error('Failed to create booking:', error);
      alert('Failed to create booking. Please try again.');
    }
  };

  // Calculate booking amount based on room type and duration
  const calculateBookingAmount = (roomType: string, checkIn: string, checkOut: string) => {
    const rates = {
      'Standard Room': 3000,
      'Deluxe Suite': 5000,
      'Premium Suite': 8000,
      'Presidential Suite': 12000
    };
    
    const days = Math.ceil((new Date(checkOut).getTime() - new Date(checkIn).getTime()) / (1000 * 60 * 60 * 24));
    return (rates[roomType as keyof typeof rates] || 3000) * Math.max(1, days);
  };

  const filteredBookings = bookings.filter(booking => {
    const matchesSearch = booking.guestName?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         booking.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         booking.roomNumber?.includes(searchTerm);
    const matchesStatus = statusFilter === 'all' || booking.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const stats = {
    total: bookings.length,
    confirmed: bookings.filter(b => b.status === 'confirmed').length,
    pending: bookings.filter(b => b.status === 'pending').length,
    revenue: bookings.reduce((sum, b) => sum + b.totalAmount, 0),
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="loading-shimmer w-full h-32 rounded-lg"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Bookings Management</h1>
          <p className="text-gray-600">Manage hotel reservations and guest information</p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button className="btn-secondary flex items-center space-x-2">
            <Download className="w-4 h-4" />
            <span>Export</span>
          </button>
          <button 
            onClick={() => setShowNewBookingModal(true)}
            className="btn-primary flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>New Booking</span>
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Bookings</p>
              <p className="text-3xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <Calendar className="w-8 h-8 text-blue-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Confirmed</p>
              <p className="text-3xl font-bold text-green-600">{stats.confirmed}</p>
            </div>
            <UserCheck className="w-8 h-8 text-green-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pending</p>
              <p className="text-3xl font-bold text-yellow-600">{stats.pending}</p>
            </div>
            <Clock className="w-8 h-8 text-yellow-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Revenue</p>
              <p className="text-3xl font-bold text-purple-600">₹{stats.revenue.toLocaleString()}</p>
            </div>
            <DollarSign className="w-8 h-8 text-purple-600" />
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search by guest name, email, or room..."
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            
            <div className="flex items-center space-x-2">
              <Filter className="w-5 h-5 text-gray-400" />
              <select
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="all">All Status</option>
                <option value="confirmed">Confirmed</option>
                <option value="pending">Pending</option>
                <option value="cancelled">Cancelled</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Bookings Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Guest Details
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Booking Info
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Room Details
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredBookings.map((booking) => (
                <tr key={booking.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{booking.guestName}</div>
                      <div className="text-sm text-gray-500">{booking.email}</div>
                      <div className="text-sm text-gray-500">{booking.phone}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">ID: {booking.id}</div>
                      <div className="text-sm text-gray-500">
                        {new Date(booking.checkIn).toLocaleDateString()} - {new Date(booking.checkOut).toLocaleDateString()}
                      </div>
                      <div className="text-sm text-gray-500">{booking.guests} Guest(s)</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">Room {booking.roomNumber}</div>
                      <div className="text-sm text-gray-500">{booking.roomType}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">₹{booking.totalAmount.toLocaleString()}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="space-y-1">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusBadge(booking.status)}`}>
                        {booking.status}
                      </span>
                      <br />
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getPaymentBadge(booking.paymentStatus)}`}>
                        {booking.paymentStatus}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex items-center space-x-2">
                      <button className="text-blue-600 hover:text-blue-800">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="text-green-600 hover:text-green-800">
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button className="text-red-600 hover:text-red-800">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* New Booking Modal */}
      {showNewBookingModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">New Booking</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Guest Name</label>
                  <input
                    type="text"
                    value={newBookingForm.guestName}
                    onChange={(e) => setNewBookingForm(prev => ({ ...prev, guestName: e.target.value }))}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter guest name"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    type="email"
                    value={newBookingForm.email}
                    onChange={(e) => setNewBookingForm(prev => ({ ...prev, email: e.target.value }))}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter email"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Phone</label>
                  <input
                    type="tel"
                    value={newBookingForm.phone}
                    onChange={(e) => setNewBookingForm(prev => ({ ...prev, phone: e.target.value }))}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter phone number"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Check-in</label>
                    <input
                      type="date"
                      value={newBookingForm.checkIn}
                      onChange={(e) => setNewBookingForm(prev => ({ ...prev, checkIn: e.target.value }))}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Check-out</label>
                    <input
                      type="date"
                      value={newBookingForm.checkOut}
                      onChange={(e) => setNewBookingForm(prev => ({ ...prev, checkOut: e.target.value }))}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Room Type</label>
                  <select 
                    value={newBookingForm.roomType}
                    onChange={(e) => setNewBookingForm(prev => ({ ...prev, roomType: e.target.value }))}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option>Standard Room</option>
                    <option>Deluxe Suite</option>
                    <option>Premium Suite</option>
                    <option>Presidential Suite</option>
                  </select>
                </div>
              </div>
              <div className="flex items-center justify-end space-x-3 mt-6">
                <button
                  onClick={() => setShowNewBookingModal(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button 
                  type="button"
                  onClick={handleCreateBooking}
                  className="btn-primary"
                >
                  Create Booking
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Bookings;