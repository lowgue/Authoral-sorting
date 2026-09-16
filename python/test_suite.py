"""
Suíte de Testes Obrigatória para Algoritmos de Ordenação.
Executa os cenários exigidos pelo enunciado do TP1.
"""

import random
import unittest
from typing import Callable, List, Tuple

from authorial import wave_merge_sort
from pfa_authorial import pfa_sort
from classical import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)


class BaseSortMixin:
    """Classe base contendo a bateria completa de cenários de teste."""
    sort_fn: Callable[[List], Tuple[List, int, int]]
    name: str

    def assert_sorted(self, original: List, result: List):
        self.assertEqual(len(result), len(original), f"Tamanho divergente em {self.name}")
        self.assertEqual(sorted(original), result, f"Ordenação incorreta em {self.name}")

    def test_01_empty_list(self):
        """Caso limite: Vetor vazio (N = 0)"""
        data = []
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_02_single_element(self):
        """Caso limite: Vetor unitário (N = 1)"""
        data = [42]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_03_already_sorted(self):
        """Melhor caso / Sensibilidade: Vetor já perfeitamente ordenado"""
        data = list(range(1, 101))
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_04_strictly_reverse_sorted(self):
        """Pior caso / Estresse: Vetor em ordem estritamente decrescente"""
        data = list(range(100, 0, -1))
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_05_all_identical_elements(self):
        """Colisão máxima: Vetor com todos os elementos iguais"""
        data = [7] * 50
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_06_many_duplicates(self):
        """Vetor com poucos valores únicos e muitas repetições"""
        random.seed(42)
        data = [random.choice([1, 2, 3, 4, 5]) for _ in range(200)]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_07_negative_and_floating_point(self):
        """Vetor misto com números negativos e de ponto flutuante"""
        data = [-10.5, 3.14, 0.0, -0.01, 100.2, -50.0, 2.718, 0.0, -10.5]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_08_random_uniform_small(self):
        """Vetores aleatórios pequenos (N = 25)"""
        random.seed(123)
        data = [random.randint(-1000, 1000) for _ in range(25)]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_09_random_uniform_medium(self):
        """Vetores aleatórios médios (N = 1000)"""
        random.seed(456)
        data = [random.randint(-10000, 10000) for _ in range(1000)]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_10_almost_sorted(self):
        """Vetor quase ordenado (95% ordenado com poucas permutações locais)"""
        data = list(range(200))
        # Introduz algumas trocas pontuais
        for i in (10, 50, 120, 180):
            data[i], data[i + 1] = data[i + 1], data[i]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)


class TestBubbleSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(bubble_sort)
    name = "Bubble Sort"


class TestSelectionSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(selection_sort)
    name = "Selection Sort"


class TestInsertionSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(insertion_sort)
    name = "Insertion Sort"


class TestMergeSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(merge_sort)
    name = "Merge Sort"


class TestQuickSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(quick_sort)
    name = "Quick Sort"


class TestAuthorialSort(unittest.TestCase, BaseSortMixin):
    sort_fn = staticmethod(wave_merge_sort)
    name = "Authorial (Ondas de Fusão)"


class TestPFASort(unittest.TestCase, BaseSortMixin):
    """PFA é O(n⁴); todos os testes com inversões usam N ≤ 50 para viabilidade."""
    sort_fn = staticmethod(pfa_sort)
    name = "PFA (Pressure-Field Adjacent)"

    def test_04_strictly_reverse_sorted(self):
        """Pior caso / Estresse — N=50 (reverso N=100 leva ~2s; PFA é O(n⁴))"""
        data = list(range(50, 0, -1))
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_06_many_duplicates(self):
        """Colisão com repetições — N=50 (duplicatas N=200 levam ~11s; PFA é O(n⁴))"""
        import random as _rnd
        _rnd.seed(42)
        data = [_rnd.choice([1, 2, 3, 4, 5]) for _ in range(50)]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_09_random_uniform_medium(self):
        """Vetores aleatórios médios — N=75 (PFA é O(n⁴); N=1000 inviável em teste unitário)"""
        import random as _rnd
        _rnd.seed(456)
        data = [_rnd.randint(-10000, 10000) for _ in range(75)]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)

    def test_10_almost_sorted(self):
        """Vetor quase ordenado — N=50 (PFA é O(n⁴); tamanho reduzido para viabilidade)"""
        data = list(range(50))
        for i in (5, 25, 40):
            data[i], data[i + 1] = data[i + 1], data[i]
        res, _, _ = self.sort_fn(data)
        self.assert_sorted(data, res)


if __name__ == "__main__":
    unittest.main(verbosity=2)
