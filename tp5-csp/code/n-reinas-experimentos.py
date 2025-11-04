"""Ejecutor de experimentos para comparar algoritmos de N-reinas (TP5).

Corre cada algoritmo 30 veces (cambiando la semilla) sobre tableros de tamaño
4, 8 y 10. Se registran tiempos, nodos explorados y si se halló solución.
Genera:
    - Un CSV con todos los resultados en `tp5-Nreinas.csv`.
    - Estadísticas resumidas impresas por consola.
    - Boxplots de tiempos y nodos guardados en `images/`.
"""

from __future__ import annotations

import csv
import importlib.util
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:  # matplotlib es opcional para gráficos
    plt = None

SEEDS = list(range(30))
TAMANIOS = [4, 8, 10]

BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "tp5-Nreinas.csv"
IMAGES_DIR = BASE_DIR / "images"

MODULO_CSP = Path(__file__).with_name("n-reinas-csp.py")
spec = importlib.util.spec_from_file_location("n_reinas_csp", MODULO_CSP)
if spec is None or spec.loader is None:
    raise ImportError(f"No se pudo cargar el módulo desde {MODULO_CSP}")
n_reinas_csp = importlib.util.module_from_spec(spec)
sys.modules["n_reinas_csp"] = n_reinas_csp
spec.loader.exec_module(n_reinas_csp)

BusquedaStats = n_reinas_csp.BusquedaStats
n_reinas_backtracking = n_reinas_csp.n_reinas_backtracking
n_reinas_forward_checking = n_reinas_csp.n_reinas_forward_checking

ALGORITMOS = {
    "backtracking": n_reinas_backtracking,
    "forward_checking": n_reinas_forward_checking,
}


def ejecutar_experimentos() -> List[Dict[str, object]]:
    resultados: List[Dict[str, object]] = []

    for n in TAMANIOS:
        for nombre, funcion in ALGORITMOS.items():
            for seed in SEEDS:
                rng = random.Random(seed)
                stats = BusquedaStats()

                inicio = time.time()
                soluciones = funcion(
                    n,
                    buscar_todas=False,
                    rng=rng,
                    stats=stats,
                )
                tiempo_total = time.time() - inicio

                exito = 1 if soluciones else 0
                registro = {
                    "algoritmo": nombre,
                    "n": n,
                    "semilla": seed,
                    "exito": exito,
                    "tiempo_segundos": tiempo_total,
                    "nodos_explorados": stats.nodos_explorados,
                }
                resultados.append(registro)

    return resultados


def guardar_csv(resultados: Iterable[Dict[str, object]]) -> None:
    campos = ["algoritmo", "n", "semilla", "exito", "tiempo_segundos", "nodos_explorados"]
    with CSV_PATH.open("w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in resultados:
            escritor.writerow(fila)


def resumen_estadistico(resultados: List[Dict[str, object]]) -> None:
    print("\n=== Estadísticas por algoritmo y tamaño ===")
    for n in TAMANIOS:
        print(f"\nTablero de {n} reinas")
        for nombre in ALGORITMOS:
            datos = [r for r in resultados if r["n"] == n and r["algoritmo"] == nombre]
            if not datos:
                continue

            exitos = [r for r in datos if r["exito"] == 1]
            porcentaje = (len(exitos) / len(datos)) * 100

            tiempos = [r["tiempo_segundos"] for r in exitos]
            nodos = [r["nodos_explorados"] for r in exitos]

            tiempo_promedio, tiempo_std = _promedio_y_std(tiempos)
            nodos_promedio, nodos_std = _promedio_y_std(nodos)

            print(f"  - {nombre}:")
            print(f"      Éxito: {porcentaje:.2f}% ({len(exitos)}/{len(datos)})")
            if tiempos:
                print(f"      Tiempo medio: {tiempo_promedio:.4f}s ± {tiempo_std:.4f}s")
            else:
                print("      Tiempo medio: n/d")
            if nodos:
                print(f"      Nodos medios: {nodos_promedio:.2f} ± {nodos_std:.2f}")
            else:
                print("      Nodos medios: n/d")


def _promedio_y_std(valores: List[float]) -> Tuple[float, float]:
    if not valores:
        return 0.0, 0.0
    if len(valores) == 1:
        return valores[0], 0.0
    return statistics.mean(valores), statistics.stdev(valores)


def generar_boxplots(resultados: List[Dict[str, object]]) -> None:
    if plt is None:
        print("\nNo se generaron boxplots: matplotlib no está disponible.")
        return

    IMAGES_DIR.mkdir(exist_ok=True)

    for n in TAMANIOS:
        datos_n = [r for r in resultados if r["n"] == n]
        if not datos_n:
            continue

        etiquetas = list(ALGORITMOS.keys())

        # Boxplot de tiempos
        fig, ax = plt.subplots()
        series_tiempos = [
            [r["tiempo_segundos"] for r in datos_n if r["algoritmo"] == nombre]
            for nombre in etiquetas
        ]
        ax.boxplot(series_tiempos, labels=etiquetas)
        ax.set_title(f"Tiempos de ejecución - {n} reinas")
        ax.set_ylabel("Tiempo (segundos)")
        fig.tight_layout()
        fig.savefig(IMAGES_DIR / f"boxplot_tiempos_{n}.png", dpi=150)
        plt.close(fig)

        # Boxplot de nodos
        fig, ax = plt.subplots()
        series_nodos = [
            [r["nodos_explorados"] for r in datos_n if r["algoritmo"] == nombre]
            for nombre in etiquetas
        ]
        ax.boxplot(series_nodos, labels=etiquetas)
        ax.set_title(f"Nodos explorados - {n} reinas")
        ax.set_ylabel("Cantidad de nodos")
        fig.tight_layout()
        fig.savefig(IMAGES_DIR / f"boxplot_nodos_{n}.png", dpi=150)
        plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(exist_ok=True)
    resultados = ejecutar_experimentos()
    guardar_csv(resultados)
    resumen_estadistico(resultados)
    generar_boxplots(resultados)
    print(f"\nResultados guardados en: {CSV_PATH}")
    print(f"Gráficos disponibles en: {IMAGES_DIR}")


if __name__ == "__main__":
    main()
