# Q-Learning Agent - Student Template

This is a template for implementing the Q-learning algorithm. The infrastructure is provided, but you need to implement the core Q-learning logic.

## What You Need to Implement

You need to complete **three main functions** in `q_agent.py`:

### 1. `max_action_q(self, observation)`
**Purpose:** Find the maximum Q-value among all valid actions for a given state.

**What to do:**
- Get the current state from the observation
- Generate all valid actions for this state using `generate_valid_actions(state)`
- Get the state ID using `self.get_state_id(state)`
- Loop through all valid actions and find the one with the highest Q-value
- Return the **maximum Q-value** (a float number, not the action)

**Hints:**
- Use `self.q_values.get((state_id, action), 0)` to safely get Q-values (default to 0 if not found)
- You can use Python's `max()` function

### 2. `select_action(self, observation, testing)`
**Purpose:** Implement epsilon-greedy action selection.

**What to do:**
- If training (`testing=False`) AND random value < epsilon: choose a **random** action (exploration)
- Otherwise: choose the action with the **highest Q-value** (exploitation)
- Make sure to initialize Q-values to 0 for new (state, action) pairs
- Return `(action, state_id)`

**Hints:**
- Use `random.uniform(0, 1)` to generate a random number between 0 and 1
- Use `random.choice(list(actions))` for random selection
- For exploitation, create a dictionary of Q-values for all actions and pick the max
- The current epsilon value is stored in `self.current_epsilon`

### 3. Q-Learning Update Rule in `play_game()`
**Purpose:** Update the Q-table after each action.

**What to do:**
Find the TODO comment around line 178 and implement the Q-learning update formula:

```
Q(s,a) = Q(s,a) + alpha * [reward + gamma * max_Q(s',a') - Q(s,a)]
```

Where:
- `Q(s,a)` = `self.q_values[state_id, action]` (current Q-value)
- `alpha` = `self.alpha` (learning rate, controls how much we update)
- `reward` = `observation.reward` (reward received from the environment)
- `gamma` = `self.gamma` (discount factor, controls importance of future rewards)
- `max_Q(s',a')` = `self.max_action_q(observation)` (max Q-value of next state)

**Hints:**
- This is just one line of code!
- You're updating `self.q_values[state_id, action]`
- The `state_id` and `action` are already available from earlier in the function

## Q-Learning Overview

Q-learning is a reinforcement learning algorithm that learns the value of taking specific actions in specific states. The Q-value Q(s,a) represents the expected future reward of taking action `a` in state `s`.

**Key concepts:**
- **Q-table**: A dictionary storing Q-values for (state, action) pairs
- **Epsilon-greedy**: Balance between exploration (trying new things) and exploitation (using what we know)
- **Learning rate (alpha)**: How much new information overrides old (0 to 1)
- **Discount factor (gamma)**: How much we value future rewards vs immediate rewards (0 to 1)

## Installation

Install the required dependencies:

```bash
pip install -e .[q_learning]
```

It is recommended to install the agent in a virtual environment.

## Running the Agent

Run the agent with:

```bash
python3 -m agents.attackers.q_learning.q_agent --episodes 1000
```

### Important Command-Line Arguments

- `--host`: Game server host (default: 127.0.0.1)
- `--port`: Game server port (default: 9000)
- `--episodes`: Number of episodes to train (default: 15000)
- `--alpha`: Learning rate (default: 0.1)
- `--gamma`: Discount factor (default: 0.9)
- `--epsilon_start`: Starting exploration rate (default: 0.9)
- `--epsilon_end`: Final exploration rate (default: 0.1)
- `--testing`: Set to True to test a trained model without learning

## Testing Your Implementation

1. Start with a small number of episodes (e.g., 100) to test if your code runs
2. Check the logs in the `logs/` directory to see if Q-values are being updated
3. Monitor the win rate - it should increase over time if your implementation is correct
4. Once it works, try training for more episodes (5000-15000)

## Expected Behavior

- Initially, the agent will perform randomly (high epsilon)
- As training progresses, epsilon decreases and the agent exploits learned knowledge
- Win rate should gradually increase
- The Q-table size will grow as new states are discovered

## Common Mistakes to Avoid

1. **Returning action instead of Q-value in `max_action_q()`** - Remember to return the VALUE, not the action
2. **Not handling the testing flag** - During testing, you should never explore (no random actions)
3. **Incorrect Q-value update** - Make sure you're adding to the old Q-value, not replacing it
4. **Forgetting to use gamma** - The discount factor is crucial for learning

## Questions?

If you get stuck, review:
1. The docstrings in each TODO section
2. The Q-learning formula above
3. How epsilon-greedy exploration works
4. The random agent implementation in `agents/attackers/random/` for reference on the basic structure
