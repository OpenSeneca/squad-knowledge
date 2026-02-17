import React from 'react';

function ActivityFeed({ feed, formatTime }) {
  const getSourceIcon = (source) => {
    if (source === 'agent') return '🤖';
    if (source === 'vault') return '📁';
    return '•';
  };

  const getSourceColor = (source) => {
    if (source === 'agent') return 'border-blue-600';
    if (source === 'vault') return 'border-purple-600';
    return 'border-gray-600';
  };

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      {feed.length === 0 ? (
        <p className="text-gray-400 text-sm">No recent activity</p>
      ) : (
        <ul className="space-y-3">
          {feed.map((item, index) => (
            <li key={index} className={`flex gap-3 pb-3 ${index < feed.length - 1 ? 'border-b border-gray-700' : ''}`}>
              <div className="text-xl flex-shrink-0">
                {getSourceIcon(item.source)}
              </div>
              <div className="flex-1 min-w-0">
                {item.source === 'agent' ? (
                  <>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold">{item.agentName}</span>
                      <span className="text-gray-400 text-xs">
                        {formatTime(item.timestamp)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-300 break-words">
                      {item.message}
                    </p>
                  </>
                ) : (
                  <>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold">{item.source_id}</span>
                      <span className="text-gray-400 text-xs">
                        {formatTime(item.timestamp)}
                      </span>
                    </div>
                    <p className="text-sm text-gray-300">
                      <span className="text-purple-400">{item.message}</span>
                    </p>
                  </>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ActivityFeed;
