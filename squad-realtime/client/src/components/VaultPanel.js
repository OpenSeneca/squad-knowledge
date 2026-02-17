import React from 'react';

function VaultPanel({ vaults }) {
  const getStatusIcon = (status) => {
    if (status === 'synced') return '✓';
    if (status === 'syncing') return '⟳';
    return '✗';
  };

  const getStatusColor = (status) => {
    if (status === 'synced') return 'text-green-400';
    if (status === 'syncing') return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      {vaults.map((vault, index) => (
        <div key={index} className="mb-4 last:mb-0">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold">{vault.vaultName}</h3>
            <span className={`text-sm ${getStatusColor(vault.status)}`}>
              {getStatusIcon(vault.status)} {vault.status.toUpperCase()}
            </span>
          </div>

          {vault.status === 'error' ? (
            <p className="text-red-400 text-sm mb-2">{vault.error}</p>
          ) : null}

          <div className="text-sm text-gray-400 mb-2">
            {vault.fileCount} files
          </div>

          {vault.recentFiles.length > 0 && (
            <div>
              <p className="text-sm text-gray-300 mb-2">Recent Updates:</p>
              <ul className="space-y-1">
                {vault.recentFiles.slice(0, 5).map((file, fileIndex) => (
                  <li key={fileIndex} className="text-xs text-gray-400 flex justify-between">
                    <span>{file.name}</span>
                    <span>{new Date(file.timestamp).toLocaleString()}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <a
            href={`file://${vault.vaultPath.replace('/home/exedev', '/Users/exedev')}`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 text-sm hover:underline"
          >
            Open Vault →
          </a>
        </div>
      ))}
    </div>
  );
}

export default VaultPanel;
