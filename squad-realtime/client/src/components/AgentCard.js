import React from 'react';

function AgentCard({ agent }) {
  const getStatusColor = (status) => {
    return status === 'online' ? 'text-green-400' : 'text-red-400';
  };

  const getStatusBg = (status) => {
    return status === 'online' ? 'bg-green-900' : 'bg-red-900';
  };

  return (
    <div className={`bg-gray-800 rounded-lg p-4 border border-gray-700 ${getStatusBg(agent.status)}`}>
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold">{agent.agentId.charAt(0).toUpperCase() + agent.agentId.slice(1)}</h3>
        <span className={`text-xs px-2 py-1 rounded ${getStatusColor(agent.status)}`}>
          {agent.status.toUpperCase()}
        </span>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Response Time:</span>
          <span className={agent.responseTime > 1000 ? 'text-yellow-400' : 'text-green-400'}>
            {agent.responseTime}ms
          </span>
        </div>

        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Error Rate:</span>
          <span className={agent.errorRate > 0.1 ? 'text-red-400' : 'text-green-400'}>
            {(agent.errorRate * 100).toFixed(1)}%
          </span>
        </div>

        <div className="text-sm">
          <span className="text-gray-400 block mb-1">Last Activity:</span>
          <span className="text-gray-200 font-mono text-xs break-all">
            {agent.activity.length > 50 ? agent.activity.slice(0, 50) + '...' : agent.activity || 'No recent activity'}
          </span>
        </div>
      </div>
    </div>
  );
}

export default AgentCard;
