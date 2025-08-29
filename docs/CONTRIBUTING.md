# Guia de Contribuição

Este documento descreve como contribuir para o ML Curso.

## Configuração do Ambiente

### Pré-requisitos

- Python 3.11+
- Git

### Instalação

```bash
git clone https://github.com/chiarorosa/machine-learning-aulas
uv sync
```

### Ativação do Ambiente

```bash
# UV gerencia automaticamente o ambiente virtual
# Comandos são executados com: uv run <comando>
```

## Desenvolvimento

### Estrutura do Projeto

```
machine-learning-aulas/
├── core/                 # Sistema de grading e utilitários
│   ├── grading/          # API de avaliação e sandbox
│   └── utils/            # Utilities (plotting, io, seeds)
├── modules/              # Conteúdo dos módulos
│   └── XX-nome-modulo/
│       ├── lessons/      # Notebooks de ensino (.ipynb)
│       ├── exercises/    # Exercícios para alunos
│       │   ├── *.ipynb   # Template do professor
│       │   ├── *_aluno.ipynb # Arquivo de trabalho do aluno
│       │   └── *_guia_exercicio.md # Guia detalhado
│       └── module.yaml   # Configuração do módulo
├── tests/                # Testes unitários e validação
│   └── exercises/        # Testes dos exercícios (XX-modulo_YY_exercicio_tests.py)
├── datasets/             # Datasets sintéticos e reais
├── scripts/              # Scripts auxiliares (grading, setup, etc.)
└── docs/                 # Documentação
```

### Fluxo de Trabalho

1. **Criar branch feature**

   ```bash
   git checkout -b feature/novo-modulo
   ```

2. **Desenvolver e testar**

   ```bash
   uv run ruff format .                    # Formatar código
   uv run ruff check .                     # Verificar código
   uv run pytest                          # Executar testes
   uv run python scripts/run_all_notebooks.py     # Testar notebooks
   uv run python scripts/check-structure.py       # Verificar estrutura
   ```

3. **Validar exercícios específicos**

   ```bash
   # Testar grading de um exercício
   uv run python scripts/grade_exercise.py \
     modules/XX-modulo/exercises/YY_exercicio_aluno.ipynb \
     tests/exercises/XX-modulo_YY_exercicio_tests.py
   ```

4. **Commit e push**

   ```bash
   git add .
   git commit -m "feat: adicionar módulo de clustering"
   git push origin feature/novo-modulo
   ```

5. **Criar Pull Request**

## Sistema de Exercícios

### Arquivos de Aluno (\_aluno.ipynb)

O projeto utiliza um sistema duplo de notebooks para exercícios:

1. **Template do Professor** (`exercicio.ipynb`)

   - Contém a solução completa
   - Serve como referência e gabarito
   - **NÃO** deve ser editado pelos alunos

2. **Arquivo do Aluno** (`exercicio_aluno.ipynb`)
   - Gerado automaticamente a partir do template
   - Contém TODOs e espaços para implementação
   - É onde o aluno desenvolve sua solução
   - É o arquivo testado pelo sistema de grading

### Configuração no module.yaml

```yaml
exercises:
  - slug: "01_exercicio"
    title: "Exercício 1"
    notebook: "exercises/01_exercicio.ipynb"
    tests: "../../tests/exercises/XX-modulo_01_exercicio_tests.py"
    max_score: 100
    create: true # ← IMPORTANTE: habilita criação automática do arquivo _aluno
```

### Verificação da Estrutura

```bash
# Verificar se todos os arquivos _aluno necessários existem
uv run python scripts/check-structure.py
```

## Adicionando Conteúdo

### Novo Módulo

1. **Criar estrutura**

   ```bash
   mkdir -p modules/XX-nome-modulo/{lessons,exercises}
   ```

2. **Criar module.yaml**

   ```yaml
   slug: "XX-nome-modulo"
   title: "Título do Módulo"
   order: XX
   prerequisites: ["YY-modulo-anterior"]
   test_enabled: true # Habilita testes para este módulo
   outcomes:
     - "Objetivo 1"
     - "Objetivo 2"
   lessons:
     - slug: "01_topico"
       title: "Tópico 1"
       notebook: "lessons/01_topico.ipynb"
       est_time_min: 45
       test_enabled: true
   exercises:
     - slug: "01_exercicio"
       title: "Exercício 1"
       notebook: "exercises/01_exercicio.ipynb"
       tests: "../../tests/exercises/XX-modulo_01_exercicio_tests.py"
       max_score: 100
       test_enabled: true
       create: true # Cria automaticamente o arquivo _aluno.ipynb
   ```

3. **Criar notebooks e testes**
   - Seguir templates existentes
   - Usar seeds fixas para reprodutibilidade
   - Implementar testes completos em `tests/exercises/`

### Nova Lição

