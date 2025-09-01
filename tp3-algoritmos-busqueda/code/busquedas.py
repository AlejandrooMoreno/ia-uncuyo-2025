import gymnasium as gym
from gymnasium import wrappers
from random_map import generate_random_map_custom 
from collections import deque

def deterministic_random_100_environment():
    env = generate_random_map_custom(100, 0.8)
    return wrappers.TimeLimit(env, 1000)

def generate_random_map_custom_start_goal(size, frozen_prob, start, goal):

    import random
    desc = [['' for _ in range(size)] for _ in range(size)]

    fila = start // size       # 5 // 100 = 0
    columna = start % size    # 5 % 100 = 5
    start_pos = (fila, columna)

    fila = goal // size       # 5 // 100 = 0
    columna = goal % size    # 5 % 100 = 5
    goal_pos = (fila, columna)

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

def random_search(start, goal):
    current = start
    env = generate_random_map_custom_start_goal(100, 0.92, start, goal)
    env.unwrapped.s = start
    state = env.unwrapped.s
    print("Posición inicial forzada:", state)
    info = env.reset()
    done = truncated = False
    costo=0
    acciones = 0
    while not (done or truncated):
        action = env.action_space.sample()
        acciones += 1
        if action == 0 or action == 2:
            costo += 1
        else:
            costo += 10
        if acciones == 1000:
            truncated = True
        # Acción aleatoria
        next_state, reward, done, _, _ = env.step(action)
        print(f"Acción: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")
        if not reward == 1.0:
            print(f"¿Ganó? (encontró el objetivo): False")
            print(f"¿Perdió? (se cayó): {done}")
            print(f"¿Frenó? (alcanzó el máximo de pasos posible): " + truncated)
        else:
            print(f"¿Ganó? (encontró el objetivo): {done}")
        state = next_state

def bfs_search(start, goal):
    env = generate_random_map_custom_start_goal(100, 0.92, start, goal)
    env.unwrapped.s = start
    visited = set()
    queue = deque()
    queue.append((start, [start]))  # (estado actual, camino hasta aquí)
    visited.add(start)

    while queue:
        current_state, path = queue.popleft()
        if current_state == goal:
            print(f"Camino encontrado: {path}")
            return path
        for action in range(env.action_space.n):
            env.unwrapped.s = current_state
            next_state, reward, done, _, _ = env.step(action)
            # Evitar casilleros 'H' (Hole)
            if next_state not in visited and env.unwrapped.desc.flatten()[next_state] != b'H':
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))
    print("No se encontró camino al objetivo.")
    return None

def main():
    random_search(5, 100)
    bfs_search(5, 100)

if __name__ == "__main__":
    main()
