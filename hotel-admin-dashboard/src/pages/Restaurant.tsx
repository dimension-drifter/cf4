import React, { useState, useEffect } from 'react';
import { 
  UtensilsCrossed, 
  Search, 
  Filter, 
  Plus, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  DollarSign,
  Users,
  Utensils
} from 'lucide-react';
import { getRestaurantOrders, createOrder, updateOrderStatus } from '../services/api';

// Mock data for restaurant orders
const orders = [
  {
    id: 'ORD001',
    tableNumber: '8',
    customerName: 'Anjali Singh',
    roomNumber: null,
    items: [
      { id: '1', name: 'Butter Chicken', quantity: 2, price: 450, category: 'Main Course' },
      { id: '2', name: 'Naan Bread', quantity: 3, price: 80, category: 'Bread' },
      { id: '3', name: 'Lassi', quantity: 2, price: 120, category: 'Beverages' },
    ],
    totalAmount: 1130,
    status: 'preparing',
    orderType: 'dine-in',
    createdAt: '2024-10-10T18:30:00Z',
  },
  {
    id: 'ORD002',
    tableNumber: null,
    customerName: 'Vikram Patel',
    roomNumber: '205',
    items: [
      { id: '3', name: 'Biryani', quantity: 1, price: 380, category: 'Main Course' },
      { id: '4', name: 'Raita', quantity: 1, price: 60, category: 'Sides' },
    ],
    totalAmount: 440,
    status: 'ready',
    orderType: 'room-service',
    createdAt: '2024-10-10T19:15:00Z',
  },
  {
    id: 'ORD003',
    tableNumber: '12',
    customerName: 'Meera Joshi',
    roomNumber: null,
    items: [
      { id: '5', name: 'Paneer Tikka', quantity: 1, price: 320, category: 'Appetizers' },
      { id: '6', name: 'Dal Tadka', quantity: 1, price: 180, category: 'Main Course' },
      { id: '7', name: 'Roti', quantity: 4, price: 60, category: 'Bread' },
    ],
    totalAmount: 740,
    status: 'served',
    orderType: 'dine-in',
    createdAt: '2024-10-10T17:45:00Z',
  },
];

const getStatusColor = (status: string) => {
  const colors = {
    pending: 'bg-yellow-100 text-yellow-800',
    preparing: 'bg-blue-100 text-blue-800',
    ready: 'bg-green-100 text-green-800',
    served: 'bg-gray-100 text-gray-800',
    billed: 'bg-purple-100 text-purple-800',
  };
  return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'pending':
      return <AlertCircle className="w-4 h-4" />;
    case 'preparing':
      return <Clock className="w-4 h-4" />;
    case 'ready':
    case 'served':
      return <CheckCircle className="w-4 h-4" />;
    default:
      return <Clock className="w-4 h-4" />;
  }
};

