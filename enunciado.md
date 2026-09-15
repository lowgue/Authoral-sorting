Trabalho Prático 1 (TP1) — Métodos de Ordenação Autorais
A ideia é simples: queremos que vocês exercitem a capacidade de projetar, modelar e analisar criticamente um algoritmo de ordenação concebido por vocês.

A performance bruta não é o critério principal. O que não é negociável é saber explicar, justificar e validar as propriedades, os invariantes e os limites assintóticos daquilo que vocês entregam.

1. Objetivo e proposta
O objetivo deste trabalho prático é desafiar o aluno a conceber, formalizar, implementar e validar experimentalmente um método de ordenação autoral.

O que deve ser feito?

Desenvolver um algoritmo de ordenação inédito ou uma adaptação estrutural profunda de métodos existentes;
Formalizar seu funcionamento matemático e deduzir sua complexidade assintótica ($O$, $\Omega$, $\Theta$);
Implementar o algoritmo e validá-lo empiricamente contra uma suíte rigorosa de casos de teste;
Comparar criticamente a proposta contra abordagens consagradas na literatura.
Qual é o foco da avaliação?

A performance de tempo de execução bruta não será o fator principal de avaliação. O foco central estará na justificativa teórica, na dedução correta das ordens de grandeza e no raciocínio projetual da solução.

Regra de ouro: um algoritmo quadratico ($O(n^2)$) com uma análise brilhante e bem fundamentada vale muito mais do que um algoritmo rápido cuja lógica o autor não saiba explicar.

2. Autoria, adaptações e uso de IA
O que é considerado autoral?
O algoritmo proposto deve refletir um esforço de concepção genuíno do aluno ou grupo. Modificações cosméticas sobre algoritmos clássicos (como renomear variáveis de um Bubble Sort ou alterar a ordem de varredura de um Selection Sort) não constituem técnica autoral.

Adaptações da literatura
Adaptações de técnicas conhecidas (ex: particionamento probabilístico, fusão em janelas deslizantes não convencionais, decomposições híbridas) são aceitas, desde que o trabalho inclua:

Identificação clara da técnica de origem;
Descrição detalhada das modificações estruturais introduzidas;
Seção de comparação direta evidenciando as diferenças teóricas e práticas em relação às abordagens estabelecidas na literatura.
Verificação de originalidade
Serão utilizadas ferramentas de IA generativa e busca semântica para verificar se existem soluções publicadas ou conhecidas com o mesmo comportamento do algoritmo proposto sem a devida atribuição.

Declaração obrigatória de uso de IA
Sempre que houver uso de ferramentas de IA (para apoio a benchmarks, geração de cenários de teste, investigação de invariantes ou escrita de código), o trabalho deverá conter uma seção informando:

Qual ferramenta ou fonte foi utilizada;
Por que ela foi utilizada;
Como ela foi utilizada;
Quais modificações foram realizadas;
Como o resultado foi validado.
3. Validação empírica e suíte de testes
Não basta que o algoritmo funcione para um exemplo simples. Ele deve ser submetido a experimentos sistemáticos.

Cenários de teste obrigatórios:

Vetores aleatórios homogêneos: Avaliação de escalabilidade com tamanhos crescentes ($N = 10, 10^2, 10^3, 10^4, \dots$);
Vetores já ordenados: Aferição de melhor caso / sensibilidade;
Vetores em ordem estritamente reversa: Avaliação de pior caso / estresse;
Vetores com elementos redundantes/repetidos: Teste de robustez e colisões;
Casos limites: Vetores vazios ($N=0$) e de elemento único ($N=1$).
Métricas a serem coletadas:

Tempo de execução médio (com repetições estatísticas);
Contagem exata ou estimada do número de comparações e movimentações de elementos.
4. Estrutura e formato de entrega
A realização e entrega do trabalho pode ser feita em um de dois formatos:

Formatos disponíveis
Opção A — Relatório Técnico Completo (PDF / Markdown):
Documento aprofundado com análise formal rigorosa, dedução matemática detalhada, discussão exaustiva do raciocínio projetual, gráficos e análise crítica dos experimentos empíricos.
Opção B — Apresentação de Slides:
Conjunto de slides estruturado de forma visual e objetiva para exposição e defesa oral em sala de aula, contemplando a intuição do algoritmo, pseudocódigo ilustrado, deduções assintóticas principais e gráficos comparativos.
Importante: Independentemente do formato escolhido (relatório ou slides), a entrega deve ser acompanhada obrigatoriamente do código-fonte executável e da suite de testes.

Regras de apresentação em sala de aula
Apresentação obrigatória ($1/3$): Cada aluno deve, obrigatoriamente, realizar a apresentação oral de ao menos $1$ das $3$ atividades práticas desenvolvidas ao longo do semestre.
Critério para ponto extra ($2/3$): Para estar elegível a concorrer à pontuação bônus de Destaque em Participação e Evolução ($P$), o aluno deverá apresentar ao menos $2$ dos $3$ trabalhos práticos do semestre.
O que o relatório/apresentação deve conter?

