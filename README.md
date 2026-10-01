# Pacote de Códigos e Benchmarks — TP1 (APA)

Este repositório contém a implementação do algoritmo de ordenação autoral "Ondas de Fusão" (`wave_merge_sort`), algoritmos clássicos de ordenação com instrumentação para análise de desempenho, além de um framework de validação e medição, desenvolvidos em **Python 3** e **C++17**.

## Estrutura de Arquivos

```text
├── Makefile                          # Automação de testes e benchmarks
├── README.md                         # Este guia
├── enunciado.md                      # Enunciado do TP1
│
├── python/
│   ├── authorial.py                  # Algoritmo autoral (Ondas de Fusão)
│   ├── classical.py                  # Algoritmos clássicos (Bubble, Selection, Insertion, Merge, Quick)
│   ├── test_suite.py                 # Suíte de testes (unittest)
│   ├── test_comprehensive.py         # Suíte abrangente (fuzz, sweeps, adversariais, estabilidade)
│   ├── benchmark.py                  # Benchmark com tabelas Markdown e gráficos matplotlib
│   ├── visualizer.py                 # Animação da ordenação no terminal
│   ├── param_sweep.py                # Sweep de block_size x gallop_threshold (calibração do relatório)
│   ├── metrics.py                    # Instrumentação (comparações, trocas, tempos)
│   └── student_template.py           # Template para estudo
│
├── cpp/                              # Código legado (clássicos + DPES de referência)
│   ├── classical.hpp/.cpp            # Algoritmos clássicos instrumentados
│   ├── authorial.hpp/.cpp            # DPES (referência, distinto do autoral atual)
│   ├── test_runner.cpp               # Testes unitários em C++
│   └── benchmark.cpp                 # Benchmark em C++
│
├── latex/artigo.tex                  # Artigo científico do TP1 (self-contained, Overleaf)
├── figuras/                          # Figuras e ilustrações do relatório
├── results/                          # Saídas analíticas (tabelas, resumo e gráfico do relatório)
│   ├── benchmark_results.png
│   └── resumo_experimental.md
└── docs/declaracao-ia.md             # Declaração obrigatória de autoria e uso de IA
```

> Observação: O diretório `cpp/` implementa o DPES, algoritmo de referência original do pacote base, o qual não corresponde à implementação autoral atual em Python. Não há paridade funcional garantida entre a versão C++ e a nova versão autoral.

## Como Executar

### 1. Suíte de Testes

* **Testes padrão (cenários do enunciado):**
  ```bash
  make test_python
  # ou: python3 python/test_suite.py
  ```

* **Testes abrangentes (fuzzing, sweeps de parâmetros, casos adversariais e de estabilidade):**
  ```bash
  make test_python_full
  # ou: python3 python/test_comprehensive.py -v
  ```

* **Execução de um teste específico:**
  ```bash
  python3 python/test_suite.py TestQuickSort.test_05_all_identical_elements
  ```

* **Testes em C++:**
  ```bash
  make test_cpp
  ```

### 2. Benchmarks e Visualização

* **Benchmark Python** — Gera tabelas Markdown e o gráfico `benchmark_results.png`:
  ```bash
  make benchmark_python
  # ou: .venv/bin/python3 python/benchmark.py --trials 3
  ```

* **Animação no Terminal** (visualização passo a passo da ordenação):
  ```bash
  make visualize
  # ou: .venv/bin/python3 python/visualizer.py --algorithm wave --size 48
  ```

* **Sweep de parâmetros do algoritmo autoral** (`block_size` x `gallop_threshold`):
  ```bash
  .venv/bin/python3 python/param_sweep.py
  ```

* **Benchmark C++:**
  ```bash
  make run_benchmark_cpp
  ```

> **Atenção:** Os comandos `benchmark_python` e `visualize` do Makefile executam o interpretador `python3` do sistema. Caso este não possua a biblioteca `matplotlib` instalada, recomenda-se a execução através do ambiente virtual (`.venv/bin/python3`), conforme ilustrado nos exemplos. Os comandos de testes não possuem dependências externas além da biblioteca padrão do Python.

### 3. Instalação de Dependências

A execução de benchmarks, visualizações e sweeps de parâmetros exige a instalação da biblioteca `matplotlib>=3.7`. Para configurar o ambiente virtual, execute:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Algoritmo Autoral — Ondas de Fusão (`wave_merge_sort`)

O algoritmo baseia-se na ordenação de blocos por inserção binária combinados através de fusão bottom-up (em cada "onda", a largura dos blocos dobra). O algoritmo implementa um mecanismo de avanço rápido (busca binária combinada com cópia em bloco) otimizado para cenários onde um subarranjo vence comparações de forma consecutiva.

* **Complexidade (Pior Caso):** O(n log n)
* **Complexidade (Melhor Caso):** O(n log n) em movimentações e O(n log k) em comparações.
* **Complexidade de Espaço (Auxiliar):** O(n)
* **Estabilidade:** Garantida (Algoritmo Estável).

> **Métrica de Movimentações (Moves):** A contagem de movimentações segue uma convenção específica. No algoritmo `wave_merge_sort`, cada gravação em memória (utilização de buffer e cópia posterior) é contabilizada, resultando em aproximadamente o dobro de movimentações registradas pelo Merge Sort clássico (que contabiliza apenas as inserções diretas). Detalhes adicionais estão descritos na documentação (docstring) de `python/authorial.py`.

## Algoritmos Clássicos

O pacote também inclui a implementação instrumentada dos seguintes algoritmos clássicos de ordenação, localizados em `python/classical.py`:
* **Bubble Sort**: Implementação com otimização de parada antecipada.
* **Selection Sort**: Implementação padrão in-place.
* **Insertion Sort**: Inserção linear, algoritmo estável.
* **Merge Sort**: Algoritmo clássico de divisão e conquista (Top-Down).
* **Quick Sort**: Utiliza partição de Hoare e escolha de pivô baseada na mediana de três.

Todos os algoritmos retornam uma tupla contendo o arranjo ordenado, o número de comparações e o número de movimentações, permitindo análise uniforme no framework de benchmarks.

## Algoritmo Legado em C++ (DPES)

O diretório `cpp/` abriga o algoritmo **Dual-Pivot Extremes Sieve Sort (DPES)**, que atuou como o algoritmo autoral de referência inicial (versão legada). Ele é mantido exclusivamente para portabilidade do pacote base em C++. Vale ressaltar que o DPES possui características distintas e **não** apresenta paridade de comportamento ou contagem de movimentações com o autoral atual (`wave_merge_sort`).

## Artigo (Relatório)

O relatório correspondente ao TP1 é fornecido no arquivo `latex/artigo.tex`, o qual foi estruturado para ser autossuficiente e compatível com as plataformas LaTeX (como Overleaf). O documento utiliza pacotes padrão (`pgfplots`, `algorithm2e`, `booktabs`), importando tabelas e gráficos diretamente do diretório `results/`.