const Restaurant: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [orderTypeFilter, setOrderTypeFilter] = useState('all');
  const [showNewOrderModal, setShowNewOrderModal] = useState(false);

  const handleStatusUpdate = async (orderId: string, newStatus: string) => {
    try {
      await updateOrderStatus(orderId, newStatus);
      // In a real app, you would refetch the orders or update the local state
      // For now, we'll just show a success message
      alert(`Order ${orderId} status updated to ${newStatus}`);
      
      // Update the local orders array (for demo purposes)
      const orderIndex = orders.findIndex(order => order.id === orderId);
      if (orderIndex !== -1) {
        orders[orderIndex].status = newStatus;
      }
      
      // Force re-render by updating a state
      setStatusFilter(statusFilter);
    } catch (error) {
      console.error('Failed to update order status:', error);
      alert('Failed to update order status. Please try again.');
    }
  };

  const filteredOrders = orders.filter(order => {
    const matchesSearch = order.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         order.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (order.tableNumber && order.tableNumber.includes(searchTerm)) ||
                         (order.roomNumber && order.roomNumber.includes(searchTerm));
    const matchesStatus = statusFilter === 'all' || order.status === statusFilter;
    const matchesType = orderTypeFilter === 'all' || order.orderType === orderTypeFilter;
    return matchesSearch && matchesStatus && matchesType;
  });

  const stats = {
    totalOrders: orders.length,
    preparing: orders.filter(o => o.status === 'preparing').length,
    ready: orders.filter(o => o.status === 'ready').length,
    revenue: orders.reduce((sum, o) => sum + o.totalAmount, 0),
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Restaurant Management</h1>
          <p className="text-gray-600">Manage restaurant orders and dining services</p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button 
            onClick={() => alert('Menu management feature coming soon!')}
            className="btn-secondary flex items-center space-x-2"
          >
            <Utensils className="w-4 h-4" />
            <span>Menu</span>
          </button>
          <button 
            onClick={() => setShowNewOrderModal(true)}
            className="btn-primary flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>New Order</span>
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Orders</p>
              <p className="text-3xl font-bold text-gray-900">{stats.totalOrders}</p>
            </div>
            <UtensilsCrossed className="w-8 h-8 text-blue-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Preparing</p>
              <p className="text-3xl font-bold text-blue-600">{stats.preparing}</p>
            </div>
            <Clock className="w-8 h-8 text-blue-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Ready to Serve</p>
              <p className="text-3xl font-bold text-green-600">{stats.ready}</p>
            </div>
            <CheckCircle className="w-8 h-8 text-green-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Today's Revenue</p>
              <p className="text-3xl font-bold text-purple-600">₹{stats.revenue.toLocaleString()}</p>
            </div>
            <DollarSign className="w-8 h-8 text-purple-600" />
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div className="flex flex-col sm:flex-row sm:items-center space-y-4 sm:space-y-0 sm:space-x-4">
            <div className="relative">
              <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search orders..."
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
                <option value="pending">Pending</option>
                <option value="preparing">Preparing</option>
                <option value="ready">Ready</option>
                <option value="served">Served</option>
              </select>
            </div>
            
            <select
              className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              value={orderTypeFilter}
              onChange={(e) => setOrderTypeFilter(e.target.value)}
            >
              <option value="all">All Types</option>
              <option value="dine-in">Dine-in</option>
              <option value="room-service">Room Service</option>
              <option value="takeaway">Takeaway</option>
            </select>
          </div>
        </div>
      </div>

      {/* Orders Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredOrders.map((order) => (
          <div key={order.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Order #{order.id}</h3>
                <p className="text-sm text-gray-600">
                  {order.orderType === 'room-service' ? `Room ${order.roomNumber}` : `Table ${order.tableNumber}`}
                </p>
              </div>
              <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
                {getStatusIcon(order.status)}
                <span className="capitalize">{order.status}</span>
              </div>
            </div>

            <div className="mb-4">
              <p className="font-medium text-gray-900">{order.customerName}</p>
              <p className="text-sm text-gray-500 capitalize">{order.orderType.replace('-', ' ')}</p>
              <p className="text-sm text-gray-500">
                {new Date(order.createdAt).toLocaleTimeString('en-IN', { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </p>
            </div>

            <div className="space-y-2 mb-4">
              {order.items.map((item) => (
                <div key={item.id} className="flex justify-between items-center text-sm">
                  <span className="text-gray-900">{item.quantity}x {item.name}</span>
                  <span className="text-gray-600">₹{(item.price * item.quantity).toLocaleString()}</span>
                </div>
              ))}
            </div>

            <div className="border-t pt-4">
              <div className="flex justify-between items-center mb-3">
                <span className="font-semibold text-gray-900">Total</span>
                <span className="font-bold text-lg text-gray-900">₹{order.totalAmount.toLocaleString()}</span>
              </div>
              
              <div className="flex space-x-2">
                {order.status === 'preparing' && (
                  <button 
                    onClick={() => handleStatusUpdate(order.id, 'ready')}
                    className="flex-1 bg-green-600 text-white py-2 px-3 rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
                  >
                    Mark Ready
                  </button>
                )}
                {order.status === 'ready' && (
                  <button 
                    onClick={() => handleStatusUpdate(order.id, 'served')}
                    className="flex-1 bg-blue-600 text-white py-2 px-3 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                  >
                    Mark Served
                  </button>
                )}
                {order.status === 'served' && (
                  <button 
                    onClick={() => alert('Bill generated for order ' + order.id)}
                    className="flex-1 bg-purple-600 text-white py-2 px-3 rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium"
                  >
                    Generate Bill
                  </button>
                )}
                <button className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium">
                  View
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* New Order Modal */}
      {showNewOrderModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">New Order</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Order Type</label>
                  <select className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                    <option>Dine-in</option>
                    <option>Room Service</option>
                    <option>Takeaway</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Customer Name</label>
                  <input
                    type="text"
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter customer name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Table/Room Number</label>
                  <input
                    type="text"
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter table or room number"
                  />
                </div>
              </div>
              <div className="flex items-center justify-end space-x-3 mt-6">
                <button
                  onClick={() => setShowNewOrderModal(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
                <button className="btn-primary">
                  Create Order
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Restaurant;