Concepção e Raciocínio Projetual: A intuição do algoritmo, metáforas e invariantes de laço que garantem a ordenação;
Especificação Formal: Pseudocódigo estruturado e passo a passo ilustrado com um exemplo numérico;
Análise Assintótica Teórica:
Análise formal de tempo: Melhor Caso ($\Omega$ ou $O$), Pior Caso ($O$) e Caso Médio ($\Theta$);
Análise de espaço auxiliar: Memória extra ($O(1)$ vs $O(N)$);
Propriedades: Estabilidade (preserva chaves equivalentes?) e operação in-place;
Comparação com a Literatura: Tabela comparativa e discussão contra pelo menos 2 métodos clássicos (Insertion, Selection, Merge, Quick);
Resultados Experimentais: Gráficos/tabelas de tempo e operações versus tamanho de entrada $N$;
Declaração de Autoria e IA: Conforme as diretrizes das Regras do Jogo.
5. Critérios de avaliação e pontuação
A avaliação do TP1 compõe 1.0 ponto na nota final (dentro do bloco de $TP = 3.0$).

Critério	Peso	O que será observado
Raciocínio Projetual e Originalidade	30%	Criatividade da ideia, coerência do mecanismo e justificativa do design proposto.
Análise Teórica de Complexidade	25%	Dedução matemática correta das ordens de grandeza (melhor, médio, pior caso) e espaço.
Corretude e Validação Experimental	25%	Aprovação em todos os cenários de teste, metodologia empírica e rigor na medição.
Qualidade da Documentação e Defesa	10%	Clareza da redação/slides, organização dos tópicos, qualidade do pseudocódigo e dos gráficos.
Declaração de Autoria e Pensamento Crítico	10%	Transparência no uso de ferramentas, autoria clara e domínio das limitações da solução.
6. Critérios de rejeito (Nota 0,0)
O trabalho será sumariamente rejeitado (nota 0,0) nas seguintes situações:

Plágio ou Cópia da Literatura sem Autoria/Adaptação:
Apresentar métodos estabelecidos na literatura como se fossem autorais (ou variações triviais, como simples renomeação de variáveis ou reordenação cosmética de laços);
Cópia não declarada de fontes externas ou código gerado integralmente por IA sem autoria substantiva do aluno.
Incorretude Funcional (Falha na Ordenação):
Algoritmo que falhe em produzir a saída ordenada em qualquer um dos cenários da suíte de testes obrigatória (vetores invertidos, repetidos, aleatórios ou casos de borda).
Desconhecimento Substancial da Solução:
Incapacidade de explicar, justificar e defender a lógica, os invariantes ou a complexidade do algoritmo durante arguição com o professor.
Ausência da Declaração Obrigatória de Autoria e IA:
Trabalhos que omitirem a seção formal de declaração detalhando o papel das ferramentas e modelos de IA utilizados.
Irreprodutibilidade ou Ausência de Código-Fonte Executável:
Submissões contendo apenas relatório teórico sem código executável funcional, ou com dependências que impeçam a reprodução dos experimentos.
7. Pacote de códigos e recursos disponibilizados
Para auxiliar no desenvolvimento, validação e benchmarking do seu algoritmo, está disponível no diretório codigo/ a seguinte estrutura:

Template Inicial do Aluno: python/student_template.py — Arquivo base para você implementar sua função e rodar os testes de sanidade locais.
Suíte de Testes Obrigatória: python/test_suite.py e cpp/test_runner.cpp — Testes de corretude em todos os cenários exigidos.
Framework de Benchmark: python/benchmark.py e cpp/benchmark.cpp — Geração automática de tabelas comparativas e gráficos de curvas de tempo e comparações.
Algoritmos Clássicos (Baseline): Implementações completas instrumentadas de Bubble, Selection, Insertion, Merge e Quick Sort em Python e C++.
Algoritmo Autoral de Referência (DPES): python/authorial.py e cpp/authorial.cpp.
8. Em resumo
Escolha o formato: Relatório completo aprofundado ou Apresentação de slides (+ código).
Apresente ao menos $1/3$ dos TPs obrigatoriamente; apresente $2/3$ para concorrer ao ponto extra de Participação ($P$).
Desenvolva uma ordenação autoral.
Performance bruta não é o foco principal.
Formalize o pseudocódigo e os invariantes de corretude.
Deduza analiticamente melhor, pior e caso médio ($O, \Omega, \Theta$).
Submeta o algoritmo à suíte obrigatória de testes.
Compare criticamente sua solução com métodos clássicos.
Declare expressamente qualquer uso de IA ou fontes externas.
Saiba explicar e defender cada decisão do seu projeto.