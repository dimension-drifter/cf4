export interface Booking {
  id: string;
  guestName: string;
  email: string;
  phone: string;
  checkIn: string;
  checkOut: string;
  roomType: string;
  roomNumber: string;
  guests: number;
  totalAmount: number;
  status: 'confirmed' | 'pending' | 'cancelled' | 'completed';
  paymentStatus: 'paid' | 'pending' | 'failed';
  createdAt: string;
  updatedAt: string;
}

export interface Room {
  id: string;
  number: string;
  type: string;
  capacity: number;
  pricePerNight: number;
  status: 'available' | 'occupied' | 'maintenance' | 'cleaning';
  amenities: string[];
  floor: number;
}

export interface RestaurantOrder {
  id: string;
  tableNumber: string;
  customerName?: string;
  roomNumber?: string;
  items: OrderItem[];
  totalAmount: number;
  status: 'pending' | 'preparing' | 'ready' | 'served' | 'billed';
  orderType: 'dine-in' | 'room-service' | 'takeaway';
  createdAt: string;
  updatedAt: string;
}

export interface OrderItem {
  id: string;
  name: string;
  quantity: number;
  price: number;
  category: string;
  notes?: string;
}

export interface CallLog {
  id: string;
  callerNumber: string;
  callerName?: string;
  intent: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  duration: number;
  startTime: string;
  endTime: string;
  outcome: 'booking_made' | 'inquiry' | 'complaint' | 'cancelled' | 'no_action';
  roomId?: string;
  bookingId?: string;
  transcript?: string;
}

export interface LiveCall {
  id: string;
  callerNumber: string;
  callerName?: string;
  intent: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  duration: number;
  startTime: string;
  status: 'active' | 'on_hold' | 'transferring';
}

export interface DashboardStats {
  totalBookings: number;
  todaysBookings: number;
  revenue: number;
  occupancyRate: number;
  totalCalls: number;
  todaysCalls: number;
  averageCallDuration: number;
  conversionRate: number;
  activeRooms: number;
  totalRooms: number;
  restaurantOrders: number;
  pendingOrders: number;
}

export interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  available: boolean;
  preparationTime: number;
  image?: string;
}

export interface Table {
  id: string;
  number: string;
  capacity: number;
  status: 'available' | 'occupied' | 'reserved' | 'cleaning';
  currentOrder?: string;
}