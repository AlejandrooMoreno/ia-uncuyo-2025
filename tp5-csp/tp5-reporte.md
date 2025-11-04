1-

Variables
Hay 81 variables, una por cada celda del tablero.

Dominios:
Cada variable puede tomar un valor del 1 al 9. Si una celda viene dada por el enunciado, el dominio de esa variable queda fijado a ese único valor. Después de fijar las pistas, se hace una propagación inicial eliminando esos valores de los dominios de las celdas que comparten la misma fila, columna o caja 3×3.

Restricciones:
El Sudoku exige que no se repitan dígitos en tres tipos de unidades:

Filas: en cada fila, las 9 celdas deben contener todos dígitos diferentes.

Columnas: lo mismo para cada columna.

Cajas 3×3: lo mismo para cada una de las 9 cajas.

En términos de CSP:

Como 27 restricciones globales de todos diferentes (9 de filas, 9 de columnas, 9 de cajas), cada una aplicada a 9 variables.

En un 9×9, cada celda tiene 20 vecinos y, en total, hay 810 pares restringidos distintos.

Grafo de restricciones:
Un grafo con una variable por nodo y una arista cuando dos celdas se “ven” (misma fila, columna o caja), obtenes 81 nodos; cada nodo tiene grado 20 y el grafo contiene esas 810 aristas de “distinto de”.

Propagación:
Con las restricciones anteriores se realiza propagación para ir reduciendo dominios:

Si una variable queda con un único valor posible, se asigna ese valor y se vuelve a propagar.

En una unidad, si un dígito solo puede ir en una de sus nueve celdas, entonces esa celda debe tomar ese dígito.

Usar la restricción global “todos-diferentes” permite detectar estos casos automáticamente y, en general, elimina más valores que solo aplicar diferente por pares.

Búsqueda:
Si después de propagar siguen quedando celdas con varios valores posibles, se usa backtracking guiado por heurísticas:

MRV (mínimos valores restantes): elegir primero la celda con menor dominio.

Desempate por grado: si hay empate, elegir la celda con más vecinos no asignados.

LCV (valor menos restrictivo): probar primero el dígito que descarta menos opciones a los vecinos.
Tras cada decisión se vuelve a propagar; si algún dominio queda vacío, se deshace la decisión y se prueba el siguiente valor.

Entrada y salida del CSP:

Entrada: el tablero inicial con sus pistas, que fijan dominios unitarios y disparan la propagación.

Salida: una asignación completa de las 81 variables con dígitos 1–9 que satisface todas las restricciones.

Números útiles del 9×9

81 variables, dominios iniciales 1–9 (salvo pistas).

27 unidades (9 filas, 9 columnas, 9 cajas).

27 restricciones “todos-diferentes”.

20 vecinos por celda; 810 pares distintos en total.


2-
Dominio inicial:
WA={r}     NT={r,g,b}   Q={r,g,b}
SA={r,g,b} NSW={r,g,b}  V={b}
T={r,g,b}

REVISE(NT,WA): quita r de NT → NT={g,b}

REVISE(SA,WA): quita r de SA → SA={g,b}

REVISE(SA,V): quita b de SA → SA={g}

REVISE(NSW,V): quita b de NSW → NSW={r,g}

Estado:
WA={r}   NT={g,b}   Q={r,g,b}
SA={g}   NSW={r,g}  V={b}
T={r,g,b}

SA es {g}, así que sus vecinos no pueden ser g:

REVISE(NT,SA): quita g de NT → NT={b}

REVISE(Q,SA): quita g de Q → Q={r,b}

REVISE(NSW,SA): quita g de NSW → NSW={r}

WA={r}   NT={b}   Q={r,b}
SA={g}   NSW={r}  V={b}
T={r,g,b}

REVISE(Q,NSW): quita r de Q → Q={b}

WA={r}   NT={b}   Q={b}
SA={g}   NSW={r}  V={b}
T={r,g,b}

REVISE(Q,NT): Q solo tiene b, y NT={b}; no hay valor en Q que difiera de NT → se elimina b de Q → Q=∅.

3-
El peor caso es O(n d^3).
AC-3 revisa arcos dirigidos; en un árbol hay e=n−1 aristas no dirigidas ⇒ 2e=O(n) arcos.

Cada operación REVISE(X,Y) cuesta O(d^2).

Un arco puede volver a la cola hasta O(d) veces (cada vez que se elimina un valor del vecino), dando el bound clásico O(e d^3).

Con e=n−1, resulta O(n d^3).

5-
Sin contar el algoritmo Random del tp4.
El porcentaje de éxito en los algoritmos del tp4 era de aproximádamente 20%, mientras que la de los algoritmos del tp5 es del 100%. Siempre encuentra la solución. Y es notoria la diferencia. 

Ambos del tp5 exploran menos estados que los del tp4, FC explora aún menos que BT.

Los del tp5 son más rápidos en ejecución que los del tp4. FC es el más rápido de todos.

En conclusión: Así como están implementados, la mejor elección es la de Forward Checking.