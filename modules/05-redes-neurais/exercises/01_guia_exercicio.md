# Guia do Exercício 01: Classificação de Dígitos MNIST

## Contexto Acadêmico

O dataset MNIST (Modified National Institute of Standards and Technology) é um dos datasets mais icônicos em Machine Learning, sendo considerado o "Hello World" das redes neurais. Este exercício introduz conceitos fundamentais de redes neurais Multi-Layer Perceptron (MLP) aplicados a um problema real de classificação de imagens.

## Objetivos de Aprendizagem

Ao concluir este exercício, você será capaz de:

1. **Carregar e explorar** datasets de imagens de dígitos manuscritos
2. **Pré-processar dados** de imagem para redes neurais
3. **Implementar e treinar** redes neurais MLP usando scikit-learn
4. **Otimizar hiperparâmetros** de arquitetura da rede
5. **Avaliar performance** usando métricas apropriadas para classificação
6. **Analisar erros** e interpretar predições do modelo
7. **Aplicar regularização** para melhorar generalização

## Fundamentação Teórica

### 1. O Dataset MNIST

**Características:**

- 70.000 imagens de dígitos manuscritos (0-9)
- 60.000 para treinamento, 10.000 para teste
- Imagens em escala de cinza de 28×28 pixels
- 784 features (28 × 28 = 784 pixels achatados)
- 10 classes balanceadas (um dígito por classe)

**Histórico:**
Criado em 1998 por Yann LeCun, é amplamente usado como benchmark para algoritmos de classificação de imagens.

### 2. Redes Neurais Multi-Layer Perceptron (MLP)

**Arquitetura:**

```
Input Layer (784) → Hidden Layer(s) → Output Layer (10)
```

**Componentes:**

- **Camada de Entrada**: 784 neurônios (um por pixel)
- **Camadas Ocultas**: Número variável de neurônios e camadas
- **Camada de Saída**: 10 neurônios (um por classe)

**Função de Ativação ReLU:**

```
ReLU(x) = max(0, x)
```

- Introduz não-linearidade
- Evita problema de gradiente desvanecente
- Computacionalmente eficiente

### 3. Pré-processamento de Imagens

#### 3.1 Normalização de Pixels

**Por que normalizar?**

- Pixels originais: valores de 0 a 255
- Redes neurais convergem melhor com valores pequenos
- Evita dominância de features com valores grandes

**Técnica comum para imagens:**

```python
X_normalized = X / 255.0  # Range [0, 1]
```

**Alternativa: StandardScaler**

```python
X_scaled = (X - mean) / std_dev
```

### 4. Otimização de Hiperparâmetros

#### 4.1 Arquitetura da Rede

**Hiperparâmetros principais:**

| Parâmetro            | Descrição                           | Valores Típicos            |
| -------------------- | ----------------------------------- | -------------------------- |
| `hidden_layer_sizes` | Tamanho e número de camadas ocultas | (50,), (100,), (100, 50)   |
| `activation`         | Função de ativação                  | 'relu', 'tanh', 'logistic' |
| `max_iter`           | Número máximo de iterações          | 10-100                     |
| `alpha`              | Parâmetro de regularização L2       | 0.0001, 0.001, 0.01        |
| `learning_rate_init` | Taxa de aprendizado inicial         | 0.001, 0.01, 0.1           |

**Trade-offs:**

- **Redes mais profundas**: Maior capacidade, mais tempo de treino, risco de overfitting
- **Redes mais rasas**: Treinamento rápido, menor capacidade, risco de underfitting

### 5. Regularização

**Objetivo:** Prevenir overfitting, melhorar generalização

**L2 Regularization (Ridge):**

```
Loss = Original_Loss + α × Σ(weights²)
```

**Efeito:**

- Penaliza pesos grandes
- Força o modelo a ser mais simples
- Alpha controla a intensidade da regularização

**Valores de Alpha:**

- **Muito baixo (0.0001)**: Pouca regularização, pode overfitar
- **Moderado (0.001-0.01)**: Bom equilíbrio geralmente
- **Alto (0.1+)**: Muita regularização, pode underfitar

### 6. Métricas de Avaliação

#### 6.1 Acurácia

```
Accuracy = (Predições Corretas) / (Total de Predições)
```

**Quando usar:** Datasets balanceados (como MNIST)

#### 6.2 Matriz de Confusão

Mostra confusões entre classes:

```
           Previsto
           0  1  2  ...  9
Real   0 [95  0  1  ...  0]
       1 [ 0 98  0  ...  0]
       2 [ 1  0 94  ...  0]
       ...
       9 [ 0  0  0  ... 97]
```

**Interpretação:**

- Diagonal principal: predições corretas
- Fora da diagonal: confusões entre classes
- Células com valores altos indicam dígitos similares

#### 6.3 Classification Report

Fornece métricas por classe:

- **Precision**: Quando prevê X, quantas vezes está correto?
- **Recall**: De todos os X verdadeiros, quantos foram encontrados?
- **F1-Score**: Média harmônica de precision e recall

## Implementação Prática

### Fluxo do Exercício

```
1. Carregar MNIST
   ↓
2. Explorar dados (visualizações, distribuição)
   ↓
3. Preparar dados (split, normalização)
   ↓
4. Treinar MLP básico
   ↓
5. Otimizar arquitetura
   ↓
6. Analisar performance (matriz de confusão)
   ↓
7. Análise de erros
   ↓
8. Experimentar regularização
   ↓
9. Conclusões
```

### Dicas de Implementação

#### Tarefa 1: Carregamento de Dados

```python
from sklearn.datasets import fetch_openml

# Carregar MNIST
mnist = fetch_openml('mnist_784', version=1, parser='auto')
X = mnist.data
y = mnist.target.astype(int)

# Visualizar imagem
plt.imshow(X[0].reshape(28, 28), cmap='gray')
```

