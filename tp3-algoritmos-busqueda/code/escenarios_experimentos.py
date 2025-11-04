import csv
import json
import os
import statistics
import time
from collections import defaultdict
from pathlib import Path

from busquedas import (
    deterministic_random_100_environment,
    random_search,
    bfs_search,
    dfs_search,
    limited_dfs_search,
    uniform_cost_search,
    a_star_search_1,
    a_star_search_2,
)
from random_map import SimpleFrozenLakeEnv, gym

try:
    from gymnasium import wrappers
except ModuleNotFoundError:  # Gymnasium no disponible en algunos entornos
    wrappers = None


TOTAL_RUNS = int(os.environ.get("RUN_TOTAL", 30))
DFS_LIMITS = [50, 75, 100]

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_CSV = BASE_DIR / "resultados_escenarios.csv"
STATS_JSON = BASE_DIR / "estadisticas_escenarios.json"
IMAGES_DIR = BASE_DIR / "images"

ALGORITHMS = [
    ("RANDOM", lambda env, start, goal: random_search(env, start, goal, verbose=False), {1, 2}),
    ("BFS", bfs_search, {1, 2}),
    ("DFS", dfs_search, {1, 2}),
    *(
        (
            f"DLS-{limit}",
            (lambda depth_limit: (lambda env, start, goal: limited_dfs_search(env, depth_limit, start, goal)))(limit),
            {1, 2},
        )
        for limit in DFS_LIMITS
    ),
    ("UCS", uniform_cost_search, {1, 2}),
    ("A1", a_star_search_1, {1}),
    ("A2", a_star_search_2, {2}),
]


def _build_env(desc_rows, start_idx, goal_idx):
    if gym is not None:
        env = gym.make("FrozenLake-v1", desc=desc_rows).env
        if wrappers is not None:
            env = wrappers.TimeLimit(env, 1000)
        return env

    return SimpleFrozenLakeEnv(desc_rows, start_idx, goal_idx, max_steps=1000)


def _extract_desc_rows(env):
    base = getattr(env, "unwrapped", env)
    desc = getattr(base, "desc", None)
    if desc is None:
        raise ValueError("El entorno no expone la descripción del mapa.")

    flat = desc.flatten()
    size = int(len(flat) ** 0.5)
    rows = []
    for row in range(size):
        start = row * size
        end = start + size
        rows.append("".join(cell.decode("ascii") for cell in flat[start:end]))
    return rows


def _mean_std(values):
    if not values:
        return None, None
    if len(values) == 1:
        return values[0], 0.0
    return statistics.mean(values), statistics.stdev(values)


def _quartiles(values):
    if not values:
        return None
    if len(values) == 1:
        value = values[0]
        return value, value, value, value, value
    sorted_vals = sorted(values)
    q1, q2, q3 = statistics.quantiles(sorted_vals, n=4, method="inclusive")
    median = statistics.median(sorted_vals)
    return min(sorted_vals), q1, median, q3, max(sorted_vals)


