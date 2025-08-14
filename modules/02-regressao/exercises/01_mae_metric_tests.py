"""Testes para o exercício de métricas de regressão."""

import numpy as np

from core.grading.api import load_notebook_funcs

# Carregar funções do notebook do estudante
student = load_notebook_funcs(
    "modules/02-regressao/exercises/01_mae_metric.ipynb",
    allowed_imports={"numpy", "pandas"},
)

# Extrair funções
mean_absolute_error = student["mean_absolute_error"]
mean_squared_error = student["mean_squared_error"]
root_mean_squared_error = student["root_mean_squared_error"]
r2_score = student["r2_score"]
evaluate_regression = student["evaluate_regression"]


def test_basic():
    """Teste básico para previsões perfeitas."""
    y_true = [1, 2, 3]
    y_pred = [1, 2, 3]

    assert (
        abs(mean_absolute_error(y_true, y_pred)) < 0.001
    ), "MAE para previsões perfeitas deve ser 0"
    assert (
        abs(mean_squared_error(y_true, y_pred)) < 0.001
    ), "MSE para previsões perfeitas deve ser 0"
    assert (
        abs(root_mean_squared_error(y_true, y_pred)) < 0.001
    ), "RMSE para previsões perfeitas deve ser 0"
    assert (
        abs(r2_score(y_true, y_pred) - 1.0) < 0.001
    ), "R² para previsões perfeitas deve ser 1"


def test_mae_simple():
    """Teste simples para MAE."""
    y_true = [1, 2, 3, 4]
    y_pred = [2, 3, 4, 5]  # Erro de +1 em todos

    mae = mean_absolute_error(y_true, y_pred)
    assert abs(mae - 1.0) < 0.001, f"MAE esperado: 1.0, obtido: {mae}"


def test_mse_simple():
    """Teste simples para MSE."""
    y_true = [1, 2, 3]
    y_pred = [2, 3, 4]  # Erro de +1 em todos, MSE = 1

    mse = mean_squared_error(y_true, y_pred)
    assert abs(mse - 1.0) < 0.001, f"MSE esperado: 1.0, obtido: {mse}"


def test_rmse_simple():
    """Teste simples para RMSE."""
    y_true = [1, 2, 3]
    y_pred = [2, 3, 4]  # Erro de +1 em todos, RMSE = sqrt(1) = 1

    rmse = root_mean_squared_error(y_true, y_pred)
    assert abs(rmse - 1.0) < 0.001, f"RMSE esperado: 1.0, obtido: {rmse}"


def test_r2_simple():
    """Teste simples para R²."""
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1, 2, 3, 4, 5]  # Previsão perfeita

    r2 = r2_score(y_true, y_pred)
    assert (
        abs(r2 - 1.0) < 0.001
    ), f"R² para previsões perfeitas deve ser 1, obtido: {r2}"


def test_r2_worst_case():
    """Teste R² para pior caso (sempre predizer a média)."""
    y_true = [1, 2, 3, 4, 5]
    y_pred = [3, 3, 3, 3, 3]  # Sempre prediz a média

    r2 = r2_score(y_true, y_pred)
    assert abs(r2 - 0.0) < 0.001, f"R² para predição da média deve ser 0, obtido: {r2}"


def test_evaluate_regression():
    """Teste da função de avaliação completa."""
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1.1, 1.9, 3.1, 3.9, 5.1]

    metrics = evaluate_regression(y_true, y_pred)

    # Verificar se retorna dicionário com chaves corretas
    expected_keys = {"mae", "mse", "rmse", "r2"}
    assert (
        set(metrics.keys()) == expected_keys
    ), f"Chaves esperadas: {expected_keys}, obtidas: {set(metrics.keys())}"

    # Verificar se valores são numéricos
    for metric, value in metrics.items():
        assert isinstance(value, int | float), f"Métrica {metric} deve ser numérica"


def test_random_hidden():
    """Teste oculto com dados aleatórios."""
    np.random.seed(123)
    y_true = np.random.randn(100)
    y_pred = y_true + np.random.normal(0, 0.1, 100)  # Adicionar pequeno ruído

    # MAE deve ser positivo e menor que 1 (pequeno ruído)
    mae = mean_absolute_error(y_true, y_pred)
    assert mae > 0, "MAE deve ser positivo"
    assert mae < 1, "MAE deve ser pequeno para dados com pouco ruído"

    # R² deve ser alto (próximo de 1) para dados com pouco ruído
    r2 = r2_score(y_true, y_pred)
    assert r2 > 0.8, f"R² deve ser alto para dados com pouco ruído, obtido: {r2}"


def test_edge_cases():
    """Teste casos extremos."""
    # Teste com arrays numpy
    y_true = np.array([1, 2, 3])
    y_pred = np.array([1, 2, 3])

    assert (
        abs(mean_absolute_error(y_true, y_pred)) < 0.001
    ), "Deve funcionar com arrays numpy"

    # Teste com listas
    y_true = [10, 20, 30]
    y_pred = [15, 25, 35]

    mae = mean_absolute_error(y_true, y_pred)
    assert abs(mae - 5.0) < 0.001, "Deve funcionar com listas"


def test_mathematical_relationships():
    """Teste relações matemáticas entre métricas."""
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1.5, 2.5, 3.5, 4.5, 5.5]

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)

    # RMSE deve ser a raiz quadrada do MSE
    assert abs(rmse - np.sqrt(mse)) < 0.001, "RMSE deve ser √MSE"

    # Para erros constantes, MAE = RMSE
    assert abs(mae - rmse) < 0.001, "Para erros constantes, MAE = RMSE"
