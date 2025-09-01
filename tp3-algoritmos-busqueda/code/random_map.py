import gymnasium as gym

def generate_random_map_custom(size, frozen_prob):

    import random
    desc = [['' for _ in range(size)] for _ in range(size)]

    # Ubicar aleatoriamente la posición inicial del agente y del objetivo
    positions = [(i, j) for i in range(size) for j in range(size)]
    start_pos = random.choice(positions)
    positions.remove(start_pos)
    goal_pos = random.choice(positions)
    positions.remove(goal_pos)

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
    return gym.make('FrozenLake-v1', desc = desc, render_mode='human').env

