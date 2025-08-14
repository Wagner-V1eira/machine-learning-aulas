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
ml-curso/
├── core/                 # Sistema de grading e utilitários
├── modules/              # Conteúdo dos módulos
├── scripts/              # Scripts auxiliares
├── tests/                # Testes unitários
├── datasets/             # Datasets sintéticos
└── docs/                 # Documentação
```

### Fluxo de Trabalho

1. **Criar branch feature**

   ```bash
   git checkout -b feature/novo-modulo
   ```

2. **Desenvolver e testar**

   ```bash
   uv run ruff format .     # Formatar código
   uv run ruff check .      # Verificar código
   uv run pytest           # Executar testes
   uv run python scripts/run_all_notebooks.py # Testar notebooks
   ```

3. **Commit e push**

   ```bash
   git add .
   git commit -m "feat: adicionar módulo de clustering"
   git push origin feature/novo-modulo
   ```

4. **Criar Pull Request**

## Adicionando Conteúdo

### Novo Módulo

1. **Criar estrutura**

   ```bash
   mkdir -p modules/XX-nome-modulo/{lessons,exercises,solutions}
   ```

2. **Criar module.yaml**

   ```yaml
   slug: "XX-nome-modulo"
   title: "Título do Módulo"
   order: XX
   prerequisites: ["YY-modulo-anterior"]
   outcomes:
     - "Objetivo 1"
     - "Objetivo 2"
   lessons:
     - slug: "01_topico"
       title: "Tópico 1"
       notebook: "lessons/01_topico.ipynb"
       est_time_min: 45
   exercises:
     - slug: "01_exercicio"
       title: "Exercício 1"
       notebook: "exercises/01_exercicio.ipynb"
       tests: "exercises/01_exercicio_tests.py"
       max_score: 100
   ```

3. **Criar notebooks e testes**
   - Seguir templates existentes
   - Usar seeds fixas para reprodutibilidade
   - Implementar testes completos

### Nova Lição

1. **Estrutura do notebook**

   - Células markdown com explicações
   - Células de código executáveis
   - Mini-quiz no final
   - Próximos passos

2. **Padrão de imports**

   ```python
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt
   # ... outros imports necessários

   # Configurar seeds
   np.random.seed(42)
   ```

### Novo Exercício

1. **Notebook do exercício**

   - Células TODO para implementação
   - Células de teste básico
   - Instruções claras

2. **Arquivo de testes**

   ```python
   from core.grading.api import load_notebook_funcs

   student = load_notebook_funcs(
       "path/to/exercise.ipynb",
       allowed_imports={"numpy", "pandas"}
   )

   function_name = student["function_name"]

   def test_basic():
       assert function_name(input) == expected_output
   ```

## Padrões de Código

### Python

- Seguir PEP 8
- Usar type hints quando possível
- Documentar funções com docstrings
- Escrever testes para todo código novo

### Notebooks

- Usar markdown para explicações
- Células de código pequenas e focadas
- Comentários em português
- Outputs limpos (não deixar prints desnecessários)

### Commits

- Usar conventional commits: `feat:`, `fix:`, `docs:`, `test:`
- Mensagens claras e descritivas
- Um commit por funcionalidade

## Testes

### Executar Testes

```bash
uv run pytest                          # Todos os testes
uv run pytest tests/                   # Apenas testes unitários
uv run python scripts/run_all_notebooks.py  # Apenas notebooks
```

### Escrever Testes

- Cobrir casos normais e extremos
- Usar fixtures quando apropriado
- Nomear testes claramente
- Manter testes rápidos (< 5s cada)

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
