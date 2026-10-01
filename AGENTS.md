# AGENTS.md

PT-BR p/ docstrings/comentários/commits. TP1 APA: autoral `wave_merge_sort` + clássicos, Py3 & C++17.

## Mapa
- `python/`: `authorial.py` (autoral, estável O(n log n); `gallop_threshold` cita Timsort), `classical.py`, `test_suite.py` (obrigatória), `test_comprehensive.py` (fuzz/sweep/adversarial/estabilidade), `benchmark.py`, `visualizer.py`, `metrics.py`, `student_template.py`, `param_sweep.py`
- `cpp/`: **legado defasado** (DPES ≠ autoral). Só portar; sem paridade Py↔C++.
- `results/`, `docs/declaracao-ia.md`, `latex/artigo.tex`: gerados/entregáveis, versionados.

## Comandos (Makefile = fonte de verdade)
`make test_python | test_python_full | benchmark_python | visualize | test_cpp | run_benchmark_cpp | clean` (clean apaga `build/` e `*.png`).
Teste único: `python3 python/test_suite.py TestQuickSort.test_05_all_identical_elements`.
Deps: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` (só `matplotlib>=3.7`).

## Gotchas
- Imports achatados: rode por caminho (`python3 python/...`), não `-m`.
- `python3` (3.12) sem matplotlib → `benchmark_python`/`visualize` usem `.venv/bin/python3`; `test*` ok com `python3`.
- `moves` incomparável entre algos: Merge conta só append; Wave conta buffer+cópia (~2×).
- 2 venvs (`.venv`, `.venv-1`): só `.venv/` no gitignore; nunca committe venv.
- O(n²) pulados p/ N>1000 (`benchmark.py:73`).
- `results/` regenerado a cada rodada; commite só rodada intencional.

## Contrato
Fns retornam `(ordenada, comps, moves)`; não mutam entrada. Algo novo: registrar em `test_suite.py`, `test_comprehensive.py` e `benchmark.py` (`algorithms`, `seed=42`).
