import React, { useState, useEffect } from 'react';
import { 
  Phone, 
  Clock, 
  User, 
  PhoneCall, 
  PhoneIncoming,
  PhoneOff,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  MessageSquare,
  Users,
  Activity
} from 'lucide-react';

// Mock data for live calls
const initialLiveCalls = [
  {
    id: 'live-1',
    callerNumber: '+91 98765 43210',
    callerName: 'Rajesh Kumar',
    intent: 'Booking Inquiry',
    sentiment: 'positive',
    duration: 125,
    startTime: new Date(Date.now() - 125000).toISOString(),
    status: 'active',
  },
  {
    id: 'live-2',
    callerNumber: '+91 98765 43211',
    callerName: 'Priya Sharma',
    intent: 'Room Service',
    sentiment: 'neutral',
    duration: 87,
    startTime: new Date(Date.now() - 87000).toISOString(),
    status: 'active',
  },
  {
    id: 'live-3',
    callerNumber: '+91 98765 43212',
    callerName: 'Waiting...',
    intent: 'Unknown',
    sentiment: 'neutral',
    duration: 23,
    startTime: new Date(Date.now() - 23000).toISOString(),
    status: 'on_hold',
  },
];

const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
};

const getSentimentColor = (sentiment: string) => {
  const colors = {
    positive: 'bg-green-100 text-green-800 border-green-200',
    neutral: 'bg-gray-100 text-gray-800 border-gray-200',
    negative: 'bg-red-100 text-red-800 border-red-200',
  };
  return colors[sentiment as keyof typeof colors] || 'bg-gray-100 text-gray-800 border-gray-200';
};

const getStatusColor = (status: string) => {
  const colors = {
    active: 'bg-green-500',
    on_hold: 'bg-yellow-500',
    transferring: 'bg-blue-500',
  };
  return colors[status as keyof typeof colors] || 'bg-gray-500';
};