#### Tarefa 2: Preparação

```python
# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Normalizar
X_train_norm = X_train / 255.0
X_test_norm = X_test / 255.0
```

#### Tarefa 3: MLP Básico

```python
from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(
    hidden_layer_sizes=(100,),
    activation='relu',
    max_iter=20,
    random_state=42,
    verbose=True
)

mlp.fit(X_train_norm, y_train)
```

#### Tarefa 4: Comparação de Arquiteturas

```python
arquiteturas = [(50,), (100,), (100, 50), (200, 100, 50)]

for arch in arquiteturas:
    mlp = MLPClassifier(hidden_layer_sizes=arch, ...)
    mlp.fit(X_train_norm, y_train)
    acc = mlp.score(X_test_norm, y_test)
    print(f"{arch}: {acc:.4f}")
```

#### Tarefa 5: Matriz de Confusão

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
```

#### Tarefa 6: Análise de Erros

```python
# Encontrar erros
erros_idx = np.where(y_test != y_pred)[0]

# Visualizar
for idx in erros_idx[:10]:
    plt.imshow(X_test[idx].reshape(28, 28), cmap='gray')
    plt.title(f"Real: {y_test[idx]}, Pred: {y_pred[idx]}")
```

#### Tarefa 7: Regularização

```python
alphas = [0.0001, 0.001, 0.01, 0.1]

for alpha in alphas:
    mlp = MLPClassifier(alpha=alpha, ...)
    mlp.fit(X_train_norm, y_train)
    # Avaliar treino e teste
```

## Resultados Esperados

### Performance Típica

- **MLP Básico (100,)**: ~95-96% de acurácia
- **MLP Otimizado (100, 50)**: ~97-98% de acurácia
- **State-of-the-art (CNNs)**: >99% de acurácia

### Confusões Comuns

Dígitos frequentemente confundidos:

- **4 ↔ 9**: Traços verticais similares
- **3 ↔ 5**: Curvaturas parecidas
- **7 ↔ 1**: Ambos têm traço vertical
- **8 ↔ 3**: Múltiplas curvas

## Conceitos Avançados (Opcional)

### Por que MLPs não são ideais para imagens?

**Limitações:**

1. **Perda de estrutura espacial**: Achatamento destrói relações espaciais 2D
2. **Muitos parâmetros**: 784 × 100 = 78.400 pesos só na primeira camada
3. **Não invariante a translação**: Mesma imagem deslocada é tratada diferente

**Solução:** Convolutional Neural Networks (CNNs)

- Preservam estrutura espacial
- Compartilham pesos (menos parâmetros)
- Invariantes a translação

### Early Stopping

```python
mlp = MLPClassifier(
    early_stopping=True,
    validation_fraction=0.1,
    n_iter_no_change=5
)
```

## Critérios de Avaliação

O exercício será avaliado considerando:

1. **Carregamento e exploração** (15 pontos)

   - Dados carregados corretamente
   - Visualizações apropriadas
   - Análise da distribuição

2. **Preparação dos dados** (15 pontos)

   - Split correto (80/20)
   - Normalização adequada
   - Verificação de shapes

3. **MLP Básico** (20 pontos)

   - Modelo treinado
   - Acurácia > 80%
   - Classification report

4. **Otimização de arquitetura** (25 pontos)

   - Pelo menos 3 arquiteturas testadas
   - Comparação sistemática
   - Escolha justificada

5. **Matriz de confusão** (15 pontos)

   - Matriz gerada corretamente
   - Visualização clara
   - Análise de confusões

6. **Análise de erros** (20 pontos)

   - Exemplos de erros visualizados
   - Interpretação dos erros
   - Insights sobre padrões

7. **Regularização** (20 pontos)

   - Múltiplos valores de alpha testados
   - Comparação treino vs teste
   - Análise do impacto

8. **Conclusões** (10 pontos)
   - Resumo dos resultados
   - Insights relevantes
   - Reflexão crítica

**Total: 140 pontos**

## Recursos Adicionais

### Documentação

- [scikit-learn MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
- [MNIST Database](http://yann.lecun.com/exdb/mnist/)

### Leituras Recomendadas

- LeCun et al. (1998) - "Gradient-Based Learning Applied to Document Recognition"
- Goodfellow et al. (2016) - "Deep Learning" (Capítulo 6: Deep Feedforward Networks)

### Próximos Passos

Após dominar este exercício, explore:

1. Implementar MLP do zero (sem scikit-learn)
2. Testar outras funções de ativação
3. Implementar CNN para MNIST
4. Aplicar Data Augmentation
5. Tentar Fashion-MNIST (dataset mais desafiador)

## Dúvidas Frequentes

**Q: Por que usar apenas 10.000 amostras se temos 70.000?**  
A: Para acelerar o treinamento durante o aprendizado. Use o dataset completo para resultados finais.

**Q: Qual a diferença entre max_iter e epochs?**  
A: No scikit-learn, max_iter é o número máximo de iterações do otimizador, similar a epochs em frameworks como TensorFlow.

**Q: Por que normalizar para [0,1] e não usar StandardScaler?**  
A: Ambos funcionam! Para imagens, [0,1] é mais intuitivo (representa intensidade), mas StandardScaler também é válido.

**Q: Como escolher o número de camadas ocultas?**  
A: Comece com 1-2 camadas. Adicione mais se o modelo underfitta. Use regularização se overfitta.

**Q: Qual a diferença entre MLP e Deep Learning?**  
A: MLP é um tipo de rede neural. Deep Learning refere-se a redes neurais profundas (muitas camadas), geralmente CNNs, RNNs, etc.

---

**Boa sorte no exercício! 🚀**
