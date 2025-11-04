try:
    import gymnasium as gym
    from gymnasium import wrappers
except ModuleNotFoundError:
    gym = None
    wrappers = None

import sys

sys.setrecursionlimit(25000)

from random_map import generate_random_map_custom 
from collections import deque
import heapq

def deterministic_random_100_environment():
    env, start, goal = generate_random_map_custom(100, 0.92)
    if wrappers is not None:
        env = wrappers.TimeLimit(env, 1000)
    elif hasattr(env, "max_steps"):
        env.max_steps = 1000
    return env, start, goal

def random_search(env, start, goal, max_steps=1000, verbose=False):
    env.unwrapped.s = start
    env.reset()

    done = False
    truncated = False
    costo = 0
    acciones = 0

    if verbose:
        print("Posición inicial forzada:", start)

    while not (done or truncated):
        action = env.action_space.sample()
        acciones += 1

        if action == 0 or action == 2:
            costo += 1
        else:
            costo += 10

        next_state, reward, done, truncated_flag, _ = env.step(action)
        truncated = truncated_flag or acciones >= max_steps

        if verbose:
            print(f"Acción: {action}, Nuevo estado: {next_state}, Recompensa: {reward}")

        if reward == 1.0:
            if verbose:
                print(f"¿Ganó? (encontró el objetivo): {done}")
            return acciones + 1, acciones, costo

    if verbose:
        print("No se encontró camino al objetivo (búsqueda aleatoria).")

    return None, None, None

def bfs_search(env, start, goal, verbose=False):
    env.unwrapped.s = start
    env.reset()

    visited = {start}
    queue = deque()
    queue.append((start, 0, 0))  # (estado, acciones acumuladas, costo acumulado)
    estados_explorados = 1
    while queue:
        current_state, acciones, costo = queue.popleft()
        if current_state == goal:
            if verbose:
                print(f"Objetivo alcanzado con {acciones} acciones y costo {costo}")
            return estados_explorados, acciones, costo
        for action in range(env.action_space.n):
            env.unwrapped.s = current_state
            next_state, _, _, _, _ = env.step(action)

            # Evitar casilleros 'H' (Hole)
            if env.unwrapped.desc.flatten()[next_state] == b'H':
                continue

            if next_state in visited:
                continue

            visited.add(next_state)
            estados_explorados += 1

            if action == 0 or action == 2:
                acciones_sig = acciones + 1
                nuevo_costo = costo + 1
            else:
                acciones_sig = acciones + 1
                nuevo_costo = costo + 10

            queue.append((next_state, acciones_sig, nuevo_costo))
    if verbose:
        print("No se encontró camino al objetivo.")
    return None, None, None

def dfs_search(env, start, goal, verbose=False):
    env.unwrapped.s = start
    env.reset()

    visited = {start}
    estados_explorados = 1

    def dfs(current_state, acciones, costo):
        nonlocal estados_explorados

        if current_state == goal:
            if verbose:
                print(f"Objetivo alcanzado con {acciones} acciones y costo {costo}")
            return estados_explorados, acciones, costo

        for action in range(env.action_space.n):
            env.unwrapped.s = current_state
            next_state, _, _, _, _ = env.step(action)

            if env.unwrapped.desc.flatten()[next_state] == b'H':
                continue

            if next_state in visited:
                continue

            visited.add(next_state)
            estados_explorados += 1

            if action == 0 or action == 2:
                nuevo_costo = costo + 1
                nuevas_acciones = acciones + 1
            else:
                nuevo_costo = costo + 10
                nuevas_acciones = acciones + 1

            resultado = dfs(next_state, nuevas_acciones, nuevo_costo)
            if resultado is not None:
                return resultado

        return None

    resultado = dfs(start, 0, 0)
    if resultado is not None:
        return resultado

    if verbose:
        print("No se encontró camino al objetivo.")
    return None, None, None


def limited_dfs_search(env, limit, start, goal, verbose=False):
    env.unwrapped.s = start
    env.reset()

    mejores_profundidades = {start: 0}
    estados_explorados = 1

    def dfs_limit(current_state, acciones, costo, profundidad, en_camino):
        nonlocal estados_explorados
        if current_state == goal:
            if verbose:
                print(f"Objetivo alcanzado con {acciones} acciones y costo {costo}")
            return estados_explorados, acciones, costo

        if profundidad >= limit:
            return None

        for action in range(env.action_space.n):
            env.unwrapped.s = current_state
            next_state, _, _, _, _ = env.step(action)

            if env.unwrapped.desc.flatten()[next_state] == b'H':
                continue

            if next_state in en_camino:
                continue

            if action == 0 or action == 2:
                paso = 1
            else:
                paso = 10
            nuevo_costo = costo + paso
            nuevas_acciones = acciones + 1

            profundidad_nueva = profundidad + 1
            mejor_prev = mejores_profundidades.get(next_state)
            if mejor_prev is not None and profundidad_nueva >= mejor_prev:
                continue

            mejores_profundidades[next_state] = profundidad_nueva
            estados_explorados += 1

            en_camino.add(next_state)
            resultado = dfs_limit(next_state, nuevas_acciones, nuevo_costo, profundidad + 1, en_camino)
            en_camino.remove(next_state)

            if resultado is not None:
                return resultado

        return None

    resultado = dfs_limit(start, 0, 0, 0, {start})
    if resultado is not None:
        return resultado

    if verbose:
        print("No se encontró camino al objetivo dentro del límite.")
    return None, None, None

