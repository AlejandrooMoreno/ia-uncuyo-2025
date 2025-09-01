import gymnasium as gym
from gymnasium import wrappers
from random_map import generate_random_map_custom 

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

def deterministic_random_100_environment_start_goal(start, goal):
    env = generate_random_map_custom_start_goal(100, 0.8, start, goal)
    return wrappers.TimeLimit(env, 1000)

def random_search_1_scenary(start, goal):
    current = start
    env = deterministic_random_100_environment_start_goal(start, goal)
    env.unwrapped.s = start
    state = env.unwrapped.s
    print("Posición inicial forzada:", state)
    info = env.reset()
    done = truncated = False
    i=0
    while not (done or truncated):
        action = env.action_space.sample()
        i+=1
        # Acción aleatoria
        next_state, reward, done, truncated, _ = env.step(action)
        print(f"Acción: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")
        if not reward == 1.0:
            print(f"¿Ganó? (encontró el objetivo): False")
            print(f"¿Perdió? (se cayó): {done}")
            print(f"¿Frenó? (alcanzó el máximo de pasos posible): {truncated}\n")
        else:
            print(f"¿Ganó? (encontró el objetivo): {done}")
        state = next_state

def random_search_2_scenary(start, goal):
    current = start
    env = deterministic_random_100_environment_start_goal(start, goal)
    env.unwrapped.s = start
    state = env.unwrapped.s
    print("Posición inicial forzada:", state)
    info = env.reset()
    done = truncated = False
    i=0
    while not (done or truncated):
        action = env.action_space.sample()
        i+=1
        # Acción aleatoria
        next_state, reward, done, truncated, _ = env.step(action)
        print(f"Acción: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")
        if not reward == 1.0:
            print(f"¿Ganó? (encontró el objetivo): False")
            print(f"¿Perdió? (se cayó): {done}")
            print(f"¿Frenó? (alcanzó el máximo de pasos posible): {truncated}\n")
        else:
            print(f"¿Ganó? (encontró el objetivo): {done}")
        state = next_state

def main():
    random_search(5, 100)

if __name__ == "__main__":
    main()
