# AGENTS.md

TP1 de Análise e Projetos de Algoritmos: um algoritmo de ordenação **autoral** + clássicos instrumentados, em Python 3 e C++17. Todas as docstrings, comentários, relatórios e mensagens de commit são em **Português** — mantenha o padrão.

## Mapa do repo

- `python/authorial.py` — Autoral `wave_merge_sort` (Ondas de Fusão): blocos com inserção binária + merge bottom-up com avanço rápido; estável, O(n log n). A funcão é `wave_merge_sort` (renomeada de `wave_gallop_sort`); o parâmetro interno `gallop_threshold` foi mantido (cita a técnica do Timsort, requisito da declaração de IA).
- `python/classical.py` — Bubble/Selection/Insertion/Merge/Quick instrumentados.
- `python/test_suite.py` — suíte obrigatória do enunciado (unittest). `test_comprehensive.py` — suíte abrangente (fuzz, sweeps de parâmetros, adversariais, estabilidade); é a mais valiosa.
- `python/benchmark.py`, `visualizer.py` — benchmark e animação no terminal.
- `results/`, `docs/declaracao-ia.md` — saídas analíticas e entregáveis do relatório (gerados por scripts, mas versionados).
- `cpp/` — **legado do pacote base, defasado**: implementa DPES, que NÃO corresponde ao autoral atual em Python. Não assuma paridade Python↔C++; só mexa em `cpp/` para portar a versão nova.

## Comandos (o Makefile é a fonte de verdade; o README está defasado)

- `make test_python` — suíte obrigatória.
- `make test_python_full` — suíte abrangente (fuzz, sweeps, casos adversariais).
- `make benchmark_python` — tabelas Markdown + `benchmark_results.png`.
- `make visualize` — animação no terminal.
- `make test_cpp`, `make run_benchmark_cpp` — C++.
- `make clean` — apaga `build/` **e `*.png`** do root.
- Teste individual: `python3 python/test_suite.py TestQuickSort.test_05_all_identical_elements`
- Instalar deps: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` (só `matplotlib>=3.7`).

## Gotchas

- **Imports achatados**: todos os módulos usam `from authorial import ...` (sem pacote). Rode sempre pelo caminho (`python3 python/test_suite.py`); `python3 -m ...` quebra.
- **`python3` do sistema (3.12) não tem matplotlib; o Makefile chama `python3` direto.** O venv `.venv` (Python 3.11) tem matplotlib. Para `benchmark_python`/`visualize`, use `.venv/bin/python3` ou o make falha no import. `test_python*` só usa stdlib, funciona com `python3`.
- **Contagem de `moves` NÃO é comparável entre algoritmos**: o Merge Sort clássico conta só o append na saída; `wave_merge_sort` conta escrita no buffer + cópia de volta (~2×). Declare a convenção por algoritmo (a docstring de `authorial.py` já alerta sobre isso).
- Existem dois venvs no repo (`.venv` e `.venv-1`); só `.venv/` está no `.gitignore` — nunca commite `.venv-1` nem venv algum.
- No benchmark, os clássicos O(n²) são pulados para N > 1000 de propósito (`benchmark.py:73`).
- `results/` é regenerado a cada rodada (PNG de ~860 KB); evite churn, commite apenas quando a rodada for intencional.

## Contrato das funções de ordenação

Toda função de ordenação (Python e C++) retorna/carrega `(lista_ordenada, comps, moves)` e **não muta a entrada** (`list(arr)` / cópia). Ao adicionar/alteraar um algoritmo, registre-o também em `test_suite.py`, `test_comprehensive.py` e `benchmark.py` (`algorithms` em `main`, com `seed=42` para o randomized).