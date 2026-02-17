import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AgentCard from './components/AgentCard';
import VaultPanel from './components/VaultPanel';
import ActivityFeed from './components/ActivityFeed';
import MetricsChart from './components/MetricsChart';

function App() {
  const [agents, setAgents] = useState([]);
  const [vaults, setVaults] = useState([]);
  const [activityFeed, setActivityFeed] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initial data fetch
    fetchAllData();

    // Set up SSE for real-time updates
    const eventSource = new EventSource('/api/events');

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'status') {
        setAgents(data.data);
      } else if (data.type === 'vaults') {
        setVaults(data.data);
      }
    };

    // Periodic refresh of non-SSE data
    const interval = setInterval(() => {
      fetchActivityFeed();
      fetchMetrics();
    }, 30000);

    return () => {
      eventSource.close();
      clearInterval(interval);
    };
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);

      const [statusRes, vaultsRes, activityRes, metricsRes] = await Promise.all([
        axios.get('/api/status'),
        axios.get('/api/vaults'),
        axios.get('/api/activity?limit=10'),
        axios.get('/api/metrics'),
      ]);

      setAgents(statusRes.data.agents);
      setVaults(vaultsRes.data);
      setActivityFeed(activityRes.data);
      setMetrics(metricsRes.data);

      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const fetchActivityFeed = async () => {
    try {
      const response = await axios.get('/api/activity?limit=10');
      setActivityFeed(response.data);
    } catch (error) {
      console.error('Error fetching activity feed:', error);
    }
  };

  const fetchMetrics = async () => {
    try {
      const response = await axios.get('/api/metrics');
      setMetrics(response.data);
    } catch (error) {
      console.error('Error fetching metrics:', error);
    }
  };

  const handleRefresh = () => {
    fetchAllData();
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">Squad Dashboard</h1>
            <p className="text-gray-400 text-sm">Real-time monitoring</p>
          </div>
          <div className="flex items-center gap-4">
            <span className={`px-3 py-1 rounded-full text-sm ${loading ? 'text-yellow-400' : 'text-green-400'}`}>
              {loading ? 'Loading...' : 'Connected'}
            </span>
            <button
              onClick={handleRefresh}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm"
            >
              Refresh
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-6">
        {/* Agent Status Grid */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Agent Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {agents.map((agent) => (
              <AgentCard key={agent.agentId} agent={agent} />
            ))}
          </div>
        </section>

        {/* Two-column layout for vaults and metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Vault Panel */}
          <section>
            <h2 className="text-xl font-semibold mb-4">Obsidian Vaults</h2>
            <VaultPanel vaults={vaults} />
          </section>

          {/* Metrics Panel */}
          <section>
            <h2 className="text-xl font-semibold mb-4">Health Metrics</h2>
            <MetricsChart metrics={metrics} />
          </section>
        </div>

        {/* Activity Feed */}
        <section>
          <h2 className="text-xl font-semibold mb-4">Activity Feed</h2>
          <ActivityFeed feed={activityFeed} formatTime={formatTime} />
        </section>
      </main>
    </div>
  );
}

export default App;