def uniform_cost_search(env, start, goal, verbose=False):
    env.unwrapped.s = start
    heap = []
    heapq.heappush(heap, (0, 0, start))  # (costo acumulado, acciones, estado)
    env.reset()
    costos = {start: 0}
    acciones_minimas = {start: 0}
    estados_explorados = 0
    while heap:
        costo, acciones, current_state = heapq.heappop(heap)
        if costo > costos.get(current_state, float("inf")):
            continue

        estados_explorados += 1

        if current_state == goal:
            if verbose:
                print(f"Objetivo alcanzado con {acciones} acciones y costo {costo}")
            return estados_explorados, acciones, costo

        for action in range(env.action_space.n):
            env.unwrapped.s = current_state
            next_state, _, _, _, _ = env.step(action)
            if env.unwrapped.desc.flatten()[next_state] != b'H':
                # Costo según acción
                if action == 0 or action == 2:
                    new_cost = costo + 1
                    new_actions = acciones + 1
                else:
                    new_cost = costo + 10
                    new_actions = acciones + 1

                if new_cost < costos.get(next_state, float("inf")):
                    costos[next_state] = new_cost
                    acciones_minimas[next_state] = new_actions
                    heapq.heappush(heap, (new_cost, new_actions, next_state))
                elif new_cost == costos.get(next_state) and new_actions < acciones_minimas.get(next_state, float("inf")):
                    acciones_minimas[next_state] = new_actions
                    heapq.heappush(heap, (new_cost, new_actions, next_state))
    if verbose:
        print("No se encontró camino al objetivo.")
    return None, None, None

def a_star_search_1(env, start, goal, verbose=False):
    def heuristic(state, goal):
        x1, y1 = divmod(state, env.unwrapped.ncol)
        x2, y2 = divmod(goal, env.unwrapped.ncol)
        return abs(x1 - x2) + abs(y1 - y2)

    env.unwrapped.s = start
    costos = {start: 0}
    heap = []
    heapq.heappush(heap, (heuristic(start, goal), 0, 0, start))  # (f, g, acciones, estado)
    visited = set()
    estados_explorados = 0

    while heap:
        f, g, acciones, current_state = heapq.heappop(heap)

        if current_state in visited:
            continue
        visited.add(current_state)
        estados_explorados += 1

        if current_state == goal:
            if verbose:
                print(f"Objetivo alcanzado con {acciones} acciones y costo {g}")
            return estados_explorados, acciones, g

        for action in range(env.action_space.n):
            env.unwrapped.s = current_state
            next_state, _, _, _, _ = env.step(action)

            if env.unwrapped.desc.flatten()[next_state] == b'H':  # Hielo => hueco, ignorar
                continue

            new_g = g + 1
            nuevas_acciones = acciones + 1
            if new_g < costos.get(next_state, float('inf')):
                costos[next_state] = new_g
                new_f = new_g + heuristic(next_state, goal)
                heapq.heappush(heap, (new_f, new_g, nuevas_acciones, next_state))

    if verbose:
        print("No se encontró camino al objetivo.")
    return None, None, None

def a_star_search_2(env, start, goal, verbose=False):
    def heuristic(state, goal):
        x1, y1 = divmod(state, env.unwrapped.ncol)
        x2, y2 = divmod(goal, env.unwrapped.ncol)
        return abs(x1 - x2) * 10 + abs(y1 - y2)

    env.unwrapped.s = start
    costos = {start: 0}
    heap = []
    heapq.heappush(heap, (heuristic(start, goal), 0, 0, start))  # (f, g, acciones, estado)
    visited = set()
    estados_explorados = 0

    while heap:
        f, g, acciones, current_state = heapq.heappop(heap)

        if current_state in visited:
            continue
        visited.add(current_state)
        estados_explorados += 1

        if current_state == goal:
            if verbose:
                print(f"Objetivo alcanzado con {acciones} acciones y costo {g}")
            return estados_explorados, acciones, g

        for action in range(env.action_space.n):
            env.unwrapped.s = current_state
            next_state, _, _, _, _ = env.step(action)

            if env.unwrapped.desc.flatten()[next_state] == b'H':  # Hielo => hueco, ignorar
                continue

            if action == 0 or action == 2:
                new_g = g + 1
                nuevas_acciones = acciones + 1
            else: 
                new_g = g + 10
                nuevas_acciones = acciones + 1
                
            if new_g < costos.get(next_state, float('inf')):
                costos[next_state] = new_g
                new_f = new_g + heuristic(next_state, goal)
                heapq.heappush(heap, (new_f, new_g, nuevas_acciones, next_state))

    if verbose:
        print("No se encontró camino al objetivo.")
    return None, None, None

def main():
    env, start, goal = deterministic_random_100_environment()
    #random_search(env, start, goal)
    #bfs_search(env, start, goal)
    #_, _, _ = uniform_cost_search(env, start, goal)

if __name__ == "__main__":
    main()
