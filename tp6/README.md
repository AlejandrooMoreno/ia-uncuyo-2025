# NetSecGameAgents

Collection of autonomous agents for the Network Security Game environment. These agents implement various strategies (random, Q-learning, LLM-based, etc.) to play as attackers, defenders, or benign users in network security scenarios.

## Installation

### Requirements
- Python 3.12+
- NetSecGame server running (typically at `127.0.0.1:9000`)

### Quick Start

```bash
# Create virtual environment
python3.12 -m venv venv-netsecagents
source venv-netsecagents/bin/activate

# Install base package
pip install -e .

# Install agent-specific dependencies
pip install -e ".[random]"
```

### Available Agent Dependencies

```bash
pip install -e ".[random]"              # Random agents
pip install -e ".[q_learning]"          # Q-learning agent
pip install -e ".[tui]"                 # Interactive TUI agent
```

## Usage

### Running Agents

```bash
# Random attacker (evaluation mode, 100 episodes)
python -m agents.attackers.random.random_agent

# Custom parameters
python -m agents.attackers.random.random_agent \
    --host 127.0.0.1 \
    --port 9000 \
    --episodes 50 \
    --test_each 10
```

### Command-line Options

- `--host`: Game server host (default: `127.0.0.1`)
- `--port`: Game server port (default: `9000`)
- `--episodes`: Number of episodes to run (default: `100`)
- `--test_each`: Report statistics every N episodes (default: `10`)
- `--logdir`: Log file directory (default: `./logs`)
- `--evaluate`: Enable evaluation mode (default: `True`)

## Agent Types

### Attackers
- **Random** (`agents.attackers.random.random_agent`): Randomly selects valid actions
- **Whitebox Random** (`agents.attackers.random.whitebox_random_agent`): Random agent with full state visibility
- **Q-learning** (`agents.attackers.q_learning.q_agent`): Tabular Q-learning agent
- **Interactive TUI** (`agents.attackers.interactive_tui.interactive_tui`): Human-in-the-loop text interface
- **Scripted** (`agents.attackers.scripted_attacker.scripted_attacker`): Pre-programmed attack sequences

## Architecture

```
NetSecGameAgents/
├── AIDojoCoordinator/      # Game protocol and data structures
│   └── game_components.py
├── agents/
│   ├── base_agent.py       # Base agent class
│   ├── agent_utils.py      # Shared utilities
│   ├── attackers/          # Attacker agents
│   ├── defenders/          # Defender agents
│   └── benign/             # Benign user agents
└── utils/                  # Helper utilities
```

## BaseAgent

All agents extend `BaseAgent` which provides:
- `register()`: Register with game server
- `make_step(action)`: Execute an action
- `request_game_reset()`: Reset the game environment
- `terminate_connection()`: Close connection

## Statistics & Logging

Agents in evaluation mode track and report:
- Win rate and detection rate
- Average returns and episode lengths
- Step counts per outcome type (win/detection/timeout)
- Statistics printed to stdout and logged to files

## Development

### Creating Custom Agents

```python
from agents.base_agent import BaseAgent
from AIDojoCoordinator.game_components import Action, Observation

class MyAgent(BaseAgent):
    def __init__(self, host, port, role):
        super().__init__(host, port, role)

    def select_action(self, observation: Observation) -> Action:
        # Your action selection logic
        pass
```

## License

See LICENSE file for details.

## Authors

- Ondrej Lukas - ondrej.lukas@aic.cvut.cz
- Sebastian Garcia - sebastian.garcia@agents.fel.cvut.cz
- Maria Rigaki - maria.rigaki@aic.fel.cvut.cz

Developed at the Stratosphere Laboratory, Czech Technical University in Prague.
