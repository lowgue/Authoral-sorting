# Resumo Experimental (n = 1000, seed 4242)

| Algoritmo | random | sorted | reverse | duplicates | almost_sorted |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Bubble (comps) | 498510 | 999 | 499500 | 483747 | 48725 |
| Selection (comps) | 499500 | 499500 | 499500 | 499500 | 499500 |
| Insertion (comps) | 245781 | 999 | 499500 | 208184 | 22351 |
| Merge (comps) | 8707 | 4932 | 5044 | 8296 | 5817 |
| Quick (comps) | 14409 | 10542 | 10549 | 12330 | 13255 |
| Ondas de Fusão (comps) | 11760 | 3449 | 4257 | 6205 | 4035 |

### Movimentações (mesmos dados)

| Bubble (moves) | 489580 | 0 | 999000 | 414370 | 42714 |
| Selection (moves) | 1992 | 0 | 1000 | 1680 | 1878 |
| Insertion (moves) | 246788 | 1998 | 501498 | 209183 | 23355 |
| Merge (moves) | 9976 | 9976 | 9976 | 9976 | 9976 |
| Quick (moves) | 5224 | 0 | 1004 | 7592 | 3722 |
| Ondas de Fusão (moves) | 18799 | 10968 | 26372 | 17329 | 11508 |

## Achado 1 — Convenção de contagem de moves

Ondas de Fusão conta cada escrita (buffer + cópia de volta) como movimentação; Merge clássico conta apenas o append na saída. Razão observada (random n=1000): 1.9x. Convenção deve ser declarada no relatório.

- Merge random: comps=8707 moves=9976
- Ondas de Fusão random: comps=11760 moves=18799
