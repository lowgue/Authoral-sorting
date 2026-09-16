"""
Suíte de Testes Abrangente do Algoritmo Autoral (e cruzamento com clássicos).

Cobertura:
    - 10 cenários obrigatórios do TP1 (reutiliza BaseSortMixin de test_suite).
    - Fuzz: várias sementes, tamanhos e distribuições.
    - Sweep de parâmetros do algoritmo autoral (block_size, gallop_threshold).
    - Estabilidade (Ondas de Fusão é estável; checado com chaves iguais).
    - Casos adversariais específicos (organ pipe, sawtooth, quase ordenado).
    - Sanidade: contadores, não-mutação da entrada, hook step_cb.
    - Vetores grandes.
    - Matriz algoritmo x distribuição (inclui clássicos, para "tudo possível").

Execute:  python3 python/test_comprehensive.py -v
"""

import random
import unittest
from typing import Any, Callable, List, Tuple

from authorial import wave_merge_sort
from pfa_authorial import pfa_sort
from classical import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)
from test_suite import BaseSortMixin

ALL_ALGORITHMS: List[Tuple[str, Callable[[List], Tuple[List, int, int]]]] = [
    ("Merge Sort", merge_sort),
    ("Quick Sort", quick_sort),
    ("Insertion Sort", insertion_sort),
    ("Selection Sort", selection_sort),
    ("Bubble Sort", bubble_sort),
    ("Authorial (Ondas de Fusão)", wave_merge_sort),
    ("PFA (Pressure-Field Adjacent)", pfa_sort),
]


def assert_sorted_ok(tc: unittest.TestCase, original: List[Any], result: List[Any], label: str) -> None:
    tc.assertEqual(len(result), len(original), f"[{label}] tamanho divergente")
    tc.assertEqual(sorted(original), result, f"[{label}] não ordenou corretamente")


# =============================================================================
# 1. Cenários padrão do TP1 para o autoral
# =============================================================================
class TestWaveMergeStandard(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(wave_merge_sort)
    name = "Authorial (Ondas de Fusão)"


# =============================================================================
# 2. Fuzz: sementes, tamanhos e distribuições variadas
# =============================================================================
class TestFuzzWaveMerge(unittest.TestCase):
    def assert_fuzz(self, sort_fn: Callable, label: str):
        rng = random.Random(2026)
        sizes = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 200]
        distributions = [
            lambda n: [rng.randint(-10_000, 10_000) for _ in range(n)],
            lambda n: [rng.uniform(-1_000.0, 1_000.0) for _ in range(n)],
            lambda n: list(range(n)),
            lambda n: list(range(n, 0, -1)),
            lambda n: [rng.choice([1, 2, 3, 5, 8]) for _ in range(n)],
            lambda n: [float(rng.randint(0, 100)) for _ in range(n)],
        ]
        for seed in range(6):
            for n in sizes:
                data = distributions[seed % len(distributions)](n)
                res, c, m = sort_fn(data)
                assert_sorted_ok(self, data, res, label)
                self.assertGreaterEqual(c, 0, f"[{label}] comps negativas")
                self.assertGreaterEqual(m, 0, f"[{label}] moves negativas")

    def test_fuzz_wave_merge(self):
        self.assert_fuzz(wave_merge_sort, "fuzz ondas de fusão")


