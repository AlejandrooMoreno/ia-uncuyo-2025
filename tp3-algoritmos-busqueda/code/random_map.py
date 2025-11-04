try:
    import gymnasium as gym
except ModuleNotFoundError:
    gym = None


class _ActionSpace:
    """Minimal action space replicating Gym's interface."""

    def __init__(self, n):
        self.n = n

    def sample(self):
        import random

        return random.randrange(self.n)


class _DescWrapper:
    """Provide a flatten() helper returning byte-encoded tiles."""

    def __init__(self, rows):
        self._rows = rows
        self._flat = [cell.encode("ascii") for row in rows for cell in row]

    def flatten(self):
        return self._flat


class SimpleFrozenLakeEnv:
    """Deterministic FrozenLake clone used when Gymnasium is unavailable."""

    _action_map = {
        0: (0, -1),   # Left
        1: (1, 0),    # Down
        2: (0, 1),    # Right
        3: (-1, 0),   # Up
    }

    def __init__(self, desc_rows, start_idx, goal_idx, max_steps=1000):
        self._desc_rows = list(desc_rows)
        self.nrow = len(desc_rows)
        self.ncol = len(desc_rows[0]) if desc_rows else 0
        self.start_state = start_idx
        self.goal_state = goal_idx
        self.max_steps = max_steps

        self.action_space = _ActionSpace(4)
        self.unwrapped = self
        self.desc = _DescWrapper(desc_rows)

        self._s = start_idx
        self.steps = 0
        self.done = False

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, value):
        self._s = value
        self.steps = 0
        self.done = False

    def clone(self):
        """Return an independent environment with the same configuration."""
        return SimpleFrozenLakeEnv(self._desc_rows, self.start_state, self.goal_state, self.max_steps)

    def reset(self):
        self.s = self.start_state
        return self.s, {}

    def step(self, action):
        if self.done:
            return self.s, 0.0, True, False, {}

        dr, dc = self._action_map.get(action, (0, 0))
        row, col = divmod(self.s, self.ncol)
        new_row = min(max(row + dr, 0), self.nrow - 1)
        new_col = min(max(col + dc, 0), self.ncol - 1)
        next_state = new_row * self.ncol + new_col

        tile = self._desc_rows[new_row][new_col]
        reward = 0.0
        terminated = False
        if tile == 'G':
            reward = 1.0
            terminated = True
        elif tile == 'H':
            terminated = True

        self.steps += 1
        truncated = self.steps >= self.max_steps and not terminated

        self._s = next_state
        self.done = terminated or truncated

        return next_state, reward, terminated, truncated, {}


def generate_random_map_custom(size, frozen_prob):

    import random
    desc = [['' for _ in range(size)] for _ in range(size)]


    # Ubicar aleatoriamente la posición inicial del agente y del objetivo
    positions = [(i, j) for i in range(size) for j in range(size)]
    start_pos = random.choice(positions)
    positions.remove(start_pos)
    goal_pos = random.choice(positions)
    positions.remove(goal_pos)

    # Convertir las posiciones a enteros
    start_idx = start_pos[0] * size + start_pos[1]
    goal_idx = goal_pos[0] * size + goal_pos[1]


    for i in range(size):
        for j in range(size):
            if (i, j) == start_pos:
                desc[i][j] = 'S'
            elif (i, j) == goal_pos:
                desc[i][j] = 'G'
            else:
                desc[i][j] = 'F' if random.random() < frozen_prob else 'H'

    # Convertir a lista de strings
    desc = [''.join(row) for row in desc]
    if gym is not None:
        env = gym.make('FrozenLake-v1', desc=desc).env
    else:
        env = SimpleFrozenLakeEnv(desc, start_idx, goal_idx)
    return env, start_idx, goal_idx
