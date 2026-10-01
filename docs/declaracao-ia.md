# Declaração Obrigatória de Autoria e Uso de IA

Disciplina: Análise e Projetos de Algoritmos (APA) — TP1
Aluno(s): **Luan Rodrigues Martins (luanmartins.aluno@unipampa.edu.br)**,
**Mariana Ferrão Chuquel (marianachuquel.aluno@unipampa.edu.br)**
Data: **<DATA>**

> Conforme o enunciado do TP1, esta seção é obrigatória. A omissão ou
> preenchimento falso constitui critério de rejeição (nota 0,0). Completar
> com absoluta transparência o que realmente foi feito.

---

## 1. Qual ferramenta ou fonte foi utilizada

- **Assistentes conversacionais de IA generativa (OpenAI ChatGPT, Anthropic
  Claude e Codex)**, atuando também por agente de terminal (opencode), e
  também na geração deste relatório.
- **Python 3.12 + matplotlib** (framework de benchmark/gráficos do pacote).
- Fontes bibliográficas consultadas: **Cormen et al., *Introduction to
  Algorithms*, 3ª ed.; Tims (Timsort, 2002); Sedgewick & Wayne, *Algorithms*,
  4ª ed.; Ghasemi, Jugé & Khalighinejad, "Galloping in fast-growth natural
  merge sorts", ICALP 2022; documentação oficial do Timsort no CPython.**

## 2. Por que foi utilizada

- **Para reduzir o custo de iteração na validação/benchmark e para apoiar a
  formalização da análise assintótica e a redação técnica do relatório.**
- **O framework de benchmark/gráficos foi parte do pacote fornecido (só
  matplotlib como dependência).**

## 3. Como foi utilizada

- **Sessões interativas de design e revisão; a IA escreveu a primeira versão
  da implementação (`wave_merge_sort`, inicialmente chamada
  `wave_gallop_sort` em referência ao galope do Timsort), do visualizador, da
  suíte abrangente e dos rascunhos deste relatório.**
- **A IA revisou a dedução de complexidade e sugeriu a validação de
  estabilidade e o *sweep* de parâmetros.**

## 4. Quais modificações foram realizadas sobre o material gerado

- **Parâmetros ajustados manualmente por nós — BLOCK_SIZE=32,
  GALLOP_THRESHOLD=3; trechos da fusão com avanço rápido reescritos e
  revisados pelos autores.**
- **Revisão crítica de cada função e texto; nenhum código foi aceito sem que
  pudéssemos explicar integralmente; nomenclatura padronizada para
  "Ondas de Fusão".**

## 5. Como o resultado foi validado

- **Suíte obrigatória `python/test_suite.py` (60 testes), suíte abrangente
  `python/test_comprehensive.py` (27 testes: fuzz com 76 vetores, casos
  adversariais, teste de estabilidade com chaves-etiqueta, escalabilidade até
  N=10⁴, sweep de parâmetros), todas passando.**
- **Benchmarks determinísticos (seed=42, N=10 a N=10⁴) com conferência de que
  toda saída ordena corretamente; comparação cruzada com `sorted()` do Python
  em todos os cenários.**

---

## Declaração de autoria substantiva

Declaramos que compreendemos e sabemos defender integralmente: o raciocínio
projetual, os invariantes de laço, a dedução das complexidades (melhor, médio,
pior caso), a escolha dos parâmetros e as limitações de cada algoritmo.

**Assinatura(s):** Luan Rodrigues Martins / Mariana Ferrão Chuquel