"""Resolución del problema de las N-reinas con técnicas de CSP.

Se implementan dos variantes:
    a) Backtracking clásico verificando restricciones.
    b) Forward checking manteniendo los dominios actualizados.

La idea es que el código quede sencillo de leer y en línea con el estilo del TP.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

# Una solución se guarda como tupla donde el índice es la columna y el valor la fila.
Solution = Tuple[int, ...]


@dataclass
class BusquedaStats:
    """Pequeño contenedor para registrar métricas de búsqueda."""

    nodos_explorados: int = 0

    def registrar_nodo(self) -> None:
        self.nodos_explorados += 1


# ---------------------------------------------------------------------------
# Utilidades comunes
# ---------------------------------------------------------------------------

def crear_dominios(n: int) -> List[Set[int]]:
    """Devuelve una lista de dominios con todas las filas posibles para cada columna."""
    return [set(range(n)) for _ in range(n)]


def es_consistente(tablero: Dict[int, int], columna: int, fila: int) -> bool:
    """Verifica que colocar una reina en (columna, fila) no rompa restricciones."""
    for otra_columna, otra_fila in tablero.items():
        if fila == otra_fila:  # misma fila
            return False
        if abs(otra_columna - columna) == abs(otra_fila - fila):  # misma diagonal
            return False
    return True


def guardar_solucion(tablero: Dict[int, int], n: int) -> Solution:
    """Convierte el tablero actual en una tupla ordenada por columna."""
    return tuple(tablero[col] for col in range(n))


def imprimir_solucion(solucion: Solution) -> str:
    """Entrega una representación visual básica del tablero."""
    n = len(solucion)
    filas = []
    for fila in range(n):
        fila_actual = []
        for col in range(n):
            fila_actual.append("Q" if solucion[col] == fila else ".")
        filas.append(" ".join(fila_actual))
    return "\n".join(filas)


# ---------------------------------------------------------------------------
# Backtracking
# ---------------------------------------------------------------------------

def n_reinas_backtracking(
    n: int,
    buscar_todas: bool = True,
    rng: Optional[random.Random] = None,
    stats: Optional[BusquedaStats] = None,
) -> List[Solution]:
    """Resuelve N-reinas con backtracking puro."""
    tablero: Dict[int, int] = {}
    soluciones: List[Solution] = []
    contador = stats or BusquedaStats()

    def backtrack(columna: int) -> bool:
        if columna == n:
            soluciones.append(guardar_solucion(tablero, n))
            return not buscar_todas  # detener si solo queremos la primera

        filas = list(range(n))
        if rng is None:
            filas.sort()
        else:
            rng.shuffle(filas)

        for fila in filas:
            contador.registrar_nodo()

            if not es_consistente(tablero, columna, fila):
                continue

            tablero[columna] = fila
            detener = backtrack(columna + 1)
            del tablero[columna]

            if detener:
                return True
        return False

    backtrack(0)
    return soluciones


# ---------------------------------------------------------------------------
# Forward checking
# ---------------------------------------------------------------------------

def actualizar_dominios(
    dominios: List[Set[int]],
    columna_actual: int,
    fila_actual: int,
) -> Optional[List[Set[int]]]:
    """Propaga las restricciones desde la asignación dada.

    Devuelve nuevos dominios si la asignación es posible o `None` cuando algún
    dominio queda vacío (inconsistencia detectada).
    """
    nuevos_dominios = [dom.copy() for dom in dominios]

    for futura_columna in range(columna_actual + 1, len(dominios)):
        dominio = nuevos_dominios[futura_columna]
        distancia = futura_columna - columna_actual

        # Eliminar fila actual y diagonales amenazadas.
        dominio.discard(fila_actual)
        dominio.discard(fila_actual + distancia)
        dominio.discard(fila_actual - distancia)

        if not dominio:
            return None

    nuevos_dominios[columna_actual] = {fila_actual}
    return nuevos_dominios


def n_reinas_forward_checking(
    n: int,
    buscar_todas: bool = True,
    rng: Optional[random.Random] = None,
    stats: Optional[BusquedaStats] = None,
) -> List[Solution]:
    """Resuelve N-reinas aplicando forward checking en cada asignación."""
    tablero: Dict[int, int] = {}
    soluciones: List[Solution] = []
    contador = stats or BusquedaStats()

    def forward(columna: int, dominios: List[Set[int]]) -> bool:
        if columna == n:
            soluciones.append(guardar_solucion(tablero, n))
            return not buscar_todas

        filas = list(dominios[columna])
        if rng is None:
            filas.sort()
        else:
            rng.shuffle(filas)

        for fila in filas:
            contador.registrar_nodo()

            if not es_consistente(tablero, columna, fila):
                continue

            nuevos_dominios = actualizar_dominios(dominios, columna, fila)
            if nuevos_dominios is None:
                continue

            tablero[columna] = fila
            detener = forward(columna + 1, nuevos_dominios)
            del tablero[columna]

            if detener:
                return True

        return False

    forward(0, crear_dominios(n))
    return soluciones


# ---------------------------------------------------------------------------
# Pequeño ejecutable
# ---------------------------------------------------------------------------

def resolver_y_mostrar(n: int) -> None:
    print(f"Resolviendo {n}-reinas con backtracking...")
    backtracking = n_reinas_backtracking(n, buscar_todas=False)
    if backtracking:
        print(imprimir_solucion(backtracking[0]))
    else:
        print("Sin solución para backtracking.")

    print("\nResolviendo con forward checking...")
    forward = n_reinas_forward_checking(n, buscar_todas=False)
    if forward:
        print(imprimir_solucion(forward[0]))
    else:
        print("Sin solución para forward checking.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Resolver N-reinas usando CSP.")
    parser.add_argument("n", type=int, help="Tamaño del tablero (número de reinas).")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Encuentra todas las soluciones en lugar de detenerse en la primera.",
    )
    opciones = parser.parse_args()

    soluciones_backtracking = n_reinas_backtracking(opciones.n, buscar_todas=opciones.all)
    soluciones_forward = n_reinas_forward_checking(opciones.n, buscar_todas=opciones.all)

    print(f"Backtracking encontró {len(soluciones_backtracking)} solución(es).")
    if soluciones_backtracking:
        print(imprimir_solucion(soluciones_backtracking[0]))

    print(f"\nForward checking encontró {len(soluciones_forward)} solución(es).")
    if soluciones_forward:
        print(imprimir_solucion(soluciones_forward[0]))
