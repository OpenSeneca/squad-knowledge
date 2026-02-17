import React from 'react';

function MetricsChart({ metrics }) {
  const getResponseTimeColor = (time) => {
    if (time < 100) return 'text-green-400';
    if (time < 500) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getErrorRateColor = (rate) => {
    if (rate < 0.01) return 'text-green-400';
    if (rate < 0.05) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      {metrics.length === 0 ? (
        <p className="text-gray-400 text-sm">No metrics available</p>
      ) : (
        <table className="w-full text-sm">
          <thead>
            <tr className="text-gray-400">
              <th className="text-left pb-2">Agent</th>
              <th className="text-right pb-2">Avg Response</th>
              <th className="text-right pb-2">Error Rate</th>
              <th className="text-right pb-2">Checks (1h)</th>
            </tr>
          </thead>
          <tbody>
            {metrics.map((metric, index) => (
              <tr key={index} className={index < metrics.length - 1 ? 'border-b border-gray-700' : ''}>
                <td className="py-2">{metric.name}</td>
                <td className={`text-right py-2 ${getResponseTimeColor(metric.avgResponseTime)}`}>
                  {metric.avgResponseTime.toFixed(0)}ms
                </td>
                <td className={`text-right py-2 ${getErrorRateColor(metric.avgErrorRate)}`}>
                  {(metric.avgErrorRate * 100).toFixed(1)}%
                </td>
                <td className="text-right py-2 text-gray-400">
                  {metric.totalChecks}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default MetricsChart;
