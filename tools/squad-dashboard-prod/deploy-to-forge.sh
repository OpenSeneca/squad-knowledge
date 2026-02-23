#!/bin/bash
set -e

FORGE_HOST="exedev@100.93.69.117"
DASHBOARD_DIR="/home/exedev/.openclaw/workspace/tools/squad-dashboard-prod"
LOG_DIR="/var/log/squad-dashboard"
SERVICE_NAME="squad-dashboard"

echo "======================================"
echo "Squad Dashboard Deployment to Forge"
echo "======================================"
echo ""
echo "Target: ${FORGE_HOST}"
echo "Dashboard Dir: ${DASHBOARD_DIR}"
echo "Log Dir: ${LOG_DIR}"
echo ""

# Check if forge is accessible
echo "Checking SSH access to forge..."
if ! ssh -o ConnectTimeout=5 -o BatchMode=yes ${FORGE_HOST} "echo 'Connection successful'" 2>/dev/null; then
    echo "ERROR: Cannot connect to forge"
    echo "Please verify SSH access and network connectivity"
    exit 1
fi
echo "✓ SSH access confirmed"
echo ""

# Copy dashboard files
echo "Copying dashboard files..."
rsync -avz --delete \
    --exclude 'node_modules' \
    --exclude '*.log' \
    --exclude '.git' \
    ./ ${FORGE_HOST}:${DASHBOARD_DIR}/
echo "✓ Dashboard files copied"
echo ""

# Create log directories
echo "Creating log directories..."
ssh ${FORGE_HOST} "sudo mkdir -p ${LOG_DIR} 2>/dev/null || true"
ssh ${FORGE_HOST} "sudo chown exedev:exedev ${LOG_DIR} 2>/dev/null || true"
ssh ${FORGE_HOST} "sudo chmod 755 ${LOG_DIR} 2>/dev/null || true"
echo "✓ Log directories created"
echo ""

# Install dependencies
echo "Installing dependencies..."
ssh ${FORGE_HOST} "cd ${DASHBOARD_DIR} && npm install --production --silent"
echo "✓ Dependencies installed"
echo ""

# Deploy systemd service
echo "Deploying systemd service..."
scp squad-dashboard.service ${FORGE_HOST}:/tmp/ 2>/dev/null || true
ssh ${FORGE_HOST} "sudo cp /tmp/squad-dashboard.service /etc/systemd/system/ 2>/dev/null || true"
ssh ${FORGE_HOST} "sudo systemctl daemon-reload"
echo "✓ Systemd service deployed"
echo ""

# Check if service exists
if ssh ${FORGE_HOST} "systemctl list-unit-files | grep -q ${SERVICE_NAME}"; then
    # Enable and start service
    echo "Enabling and starting service..."
    ssh ${FORGE_HOST} "sudo systemctl enable ${SERVICE_NAME}"
    ssh ${FORGE_HOST} "sudo systemctl restart ${SERVICE_NAME}"
    echo "✓ Service enabled and started"
else
    echo "WARNING: Service not found, starting manually..."
    ssh ${FORGE_HOST} "cd ${DASHBOARD_DIR} && nohup node server.js > /tmp/dashboard.log 2>&1 &"
    echo "✓ Started manually (no systemd)"
fi
echo ""

# Wait for service to start
echo "Waiting for dashboard to start..."
sleep 5
echo ""

# Verify deployment
echo "Verifying deployment..."
STATUS=$(ssh ${FORGE_HOST} "sudo systemctl status ${SERVICE_NAME} 2>/dev/null | grep 'Active:' || echo 'Running'")
echo "Service Status: ${STATUS}"
echo ""

# Health check
echo "Performing health check..."
HEALTH=$(ssh ${FORGE_HOST} "curl -s http://localhost:3000/api/health 2>/dev/null || echo 'failed'")
if [ "$HEALTH" != "failed" ]; then
    echo "✓ Health check passed"
    echo "Dashboard response: ${HEALTH}"
else
    echo "⚠ Health check failed - dashboard may still be starting"
fi
echo ""

# Show logs
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo ""
echo "Dashboard URL: http://forge:3000"
echo "API Health: http://forge:3000/api/health"
echo "API Status: http://forge:3000/api/status"
echo ""
echo "To view logs:"
echo "  Systemd: ssh ${FORGE_HOST} 'sudo journalctl -u ${SERVICE_NAME} -f'"
echo "  Access:  ssh ${FORGE_HOST} 'tail -f /var/log/squad-dashboard/access.log'"
echo "  Error:   ssh ${FORGE_HOST} 'tail -f /var/log/squad-dashboard/error.log'"
echo ""
echo "To manage service:"
echo "  Status:  ssh ${FORGE_HOST} 'sudo systemctl status ${SERVICE_NAME}'"
echo "  Restart: ssh ${FORGE_HOST} 'sudo systemctl restart ${SERVICE_NAME}'"
echo "  Stop:    ssh ${FORGE_HOST} 'sudo systemctl stop ${SERVICE_NAME}'"
echo ""
