2.10 Consider a modified version of the vacuum environment in Exercise 2.8, in which the
agent is penalized one point for each movement.
    a. Can a simple reflex agent be perfectly rational for this environment? Explain.
    b. What about a reflex agent with state? Design such an agent.
    c. How do your answers to a and b change if the agent’s percepts give it the clean/dirty
    status of every square in the environment?

2.11 Consider a modified version of the vacuum environment in Exercise 2.8, in which the
geography of the environment—its extent, boundaries, and obstacles—is unknown, as is the
initial dirt configuration. (The agent can go Up and Down as well as Left and Right.)
    a. Can a simple reflex agent be perfectly rational for this environment? Explain.
    b. Can a simple reflex agent with a randomized agent function outperform a simple reflex
    agent? Design such an agent and measure its performance on several environments.
    c. Can you design an environment in which your randomized agent will perform poorly?
    Show your results.
    d. Can a reflex agent with state outperform a simple reflex agent? Design such an agent
    and measure its performance on several environments. Can you design a rational agent
    of this type?

2.10.
a.Un agente reflexivo simple no podria ser perfectamente racional en un entorno en el cual se le penalice por cada movimiento que realice. Un agente reflexivo simple no recuerda sus movimientos anteriores. Solo sabe adonde está, sigue una serie de reglas que se le hayan asignado y ejecuta una acción. No podría tratar de minimizar los movimientos recordando, por ejemplo, si ya había estado en el casillero de la derecha. 

b.Uno con estado si podría, ya que podría recordar por que casilleros ya ha estado, lo que podría minimizar la cantidad de movimientos que realice. Un ejemplo podría ser un agente que realiza movimientos aleatorios (arriba, derecha, izquierda, abajo) y que si se encuentra en un casillero sucio, limpia. Este mismo tiene memoria de en que casilleros ya ha estado. Si al momento de moverse, ya ha pasado por uno de los casilleros limítrofes (por ejemplo el de la derecha), este es descartado de las opciones a realizar aleatoriamente(en el ejemplo, quedarían las opciones de arriba, abajo e izquierda).

c.En ese caso, el agente debería calcular la distancia mínima a cada uno de los casilleros sucios al comienzo y luego de haber limpiado algún casillero. Luego, dirigirse al más cercano, de la forma más optima posible. Bueno, esa es una solución rápida que se me ocurre para minimizar los movimientos. 

2.11
a. Sigue sin poder ser completamente racional ya que no recuerda por donde ha pasado y, de esta forma, tampoco va a poder determinar en algun momento el tamaño del entorno. 

b.Podría tener mejores resultados, pero va a depender mucho del tamaño del entorno y de los resultados aleatorios de cada uno. Independientemente del entorno, si solo hay un casillero sucio y el agente empieza justo ahí, el agente aleatorio podrá, a lo sumo, igualarlo en cantidad de acciones. Dependerá de que justo la acción que salga aleatoria sea la de limpiar. Pero mientras más grande sea el entorno y mayor sea la cantidad de celdas sucias, las probabilidades de que el agente aleatorio le gane en performance al reflexivo simple son cada vez menores. 

c.En un entorno muy grande, donde solo hay un casillero sucio y el agente no se encuentra cerca del mismo, las probabilidades de que al agente le tome muchísimas acciones limpiar esa celda son muy altas. Al ser aleatorio, es muy difícil que logre caer en esa celda. Pero no solo eso, sino que, cuando caiga, justo la decisión aleatoria sea la de limpiar. Si no es esta la decisión, deberá volver aleatoriamente y repetir el proceso. 

d.El que mencioné anteriormente, el agente que realiza movimientos aleatorios (arriba, derecha, izquierda, abajo) y que si se encuentra en un casillero sucio, limpia. Este mismo tiene memoria de en que casilleros ya ha estado. Si al momento de moverse, ya ha pasado por uno de los casilleros limítrofes (por ejemplo el de la derecha), este es descartado de las opciones a realizar aleatoriamente(en el ejemplo, quedarían las opciones de arriba, abajo e izquierda). En entornos amplios, la diferencia de performance y acciones realizadas va a ser abismal. Lógicamente, en entornos más pequeños se van a ver más emparejados, debido a la aleatoriedad de movimientos de ambos, aunque el de estados va a ir descartando algunas de las opciones que deja a la aleatoriedad. 