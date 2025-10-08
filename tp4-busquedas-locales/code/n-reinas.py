def get_neighbors(s):
        neighbors = []
        for col in range(len(s)):
            for row in range(len(s)):
                if s[col] != row:
                    neighbor = list(s)
                    neighbor[col] = row
                    neighbors.append(tuple(neighbor))
        return neighbors

def heuristic(s):
    h = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if s[i] == s[j] or abs(s[i] - s[j]) == abs(i - j):
                h += 1
    return h

def hill_climbing(state, max_estados_explorados, trace=None):
    current = state
    current_h = heuristic(current)
    if trace is not None:
        trace.append(current_h)
    estados_explorados = 1

    while estados_explorados < max_estados_explorados:
        if current_h == 0:
            break
        neighbors = get_neighbors(current)
        if not neighbors:
            break
        if estados_explorados + len(neighbors) > max_estados_explorados:
            neighbors = neighbors[:max_estados_explorados - estados_explorados]
        estados_explorados += len(neighbors)
        neighbor = min(neighbors, key=heuristic)
        neighbor_h = heuristic(neighbor)
        if neighbor_h >= current_h:
            break
        current = neighbor
        current_h = neighbor_h
        if trace is not None:
            trace.append(current_h)

    return current, current_h, estados_explorados

def simulated_annealing(state, max_estados_explorados, initial_temp=1000, cooling_rate=0.99, trace=None):
    import math
    import random

    current = state
    current_h = heuristic(current)
    if trace is not None:
        trace.append(current_h)
    temp = initial_temp
    estados_explorados = 1

    while estados_explorados < max_estados_explorados and temp > 1:
        if current_h == 0:
            break
        neighbors = get_neighbors(current)
        if not neighbors:
            break
        neighbor = random.choice(neighbors)
        neighbor_h = heuristic(neighbor)
        estados_explorados += 1
        delta_e = neighbor_h - current_h

        if delta_e < 0 or random.uniform(0, 1) < math.exp(-delta_e / temp):
            current = neighbor
            current_h = neighbor_h

        if trace is not None:
            trace.append(current_h)
        temp *= cooling_rate

    return current, current_h, estados_explorados

def genetic_algorithm(individual, max_estados_explorados, population_size, mutation_rate = 0.1, trace=None):
    import random

    def initialize_population(size, n):
        pop = set()
        while len(pop) < size:
            individual = tuple(random.randint(0, n - 1) for _ in range(n))
            pop.add(individual)
        return list(pop)

    def select_parents(population):
        weights = [1 / (1 + heuristic(ind)) for ind in population]
        total = sum(weights)
        probabilities = [w / total for w in weights]
        return random.choices(population, probabilities, k=2)

    def order_crossover(parent1, parent2):
        n = len(parent1)
        i, j = sorted(random.sample(range(n), 2))
        child = [None] * n
        child[i:j] = parent1[i:j]

        fill_positions = [idx for idx in range(n) if idx < i or idx >= j]
        fill_iter = iter(fill_positions)

        for gene in parent2[j:] + parent2[:j]:
            try:
                position = next(fill_iter)
            except StopIteration:
                break
            child[position] = gene

        return tuple(child)

    def crossover(parent1, parent2):
        child1 = order_crossover(parent1, parent2)
        child2 = order_crossover(parent2, parent1)
        return child1, child2

    def mutate(individual):
        if random.random() < mutation_rate:
            if len(individual) > 1:
                start, end = sorted(random.sample(range(len(individual)), 2))
                individual = list(individual)
                individual[start:end + 1] = reversed(individual[start:end + 1])
                return tuple(individual)
        return individual
    
    if population_size == None:
        population_size = len(individual) * 8

    current_population = initialize_population(population_size - 1, len(individual))
    current_population.append(individual)
    best_individual = min(current_population, key=heuristic)
    best_h = heuristic(best_individual)
    if trace is not None:
        trace.append(best_h)
    estados_explorados = len(current_population)

    while estados_explorados < max_estados_explorados:
        if best_h == 0:
            break
        next_population = []
        while len(next_population) < len(current_population) and estados_explorados < max_estados_explorados:
            parent1, parent2 = select_parents(current_population)
            child1, child2 = crossover(parent1, parent2)
            next_population.append(mutate(child1))
            estados_explorados += 1
            if estados_explorados == max_estados_explorados:
                break
            next_population.append(mutate(child2))
            estados_explorados += 1
        if not next_population:
            break
        tamano = len(current_population) if len(next_population) > len(current_population) else len(next_population)
        next_population.sort(key = heuristic)
        current_population = next_population[:tamano]
        best_individual = current_population[0]
        best_h = heuristic(best_individual)
        if trace is not None:
            trace.append(best_h)

    return best_individual, best_h, estados_explorados

def random_algorithm(state, max_estados_explorados, trace=None):
    import random

    current = state
    current_h = heuristic(current)
    if trace is not None:
        trace.append(current_h)
    estados_explorados = 1
    n = len(state)

    while estados_explorados < max_estados_explorados:
        if current_h == 0:
            break
        candidate = tuple(random.randint(0, n - 1) for _ in range(n))
        estados_explorados += 1
        candidate_h = heuristic(candidate)
        if candidate_h < current_h:
            current = candidate
            current_h = candidate_h
        if trace is not None:
            trace.append(current_h)

    return current, current_h, estados_explorados
