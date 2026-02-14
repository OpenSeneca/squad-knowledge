# agt — Agent Scaffolding Tool

Create new AI agent projects with best-practice structure, inspired by CrewAI and modern agent frameworks.

## Installation

The tool is already symlinked to `~/.local/bin/agt`

```bash
# Verify installation
agt --help
```

## Usage

### List Available Templates

```bash
agt templates
```

Templates available:
- `research` - Research agent for analysis tasks
- `code` - Code generation and debugging
- `writer` - Content creation
- `analyst` - Data analysis
- `custom` - Custom agent for your needs

### Create a New Project

```bash
# Basic usage
agt create my-agent

# With template
agt create my-research-agent --template research

# With custom description
agt create my-agent --template code --description "AI agent for code review"

# Short options
agt create my-agent -t writer -d "Blog post generator"
```

### Project Structure

Every project includes:

```
my-agent/
├── my-agent/
│   ├── __init__.py
│   ├── agent.py      # Agent implementation with ABC base class
│   ├── config.py     # Configuration management
│   └── main.py      # Entry point
├── tests/
│   ├── __init__.py
│   └── test_agent.py
├── requirements.txt  # Dependencies
├── README.md       # Documentation
└── .env.example   # Environment template
```

### Getting Started

```bash
# 1. Create project
agt create my-agent --template research

# 2. Navigate and setup
cd my-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env with your API keys

# 5. Run
python -m my-agent.main
```

## Features

### Agent Base Class

Every agent includes:

- **Abstract base class** with common methods
- **Health check** method
- **Configuration** management
- **Async** support for modern async/await
- **Type hints** for better IDE support

### Configuration

Built-in config management:

```python
from my_agent.config import Config

config = Config()
agent_config = config.get_agent_config()
api_keys = config.get_api_keys()
```

### Agent Implementation

Implement your agent logic:

```python
class MyAgentImpl(MyAgent):
    async def process(self, input_data: Any) -> Dict[str, Any]:
        # Your agent logic here
        result = {
            "status": "success",
            "output": "Processed result"
        }
        return result
```

## Examples

### Research Agent

```bash
agt create research-assistant --template research
```

Creates an agent ready for research tasks with:
- Research role
- Analysis methods
- Data processing capabilities

### Code Agent

```bash
agt create code-reviewer --template code
```

Creates an agent for:
- Code generation
- Code review
- Debugging tasks

### Writer Agent

```bash
agt create content-writer --template writer
```

Creates an agent for:
- Blog posts
- Documentation
- Content creation

## Customization

### Add Your Own Template

Edit `agt.py` and add to `AGENT_TEMPLATES`:

```python
AGENT_TEMPLATES = {
    "research": {...},
    "my_custom": {
        "role": "My Role",
        "description": "Custom agent description"
    }
}
```

### Modify Templates

The templates in `agt.py` are just Python strings:
- `AGENT_PY` - Agent class template
- `MAIN_PY` - Entry point template
- `CONFIG_PY` - Configuration template
- `README_MD` - Documentation template

## Testing

Projects include pytest setup:

```bash
cd my-agent
pip install pytest
pytest tests/
```

## Best Practices

1. **Use async** - All agent methods are async-ready
2. **Type hints** - Full type annotations included
3. **Config management** - Environment-based configuration
4. **Health checks** - Every agent has a health_check method
5. **Testing** - Test template included

## Inspired By

- **CrewAI** - Role-playing autonomous agents
- **AgentGPT** - Browser-based agent configuration
- **Modern agent frameworks** - Best practices from open-source community

## License

MIT

---

**Ship small, iterate fast** — Build agents with confidence.
