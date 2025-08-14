# Estendendo o ML Curso

Este guia mostra como adicionar novos módulos, lições e exercícios ao curso.

## Criando um Novo Módulo

### 1. Estrutura de Diretórios

```bash
# Criar estrutura do módulo (exemplo: clustering)
mkdir -p modules/06-clustering/{lessons,exercises,solutions}
```

### 2. Arquivo module.yaml

Criar `modules/06-clus2. **Notebook não ex3. **Testes falham\*\*

```bash
# Debug individual
uv run python -c "
from core.grading.api import load_notebook_funcs
student = load_notebook_funcs('exercise.ipynb', {'numpy'})
print(student.keys())
"
```

````bash
# Verificar sintaxe
uv run python -c "import json; json.load(open('notebook.ipynb'))"

# Executar célula por célula
uv run jupyter nbconvert --to python notebook.ipynb
uv run python notebook.py
```ule.yaml`:

```yaml
slug: "06-clustering"
title: "Aprendizado Não Supervisionado - Clustering"
order: 6
prerequisites: ["01-fundamentos", "04-validacao"]
outcomes:
- "Explicar algoritmos de clustering (K-Means, DBSCAN)"
- "Avaliar qualidade de clusters com métricas apropriadas"
- "Aplicar clustering para segmentação de dados"
lessons:
- slug: "01_kmeans"
 title: "K-Means Clustering"
 notebook: "lessons/01_kmeans.ipynb"
 est_time_min: 50
- slug: "02_dbscan"
 title: "DBSCAN e Clustering Baseado em Densidade"
 notebook: "lessons/02_dbscan.ipynb"
 est_time_min: 45
exercises:
- slug: "01_kmeans_impl"
 title: "Implementando K-Means"
 notebook: "exercises/01_kmeans_impl.ipynb"
 tests: "exercises/01_kmeans_impl_tests.py"
 max_score: 100
- slug: "02_cluster_metrics"
 title: "Métricas de Clustering"
 notebook: "exercises/02_cluster_metrics.ipynb"
 tests: "exercises/02_cluster_metrics_tests.py"
 max_score: 100
````

### 3. Notebooks de Lição

Template para `modules/06-clustering/lessons/01_kmeans.ipynb`:

```json
{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# K-Means Clustering\n",
        "\n",
        "## Objetivos\n",
        "- Compreender o algoritmo K-Means\n",
        "- Implementar K-Means do zero\n",
        "- Aplicar K-Means em dados reais\n",
        "\n",
        "## Pré-requisitos\n",
        "- Fundamentos de ML\n",
        "- Métricas de distância"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "# Imports padrão\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "from sklearn.cluster import KMeans\n",
        "from sklearn.datasets import make_blobs\n",
        "\n",
        "# Seeds para reprodutibilidade\n",
        "np.random.seed(42)\n",
        "\n",
        "# Configurar gráficos\n",
        "plt.style.use('default')\n",
        "plt.rcParams['figure.figsize'] = (10, 6)"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}
```

### 4. Notebooks de Exercício

Template para `modules/06-clustering/exercises/01_kmeans_impl.ipynb`:

```python
# Célula 1: Instruções
"""
# Exercício: Implementando K-Means

## Objetivo
Implementar o algoritmo K-Means do zero para compreender seu funcionamento.

## Instruções
- Complete as funções marcadas com TODO
- Use apenas numpy
- Mantenha as assinaturas das funções
"""

# Célula 2: Imports
"""
import numpy as np
np.random.seed(42)
"""

# Célula 3: Exercício
"""
def kmeans_fit(X, k, max_iters=100, tol=1e-4):
    \"\"\"
    Implementa o algoritmo K-Means.

    Parâmetros:
    X (array): Dados de entrada (n_samples, n_features)
    k (int): Número de clusters
    max_iters (int): Máximo de iterações
    tol (float): Tolerância para convergência

    Retorna:
    tuple: (centroids, labels)
    \"\"\"
    # TODO: Implementar K-Means
    # 1. Inicializar centroides aleatoriamente
    # 2. Repetir até convergência:
    #    a. Atribuir pontos ao centroide mais próximo
    #    b. Atualizar centroides
    # 3. Retornar centroides finais e labels

    pass
"""
```

### 5. Arquivo de Testes

Criar `modules/06-clustering/exercises/01_kmeans_impl_tests.py`:

```python
"""Testes para implementação do K-Means."""

import numpy as np
from core.grading.api import load_notebook_funcs

student = load_notebook_funcs(
    "modules/06-clustering/exercises/01_kmeans_impl.ipynb",
    allowed_imports={"numpy"}
)

kmeans_fit = student["kmeans_fit"]


def test_kmeans_basic():
    """Teste básico do K-Means."""
    # Dados simples com 2 clusters claros
    X = np.array([[0, 0], [1, 1], [10, 10], [11, 11]])

    centroids, labels = kmeans_fit(X, k=2, max_iters=10)

    # Verificar formato das saídas
    assert centroids.shape == (2, 2), "Centroides devem ter formato (k, n_features)"
    assert labels.shape == (4,), "Labels devem ter formato (n_samples,)"

    # Verificar se labels são 0 ou 1
    assert set(labels) <= {0, 1}, "Labels devem ser 0 ou 1"


def test_kmeans_convergence():
    """Teste de convergência."""
    np.random.seed(42)
    X = np.random.randn(50, 2)

    centroids, labels = kmeans_fit(X, k=3, max_iters=100)

    # Deve retornar 3 centroides
    assert len(centroids) == 3, "Deve retornar k centroides"

    # Todos os pontos devem ter label
    assert len(labels) == 50, "Todos os pontos devem ter label"
    assert all(0 <= label < 3 for label in labels), "Labels devem estar em [0, k-1]"
```