def _create_boxplot(data, title, xlabel, output_path):
    cleaned = [(name, [v for v in series if v is not None]) for name, series in data.items()]
    cleaned = [(name, series) for name, series in cleaned if series]
    if not cleaned:
        return

    width = 960
    bar_height = 32
    gap = 16
    left_margin = 220
    right_margin = 80
    top_margin = 70
    bottom_margin = 80

    stats = []
    max_value = 0
    for name, series in cleaned:
        quart = _quartiles(series)
        if quart is None:
            continue
        stats.append((name, quart, len(series)))
        max_value = max(max_value, quart[-1])

    if not stats:
        return

    height = top_margin + bottom_margin + len(stats) * (bar_height + gap) - gap
    usable_width = width - left_margin - right_margin
    scale = usable_width / max_value if max_value else 1

    lines = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}' font-family='sans-serif'>",
        "  <style>text { fill: #1a1a1a; font-size: 16px; } .axis { stroke: #444; stroke-width: 1; } .grid { stroke: #d0d0d0; stroke-dasharray: 4 4; stroke-width: 1; } .box { fill: #74add1; stroke: #225ea8; stroke-width: 1.5; } .median { stroke: #034e7b; stroke-width: 2.5; } .whisker { stroke: #045a8d; stroke-width: 1.5; }</style>",
        "  <rect width='100%' height='100%' fill='white' />",
        f"  <text x='{width/2}' y='{top_margin/2}' text-anchor='middle' font-size='22' font-weight='bold'>{title}</text>",
        f"  <text x='{width/2}' y='{height - 25}' text-anchor='middle' font-size='16'>{xlabel}</text>",
    ]

    divisions = 5
    step = max_value / divisions if divisions else max_value
    tick = step
    while tick <= max_value + 1e-6:
        x = left_margin + tick * scale
        lines.append(f"  <line x1='{x}' y1='{top_margin - 10}' x2='{x}' y2='{height - bottom_margin + 20}' class='grid' />")
        lines.append(f"  <text x='{x}' y='{height - bottom_margin + 40}' text-anchor='middle'>{tick:.1f}</text>")
        tick += step

    for idx, (name, (min_v, q1, median, q3, max_v), count) in enumerate(stats):
        y = top_margin + idx * (bar_height + gap)
        center = y + bar_height / 2

        min_x = left_margin + min_v * scale
        max_x = left_margin + max_v * scale
        q1_x = left_margin + q1 * scale
        q3_x = left_margin + q3 * scale
        median_x = left_margin + median * scale

        lines.append(f"  <line x1='{min_x}' y1='{center}' x2='{max_x}' y2='{center}' class='whisker' />")
        lines.append(f"  <rect x='{q1_x}' y='{y}' width='{max(q3_x - q1_x, 1)}' height='{bar_height}' class='box' />")
        lines.append(f"  <line x1='{median_x}' y1='{y}' x2='{median_x}' y2='{y + bar_height}' class='median' />")
        lines.append(f"  <line x1='{min_x}' y1='{center - bar_height/3}' x2='{min_x}' y2='{center + bar_height/3}' class='median' />")
        lines.append(f"  <line x1='{max_x}' y1='{center - bar_height/3}' x2='{max_x}' y2='{center + bar_height/3}' class='median' />")
        lines.append(f"  <text x='{left_margin - 15}' y='{center + 6}' text-anchor='end'>{name} (n={count})</text>")

    lines.append("</svg>")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    rows = []
    scenario_metrics = {
        1: {"states": defaultdict(list), "actions": defaultdict(list), "cost": defaultdict(list), "time": defaultdict(list)},
        2: {"states": defaultdict(list), "actions": defaultdict(list), "cost": defaultdict(list), "time": defaultdict(list)},
    }

    for env_idx in range(1, TOTAL_RUNS + 1):
        env, start, goal = deterministic_random_100_environment()
        desc_rows = _extract_desc_rows(env)

        for name, func, scenarios in ALGORITHMS:
            env_instance = _build_env(desc_rows, start, goal)
            start_time = time.perf_counter()
            try:
                result = func(env_instance, start, goal)
            except Exception as exc:
                print(f"[{name}] Error durante la ejecución en entorno {env_idx}: {exc}")
                result = (None, None, None)
            elapsed = time.perf_counter() - start_time

            states, actions, cost = result if result else (None, None, None)
            success = all(value is not None for value in (states, actions, cost))

            if 1 in scenarios:
                scenario_rows = {
                    "env": env_idx,
                    "algorithm": name,
                    "scenario": 1,
                    "states_explored": states if success else None,
                    "actions_taken": actions if success else None,
                    "total_cost": actions if success else None,
                    "time_seconds": elapsed,
                    "solution_found": success,
                }
                rows.append(scenario_rows)
                if success:
                    scenario_metrics[1]["states"][name].append(states)
                    scenario_metrics[1]["actions"][name].append(actions)
                    scenario_metrics[1]["cost"][name].append(actions)
                scenario_metrics[1]["time"][name].append(elapsed)

            if 2 in scenarios:
                scenario_rows = {
                    "env": env_idx,
                    "algorithm": name,
                    "scenario": 2,
                    "states_explored": states if success else None,
                    "actions_taken": actions if success else None,
                    "total_cost": cost if success else None,
                    "time_seconds": elapsed,
                    "solution_found": success,
                }
                rows.append(scenario_rows)
                if success:
                    scenario_metrics[2]["states"][name].append(states)
                    scenario_metrics[2]["actions"][name].append(actions)
                    scenario_metrics[2]["cost"][name].append(cost)
                scenario_metrics[2]["time"][name].append(elapsed)

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "env",
                "algorithm",
                "scenario",
                "states_explored",
                "actions_taken",
                "total_cost",
                "time_seconds",
                "solution_found",
            ],
        )
        writer.writeheader()
        for row in rows:
            formatted = row.copy()
            for key in ("states_explored", "actions_taken", "total_cost"):
                if formatted[key] is None:
                    formatted[key] = ""
            writer.writerow(formatted)

    stats_output = {}
    for scenario, metrics in scenario_metrics.items():
        stats_output[scenario] = {}
        for metric_name, values_map in metrics.items():
            stats_output[scenario][metric_name] = {}
            for algorithm_name, values in values_map.items():
                mean, std_dev = _mean_std(values)
                if mean is not None:
                    stats_output[scenario][metric_name][algorithm_name] = {
                        "mean": mean,
                        "std": std_dev,
                        "n": len(values),
                    }

    STATS_JSON.write_text(json.dumps(stats_output, indent=2), encoding="utf-8")

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    metric_titles = {
        "states": "Estados explorados",
        "actions": "Acciones tomadas",
        "cost": "Costo total",
        "time": "Tiempo (segundos)",
    }

    for scenario in (1, 2):
        suffix = f"escenario{scenario}"
        for metric_key, title in metric_titles.items():
            data = scenario_metrics[scenario][metric_key]
            output_path = IMAGES_DIR / f"boxplot_{metric_key}_{suffix}.svg"
            plot_title = f"{title} - Escenario {scenario}"
            _create_boxplot(data, plot_title, title, output_path)


if __name__ == "__main__":
    main()
