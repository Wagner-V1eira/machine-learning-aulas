"""Testes para o exercício de implementação do perceptron."""

import numpy as np

from core.grading.api import load_notebook_funcs

# Carregar funções do notebook do estudante
student = load_notebook_funcs("modules/08-redes-neurais/exercises/01_perceptron_impl.ipynb", allowed_imports={"numpy"})

# Extrair funções e classes
step_function = student["step_function"]
sigmoid = student["sigmoid"]
Perceptron = student["Perceptron"]
generate_linearly_separable_data = student["generate_linearly_separable_data"]
accuracy_score = student["accuracy_score"]


def test_step_function():
    """Teste da função degrau."""
    assert step_function(1) == 1, "step_function(1) deve retornar 1"
    assert step_function(-1) == 0, "step_function(-1) deve retornar 0"
    assert step_function(0) == 1, "step_function(0) deve retornar 1"

    # Teste com array
    result = step_function([1, -1, 0, 2, -2])
    expected = [1, 0, 1, 1, 0]
    np.testing.assert_array_equal(result, expected, "step_function deve funcionar com arrays")


def test_sigmoid():
    """Teste da função sigmoid."""
    # Teste valores conhecidos
    assert abs(sigmoid(0) - 0.5) < 0.001, "sigmoid(0) deve ser ~0.5"

    # sigmoid(-x) = 1 - sigmoid(x)
    x = 2.0
    assert abs(sigmoid(-x) - (1 - sigmoid(x))) < 0.001, "Propriedade sigmoid(-x) = 1 - sigmoid(x)"

    # Teste limites
    assert sigmoid(100) > 0.99, "sigmoid de valor grande deve ser ~1"
    assert sigmoid(-100) < 0.01, "sigmoid de valor muito negativo deve ser ~0"

    # Teste com array
    result = sigmoid(np.array([0, 1, -1]))
    assert len(result) == 3, "sigmoid deve funcionar com arrays"
    assert all(0 <= x <= 1 for x in result), "Todos valores sigmoid devem estar entre 0 e 1"


def test_accuracy_score():
    """Teste da função de acurácia."""
    y_true = [1, 0, 1, 1, 0]
    y_pred = [1, 0, 1, 1, 0]

    acc = accuracy_score(y_true, y_pred)
    assert abs(acc - 1.0) < 0.001, "Acurácia para predições perfeitas deve ser 1.0"

    y_pred_wrong = [0, 1, 0, 0, 1]
    acc_wrong = accuracy_score(y_true, y_pred_wrong)
    assert abs(acc_wrong - 0.0) < 0.001, "Acurácia para predições totalmente erradas deve ser 0.0"

    y_pred_half = [1, 0, 0, 1, 1]  # 3/5 corretas
    acc_half = accuracy_score(y_true, y_pred_half)
    assert abs(acc_half - 0.6) < 0.001, "Acurácia deve ser 0.6 para 3/5 corretas"


def test_generate_linearly_separable_data():
    """Teste da geração de dados linearmente separáveis."""
    X, y = generate_linearly_separable_data(n_samples=100, noise=0.0, random_state=42)

    # Verificar formato
    assert X.shape == (100, 2), "X deve ter formato (100, 2)"
    assert y.shape == (100,), "y deve ter formato (100,)"

    # Verificar se labels são 0 ou 1
    assert set(y) <= {0, 1}, "Labels devem ser apenas 0 ou 1"

    # Verificar reprodutibilidade
    X2, y2 = generate_linearly_separable_data(n_samples=100, noise=0.0, random_state=42)
    np.testing.assert_array_equal(X, X2, "Deve ser reprodutível com mesmo random_state")
    np.testing.assert_array_equal(y, y2, "Deve ser reprodutível com mesmo random_state")


def test_perceptron_init():
    """Teste de inicialização do perceptron."""
    p = Perceptron(learning_rate=0.2, n_iterations=50)

    assert p.learning_rate == 0.2, "Learning rate deve ser definido corretamente"
    assert p.n_iterations == 50, "Número de iterações deve ser definido corretamente"
    assert p.weights is None, "Pesos devem ser None antes do treinamento"
    assert p.bias is None, "Bias deve ser None antes do treinamento"


def test_perceptron_and_gate():
    """Teste do perceptron com função AND."""
    # Dados para função AND
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 0, 0, 1])  # AND logic

    p = Perceptron(learning_rate=0.1, n_iterations=100)
    p.fit(X, y)

    # Verificar se pesos e bias foram inicializados
    assert p.weights is not None, "Pesos devem ser inicializados após fit"
    assert p.bias is not None, "Bias deve ser inicializado após fit"
    assert len(p.weights) == 2, "Deve haver 2 pesos para 2 features"

    # Fazer predições
    predictions = p.predict(X)

    # O perceptron deve conseguir aprender AND perfeitamente
    acc = accuracy_score(y, predictions)
    assert acc >= 0.75, f"Perceptron deve aprender AND com acurácia >= 75%, obteve {acc}"


def test_perceptron_linearly_separable():
    """Teste do perceptron com dados linearmente separáveis."""
    # Gerar dados linearmente separáveis
    X, y = generate_linearly_separable_data(n_samples=50, noise=0.0, random_state=42)

    p = Perceptron(learning_rate=0.1, n_iterations=100)
    p.fit(X, y)

    predictions = p.predict(X)
    acc = accuracy_score(y, predictions)

    # Para dados linearmente separáveis sem ruído, deve conseguir alta acurácia
    assert acc >= 0.9, f"Perceptron deve ter alta acurácia em dados linearmente separáveis, obteve {acc}"


def test_perceptron_predict_shape():
    """Teste do formato das predições."""
    X = np.array([[1, 2], [3, 4], [5, 6]])
    y = np.array([0, 1, 1])

    p = Perceptron()
    p.fit(X, y)

    # Predição única
    pred_single = p.predict(np.array([[1, 2]]))
    assert len(pred_single) == 1, "Predição única deve retornar array de tamanho 1"

    # Múltiplas predições
    pred_multiple = p.predict(X)
    assert len(pred_multiple) == 3, "Predições múltiplas devem ter mesmo tamanho que entrada"

    # Verificar se predições são 0 ou 1
    assert all(p in [0, 1] for p in pred_multiple), "Predições devem ser 0 ou 1"


def test_hidden_robustness():
    """Testes ocultos de robustez."""
    # Teste com dados mais difíceis
    np.random.seed(123)
    X = np.random.randn(100, 2)
    # Criar separação não-linear (mais difícil)
    y = (X[:, 0] ** 2 + X[:, 1] ** 2 > 1).astype(int)

    p = Perceptron(learning_rate=0.1, n_iterations=50)
    p.fit(X, y)

    predictions = p.predict(X)
    acc = accuracy_score(y, predictions)

    # Mesmo para dados não-lineares, deve ter alguma performance
    assert acc > 0.4, "Perceptron deve ter performance mínima mesmo em dados difíceis"

    # Teste estabilidade numérica
    X_extreme = np.array([[1000, -1000], [-500, 500]])
    y_extreme = np.array([1, 0])

    p_extreme = Perceptron(learning_rate=0.001, n_iterations=10)
    p_extreme.fit(X_extreme, y_extreme)
    pred_extreme = p_extreme.predict(X_extreme)

    # Não deve quebrar com valores extremos
    assert len(pred_extreme) == 2, "Deve funcionar com valores extremos"
