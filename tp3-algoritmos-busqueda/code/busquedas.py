import gymnasium as gym
from gymnasium import wrappers
from random_map import generate_random_map_custom 
from collections import deque
import heapq

def deterministic_random_100_environment():
    env, start, goal = generate_random_map_custom(100, 0.92)
    env = wrappers.TimeLimit(env, 1000)
    return env, start, goal

def random_search(env, start, goal):
    current = start
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
            return acciones + 1, acciones, costo
        state = next_state
    return None, None, None

def bfs_search(env, start, goal):
    env.unwrapped.s = start
    visited = set()
    queue = deque()
    queue.append((start, [start], 1)) # (estado actual, camino hasta aquí)
    visited.add(start)
    info = env.reset()
    estados_explorados = 1
    while queue:
        current_state, path, costo = queue.popleft()
        if current_state == goal:
            print(f"Camino encontrado: {path}")
            return estados_explorados, len(path) - 1, costo
        for action in range(env.action_space.n):
            env.unwrapped.s = current_state
            next_state, _, _, _, _ = env.step(action)
            if next_state not in visited:
                estados_explorados += 1
                visited.add(next_state)
            # Evitar casilleros 'H' (Hole)
            if next_state not in visited and env.unwrapped.desc.flatten()[next_state] != b'H':
                if action == 0 or action == 2:
                    nuevo_costo = costo + 1
                else:
                    nuevo_costo = costo + 10
                queue.append((next_state, path + [next_state], nuevo_costo))
    print("No se encontró camino al objetivo.")
    return None, None, None

def dfs_search(env, start, goal):
    env.unwrapped.s = start
    visited = set()
    stack = []
    stack.append((start, [start], 0))  # (estado actual, camino hasta aquí)
    visited.add(start)
    info = env.reset()
    return dfs_searchR(env, goal, stack, visited, 1)

def dfs_searchR(env, goal, stack, visited, estados_explorados):
    current_state, path, costo = stack.pop()
    if current_state == goal:
        print(f"Camino encontrado: {path}")
        return estados_explorados, len(path) - 1, costo
    for action in range(env.action_space.n):
        env.unwrapped.s = current_state
        next_state, _, _, _, _ = env.step(action)
        if next_state not in visited:
            estados_explorados += 1
            visited.add(next_state)
        # Evitar casilleros 'H' (Hole)
        if next_state not in visited and env.unwrapped.desc.flatten()[next_state] != b'H':
            if action == 0 or action == 2:
                nuevo_costo = costo + 1
            else:
                nuevo_costo = costo + 10
            stack.append((next_state, path + [next_state], nuevo_costo))
        Restados_explorados, Racciones, Rcosto = dfs_searchR(env, goal, stack, visited)
        if Restados_explorados is not None:
            return Restados_explorados, Racciones, Rcosto
    return None, None, None

def limited_dfs_search(env, limit, start, goal):
    env.unwrapped.s = start
    visited = set()
    stack = []
    stack.append((start, [start], 0))  # (estado actual, camino hasta aquí)
    visited.add(start)
    info = env.reset()
    return dfs_searchR(env, limit, goal, stack, visited, 1)

def limited_dfs_searchR(env, limit, goal, stack, visited, estados_explorados):
    current_state, path, costo = stack.pop()
    if current_state == goal:
        print(f"Camino encontrado: {path}")
        return estados_explorados, len(path) - 1, costo
    if len(path) == limit:
        return None, None, None
    for action in range(env.action_space.n):
        env.unwrapped.s = current_state
        next_state, _, _, _, _ = env.step(action)
        if next_state not in visited:
            estados_explorados += 1
            visited.add(next_state)
        # Evitar casilleros 'H' (Hole)
        if next_state not in visited and env.unwrapped.desc.flatten()[next_state] != b'H':
            if action == 0 or action == 2:
                nuevo_costo = costo + 1
            else:
                nuevo_costo = costo + 10
            stack.append((next_state, path + [next_state], nuevo_costo))
        Restados_explorados, Racciones, Rcosto = dfs_searchR(env, goal, stack, visited)
        if Restados_explorados is not None:
            return Restados_explorados, Racciones, Rcosto
    return None, None, None

def uniform_cost_search(env, start, goal):
    env.unwrapped.s = start
    visited = set()
    heap = []
    heapq.heappush(heap, (0, start, [start]))  # (costo acumulado, estado actual, camino)
    info = env.reset()
    costos = {start: 0}
    estados_explorados = 1
    while heap:
        costo, current_state, path = heapq.heappop(heap)
        if current_state == goal:
            print(f"Camino encontrado: {path}")
            return estados_explorados, len(path) - 1, costo
        if costo > costos.get(current_state, float('inf')):
            continue
        for action in range(env.action_space.n):
            env.unwrapped.s = current_state
            next_state, _, _, _, _ = env.step(action)
            if next_state not in visited:
                estados_explorados += 1
                visited.add(next_state)
            if env.unwrapped.desc.flatten()[next_state] != b'H':
                # Costo según acción
                if action == 0 or action == 2:
                    new_cost = costo + 1
                else:
                    new_cost = costo + 10
                if next_state in visited:
                    if new_cost < costos.get(next_state, float('inf')):
                        costos[next_state] = new_cost
                heapq.heappush(heap, (new_cost, next_state, path + [next_state]))
    print("No se encontró camino al objetivo.")
    return None, None, None

def main():
    env, start, goal = deterministic_random_100_environment()
    #random_search(env, start, goal)
    bfs_search(env, start, goal)

if __name__ == "__main__":
    main()