# =============================================================================
# 3. Sweep de parâmetros do autoral
# =============================================================================
class TestParamSweepWaveMerge(unittest.TestCase):
    def test_sweep_block_and_gallop(self):
        rng = random.Random(7)
        combos = [(b, g) for b in (1, 2, 4, 8, 16, 32, 64, 128) for g in (1, 2, 3, 7)]
        datasets = {
            "random": [rng.randint(0, 500) for _ in range(200)],
            "sorted": list(range(150)),
            "reverse": list(range(150, 0, -1)),
            "duplicates": [rng.choice([1, 2, 3, 5, 8]) for _ in range(200)],
            "pipe": [rng.randint(0, 50) for _ in range(100)] + [rng.randint(0, 50) for _ in range(100)],
        }
        for block_size, gallop in combos:
            for dist_name, data in datasets.items():
                res, c, m = wave_merge_sort(data, block_size=block_size, gallop_threshold=gallop)
                label = f"wave bs={block_size} g={gallop} [{dist_name}]"
                assert_sorted_ok(self, data, res, label)
                self.assertIsInstance(c, int)
                self.assertIsInstance(m, int)

    def test_extreme_gallop_threshold_high(self):
        data = list(range(300))
        res, _, _ = wave_merge_sort(data, gallop_threshold=10_000)
        assert_sorted_ok(self, data, res, "avanço rápido quase nunca dispara")

    def test_block_size_1(self):
        data = [random.Random(1).randint(0, 100) for _ in range(120)]
        res, _, _ = wave_merge_sort(data, block_size=1, gallop_threshold=3)
        assert_sorted_ok(self, data, res, "blocos unitários")


# =============================================================================
# 4. Estabilidade do Ondas de Fusão
# =============================================================================
class _Key:
    __slots__ = ("val", "tag")

    def __init__(self, val: Any, tag: int):
        self.val = val
        self.tag = tag

    def __lt__(self, other: "_Key") -> bool:
        return self.val < other.val

    def __le__(self, other: "_Key") -> bool:
        return self.val <= other.val

    def __gt__(self, other: "_Key") -> bool:
        return self.val > other.val

    def __ge__(self, other: "_Key") -> bool:
        return self.val >= other.val

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, _Key) and self.val == other.val


class TestStabilityWaveMerge(unittest.TestCase):
    def _run_stability_check(self, data_vals: List[Any]):
        keys = [_Key(v, i) for i, v in enumerate(data_vals)]
        res, _, _ = wave_merge_sort(keys)
        self.assertEqual(len(res), len(keys))
        prev_val = None
        prev_tag = None
        for k in res:
            if prev_val is not None and k.val == prev_val:
                self.assertGreater(
                    k.tag, prev_tag,
                    f"ondas de fusão não preservaram a ordem relativa de chaves iguais val={k.val}",
                )
            elif prev_val is not None:
                self.assertLessEqual(prev_val, k.val, "chaves fora de ordem")
            prev_val, prev_tag = k.val, k.tag

    def test_stability_many_duplicates(self):
        for _ in range(10):
            vals = [random.Random(_).choice([1, 2, 3, 4, 5]) for _ in range(120)]
            self._run_stability_check(vals)

    def test_stability_one_value(self):
        self._run_stability_check([9] * 50)


