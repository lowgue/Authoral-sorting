"""
Algoritmo Autoral 1: Ordenação em Ondas de Fusão (Wave-Merge Sort).

Raciocínio Projetual:
1. Divide o vetor em blocos-base de tamanho BLOCK_SIZE e ordena cada bloco
   isoladamente com inserção binária: a busca binária descobre a posição de
   inserção em O(log k) comparações, o deslocamento físico continua O(k).
2. Combina os blocos via merge sort bottom-up: a cada rodada (a "onda"), a
   largura dos blocos ordenados dobra, com buffer auxiliar O(n).
3. Avanço rápido: durante a fusão, quando um mesmo lado vence
   GALLOP_THRESHOLD comparações consecutivas, ativa-se uma busca binária
   nesse lado para descobrir até onde ele avança antes de o outro lado
   voltar a competir, copiando o trecho inteiro em uma única operação.

Fusão estrutural: as três peças existem na literatura (inserção binária,
merge sort e o "galope"/galloping do Timsort), mas o gatilho e o
comportamento do avanço rápido são aplicados aqui a blocos artificialmente
criados pelo próprio algoritmo — não a runs naturais do vetor de entrada.

Complexidade:
    Pior caso: O(n log n) (blocos entrelaçados, avanço rápido nunca dispara).
    Melhor caso: O(n log n) cópias, mas com O(n log k) comparações quando
    os blocos estão bem separados (avanço rápido dispara com frequência).
Espaço auxiliar: O(n). Estabilidade: estável.

Contagem de movimentações: conta-se cada gravação de elemento em endereço
de memória (escrita no buffer temporário + cópia de volta para o vetor), o
que dá ~2 movimentações por elemento por nível de fusão. Essa convenção é
estrita e exata, porém DIFERENTE da do Merge Sort clássico do pacote (que
conta apenas o append na saída) — a razão observada é ~1,9. O relatório
deve declarar explicitamente a convenção adotada em cada algoritmo.
"""

from typing import Any, Callable, List, Optional, Tuple

BLOCK_SIZE = 32
GALLOP_THRESHOLD = 3


def wave_merge_sort(
    arr: List[Any],
    block_size: int = BLOCK_SIZE,
    gallop_threshold: int = GALLOP_THRESHOLD,
    step_cb: Optional[Callable[[List[Any], int, int], None]] = None,
) -> Tuple[List[Any], int, int]:
    """
    Ordenação em Ondas de Fusão (Wave-Merge Sort).

    Parâmetros:
        arr: lista de entrada.
        block_size: tamanho dos blocos-base da inserção binária.
        gallop_threshold: vitórias seguidas que ativam o avanço rápido.
        step_cb: callback (a, comps, moves) chamado após cada mutação
                 visível do vetor (usado pelo visualizador em tempo real).

    Retorna:
        Tuple[List[Any], int, int]: (lista_ordenada, comparacoes, movimentacoes)
    """
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a, 0, 0

    comps = [0]
    moves = [0]

    def _notify() -> None:
        if step_cb is not None:
            step_cb(a, comps[0], moves[0])

    def _binary_insertion(low: int, high: int) -> None:
        for i in range(low + 1, high + 1):
            key = a[i]
            lo = low
            hi = i
            while lo < hi:
                comps[0] += 1
                mid = (lo + hi) // 2
                if a[mid] <= key:
                    lo = mid + 1
                else:
                    hi = mid
            for j in range(i, lo, -1):
                a[j] = a[j - 1]
                moves[0] += 1
                _notify()
            a[lo] = key
            moves[0] += 1
            _notify()

    def _gallop_merge(left: int, mid: int, right: int, tmp: List[Any]) -> None:
        i = left
        j = mid + 1
        k = left
        streak_left = 0
        streak_right = 0

        while i <= mid and j <= right:
            comps[0] += 1
            if a[i] <= a[j]:
                tmp[k] = a[i]
                moves[0] += 1
                k += 1
                i += 1
                streak_left += 1
                streak_right = 0

                if streak_left >= gallop_threshold and i <= mid and j <= right:
                    lo = i
                    hi = mid + 1
                    while lo < hi:
                        comps[0] += 1
                        m = (lo + hi) // 2
                        if a[m] <= a[j]:
                            lo = m + 1
                        else:
                            hi = m
                    for t in range(i, lo):
                        tmp[k] = a[t]
                        moves[0] += 1
                        k += 1
                    i = lo
                    streak_left = 0
            else:
                tmp[k] = a[j]
                moves[0] += 1
                k += 1
                j += 1
                streak_right += 1
                streak_left = 0

                if streak_right >= gallop_threshold and i <= mid and j <= right:
                    lo = j
                    hi = right + 1
                    while lo < hi:
                        comps[0] += 1
                        m = (lo + hi) // 2
                        if a[m] < a[i]:
                            lo = m + 1
                        else:
                            hi = m
                    for t in range(j, lo):
                        tmp[k] = a[t]
                        moves[0] += 1
                        k += 1
                    j = lo
                    streak_right = 0

        while i <= mid:
            tmp[k] = a[i]
            moves[0] += 1
            k += 1
            i += 1
        while j <= right:
            tmp[k] = a[j]
            moves[0] += 1
            k += 1
            j += 1

        for t in range(left, right + 1):
            a[t] = tmp[t]
            moves[0] += 1
            _notify()

    for low in range(0, n, block_size):
        high = min(low + block_size, n) - 1
        _binary_insertion(low, high)

    tmp = [None] * n
    width = block_size
    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width - 1, n - 1)
            right = min(left + 2 * width - 1, n - 1)
            if mid < right:
                _gallop_merge(left, mid, right, tmp)
        width *= 2

    return a, comps[0], moves[0]