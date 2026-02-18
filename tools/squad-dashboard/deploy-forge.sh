#!/bin/bash

# Squad Dashboard Deployment Script
# Deploys the dashboard to forge (100.93.69.117)

set -e

# Configuration
FORGE_HOST="100.93.69.117"
FORGE_USER="${FORGE_USER:-exedev}"
FORGE_DIR="${FORGE_DIR:-~/dashboard}"
LOCAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="squad-dashboard"
PORT="${PORT:-8000}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if SSH is available
check_ssh() {
    log_info "Checking SSH connection to $FORGE_HOST..."

    if ssh -o ConnectTimeout=5 -o BatchMode=yes "${FORGE_USER}@${FORGE_HOST}" exit 2>/dev/null; then
        log_info "✓ SSH connection available"
        return 0
    else
        log_error "✗ SSH connection failed"
        log_warn "Please ensure:"
        log_warn "  - Forge server is reachable at $FORGE_HOST"
        log_warn "  - SSH keys are configured"
        log_warn "  - You have permission to SSH to ${FORGE_USER}@${FORGE_HOST}"
        return 1
    fi
}

# Deploy files to forge
deploy_files() {
    log_info "Deploying files to $FORGE_HOST:$FORGE_DIR..."

    # Create remote directory
    ssh "${FORGE_USER}@${FORGE_HOST}" "mkdir -p $FORGE_DIR"

    # Copy files
    rsync -avz --exclude='*.log' --exclude='node_modules' \
        "$LOCAL_DIR/" \
        "${FORGE_USER}@${FORGE_HOST}:${FORGE_DIR}/"

    log_info "✓ Files deployed"
}

# Install PM2 if not present
install_pm2() {
    log_info "Checking if PM2 is installed on forge..."

    if ssh "${FORGE_USER}@${FORGE_HOST}" "command -v pm2" >/dev/null 2>&1; then
        log_info "✓ PM2 is already installed"
    else
        log_warn "PM2 not found. Installing..."
        ssh "${FORGE_USER}@${FORGE_HOST}" "npm install -g pm2"
        log_info "✓ PM2 installed"
    fi
}

# Start/Restart the service
start_service() {
    log_info "Starting/Restarting dashboard service..."

    # Stop existing service if running
    ssh "${FORGE_USER}@${FORGE_HOST}" "pm2 stop $SERVICE_NAME 2>/dev/null || true"

    # Start service
    ssh "${FORGE_USER}@${FORGE_HOST}" "cd $FORGE_DIR && pm2 start server.js --name $SERVICE_NAME --env PORT=$PORT"

    # Save PM2 configuration
    ssh "${FORGE_USER}@${FORGE_HOST}" "pm2 save"

    log_info "✓ Service started"
}

# Check service status
check_status() {
    log_info "Checking service status..."

    ssh "${FORGE_USER}@${FORGE_HOST}" "pm2 status $SERVICE_NAME"

    echo ""
    log_info "Dashboard URL: http://$FORGE_HOST:$PORT"
    log_info "API Endpoint: http://$FORGE_HOST:$PORT/api/status"
}

# Setup PM2 startup script (optional)
setup_startup() {
    read -p "Setup PM2 to auto-start on boot? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Setting up PM2 startup script..."

        ssh "${FORGE_USER}@${FORGE_HOST}" "pm2 startup" || {
            log_warn "PM2 startup setup failed. Run this manually on forge:"
            log_warn "  ssh $FORGE_USER@$FORGE_HOST 'pm2 startup'"
        }
    fi
}

# Main deployment flow
main() {
    echo "=========================================="
    echo "  Squad Dashboard Deployment Script"
    echo "  Target: ${FORGE_USER}@${FORGE_HOST}:${FORGE_DIR}"
    echo "=========================================="
    echo ""

    # Check SSH
    if ! check_ssh; then
        exit 1
    fi
    echo ""

    # Deploy files
    deploy_files
    echo ""

    # Install PM2
    install_pm2
    echo ""

    # Start service
    start_service
    echo ""

    # Check status
    check_status
    echo ""

    # Setup startup (optional)
    setup_startup
    echo ""

    log_info "Deployment complete!"
    log_warn "Note: data.json must be updated by Argus or manually"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            FORGE_HOST="$2"
            shift 2
            ;;
        --user)
            FORGE_USER="$2"
            shift 2
            ;;
        --dir)
            FORGE_DIR="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --host HOST     Forge host (default: 100.93.69.117)"
            echo "  --user USER     SSH user (default: exedev)"
            echo "  --dir DIR       Remote directory (default: ~/dashboard)"
            echo "  --port PORT     Server port (default: 8000)"
            echo "  --help          Show this help"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main
main
