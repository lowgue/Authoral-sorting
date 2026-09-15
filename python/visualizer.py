"""
Visualizador em tempo real da ordenação no terminal (ANSI).

Uso:
    python3 python/visualizer.py --algorithm wave --size 48 --delay 25
    python3 python/visualizer.py --algorithm quick --delay 5 --distribution reverse
"""

import argparse
import math
import random
import sys
import time
from typing import Any, Callable, List, Optional, Tuple

from authorial import wave_merge_sort
from classical import bubble_sort, insertion_sort, quick_sort, selection_sort

GREEN = "\x1b[32m"
CYAN = "\x1b[36m"
YELLOW = "\x1b[33m"
DIM = "\x1b[2m"
BOLD = "\x1b[1m"
RESET = "\x1b[0m"
CLEAR = "\x1b[H\x1b[2J"
HIGHLIGHT = "\x1b[7m"

ALGORITHMS = {
    "wave": ("Authorial · Ondas de Fusão", wave_merge_sort),
    "quick": ("Quick Sort", quick_sort),
    "insertion": ("Insertion Sort", insertion_sort),
    "selection": ("Selection Sort", selection_sort),
    "bubble": ("Bubble Sort", bubble_sort),
}


def generate_data(size: int, distribution: str, seed: Optional[int]) -> List[int]:
    rng = random.Random(seed)

    if distribution == "random":
        return [rng.randint(0, 2 * size) for _ in range(size)]
    elif distribution == "sorted":
        return list(range(size))
    elif distribution == "reverse":
        return list(range(size, 0, -1))
    elif distribution == "duplicates":
        return [rng.choice([1, 2, 3, 5, 8, 13]) for _ in range(size)]
    elif distribution == "almost_sorted":
        arr = list(range(size))
        for _ in range(max(1, size // 8)):
            i = rng.randint(0, size - 1)
            j = rng.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif distribution == "organ_pipe":
        half = size // 2
        return list(range(half)) + list(range(size - half, 0, -1))
    elif distribution == "sawtooth":
        return [size - ((i * 7) % (size + 1)) for i in range(size)]
    else:
        raise ValueError(f"Distribuição desconhecida: {distribution}")


def _is_numeric(data: List[Any]) -> bool:
    return all(isinstance(v, (int, float)) for v in data)


def render_frame(
    data: List[Any],
    label: str,
    comps: int,
    moves: int,
    changed: List[int],
    scale_w: int,
    show_color: bool,
) -> str:
    rows: List[str] = []
    min_v = min(data)
    max_v = max(data)
    span = max_v - min_v if data else 0

    def _bar(v: Any) -> str:
        if not isinstance(v, (int, float)):
            return f" {v}"
        if span == 0:
            frac = 0.5
        else:
            frac = (v - min_v) / span
        filled = int(round(frac * scale_w))
        return "█" * filled + "░" * (scale_w - filled)

    for idx, v in enumerate(data):
        bar = _bar(v)
        hl = idx in changed
        if show_color:
            base = CYAN if idx % 2 else GREEN
            color = HIGHLIGHT + YELLOW if hl else base
            text = f"{color}{bar}{RESET} {v:>6}"
        else:
            mark = "▶" if hl else " "
            text = f"{mark}{bar} {v:>6}"
        rows.append(text)

    out = [
        CLEAR + BOLD + label + RESET,
        DIM + f"  size={len(data)}  comps={comps}  moves={moves}" + RESET,
        DIM + "  " + "─" * (scale_w + 8) + RESET,
        *rows,
    ]
    return "\n".join(out)


def animate(
    fn: Callable[..., Tuple[List[Any], int, int]],
    label: str,
    data: List[Any],
    delay_s: float,
    scale_w: int,
    show_color: bool,
    params: dict,
) -> Tuple[List[Any], int, int]:
    prev = list(data)
    changed: List[int] = []
    stride = max(1, math.ceil(len(data) / 90))

    def _snapshot(a: List[Any]) -> List[int]:
        if len(prev) != len(a):
            return list(range(0, len(a), stride))
        return [i for i in range(0, len(a), stride) if a[i] != prev[i]]

    def cb(a: List[Any], comps: int, moves: int) -> None:
        nonlocal changed
        changed = _snapshot(a)
        prev[:] = a
        print(render_frame(a, label, comps, moves, changed, scale_w, show_color), end="", flush=True)
        time.sleep(delay_s)

    start = time.perf_counter()
    res, c, m = fn(data, step_cb=cb, **params)
    elapsed = (time.perf_counter() - start) * 1000.0

    print(render_frame(res, label, c, m, [], scale_w, show_color), end="", flush=True)
    time.sleep(delay_s)
    print(f"\n{BOLD}✔ Ordenado!{RESET}  {c} comparações, {m} movimentações, {elapsed:.1f} ms", flush=True)
    return res, c, m


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualizador em tempo real da ordenação (terminal)")
    parser.add_argument("--algorithm", choices=list(ALGORITHMS), default="wave", help="Algoritmo a animar")
    parser.add_argument("--size", type=int, default=40, help="Tamanho do vetor")
    parser.add_argument("--distribution", choices=[
        "random", "sorted", "reverse", "duplicates", "almost_sorted", "organ_pipe", "sawtooth",
    ], default="random")
    parser.add_argument("--delay", type=float, default=30.0, metavar="MS", help="Atraso entre passos em milissegundos")
    parser.add_argument("--seed", type=int, default=42, help="Semente aleatória")
    parser.add_argument("--block-size", type=int, default=None, help="[wave] tamanho dos blocos-base")
    parser.add_argument("--gallop-threshold", type=int, default=None, help="[wave] vitórias seguidas para ativar o avanço rápido")
    parser.add_argument("--no-color", action="store_true", help="Desativa cores ANSI")
    parser.add_argument("--width", type=int, default=60, help="Largura máxima da barra")
    args = parser.parse_args()

    label, fn = ALGORITHMS[args.algorithm]

    data = generate_data(args.size, args.distribution, args.seed)
    if not data:
        print("Vetor vazio — nada a animar.")
        return

    if not _is_numeric(data):
        print("Distribuição gerou dados não numéricos; usando índices como valores.")
        data = list(range(len(data)))

    params: dict = {}
    if args.algorithm == "wave":
        if args.block_size is not None:
            params["block_size"] = args.block_size
        if args.gallop_threshold is not None:
            params["gallop_threshold"] = args.gallop_threshold

    delay_s = max(0.0, args.delay / 1000.0)
    scale_w = max(10, min(args.width, 100))

    if args.size > 90:
        print(f"\n{DIM}⚠ Vetor grande ({args.size}): exibindo 1 a cada {math.ceil(args.size / 90)} elementos.{RESET}")

    animate(fn, label, data, delay_s, scale_w, not args.no_color, params)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[interrompido]")
        sys.exit(130)