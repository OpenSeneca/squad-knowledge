#!/bin/bash
# Start Squad Dashboard server on port 8080

cd "$(dirname "$0")"
export PORT=8080

# Kill any existing dashboard server
pkill -f "node server.js" 2>/dev/null || true
sleep 1

# Start server in background
nohup node server.js > dashboard.log 2>&1 &
SERVER_PID=$!

echo "Starting Squad Dashboard server..."
echo "PID: $SERVER_PID"
echo "URL: http://localhost:8080"
echo "Tailscale URL: http://100.100.56.102:8080"
echo ""

# Wait for server to start
sleep 2

# Check if server is running
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server started successfully"
    tail -10 dashboard.log
else
    echo "❌ Server failed to start"
    cat dashboard.log
    exit 1
fi
