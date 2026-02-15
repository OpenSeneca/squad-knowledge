#!/bin/bash
# ghflow — Convert flow workflows to GitHub Agentic Workflows
# Convert YAML-based flow workflows to GitHub Agentic Workflows (Markdown)

GHFLOW_VERSION="0.1.0"
FLOW_DIR="${FLOW_DIR:-$HOME/.flow}"
GHAW_DIR="${GITHUB_WORKFLOWS_DIR:-.github/workflows}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

help() {
    cat << HELP
ghflow v$GHFLOW_VERSION — Convert flow workflows to GitHub Agentic Workflows

Convert flow (YAML) workflows to GitHub Agentic Workflows (Markdown)

USAGE:
    ghflow <command> [options]

COMMANDS:
    list                List all available flow workflows
    convert <name>      Convert a flow workflow to GitHub Agentic Workflow
    convert-all         Convert all flow workflows
    show <name>         Show the generated GitHub Agentic Workflow
    validate <name>     Validate flow workflow structure

OPTIONS:
    -o, --output <dir>  Output directory (default: .github/workflows)
    -t, --trigger <type> Trigger type (manual, schedule, push, pr)
    -f, --force         Overwrite existing files
    -h, --help          Show this help message
    -v, --version       Show version

EXAMPLES:
    ghflow list                    List all flow workflows
    ghflow convert deploy          Convert deploy workflow
    ghflow convert deploy -o ./workflows
    ghflow convert-all             Convert all workflows
    ghflow show deploy             Show GitHub Agentic Workflow

FLOW TO GITHUB MAPPING:
    prj create     → GitHub: Create new repo/files
    agt create     → GitHub: Create agent repository
    tick add       → GitHub: Create issue
    snip add       → GitHub: Add to project wiki/docs
    crw run        → GitHub: Run agent workflow in Actions

HELP
}

version() {
    echo "ghflow v$GHFLOW_VERSION"
}

# Check if jq is available
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        echo "${YELLOW}Warning: jq not found. JSON parsing limited.${NC}"
        echo "Install with: sudo apt-get install jq (Linux) or brew install jq (macOS)"
    fi
}

# List all flow workflows
list_workflows() {
    local flows_json="$FLOW_DIR/flows.json"

    if [ ! -f "$flows_json" ]; then
        echo "${RED}❌ Flow directory not initialized${NC}"
        echo "Run: flow init"
        exit 1
    fi

    echo "Available flow workflows:"
    echo ""

    if [ -n "$(command -v jq 2>/dev/null)" ]; then
        jq -r '.[] | "  • \(.name) - \(.description // "No description")"' "$flows_json" 2>/dev/null || echo "  (No workflows found)"
    else
        # Fallback without jq
        grep -o '"name":"[^"]*"' "$flows_json" | sed 's/"name":"//;s/"//' | while read name; do
            echo "  • $name"
        done
    fi
}

# Validate flow workflow structure
validate_workflow() {
    local name="$1"
    local flow_file="$FLOW_DIR/$name/workflow.yaml"

    if [ ! -f "$flow_file" ]; then
        echo "${RED}❌ Workflow '$name' not found${NC}"
        exit 1
    fi

    echo "${BLUE}Validating workflow: $name${NC}"

    # Check for required sections
    if ! grep -q "stages:" "$flow_file"; then
        echo "${RED}❌ Missing 'stages' section${NC}"
        exit 1
    fi

    echo "${GREEN}✓${NC} Workflow structure is valid"
}