# =============================================================================
# 5. Casos adversariais específicos
# =============================================================================
def adversarial_sets() -> List[Tuple[str, List[Any]]]:
    n = 120
    half = n // 2
    return [
        ("empty", []),
        ("single", [42]),
        ("two equal", [5, 5]),
        ("two reversed", [7, 1]),
        ("three", [3, 1, 2]),
        ("sorted", list(range(n))),
        ("reverse", list(range(n, 0, -1))),
        ("all identical", [7] * n),
        ("organ pipe", list(range(half)) + list(range(n - half, 0, -1))),
        ("sawtooth", [n - ((i * 7) % (n + 1)) for i in range(n)]),
        ("almost sorted", [*range(n // 2), 3, 2, 1, *range(n // 2 + 1, n)]),
        ("negatives", [-10.5, 3.14, 0.0, -0.01, 100.2, -50.0, 2.718, 0.0, -10.5]),
        ("strings", ["banana", "abacaxi", "melao", "uva", "caju"]),
        ("mix int float", [1, 2.5, -3, 0.0, 10, -0.5]),
    ]


class TestAdversarial(unittest.TestCase):
    def test_adversarial_wave_merge(self):
        for name, data in adversarial_sets():
            res, _, _ = wave_merge_sort(data)
            assert_sorted_ok(self, data, res, f"ondas de fusão [{name}]")


# =============================================================================
# 6. Todos os algoritmos x distribuições (matriz) — inclui clássicos
# =============================================================================
class TestAllAlgorithmsMatrix(unittest.TestCase):
    def test_matrix(self):
        rng = random.Random(13)
        n = 50
        datasets = {
            "random": [rng.randint(0, 100) for _ in range(n)],
            "sorted": list(range(n)),
            "reverse": list(range(n, 0, -1)),
            "duplicates": [rng.choice([1, 2, 3]) for _ in range(n)],
            "almost_sorted": [*range(n // 2), 42, 7, *range(n // 2 + 2, n)],
        }
        for name, fn in ALL_ALGORITHMS:
            for dist_name, data in datasets.items():
                res, _, _ = fn(data)
                assert_sorted_ok(self, data, res, f"{name} [{dist_name}]")


# =============================================================================
# 7. Sanidade: contadores, não-mutação da entrada, hook step_cb, vetores grandes
# =============================================================================
class TestSanity(unittest.TestCase):
    def test_input_not_mutated(self):
        rng = random.Random(5)
        data = [rng.randint(0, 1000) for _ in range(100)]
        original = list(data)
        wave_merge_sort(data)
        self.assertEqual(data, original, "ondas de fusão mutaram a entrada")

    def test_step_cb_reports_final_counts(self):
        rng = random.Random(9)
        data = [rng.randint(0, 1000) for _ in range(80)]
        frames: List[Tuple[int, int]] = []

        def cb(a: List[Any], comps: int, moves: int) -> None:
            frames.append((comps, moves))

        res, c, m = wave_merge_sort(data, step_cb=cb)
        self.assertEqual(frames[-1], (c, m))
        assert_sorted_ok(self, data, res, "step_cb ondas de fusão")

    def test_step_cb_every_mutation_visible(self):
        rng = random.Random(2)
        data = [rng.randint(0, 100) for _ in range(40)]
        snapshots: List[List[Any]] = []

        def cb(a: List[Any], comps: int, moves: int) -> None:
            snapshots.append(list(a))

        wave_merge_sort(data, step_cb=cb)
        self.assertTrue(snapshots, "nenhum frame foi emitido")
        for snap in snapshots:
            self.assertEqual(len(snap), len(data))
        self.assertEqual(snapshots[0], data)
        self.assertEqual(snapshots[-1], sorted(data), "último frame deve estar ordenado")

    def test_large_reverse_no_stack_overflow(self):
        n = 5000
        data = list(range(n, 0, -1))
        res, _, _ = wave_merge_sort(data)
        assert_sorted_ok(self, data, res, "ondas de fusão n=5000 reverse")

    def test_large_random_no_stack_overflow(self):
        rng = random.Random(99)
        data = [rng.randint(0, 100_000) for _ in range(4000)]
        res, _, _ = wave_merge_sort(data)
        assert_sorted_ok(self, data, res, "ondas de fusão n=4000 random")


class TestScalability(unittest.TestCase):
    """Escalabilidade exigida pelo enunciado: N = 10³, 10⁴, ..."""

    def test_random_10000(self):
        rng = random.Random(31415)
        data = [rng.randint(0, 1_000_000) for _ in range(10_000)]
        res, _, _ = wave_merge_sort(data)
        assert_sorted_ok(self, data, res, "ondas de fusão random n=10000")

    def test_reverse_10000(self):
        data = list(range(10_000, 0, -1))
        res, _, _ = wave_merge_sort(data)
        assert_sorted_ok(self, data, res, "ondas de fusão reverse n=10000")

    def test_sorted_10000(self):
        data = list(range(10_000))
        res, _, _ = wave_merge_sort(data)
        assert_sorted_ok(self, data, res, "ondas de fusão sorted n=10000")

    def test_duplicates_10000(self):
        rng = random.Random(2718)
        data = [rng.choice([1, 2, 3, 5, 8]) for _ in range(10_000)]
        res, _, _ = wave_merge_sort(data)
        assert_sorted_ok(self, data, res, "ondas de fusão duplicates n=10000")


if __name__ == "__main__":
    unittest.main(verbosity=2)