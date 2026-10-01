# Pacote de Códigos e Benchmarks — TP1 (APA)

Implementação do algoritmo de ordenação **autoral** (Ondas de Fusão, `wave_merge_sort`), dos clássicos instrumentados e o framework de validação e medição de desempenho, em **Python 3** e **C++17**.

## 📂 Estrutura de Arquivos

```text
├── Makefile                          # Automação de testes e benchmarks
├── README.md                         # Este guia
├── enunciado.md                      # Enunciado do TP1
│
├── python/
│   ├── authorial.py                  # Algoritmo autoral (Ondas de Fusão)
│   ├── classical.py                  # Algoritmos clássicos (Bubble, Selection, Insertion, Merge, Quick)
│   ├── test_suite.py                 # Suíte de testes obrigatória (unittest)
│   ├── test_comprehensive.py         # Suíte abrangente (fuzz, sweeps, adversariais, estabilidade)
│   ├── benchmark.py                  # Benchmark com tabelas Markdown e gráficos matplotlib
│   ├── visualizer.py                 # Animação da ordenação no terminal
│   ├── param_sweep.py                # Sweep de block_size x gallop_threshold (calibração do relatório)
│   ├── metrics.py                    # Instrumentação (comparações, trocas, tempos)
│   └── student_template.py           # Template de estudo
│
├── cpp/                              # Legado do pacote base (clássicos + DPES de referência)
│   ├── classical.hpp/.cpp            # Algoritmos clássicos instrumentados
│   ├── authorial.hpp/.cpp            # DPES (referência do pacote, NÃO é o autoral atual)
│   ├── test_runner.cpp               # Testes unitários em C++
│   └── benchmark.cpp                 # Benchmark em C++
│
├── latex/artigo.tex                  # Artigo científico do TP1 (self-contained, Overleaf)
├── figuras/                          # Figuras do relatório
├── results/                          # Saídas analíticas (tabelas, resumo e gráfico do relatório)
│   ├── benchmark_results.png
│   └── resumo_experimental.md
└── docs/declaracao-ia.md             # Declaração obrigatória de autoria e uso de IA
```

> Obs.: o `cpp/` implementa DPES, algoritmo de referência do pacote base, que **não** corresponde ao autoral atual em Python. A paridade entre C++ e o autoral não é garantida.

## 🚀 Como Executar

### 1. Suíte de Testes

* **Obrigatória (cenários do enunciado):**
  ```bash
  make test_python
  # ou: python3 python/test_suite.py
  ```

* **Abrangente (fuzz, sweeps de parâmetros, casos adversariais, estabilidade):**
  ```bash
  make test_python_full
  # ou: python3 python/test_comprehensive.py -v
  ```

* **Teste individual:**
  ```bash
  python3 python/test_suite.py TestQuickSort.test_05_all_identical_elements
  ```

* **C++:**
  ```bash
  make test_cpp
  ```

### 2. Benchmarks e Visualização

* **Benchmark Python** — tabelas Markdown + gráfico `benchmark_results.png`:
  ```bash
  make benchmark_python
  # ou: .venv/bin/python3 python/benchmark.py --trials 3
  ```

* **Animação no terminal** (visualize o autoral ou os clássicos passo a passo):
  ```bash
  make visualize
  # ou: .venv/bin/python3 python/visualizer.py --algorithm wave --size 48
  ```

* **Sweep de parâmetros** do autoral (`block_size` x `gallop_threshold`):
  ```bash
  .venv/bin/python3 python/param_sweep.py
  ```

* **Benchmark C++:**
  ```bash
  make run_benchmark_cpp
  ```

> **Atenção:** os alvos `benchmark_python` e `visualize` do Makefile chamam `python3`
> direto. Se o `python3` do sistema não tiver `matplotlib`, use `.venv/bin/python3`
> nos exemplos acima. Os alvos de teste só usam a stdlib e rodam com `python3`.

### 3. Instalação de Dependências

Só o `matplotlib>=3.7` é necessário (apenas para benchmark/visualização/sweep):

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

## 🧑‍💻 Algoritmo Autoral — Ondas de Fusão (`wave_merge_sort`)

Blocos-base ordenados com inserção binária, combinados por fusão bottom-up
(a cada "onda" a largura dos blocos dobra) e com avanço rápido (busca
binária + cópia em bloco) quando um lado vence comparações consecutivas.

* **Pior caso:** O(n log n) · **Melhor caso:** O(n log n) cópias com O(n log k) comparações
* **Espaço auxiliar:** O(n) · **Estável:** sim

> A contagem de `moves` é **por convenção**: `wave_merge_sort` conta cada
> gravação em endereço de memória (buffer + cópia), ~2× a do Merge Sort
> clássico (que conta só o append). Detalhe na docstring de `python/authorial.py`.

## 📄 Artigo (Relatório)

O relatório do TP1 é o arquivo único e self-contained `latex/artigo.tex`
(pacotes padrão: `pgfplots`, `algorithm2e`, `booktabs`), pronto para importar
no Overleaf. As tabelas e gráficos vêm de `results/`.