1. **Estrutura do notebook**

   - Células markdown com explicações didáticas
   - Células de código executáveis com exemplos práticos
   - Visualizações e gráficos quando apropriado
   - Mini-quiz ou perguntas reflexivas no final
   - Próximos passos e conectividade com exercícios

2. **Padrão de imports e configuração**

   ```python
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt
   # ... outros imports necessários

   # Configurar seeds para reprodutibilidade
   np.random.seed(42)
   ```

3. **Localização**
   - Arquivo deve estar em `modules/XX-modulo/lessons/YY_topico.ipynb`
   - Referenciado no `module.yaml` na seção `lessons`

### Novo Exercício

1. **Estrutura de arquivos**

   ```
   modules/XX-modulo/exercises/
   ├── YY_exercicio.ipynb        # Template do professor (completo)
   ├── YY_exercicio_aluno.ipynb  # Arquivo de trabalho do aluno (gerado automaticamente)
   └── YY_guia_exercicio.md      # Guia detalhado com teoria e dicas
   ```

2. **Notebook do exercício (template)**

   - Células TODO para implementação pelos alunos
   - Células de teste básico para validação imediata
   - Instruções claras e exemplos de uso
   - Estrutura de funções bem definida

3. **Arquivo de testes**

   Criar em `tests/exercises/XX-modulo_YY_exercicio_tests.py`:

   ```python
   """Testes para exercício YY do módulo XX."""

   from core.grading.api import load_notebook_funcs

   # Carrega funções do notebook do aluno
   student = load_notebook_funcs(
       "modules/XX-modulo/exercises/YY_exercicio_aluno.ipynb",
       allowed_imports={"numpy", "pandas", "matplotlib"}
   )

   function_name = student["function_name"]

   def test_basic():
       """Teste básico da funcionalidade."""
       assert function_name(input_data) == expected_output

   def test_edge_cases():
       """Teste de casos extremos."""
       # Implementar testes para casos limite
       pass

   def test_performance():
       """Teste de performance (opcional)."""
       # Verificar se executa em tempo razoável
       pass
   ```

4. **Guia do exercício**

   - Fundamentação teórica dos conceitos
   - Dicas de implementação específicas
   - Critérios de avaliação
   - Casos de teste explicados
   - Erros comuns e como evitar

## Padrões de Código

### Python

- Seguir PEP 8
- Usar type hints quando possível
- Documentar funções com docstrings
- Escrever testes para todo código novo

### Notebooks

- Usar markdown para explicações didáticas
- Células de código pequenas e focadas
- Comentários em português brasileiro
- Outputs limpos (não deixar prints desnecessários)
- **Lessons**: Conteúdo explicativo com exemplos
- **Exercises**: Templates com TODOs para alunos implementarem
- **Guides**: Arquivos `.md` com fundamentação teórica detalhada

### Commits

- Usar conventional commits: `feat:`, `fix:`, `docs:`, `test:`
- Mensagens claras e descritivas
- Um commit por funcionalidade

## Testes

### Estrutura de Testes

```
tests/
├── test_content_schema.py          # Validação de estrutura dos módulos
├── test_core_grading.py           # Testes do sistema de grading
├── test_examples_execute.py       # Execução de notebooks
└── exercises/                     # Testes específicos dos exercícios
    ├── README.md                  # Documentação dos testes
    └── XX-modulo_YY_exercicio_tests.py  # Nomenclatura: {módulo}_{exercício}_tests.py
```

### Executar Testes

```bash
uv run pytest                          # Todos os testes
uv run pytest tests/                   # Apenas testes unitários
uv run pytest tests/exercises/         # Apenas testes de exercícios
uv run python scripts/run_all_notebooks.py  # Execução de notebooks
uv run python scripts/grade_exercise.py     # Testar grading de exercício específico
```

### Escrever Testes para Exercícios

1. **Nomenclatura**: Seguir padrão `XX-modulo_YY_exercicio_tests.py`
2. **Target**: Testar sempre o notebook `*_aluno.ipynb`
3. **Cobertura**: Incluir casos básicos, extremos e edge cases
4. **Performance**: Manter cada teste < 5s
5. **Imports**: Especificar `allowed_imports` para segurança

## Qualidade

### Métricas Mínimas

- Cobertura de testes: ≥ 85%
- Lint score: sem erros
- Type checking: sem erros
- Todos notebooks executam sem erro

### Code Review

- Pelo menos 1 aprovação necessária
- CI deve passar
- Código documentado
- Testes incluídos

## Documentação

### Atualizar Documentação

- README.md para mudanças principais
- Docstrings para funções
- Comentários em código complexo
- CHANGELOG.md para releases

### Estilo de Documentação

- Português brasileiro
- Exemplos práticos
- Links para referências
- Formato markdown

## Dúvidas e Suporte

- Abrir issue para bugs ou sugestões
- Usar discussions para dúvidas
- Seguir templates de issue/PR
- Ser respeitoso e construtivo