## Adicionando uma Nova Lição

### 1. Atualizar module.yaml

Adicionar nova entrada em `lessons`:

```yaml
lessons:
  # ... lições existentes ...
  - slug: "03_nova_licao"
    title: "Nova Lição"
    notebook: "lessons/03_nova_licao.ipynb"
    est_time_min: 40
```

### 2. Criar Notebook

Seguir estrutura padrão:

- Título e objetivos
- Imports e setup
- Seções teóricas (markdown)
- Exemplos práticos (code)
- Mini-quiz
- Próximos passos

### 3. Testar Execução

```bash
# Testar notebook individual
uv run python scripts/run_all_notebooks.py

# Ou executar manualmente
uv run jupyter nbconvert --to notebook --execute lessons/03_nova_licao.ipynb
```

## Adicionando um Novo Exercício

### 1. Atualizar module.yaml

```yaml
exercises:
  # ... exercícios existentes ...
  - slug: "03_novo_exercicio"
    title: "Novo Exercício"
    notebook: "exercises/03_novo_exercicio.ipynb"
    tests: "exercises/03_novo_exercicio_tests.py"
    max_score: 100
```

### 2. Criar Notebook do Exercício

Template padrão com:

- Instruções claras
- Funções com TODO
- Docstrings completas
- Testes básicos para verificação

### 3. Criar Arquivo de Testes

```python
# Estrutura padrão
from core.grading.api import load_notebook_funcs

student = load_notebook_funcs("path/to/exercise.ipynb", allowed_imports={"numpy"})
func = student["function_name"]

def test_basic():
    # Teste básico
    pass

def test_edge_cases():
    # Casos extremos
    pass

def test_hidden():
    # Testes ocultos mais complexos
    pass
```

### 4. Testar Autograder

```bash
uv run python scripts/grade_exercise.py \
  modules/XX-modulo/exercises/YY_exercicio.ipynb \
  modules/XX-modulo/exercises/YY_exercicio_tests.py
```

## Validação e Testes

### 1. Executar Suite Completa

```bash
uv run ruff check .        # Verificar código
uv run pytest             # Testes unitários
uv run python scripts/run_all_notebooks.py # Executar todos notebooks
```

### 2. Verificar Schema

```bash
uv run python -c "
import yaml
with open('modules/XX-modulo/module.yaml') as f:
    data = yaml.safe_load(f)
    print('Schema válido!')
"
```

### 3. Testar CI Localmente

```bash
# Simular pipeline CI
uv run ruff check .
uv run ruff format --check .
uv run mypy core/ scripts/
uv run pytest tests/
uv run python scripts/run_all_notebooks.py
```

## Boas Práticas

### Conteúdo Pedagógico

- **Progressão gradual**: Do simples ao complexo
- **Exemplos práticos**: Sempre mostrar aplicação
- **Interatividade**: Exercícios após cada conceito
- **Feedback**: Testes claros com mensagens úteis

### Técnicas

- **Reprodutibilidade**: Seeds fixas em todos notebooks
- **Modularidade**: Funções reutilizáveis em `core/`
- **Performance**: Exercícios executam em < 30s
- **Robustez**: Testes cobrem casos extremos

### Documentação

- **Docstrings**: Todas as funções documentadas
- **Comentários**: Código complexo explicado
- **README**: Atualizar com novos módulos
- **Schemas**: Seguir padrões definidos

## Debugging

### Problemas Comuns

1. **Notebook não executa**

   ```bash
   # Verificar sintaxe
   python -c "import json; json.load(open('notebook.ipynb'))"

   # Executar célula por célula
   jupyter nbconvert --to python notebook.ipynb
   python notebook.py
   ```

2. **Testes falham**

   ```bash
   # Debug individual
   python -c "
   from core.grading.api import load_notebook_funcs
   student = load_notebook_funcs('exercise.ipynb', {'numpy'})
   print(student.keys())
   "
   ```

3. **Imports não funcionam**
   - Verificar `allowed_imports` nos testes
   - Confirmar que bibliotecas estão em `requirements.txt`
   - Checar se paths estão corretos

### Ferramentas de Debug

```bash
# Executar teste específico
uv run pytest tests/test_content_schema.py::test_module_yaml_schema -v

# Ver logs detalhados do grading
uv run python scripts/grade_exercise.py exercise.ipynb tests.py --output results.json

# Verificar estrutura de notebook
uv run python -c "
import json
with open('notebook.ipynb') as f:
    nb = json.load(f)
    for i, cell in enumerate(nb['cells']):
        print(f'Cell {i}: {cell[\"cell_type\"]}')
"
```

## Contribuição

Após criar novo conteúdo:

1. **Testar localmente** com todos os comandos uv
2. **Commitar** seguindo conventional commits
3. **Abrir PR** com descrição clara
4. **Aguardar review** e CI passar
5. **Atualizar documentação** se necessário

Para dúvidas específicas, consultar:

- `docs/CONTRIBUTING.md` - Processo de contribuição
- `docs/CONTENT_SCHEMA.md` - Especificações técnicas
- Issues/Discussions do repositório
