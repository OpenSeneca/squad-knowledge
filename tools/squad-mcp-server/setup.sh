#!/bin/bash
set -e

SQUAD_TOOLS_BASE="/home/exedev/.openclaw/workspace/tools"
MCP_SERVER_DIR="${SQUAD_TOOLS_BASE}/squad-mcp-server"
PYTHON_CMD=$(which python3 || which python)

echo "======================================"
echo "Squad MCP Server Setup"
echo "======================================"
echo ""
echo "Python Command: ${PYTHON_CMD}"
echo "MCP Server Dir: ${MCP_SERVER_DIR}"
echo ""

# Check Python
if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: Python not found. Please install Python 3.8+"
    exit 1
fi
echo "✓ Python found: ${PYTHON_CMD}"
echo ""

# Install dependencies
echo "Installing dependencies..."
cd "$MCP_SERVER_DIR"
$PYTHON_CMD -m pip install -r requirements.txt --user
echo "✓ Dependencies installed"
echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x mcp_server.py
chmod +x setup.sh
echo "✓ Scripts made executable"
echo ""

# Verify installation
echo "Verifying installation..."
if [ -f "$MCP_SERVER_DIR/mcp_server.py" ]; then
    echo "✓ MCP server script found"
else
    echo "ERROR: MCP server script not found"
    exit 1
fi
echo ""

# Check squad tools
echo "Checking squad tools..."
TOOLS_COUNT=0
for tool_path in "$SQUAD_TOOLS_BASE"/*/; do
    if [ -f "$tool_path"/*.py" ]; then
        TOOLS_COUNT=$((TOOLS_COUNT + 1))
    fi
done
echo "✓ Found $TOOLS_COUNT squad tools"
echo ""

# Check squad knowledge
if [ -f "$SQUAD_TOOLS_BASE/squad-knowledge/knowledge.db" ]; then
    echo "✓ Squad knowledge database found"
else
    echo "⚠ Squad knowledge database not found"
fi
echo ""

echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next Steps:"
echo ""
echo "1. Configure Claude Desktop:"
echo "   - Open Claude Desktop"
echo "   - Go to Settings → Tools → MCP Servers"
echo "   - Click 'Add Server'"
echo "   - Select 'Local'"
echo "   - Use: ${PYTHON_CMD} ${MCP_SERVER_DIR}/mcp_server.py"
echo "   - Name: 'Squad Tools'"
echo ""
echo "2. Test MCP connection:"
echo "   ${PYTHON_CMD} ${MCP_SERVER_DIR}/mcp_server.py squad-tools-list"
echo ""
echo "3. Ask Claude to use squad tools:"
echo "   'List all available squad tools'"
echo "   'Search squad knowledge for dashboard'"
echo "   'Get a complete squad overview'"
echo ""
echo "Documentation: ${MCP_SERVER_DIR}/README.md"
echo ""
