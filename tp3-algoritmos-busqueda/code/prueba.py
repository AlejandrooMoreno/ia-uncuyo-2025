import gymnasium as gym

env = gym.make('FrozenLake-v1', render_mode='human')
               
print("Número de estados:", env.observation_space.n)
print("Número de acciones:", env.action_space.n)

state = env.reset()
print("Posición inicial del agente:", state[0])
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