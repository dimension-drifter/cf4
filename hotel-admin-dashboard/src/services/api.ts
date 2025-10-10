import api from '../lib/api';
import { DashboardStats, Booking, CallLog, LiveCall, RestaurantOrder } from '../types';

// Dashboard API
export const getDashboardStats = async (): Promise<DashboardStats> => {
  try {
    const response = await api.get('/api/dashboard/stats');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error);
    // Mock data as fallback
    return {
      totalBookings: 347,
      todaysBookings: 23,
      revenue: 567000,
      occupancyRate: 87,
      totalCalls: 89,
      todaysCalls: 12,
      averageCallDuration: 225,
      conversionRate: 68,
      activeRooms: 44,
      totalRooms: 50,
      restaurantOrders: 34,
      pendingOrders: 8,
    };
  }
};

// Bookings API
export const getBookings = async (): Promise<Booking[]> => {
  try {
    const response = await api.get('/api/bookings');
    return response.data;
  } catch (error) {
    // Mock data for demo
    return [];
  }
};

export const createBooking = async (booking: Partial<Booking>): Promise<Booking> => {
  try {
    const response = await api.post('/api/bookings', booking);
    return response.data;
  } catch (error) {
    throw new Error('Failed to create booking');
  }
};

export const updateBooking = async (id: string, booking: Partial<Booking>): Promise<Booking> => {
  try {
    const response = await api.put(`/api/bookings/${id}`, booking);
    return response.data;
  } catch (error) {
    throw new Error('Failed to update booking');
  }
};

export const deleteBooking = async (id: string): Promise<void> => {
  try {
    await api.delete(`/api/bookings/${id}`);
  } catch (error) {
    throw new Error('Failed to delete booking');
  }
};

// Restaurant API
export const getRestaurantOrders = async (): Promise<RestaurantOrder[]> => {
  try {
    const response = await api.get('/api/restaurant/orders');
    return response.data;
  } catch (error) {
    return [];
  }
};

export const createOrder = async (order: Partial<RestaurantOrder>): Promise<RestaurantOrder> => {
  try {
    const response = await api.post('/api/restaurant/orders', order);
    return response.data;
  } catch (error) {
    throw new Error('Failed to create order');
  }
};

export const updateOrderStatus = async (id: string, status: string): Promise<RestaurantOrder> => {
  try {
    const response = await api.patch(`/api/restaurant/orders/${id}/status`, { status });
    return response.data;
  } catch (error) {
    throw new Error('Failed to update order status');
  }
};

// Call Analytics API
export const getCallLogs = async (filters?: {
  startDate?: string;
  endDate?: string;
  sentiment?: string;
  intent?: string;
}): Promise<CallLog[]> => {
  try {
    const response = await api.get('/api/calls/logs', { params: filters });
    return response.data;
  } catch (error) {
    return [];
  }
};

export const getCallAnalytics = async (timeframe: string = 'today') => {
  try {
    const response = await api.get(`/api/calls/analytics/${timeframe}`);
    return response.data;
  } catch (error) {
    return null;
  }
};

// Live Calls API
export const getLiveCalls = async (): Promise<LiveCall[]> => {
  try {
    const response = await api.get('/api/calls/live');
    return response.data;
  } catch (error) {
    return [];
  }
};

export const answerCall = async (callId: string): Promise<void> => {
  try {
    await api.post(`/api/calls/${callId}/answer`);
  } catch (error) {
    throw new Error('Failed to answer call');
  }
};

export const endCall = async (callId: string): Promise<void> => {
  try {
    await api.post(`/api/calls/${callId}/end`);
  } catch (error) {
    throw new Error('Failed to end call');
  }
};

export const holdCall = async (callId: string): Promise<void> => {
  try {
    await api.post(`/api/calls/${callId}/hold`);
  } catch (error) {
    throw new Error('Failed to hold call');
  }
};

// LiveKit Integration
export const createToken = async (userName: string): Promise<{token: string, livekit_url: string}> => {
  try {
    const response = await api.post('/create_token', { name: userName });
    return response.data;
  } catch (error) {
    throw new Error('Failed to create LiveKit token');
  }
};