const LiveCalls: React.FC = () => {
  const [liveCalls, setLiveCalls] = useState(initialLiveCalls);
  const [selectedCall, setSelectedCall] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [isMuted, setIsMuted] = useState(false);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setLiveCalls(prev => 
        prev.map(call => ({
          ...call,
          duration: call.duration + 1,
        }))
      );
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  // Simulate random call events
  useEffect(() => {
    const eventInterval = setInterval(() => {
      if (Math.random() > 0.8) {
        // Simulate new call
        const newCall = {
          id: `live-${Date.now()}`,
          callerNumber: `+91 ${Math.floor(Math.random() * 10000000000)}`,
          callerName: 'Incoming Call...',
          intent: 'Unknown',
          sentiment: 'neutral' as const,
          duration: 0,
          startTime: new Date().toISOString(),
          status: 'on_hold' as const,
        };
        
        setLiveCalls(prev => [...prev, newCall]);
        
        // Remove the call after some time (simulate call end)
        setTimeout(() => {
          setLiveCalls(prev => prev.filter(call => call.id !== newCall.id));
        }, Math.random() * 30000 + 10000);
      }
    }, 10000);

    return () => clearInterval(eventInterval);
  }, []);

  const stats = {
    activeCalls: liveCalls.filter(call => call.status === 'active').length,
    waitingCalls: liveCalls.filter(call => call.status === 'on_hold').length,
    totalAgents: 5,
    availableAgents: 2,
  };

  const handleCallAction = (callId: string, action: string) => {
    setLiveCalls(prev => 
      prev.map(call => 
        call.id === callId 
          ? { ...call, status: action === 'answer' ? 'active' : 'on_hold' }
          : call
      )
    );
  };

  const endCall = (callId: string) => {
    setLiveCalls(prev => prev.filter(call => call.id !== callId));
    if (selectedCall === callId) {
      setSelectedCall(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Live Calls</h1>
          <p className="text-gray-600">Monitor and manage active voice calls in real-time</p>
        </div>
        <div className="mt-4 sm:mt-0 flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600">Live Monitoring</span>
          </div>
        </div>
      </div>

      {/* Live Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Calls</p>
              <p className="text-3xl font-bold text-green-600">{stats.activeCalls}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-full">
              <PhoneCall className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Waiting Calls</p>
              <p className="text-3xl font-bold text-yellow-600">{stats.waitingCalls}</p>
            </div>
            <div className="p-3 bg-yellow-100 rounded-full">
              <Clock className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Agents</p>
              <p className="text-3xl font-bold text-blue-600">{stats.totalAgents}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <Users className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Available Agents</p>
              <p className="text-3xl font-bold text-purple-600">{stats.availableAgents}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-full">
              <User className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Live Calls Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {liveCalls.map((call) => (
          <div 
            key={call.id} 
            className={`bg-white rounded-lg shadow-sm border-2 p-6 cursor-pointer transition-all duration-200 hover:shadow-md ${
              selectedCall === call.id ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-200'
            }`}
            onClick={() => setSelectedCall(call.id)}
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${getStatusColor(call.status)} animate-pulse`}></div>
                <span className="text-sm font-medium text-gray-600 capitalize">
                  {call.status.replace('_', ' ')}
                </span>
              </div>
              <div className="text-lg font-bold text-gray-900">
                {formatDuration(call.duration)}
              </div>
            </div>

            <div className="mb-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-1">{call.callerName}</h3>
              <p className="text-sm text-gray-600">{call.callerNumber}</p>
            </div>

            <div className="flex items-center justify-between mb-4">
              <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                {call.intent}
              </span>
              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSentimentColor(call.sentiment)}`}>
                {call.sentiment}
              </span>
            </div>

            <div className="flex space-x-2">
              {call.status === 'on_hold' && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleCallAction(call.id, 'answer');
                  }}
                  className="flex-1 bg-green-600 text-white py-2 px-3 rounded-lg hover:bg-green-700 transition-colors text-sm font-medium flex items-center justify-center space-x-1"
                >
                  <PhoneIncoming className="w-4 h-4" />
                  <span>Answer</span>
                </button>
              )}
              
              {call.status === 'active' && (
                <>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setIsListening(!isListening);
                    }}
                    className={`flex-1 py-2 px-3 rounded-lg transition-colors text-sm font-medium flex items-center justify-center space-x-1 ${
                      isListening 
                        ? 'bg-blue-600 text-white hover:bg-blue-700' 
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {isListening ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
                    <span>Listen</span>
                  </button>
                  
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setIsMuted(!isMuted);
                    }}
                    className={`py-2 px-3 rounded-lg transition-colors text-sm font-medium flex items-center justify-center ${
                      isMuted 
                        ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {isMuted ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                  </button>
                </>
              )}
              
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  endCall(call.id);
                }}
                className="py-2 px-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium flex items-center justify-center"
              >
                <PhoneOff className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Call Details Panel */}
      {selectedCall && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Call Details</h3>
            <button
              onClick={() => setSelectedCall(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>
          
          {(() => {
            const call = liveCalls.find(c => c.id === selectedCall);
            if (!call) return null;
            
            return (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Call Information</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Caller:</span>
                      <span className="font-medium">{call.callerName}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Number:</span>
                      <span className="font-medium">{call.callerNumber}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Duration:</span>
                      <span className="font-medium">{formatDuration(call.duration)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Status:</span>
                      <span className="font-medium capitalize">{call.status.replace('_', ' ')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Intent:</span>
                      <span className="font-medium">{call.intent}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Sentiment:</span>
                      <span className={`font-medium ${
                        call.sentiment === 'positive' ? 'text-green-600' :
                        call.sentiment === 'negative' ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        {call.sentiment}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Live Transcript</h4>
                  <div className="bg-gray-50 rounded-lg p-4 h-32 overflow-y-auto text-sm">
                    <div className="space-y-2">
                      <div className="text-blue-600 font-medium">Customer:</div>
                      <div className="text-gray-700 mb-2">
                        Hello, I would like to make a reservation for this weekend...
                      </div>
                      <div className="text-green-600 font-medium">Agent:</div>
                      <div className="text-gray-700">
                        Of course! I'd be happy to help you with a reservation. What dates were you looking for?
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-4 flex space-x-2">
                    <button 
                      onClick={() => alert('Full transcript for call ' + selectedCall)}
                      className="btn-secondary flex items-center space-x-2"
                    >
                      <MessageSquare className="w-4 h-4" />
                      <span>Full Transcript</span>
                    </button>
                    <button 
                      onClick={() => alert('Call analytics for call ' + selectedCall)}
                      className="btn-secondary flex items-center space-x-2"
                    >
                      <Activity className="w-4 h-4" />
                      <span>Call Analytics</span>
                    </button>
                  </div>
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* No Active Calls */}
      {liveCalls.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <Phone className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Active Calls</h3>
          <p className="text-gray-600">All agents are currently available. Calls will appear here when they come in.</p>
        </div>
      )}
    </div>
  );
};

export default LiveCalls;