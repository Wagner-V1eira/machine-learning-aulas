# Schema de Conteúdo

Este documento define a estrutura e formato dos conteúdos do ML Curso.

## Estrutura de Módulos

### module.yaml

Cada módulo deve ter um arquivo `module.yaml` seguindo este schema:

```yaml
# Identificador único do módulo
slug: "XX-nome-modulo"

# Título legível do módulo
title: "Nome do Módulo"

# Ordem sequencial (começando em 1)
order: 1

# Lista de módulos pré-requisitos (slugs)
prerequisites:
  - "01-fundamentos"
  - "02-outro-modulo"

# Objetivos de aprendizagem
outcomes:
  - "Explicar conceito X"
  - "Implementar algoritmo Y"
  - "Aplicar técnica Z"

# Lista de lições
lessons:
  - slug: "01_topico" # Identificador da lição
    title: "Título da Lição" # Título legível
    notebook: "lessons/01_topico.ipynb" # Caminho relativo
    est_time_min: 45 # Tempo estimado em minutos

# Lista de exercícios
exercises:
  - slug: "01_exercicio" # Identificador do exercício
    title: "Título do Exercício" # Título legível
    notebook: "exercises/01_exercicio.ipynb" # Notebook do aluno
    tests: "../../tests/exercises/{modulo}_{exercício}_tests.py" # Arquivo de testes
    max_score: 100 # Pontuação máxima
```

## Estrutura de Notebooks

### Notebooks de Lição

Estrutura padrão para notebooks de lição:

```python
# Célula 1: Markdown - Título e Objetivos
"""
# Título da Lição

## Objetivos
- Objetivo 1
- Objetivo 2

## Pré-requisitos
- Conhecimento necessário
"""

# Célula 2: Code - Imports e Setup
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configurar seeds para reprodutibilidade
np.random.seed(42)

# Configurar estilo dos gráficos
plt.style.use('default')
"""

# Células 3-N: Alternando Markdown (teoria) e Code (exemplos)

# Célula N-1: Markdown - Mini-Quiz
"""
## Mini-Quiz

**Pergunta 1:** ...
- a) opção 1
- b) opção 2
- c) opção 3

## Respostas
1. **b)** - Explicação
"""

# Célula N: Markdown - Próximos Passos
"""
## Próximos Passos

Na próxima lição...
"""
```

### Notebooks de Exercício

Estrutura padrão para notebooks de exercício:

```python
# Célula 1: Markdown - Instruções
"""
# Exercício: Título

## Objetivo
Descrição do que será implementado

## Instruções
- Complete as funções nas células marcadas com `# TODO`
- Mantenha a assinatura das funções
- Use apenas as bibliotecas importadas
"""

# Célula 2: Code - Imports Permitidos
"""
# Importações permitidas
import numpy as np
import pandas as pd

# Configurar seed
np.random.seed(42)
"""

# Células 3-N: Exercícios com TODO
"""
def funcao_exercicio(parametros):
    \"\"\"
    Docstring da função.

    Parâmetros:
    parametros: descrição

    Retorna:
    tipo: descrição
    \"\"\"
    # TODO: Implementar função
    # Dicas podem ser fornecidas aqui

    pass  # Remover ao implementar
"""

# Células finais: Testes básicos para verificação
```

## Arquivo de Testes

Estrutura padrão para arquivos de teste (localizados em `tests/exercises/`):

**Nomenclatura:** `{modulo}_{exercicio}_tests.py`

**Exemplos:**

- `01-fundamentos_01_preprocess_tests.py`
- `02-classificacao_01_classification_metrics_tests.py`

```python
"""Testes para o exercício X."""

import numpy as np
import pandas as pd
from core.grading.api import load_notebook_funcs

# Carregar funções do notebook do estudante
student = load_notebook_funcs(
    "../../modules/XX-modulo/exercises/YY_exercicio_aluno.ipynb",
    allowed_imports={"numpy", "pandas", "sklearn"}
)

# Extrair funções
funcao1 = student["funcao1"]
funcao2 = student["funcao2"]


def test_funcao1_basic():
    """Teste básico da função 1."""
    resultado = funcao1(entrada_simples)
    assert resultado == saida_esperada, "Mensagem de erro"


def test_funcao1_edge_cases():
    """Teste de casos extremos."""
    # Teste com entrada vazia, nula, etc.
    pass


def test_funcao2_mathematical_properties():
    """Teste de propriedades matemáticas."""
    # Verificar propriedades como comutatividade, etc.
    pass


def test_hidden_comprehensive():
    """Teste oculto abrangente."""
    # Testes que o aluno não vê
    # Casos mais complexos
    pass
```

## Padrões de Qualidade

### Código

- **Imports**: Apenas bibliotecas aprovadas
- **Seeds**: Sempre fixar random seeds (42)
- **Docstrings**: Todas as funções documentadas
- **Type hints**: Usar quando possível
- **Comentários**: Em português brasileiro

### Notebooks

- **Execução**: Todos devem executar sem erro
- **Outputs**: Limpos, sem warnings desnecessários
- **Visualizações**: Títulos e labels em português
- **Markdown**: Formatação consistente

### Testes

- **Cobertura**: Pelo menos 5 testes por exercício
- **Casos**: Básicos, extremos, e ocultos
- **Performance**: Máximo 30 segundos por teste
- **Mensagens**: Claras e em português

## Datasets

### Sintéticos

- Gerados por `scripts/make_dataset_synth.py`
- Tamanho ≤ 5MB
- Seeds fixas para reprodutibilidade
- Documentados em `datasets/README.md`

### Externos (opcional)

- Scripts de download em `scripts/download_*.py`
- CI não deve depender de downloads
- Licenças compatíveis
- Dados anonimizados

## Versionamento

### Módulos

- Ordem sequencial sem gaps
- Pré-requisitos sempre anteriores
- Backward compatibility mantida

### Exercícios

- max_score pode mudar apenas aumentando
- Testes podem ser adicionados, não removidos
- Interface das funções não deve mudar

### Datasets

- Versionamento por nome de arquivo
- Manter versões antigas por compatibilidade
- Documentar mudanças

## Validação

### Automática (CI)

- Schema YAML válido
- Notebooks executam
- Testes passam
- Links funcionam

### Manual (Code Review)

- Qualidade pedagógica
- Clareza das explicações
- Progressão lógica
- Exercícios apropriados

## Extensibilidade

### Novos Módulos

- Seguir numeração sequencial
- Documentar em `docs/EXTENDING.md`
- Atualizar README principal

### Novas Métricas

- Adicionar em `core/grading/`
- Documentar API
- Incluir testes

### Novos Tipos de Exercício

- Estender `core/grading/api.py`
- Manter backward compatibility
- Documentar mudanças
