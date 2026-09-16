"""
Algoritmo Autoral: PFA — Pressure-Field Adjacent sort.

Raciocínio Projetual:
1. Identifica as "zonas de conflito": trechos contíguos do vetor onde
   há pelo menos uma inversão adjacente (a[i] > a[i+1]).
2. Para cada elemento, define sua "pressão": quantos elementos antes
   dele são maiores + quantos elementos depois dele são menores. É
   uma medida de quão deslocado aquele elemento está em relação à
   ordenação final, considerando TODO o vetor, não só seus vizinhos.
3. Escolhe a zona de conflito com maior soma de pressão (a região
   "mais tensa" do vetor).
4. Dentro dela, escolhe a aresta de conflito (i, i+1) cuja soma de
   pressão dos dois elementos é máxima, e troca esses dois elementos.
5. Repete até não haver mais nenhuma inversão adjacente.

Invariante de terminação:
    Seja Phi(a) = número de inversões de a (pares fora de ordem, não
    necessariamente adjacentes). Toda troca do passo 4 troca um par
    ADJACENTE que está fora de ordem, e uma troca adjacente de um par
    invertido sempre reduz Phi em exatamente 1 (a relação entre esses
    dois elementos se torna correta; a relação de cada um deles com
    qualquer terceiro elemento não muda, pois a posição relativa de
    ambos em relação a esse terceiro elemento é preservada).
    Como Phi é inteiro, Phi >= 0 sempre, e Phi(a) = 0 se e somente se
    a está ordenado, o laço termina em exatamente Phi(a0) iterações,
    para qualquer entrada (com ou sem repetições) — nunca entra em
    ciclo.

Corretude: ao final do laço não existe nenhum i com a[i] > a[i+1],
ou seja, a é fracamente crescente — logo ordenado.

Estabilidade: a troca de dois elementos ADJACENTES e DIFERENTES só
ocorre quando a[i] > a[i+1] (nunca quando são iguais, pois nesse caso
a aresta não é um conflito e não entra em nenhuma zona). Logo,
elementos com a mesma chave nunca trocam de ordem relativa: o
algoritmo é estável.

Espaço auxiliar: O(n) (vetor de pressões + estrutura de zonas),
além da cópia de entrada. Não é in-place.

Análise Assintótica:
    Seja Phi = número de inversões da entrada (0 ≤ Phi ≤ n(n-1)/2).
    O algoritmo executa exatamente Phi iterações do laço principal.

    Custo por iteração:
        - conflict_edges():    O(n)  comparações
        - merge_into_zones():  O(k)  ≤ O(n)  (k = nº de arestas em conflito)
        - pressure(i) p/ i∈[0,n): n chamadas × O(n) cada = O(n²)
        - seleção de zona:     O(z)  ≤ O(n)  (z = nº de zonas)
        - seleção de aresta:   O(n)
        Total por iteração:    O(n²)

    Portanto o custo total é O(Phi × n²).

    Melhor caso — Ω(n):
        Entrada já ordenada → Phi = 0 → o laço não executa.
        conflict_edges() faz n-1 comparações e retorna lista vazia.
        Total: Θ(n).

    Pior caso — O(n⁴):
        Entrada em ordem reversa → Phi = n(n-1)/2.
        Custo: O(n²/2 × n²) = O(n⁴).

    Caso médio — O(n⁴):
        Para uma permutação uniforme aleatória E[Phi] = n(n-1)/4 = Θ(n²).
        Custo esperado: Θ(n² × n²) — contudo, na prática cada iteração
        tende a ser mais curta (zonas pequenas, pressão concentrada),
        mas o limitante superior permanece O(n⁴) e o esperado O(n⁴).
        Nota: comparado ao Bubble Sort (O(n²) mesmo caso), o PFA paga
        O(n²) de overhead por troca para calcular o campo de pressão
        global; a vantagem é a heurística de seleção, não a velocidade.
"""

from typing import Any, List, Tuple


def pfa_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """
    PFA — Pressure-Field Adjacent sort.

    Retorna:
        Tuple[List[Any], int, int]: (lista_ordenada, comparacoes, movimentacoes)

    Convenção de contagem (igual à de classical.py / authorial.py):
    - toda comparação '<' ou '>' entre dois valores conta 1 em `comps`,
      seja entre elementos do vetor, seja entre pressões/somas usadas
      para decidir qual zona/aresta escolher;
    - toda escrita em uma posição do vetor conta 1 em `moves`; uma
      troca (swap) conta 2.
    """
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a, 0, 0

    comps = 0
    moves = 0

    def pressure(i: int) -> int:
        nonlocal comps
        x = a[i]
        p = 0
        for j in range(i):
            comps += 1
            if a[j] > x:
                p += 1
        for j in range(i + 1, n):
            comps += 1
            if a[j] < x:
                p += 1
        return p

    def conflict_edges() -> List[int]:
        nonlocal comps
        edges = []
        for i in range(n - 1):
            comps += 1
            if a[i] > a[i + 1]:
                edges.append(i)
        return edges

    def merge_into_zones(edges: List[int]) -> List[Tuple[int, int]]:
        # agrupar índices de arestas consecutivos (i, i+1, i+2, ...)
        # em zonas (start, end); não envolve comparação de elementos
        # do vetor, só de índices inteiros -- contamos também, por
        # completude e simetria com o restante do algoritmo.
        nonlocal comps
        if not edges:
            return []
        zones = []
        start = prev = edges[0]
        for e in edges[1:]:
            comps += 1
            if e == prev + 1:
                prev = e
            else:
                zones.append((start, prev + 1))
                start = prev = e
        zones.append((start, prev + 1))
        return zones

    while True:
        edges = conflict_edges()
        if not edges:
            break

        zones = merge_into_zones(edges)
        pressures = [pressure(i) for i in range(n)]

        # zona de maior soma de pressao
        best_zone = zones[0]
        best_sum = sum(pressures[best_zone[0]:best_zone[1] + 1])
        for z in zones[1:]:
            s = sum(pressures[z[0]:z[1] + 1])
            comps += 1
            if s > best_sum:
                best_sum = s
                best_zone = z
        left, right = best_zone

        # aresta de conflito de maior pressao combinada dentro da zona
        best_i = None
        best_p = -1
        for p in range(left, right):
            comps += 1
            if a[p] > a[p + 1]:
                combined = pressures[p] + pressures[p + 1]
                comps += 1
                if combined > best_p:
                    best_p = combined
                    best_i = p

        i = best_i
        a[i], a[i + 1] = a[i + 1], a[i]
        moves += 2

    return a, comps, moves
