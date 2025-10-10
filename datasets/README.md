# Datasets

Esta pasta contém os datasets utilizados no curso.

## Estrutura

- `synthetic/` - Datasets sintéticos gerados por scripts
- `downloads/` - Datasets baixados (gitignored)

## Política de Dados

- Preferência por datasets pequenos (≤ 5MB)
- Datasets sintéticos para garantir reprodutibilidade
- Scripts de download para datasets públicos opcionais
- Não incluir dados pessoais ou sensíveis

## Datasets Disponíveis

### Sintéticos (gerados por `scripts/make_dataset_synth.py`)

- `regression_dataset.csv` - Dataset de regressão (500 amostras, 5 features)
- `classification_dataset.csv` - Dataset de classificação (500 amostras, 8 features, 3 classes)
- `clustering_dataset.csv` - Dataset de clustering (300 amostras, 2 features, 4 clusters)

### Como Usar

```python
import pandas as pd

# Carregar dataset de regressão
df = pd.read_csv('datasets/synthetic/regression_dataset.csv')

# Separar features e target
X = df.drop('target', axis=1)
y = df['target']
```

## Adicionando Novos Datasets

1. Para datasets sintéticos: modificar `scripts/make_dataset_synth.py`
2. Para datasets externos: criar script em `scripts/download_*.py`
3. Documentar aqui o novo dataset
