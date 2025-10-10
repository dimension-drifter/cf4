import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import Bookings from './pages/Bookings';
import Restaurant from './pages/Restaurant';
import CallAnalytics from './pages/CallAnalytics';
import LiveCalls from './pages/LiveCalls';
import Settings from './pages/Settings';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App">
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/bookings" element={<Bookings />} />
              <Route path="/restaurant" element={<Restaurant />} />
              <Route path="/analytics" element={<CallAnalytics />} />
              <Route path="/live-calls" element={<LiveCalls />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Layout>
          <Toaster richColors position="top-right" />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;