# Guia do Exercício 01: Pré-processamento Básico de Dados

## Contexto Acadêmico

O pré-processamento de dados é uma etapa **fundamental** no pipeline de Machine Learning, representando frequentemente 70-80% do tempo total de um projeto de ciência de dados. Este exercício introduz as técnicas essenciais que vocês utilizarão ao longo de toda a disciplina e carreira profissional.

## Objetivos de Aprendizagem

Ao concluir este exercício, você será capaz de:

1. **Identificar e tratar valores ausentes** usando diferentes estratégias estatísticas
2. **Detectar outliers** através do método IQR (Interquartile Range)
3. **Normalizar dados** aplicando técnicas de Min-Max e Z-Score
4. **Dividir datasets** em conjuntos de treino e teste de forma adequada
5. **Implementar funções robustas** seguindo boas práticas de programação

## Fundamentação Teórica

### 1. Tratamento de Valores Ausentes (Missing Values)

**Por que acontece?**

- Falhas na coleta de dados
- Problemas técnicos em sensores
- Dados não aplicáveis (ex: salário para desempregados)
- Recusa em responder surveys

**Estratégias de Imputação:**

| Estratégia  | Quando Usar                          | Vantagens                        | Desvantagens                                |
| ----------- | ------------------------------------ | -------------------------------- | ------------------------------------------- |
| **Média**   | Dados numéricos, distribuição normal | Simples, preserva média          | Reduz variância, sensível a outliers        |
| **Mediana** | Dados numéricos, outliers presentes  | Robusta a outliers               | Pode não representar bem a distribuição     |
| **Moda**    | Dados categóricos                    | Preserva distribuição categórica | Pode aumentar viés para categoria dominante |

### 2. Detecção de Outliers com IQR

**Conceito:**
O método IQR identifica valores que estão significativamente distantes da distribuição central dos dados.

**Fórmula Matemática:**

```
Q1 = Primeiro quartil (25%)
Q3 = Terceiro quartil (75%)
IQR = Q3 - Q1
Limite Inferior = Q1 - 1.5 × IQR
Limite Superior = Q3 + 1.5 × IQR
```

**Interpretação:**

- Valores fora dos limites são considerados outliers
- O fator 1.5 é convenção estatística (regra de Tukey)
- Outliers podem ser errores ou informações valiosas

### 3. Normalização de Dados

**Motivação:**
Algoritmos de ML são sensíveis à escala dos dados. Features com magnitudes diferentes podem dominar o processo de aprendizagem.

#### 3.1 Min-Max Normalization

**Fórmula:** `X_norm = (X - X_min) / (X_max - X_min)`

**Características:**

- Transforma dados para range [0, 1]
- Preserva relações proporcionais
- Sensível a outliers

#### 3.2 Z-Score Normalization (Standardization)

**Fórmula:** `X_norm = (X - μ) / σ`

**Características:**

- Média = 0, Desvio Padrão = 1
- Não limitada a range específico
- Assume distribuição normal

### 4. Divisão Treino-Teste

**Princípio Fundamental:**
Nunca treine e teste no mesmo conjunto de dados - isso leva ao **overfitting**.

**Boas Práticas:**

- Proporção comum: 80% treino, 20% teste
- Usar `random_state` para reprodutibilidade
- Considerar estratificação para dados desbalanceados

## Implementação Prática

### Estrutura das Funções

Cada função segue o padrão:

```python
def nome_funcao(parametros):
    """
    Docstring explicativa
    """
    # Implementação aqui
    return resultado
```

### Dicas de Implementação

#### Exercício 1: `fill_missing_values()`

```python
# Identificar colunas numéricas
numeric_cols = data.select_dtypes(include=[np.number]).columns

# Aplicar estratégia apenas onde necessário
if strategy == "mean":
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())
```

**Ponto de Atenção:**

- Média e mediana só se aplicam a dados numéricos
- Moda pode ser aplicada a qualquer tipo de dado

#### Exercício 2: `detect_outliers_iqr()`

```python
# Calcular quartis
Q1 = data[column].quantile(0.25)
Q3 = data[column].quantile(0.75)

# Aplicar regra de Tukey
outliers = (data[column] < lower_bound) | (data[column] > upper_bound)
```

**Ponto de Atenção:**

- Use operador `|` (OR) para combinar condições
- Retorne uma Series booleana, não os valores

#### Exercício 3: `normalize_data()`

```python
# Sempre trabalhe com cópia dos dados
result = data.copy()

# Evite divisão por zero
if max_val != min_val:  # Para Min-Max
if std_val != 0:        # Para Z-Score
```

#### Exercício 4: `train_test_split_custom()`

```python
# Configurar seed para reprodutibilidade
np.random.seed(random_state)

# Gerar índices aleatórios
indices = np.random.permutation(n_samples)

# Usar iloc para indexação posicional
X_train = X.iloc[train_indices]
```

## Critérios de Avaliação

### Funcionalidade (70%)

- [ ] Todas as funções executam sem erro
- [ ] Resultados corretos nos casos de teste
- [ ] Tratamento adequado de casos extremos

### Qualidade do Código (20%)

- [ ] Código limpo e legível
- [ ] Comentários quando necessário
- [ ] Nomes de variáveis descritivos

### Compreensão Conceitual (10%)

- [ ] Uso adequado das técnicas
- [ ] Escolhas justificadas de implementação

## Casos de Teste Explicados

### Teste 1: Missing Values

```python
test_data = pd.DataFrame({
    "A": [1, 2, np.nan, 4, 5],      # Numérico com NaN
    "B": [10, np.nan, 30, 40, 50],  # Numérico com NaN
    "C": ["x", "y", np.nan, "x", "y"] # Categórico com NaN
})
```

**Resultado Esperado (mean):**

- A: NaN → 3.0 (média de 1,2,4,5)
- B: NaN → 32.5 (média de 10,30,40,50)
- C: permanece NaN (mean não se aplica)

### Teste 2: Outliers

```python
outlier_data = pd.DataFrame({"values": [1, 2, 3, 4, 5, 100]})
```

**Cálculo IQR:**

- Q1 = 2.25, Q3 = 4.75, IQR = 2.5
- Lower = 2.25 - 1.5×2.5 = -1.5
- Upper = 4.75 + 1.5×2.5 = 8.5
- Outlier: 100 > 8.5 ✓

### Teste 3: Normalização

```python
norm_data = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})
```

**Min-Max para coluna A:**

- (1-1)/(5-1) = 0.0
- (2-1)/(5-1) = 0.25
- (3-1)/(5-1) = 0.5
- etc.

## Erros Comuns e Como Evitar

1. **Modificar dados originais**: Sempre use `.copy()`
2. **Divisão por zero**: Verifique denominadores antes de dividir
3. **Tipos de dados incorretos**: Use `select_dtypes()` para filtrar
4. **Índices desalinhados**: Use `.iloc[]` para posicionamento
5. **Seed não definido**: Sempre configure `random_state`

## Referências e Leitura Complementar

- **Livro:** "Hands-On Machine Learning" - Aurélien Géron (Capítulo 2)
- **Artigo:** "Data Preprocessing in Data Mining" - García et al. (2016)
- **Documentação:** Pandas User Guide - Working with missing data
- **Paper:** "Outlier Detection: A Survey" - Chandola et al. (2009)
