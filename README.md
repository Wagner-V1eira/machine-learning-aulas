# ML Curso - Repositório Guiado de Machine Learning

Repositório didático e executável para aprendizado progressivo de Machine Learning em Python.

## Estrutura do Curso

1. **Fundamentos de ML** - Conceitos, fluxo, ética de dados
2. **Regressão Supervisionada** - Linear, Regularização
3. **Classificação Supervisionada** - Logística, SVM, Árvores, Florestas
4. **Validação & Métricas** - holdout, k-fold, métricas, tuning
5. **Feature Engineering & Pipelines** - Scaler, OneHot, ColumnTransformer
6. **Não Supervisionado** - KMeans, DBSCAN, PCA
7. **Séries Temporais** - fundamentos, divisão temporal
8. **Redes Neurais** - Perceptron, MLP, backprop
9. **Deep Learning** - PyTorch básico
10. **Projetos de Consolidação** - casos reais

## Instalação

```bash
# Clonar repositório
git clone https://github.com/chiarorosa/machine-learning-aulas

# Instalar UV (gerenciador de pacotes Python moderno)
pip install uv

# Configurar ambiente automaticamente
uv run python scripts/tasks.py setup
```

### Instalação Rápida (Recomendada)

Para novos usuários, use os scripts automáticos:

```bash
# Windows
install.bat

# Linux/macOS
./install.sh
```

## Comandos UV

Todos os comandos usam UV como base. Sintaxe: `uv run python scripts/tasks.py [comando]`

```bash
# 🔧 Configuração
uv run python scripts/tasks.py setup          # Configurar ambiente
uv run python scripts/tasks.py install        # Instalar em modo desenvolvimento

# 🔍 Qualidade de código
uv run python scripts/tasks.py lint           # Verificar código (ruff + black + isort)
uv run python scripts/tasks.py fmt            # Formatar código
uv run python scripts/tasks.py typecheck      # Verificação de tipos (mypy)

# 🧪 Testes
uv run python scripts/tasks.py test           # Executar testes unitários
uv run python scripts/tasks.py test-status    # Ver status dos módulos para testes
uv run python scripts/tasks.py run-notebooks  # Executar todos notebooks

# 🎛️ Controle de Módulos (para desenvolvimento)
uv run python scripts/manage_tests.py enable 08-redes-neurais   # Habilitar módulo para testes
uv run python scripts/manage_tests.py disable 03-classificacao  # Desabilitar módulo temporariamente
uv run python scripts/manage_tests.py list                      # Listar status detalhado

# 📝 Avaliação
uv run python scripts/tasks.py grade --module 02-regressao --exercise 01_mae_metric

# 🧹 Manutenção
uv run python scripts/tasks.py clean          # Limpar arquivos temporários
uv run python scripts/tasks.py update         # Atualizar dependências

# ❓ Ajuda
uv run python scripts/tasks.py help           # Ver todos os comandos
```

> **📝 Nota**: Módulos desabilitados não são testados, permitindo desenvolvimento iterativo sem quebrar o pipeline de testes.

### Modo Direto (Opcional)

Após executar `uv run python scripts/tasks.py install`, você pode usar comandos mais curtos:

```bash
uv run ml-curso setup
uv run ml-curso lint
uv run ml-curso test
uv run ml-curso grade --module 02-regressao --exercise 01_mae_metric
```

### Como Usar

1. **Estudar lições**: Abrir notebooks em `modules/*/lessons/`
2. **Fazer exercícios**: Editar células `# TODO` em `modules/*/exercises/`
3. **Verificar progresso**: Usar `uv run python scripts/tasks.py grade --module [módulo] --exercise [exercício]`

## Por que UV?

- **⚡ Ultra-rápido**: 10-100x mais rápido que pip
- **🌍 Multiplataforma**: Funciona identicamente em Windows, macOS e Linux
- **🔒 Reprodutível**: Lock files garantem builds determinísticos
- **🎯 Moderno**: Padrão atual da comunidade Python
- **🔧 Simples**: Uma ferramenta para tudo

## Estrutura de Módulos

Cada módulo contém:

- `module.yaml` - Metadados e configuração
- `lessons/` - Notebooks com teoria e exemplos
- `exercises/` - Exercícios práticos com autograder
- `solutions/` - Soluções dos exercícios

## Documentação

### 📚 Documentação Técnica

- **📝 [Esquema de Conteúdo](docs/CONTENT_SCHEMA.md)** - Estrutura e formato dos módulos, lições e exercícios
- **🔧 [Estendendo o Curso](docs/EXTENDING.md)** - Como adicionar novos módulos, lições e exercícios

## Contribuir

- **🤝 [Guia de Contribuição](docs/CONTRIBUTING.md)** - Diretrizes para contribuir com o projeto

## Licença

MIT License - ver arquivo LICENSE
