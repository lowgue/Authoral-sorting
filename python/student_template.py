"""
TEMPLATE PARA O ALUNO — TRABALHO PRÁTICO 1 (TP1)
Disciplina: Análise e Projetos de Algoritmos (APA)

Instruções:
1. Implemente seu método de ordenação autoral na função `my_authorial_sort`.
2. O retorno deve ser obrigatoriamente a tupla: (lista_ordenada, total_comparacoes, total_movimentacoes).
3. Execute este arquivo diretamente para rodar a suíte de testes de corretude e o benchmark rápido.

Algoritmo implementado: **Ordenação em Ondas de Fusão (Wave-Merge Sort)**.

Raciocínio Projetual:
1. Divide o vetor em blocos-base de BLOCK_SIZE elementos e ordena cada bloco
   com inserção binária (busca binária acha a posição em O(log k) comparações).
2. Combina os blocos via merge sort bottom-up dobrando o tamanho a cada rodada.
3. Avanço rápido: durante a fusão, quando um mesmo lado vence GALLOP_THRESHOLD
   comparações consecutivas, busca binária no lado vencedor descobre até onde
   ele avança antes de o outro voltar a competir, e copia o trecho de uma vez.
"""

from typing import Any, List, Tuple
import unittest

BLOCK_SIZE = 32
GALLOP_THRESHOLD = 3


def my_authorial_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    Ordenação em Ondas de Fusão (Wave-Merge Sort).

    Parâmetros:
        arr (List[Any]): Lista de entrada a ser ordenada.

    Retorno:
        Tuple[List[Any], int, int]:
            - Lista ordenada
            - Total de comparações realizadas
            - Total de movimentações/trocas realizadas
    """
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a, 0, 0

    comps = 0
    moves = 0

    def _binary_insertion(low: int, high: int) -> None:
        nonlocal comps, moves
        for i in range(low + 1, high + 1):
            key = a[i]
            lo = low
            hi = i
            while lo < hi:
                comps += 1
                mid = (lo + hi) // 2
                if a[mid] <= key:
                    lo = mid + 1
                else:
                    hi = mid
            for j in range(i, lo, -1):
                a[j] = a[j - 1]
                moves += 1
            a[lo] = key
            moves += 1

    def _gallop_merge(left: int, mid: int, right: int, tmp: List[Any]) -> None:
        nonlocal comps, moves
        i = left
        j = mid + 1
        k = left
        streak_left = 0
        streak_right = 0

        while i <= mid and j <= right:
            comps += 1
            if a[i] <= a[j]:
                tmp[k] = a[i]
                moves += 1
                k += 1
                i += 1
                streak_left += 1
                streak_right = 0

                if streak_left >= GALLOP_THRESHOLD and i <= mid and j <= right:
                    lo = i
                    hi = mid + 1
                    while lo < hi:
                        comps += 1
                        m = (lo + hi) // 2
                        if a[m] <= a[j]:
                            lo = m + 1
                        else:
                            hi = m
                    for t in range(i, lo):
                        tmp[k] = a[t]
                        moves += 1
                        k += 1
                    i = lo
                    streak_left = 0
            else:
                tmp[k] = a[j]
                moves += 1
                k += 1
                j += 1
                streak_right += 1
                streak_left = 0

                if streak_right >= GALLOP_THRESHOLD and i <= mid and j <= right:
                    lo = j
                    hi = right + 1
                    while lo < hi:
                        comps += 1
                        m = (lo + hi) // 2
                        if a[m] < a[i]:
                            lo = m + 1
                        else:
                            hi = m
                    for t in range(j, lo):
                        tmp[k] = a[t]
                        moves += 1
                        k += 1
                    j = lo
                    streak_right = 0

        while i <= mid:
            tmp[k] = a[i]
            moves += 1
            k += 1
            i += 1
        while j <= right:
            tmp[k] = a[j]
            moves += 1
            k += 1
            j += 1

        for t in range(left, right + 1):
            a[t] = tmp[t]
            moves += 1

    # Fase 1: blocos-base ordenados com inserção binária
    for low in range(0, n, BLOCK_SIZE):
        high = min(low + BLOCK_SIZE, n) - 1
        _binary_insertion(low, high)

    # Fase 2: merge bottom-up com avanço rápido
    tmp = [None] * n
    width = BLOCK_SIZE
    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width - 1, n - 1)
            right = min(left + 2 * width - 1, n - 1)
            if mid < right:
                _gallop_merge(left, mid, right, tmp)
        width *= 2

    return a, comps, moves


# =============================================================================
# SUÍTE DE TESTES AUTOMÁTICA DE VALIDAÇÃO
# =============================================================================
class TestStudentAuthorialSort(unittest.TestCase):
    def assert_sorted(self, original: List, result: List):
        self.assertEqual(len(result), len(original), "Tamanho divergente!")
        self.assertEqual(sorted(original), result, "A lista não foi ordenada corretamente!")

    def test_empty(self):
        res, _, _ = my_authorial_sort([])
        self.assert_sorted([], res)

    def test_single(self):
        res, _, _ = my_authorial_sort([99])
        self.assert_sorted([99], res)

    def test_sorted(self):
        data = list(range(100))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_reverse(self):
        data = list(range(100, 0, -1))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_identical(self):
        data = [5] * 50
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_random(self):
        import random
        random.seed(42)
        data = [random.randint(-1000, 1000) for _ in range(200)]
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)


if __name__ == "__main__":
    print("🧪 Executando testes unitários no seu algoritmo autoral...")
    unittest.main(verbosity=2)