# Convert flow workflow to GitHub Agentic Workflow
convert_workflow() {
    local name="$1"
    local flow_file="$FLOW_DIR/$name/workflow.yaml"
    local output_dir="${OUTPUT_DIR:-$GHAW_DIR}"
    local trigger="${TRIGGER_TYPE:-manual}"

    if [ ! -f "$flow_file" ]; then
        echo "${RED}❌ Workflow '$name' not found${NC}"
        echo "Run: ghflow list"
        exit 1
    fi

    # Validate first
    validate_workflow "$name"

    # Create output directory if it doesn't exist
    mkdir -p "$output_dir"

    local output_file="$output_dir/$name.md"
    local yaml_file="$output_dir/$name.yaml"

    # Check if file exists and not forcing
    if [ -f "$output_file" ] && [ "$FORCE" != "true" ]; then
        echo "${YELLOW}⚠${NC} $output_file already exists"
        echo "Use --force to overwrite"
        exit 1
    fi

    echo "${BLUE}Converting workflow: $name${NC}"
    echo "Trigger: $trigger"
    echo "Output: $output_file"

    # Extract description from YAML (simple grep)
    local description=$(grep -m1 "^description:" "$flow_file" | sed 's/description: //' | sed 's/"//g')
    description="${description:-Automated workflow converted from flow}"

    # Generate GitHub Agentic Workflow (Markdown)
    cat > "$output_file" << MARKDOWN_EOF
# $name

$description

## Trigger

This workflow is triggered on $trigger.

---

This is a GitHub Agentic Workflow. It describes automation goals in natural language.
The AI agent figures out how to execute it.

## Workflow Goals

This workflow manages the following stages:

MARKDOWN_EOF

    # Parse stages and convert to natural language
    echo "" >> "$output_file"
    local stage_num=1
    local in_stage=false

    while IFS= read -r line; do
        if echo "$line" | grep -q '^[[:space:]]*- id:'; then
            local stage_id=$(echo "$line" | sed 's/.*id: //' | sed 's/"//g' | tr -d ' ')
            in_stage=true
        elif echo "$line" | grep -q '^[[:space:]]*name:' && [ "$in_stage" = true ]; then
            local stage_name=$(echo "$line" | sed 's/.*name: //' | sed 's/"//g' | tr -d ' ')
            echo "### Stage $stage_num: $stage_name" >> "$output_file"
            echo "" >> "$output_file"
            stage_num=$((stage_num + 1))
        elif echo "$line" | grep -q '^[[:space:]]*description:' && [ "$in_stage" = true ]; then
            local stage_desc=$(echo "$line" | sed 's/.*description: //' | sed 's/"//g' | tr -d ' ')
            echo "$stage_desc" >> "$output_file"
            echo "" >> "$output_file"
        elif echo "$line" | grep -q '^[[:space:]]*commands:'; then
            in_stage=false
        elif echo "$line" | grep -q '^[[:space:]]*tool:' && [ "$stage_num" -gt 1 ]; then
            local tool=$(echo "$line" | sed 's/.*tool: //' | sed 's/"//g' | tr -d ' ')
            echo "**Tool:** \`$tool\`" >> "$output_file"
        elif echo "$line" | grep -q '^[[:space:]]*action:' && [ "$stage_num" -gt 1 ]; then
            local action=$(echo "$line" | sed 's/.*action: //' | sed 's/"//g' | tr -d ' ')
            echo "**Action:** $action" >> "$output_file"
        elif echo "$line" | grep -q '^[[:space:]]*args:' && [ "$stage_num" -gt 1 ]; then
            local args=$(echo "$line" | sed 's/.*args: //' | sed 's/\[//;s/\]//;s/"//g' | tr -d ' ')
            echo "**Arguments:** $args" >> "$output_file"
            echo "" >> "$output_file"
        fi
    done < "$flow_file"

    # Add metadata
    cat >> "$output_file" << MARKDOWN_EOF

## Tool Mapping

This workflow uses the following flow tools:

| Flow Tool | GitHub Equivalent |
|-----------|------------------|
| prj create | Create new repository/files |
| agt create | Create agent repository structure |
| tick add | Create GitHub issue |
| snip add | Add to project wiki or documentation |
| crw run | Execute agent workflow in GitHub Actions |

## Running this Workflow

To compile this workflow into a GitHub Actions workflow:

\`\`\`bash
gh aw compile $name.md
\`\`\`

This generates a standard GitHub Actions YAML file that can be committed to the repository.

## Generated by

ghflow v$GHFLOW_VERSION — https://github.com/openclaw/tools
MARKDOWN_EOF

    # Generate GitHub Actions YAML (basic template)
    cat > "$yaml_file" << YAML_EOF
name: $name

on:
  $trigger:
    types: [requested]

permissions:
  contents: read

jobs:
  agent-workflow:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run Agent Workflow
        uses: github/agent-workflow@v1
        with:
          workflow: $name.md
          agent: github-copilot-cli
YAML_EOF

    echo "${GREEN}✓${NC} Converted workflow: $name"
    echo "  Markdown: $output_file"
    echo "  YAML: $yaml_file"
    echo ""
    echo "${YELLOW}To compile and use:${NC}"
    echo "  gh aw compile $output_file"
}

# Show generated GitHub Agentic Workflow
show_workflow() {
    local name="$1"
    local output_file="${OUTPUT_DIR:-$GHAW_DIR}/$name.md"

    if [ ! -f "$output_file" ]; then
        echo "${YELLOW}⚠${NC} $output_file not found"
        echo "Run: ghflow convert $name"
        exit 1
    fi

    cat "$output_file"
}

# Convert all flow workflows
convert_all_workflows() {
    local flows_json="$FLOW_DIR/flows.json"

    if [ ! -f "$flows_json" ]; then
        echo "${RED}❌ Flow directory not initialized${NC}"
        exit 1
    fi

    echo "${BLUE}Converting all flow workflows...${NC}"
    echo ""

    # Extract workflow names
    local workflows=$(grep -o '"name":"[^"]*"' "$flows_json" | sed 's/"name":"//;s/"//')

    local count=0
    for name in $workflows; do
        if [ -f "$FLOW_DIR/$name/workflow.yaml" ]; then
            convert_workflow "$name"
            count=$((count + 1))
        fi
    done

    echo ""
    echo "${GREEN}✓${NC} Converted $count workflows"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -t|--trigger)
            TRIGGER_TYPE="$2"
            shift 2
            ;;
        -f|--force)
            FORCE="true"
            shift
            ;;
        -h|--help)
            help
            exit 0
            ;;
        -v|--version)
            version
            exit 0
            ;;
        *)
            break
            ;;
    esac
done

# Main command handler
check_dependencies

case "$1" in
    list)
        list_workflows
        ;;
    convert)
        if [ -z "$2" ]; then
            echo "${RED}Error: workflow name required${NC}"
            echo "Usage: ghflow convert <name>"
            exit 1
        fi
        convert_workflow "$2"
        ;;
    convert-all)
        convert_all_workflows
        ;;
    show)
        if [ -z "$2" ]; then
            echo "${RED}Error: workflow name required${NC}"
            echo "Usage: ghflow show <name>"
            exit 1
        fi
        show_workflow "$2"
        ;;
    validate)
        if [ -z "$2" ]; then
            echo "${RED}Error: workflow name required${NC}"
            echo "Usage: ghflow validate <name>"
            exit 1
        fi
        validate_workflow "$2"
        ;;
    "")
        help
        ;;
    *)
        echo "${RED}Unknown command: $1${NC}"
        echo ""
        help
        exit 1
        ;;
esac
