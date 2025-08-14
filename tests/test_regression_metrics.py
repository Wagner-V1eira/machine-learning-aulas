"""Testes específicos para exercícios de métricas de regressão."""

import numpy as np

from core.grading.api import load_notebook_funcs


def test_mean_absolute_error():
    """Testa a implementação do Mean Absolute Error."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs("regression_metrics_complete.ipynb")
    mean_absolute_error = funcs["mean_absolute_error"]

    # Dados de teste
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1, 2, 3, 4, 5]

    # Teste com previsões perfeitas
    mae_perfect = mean_absolute_error(y_true, y_pred)
    assert mae_perfect == 0.0, f"MAE deveria ser 0 para previsões perfeitas, obtido: {mae_perfect}"

    # Teste com erros conhecidos
    y_true = [1, 2, 3, 4, 5]
    y_pred = [2, 3, 4, 5, 6]  # Erro de +1 em todas as previsões

    mae_error = mean_absolute_error(y_true, y_pred)
    assert mae_error == 1.0, f"MAE deveria ser 1.0, obtido: {mae_error}"


def test_mean_squared_error():
    """Testa a implementação do Mean Squared Error."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs("regression_metrics_complete.ipynb")
    mean_squared_error = funcs["mean_squared_error"]

    # Teste com previsões perfeitas
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1, 2, 3, 4, 5]

    mse_perfect = mean_squared_error(y_true, y_pred)
    assert mse_perfect == 0.0, f"MSE deveria ser 0 para previsões perfeitas, obtido: {mse_perfect}"

    # Teste com erros conhecidos
    y_true = [1, 2, 3, 4, 5]
    y_pred = [2, 3, 4, 5, 6]  # Erro de +1 em todas as previsões

    mse_error = mean_squared_error(y_true, y_pred)
    assert mse_error == 1.0, f"MSE deveria ser 1.0, obtido: {mse_error}"


def test_root_mean_squared_error():
    """Testa a implementação do Root Mean Squared Error."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs("regression_metrics_complete.ipynb")
    root_mean_squared_error = funcs["root_mean_squared_error"]

    # Teste com previsões perfeitas
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1, 2, 3, 4, 5]

    rmse_perfect = root_mean_squared_error(y_true, y_pred)
    assert rmse_perfect == 0.0, f"RMSE deveria ser 0 para previsões perfeitas, obtido: {rmse_perfect}"

    # Teste com erros conhecidos
    y_true = [1, 2, 3, 4, 5]
    y_pred = [2, 3, 4, 5, 6]  # Erro de +1 em todas as previsões

    rmse_error = root_mean_squared_error(y_true, y_pred)
    assert rmse_error == 1.0, f"RMSE deveria ser 1.0, obtido: {rmse_error}"


def test_r2_score():
    """Testa a implementação do R² Score."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs("regression_metrics_complete.ipynb")
    r2_score = funcs["r2_score"]

    # Teste com previsões perfeitas
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1, 2, 3, 4, 5]

    r2_perfect = r2_score(y_true, y_pred)
    assert r2_perfect == 1.0, f"R² deveria ser 1.0 para previsões perfeitas, obtido: {r2_perfect}"

    # Teste com previsões = média (R² = 0)
    y_true = [1, 2, 3, 4, 5]
    y_pred = [3, 3, 3, 3, 3]  # Todas as previsões = média

    r2_mean = r2_score(y_true, y_pred)
    assert abs(r2_mean - 0.0) < 1e-10, f"R² deveria ser ~0.0 para previsões = média, obtido: {r2_mean}"


def test_evaluate_regression():
    """Testa a função de avaliação completa."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs("regression_metrics_complete.ipynb")
    evaluate_regression = funcs["evaluate_regression"]

    y_true = [1, 2, 3, 4, 5]
    y_pred = [1, 2, 3, 4, 5]

    metrics = evaluate_regression(y_true, y_pred)

    # Verificar se todas as métricas estão presentes
    expected_keys = {"mae", "mse", "rmse", "r2"}
    assert set(metrics.keys()) == expected_keys, f"Métricas esperadas: {expected_keys}, obtidas: {set(metrics.keys())}"

    # Verificar valores para previsões perfeitas
    assert metrics["mae"] == 0.0, f"MAE deveria ser 0.0, obtido: {metrics['mae']}"
    assert metrics["mse"] == 0.0, f"MSE deveria ser 0.0, obtido: {metrics['mse']}"
    assert metrics["rmse"] == 0.0, f"RMSE deveria ser 0.0, obtido: {metrics['rmse']}"
    assert metrics["r2"] == 1.0, f"R² deveria ser 1.0, obtido: {metrics['r2']}"


def test_metrics_with_numpy_arrays():
    """Testa se as métricas funcionam com arrays numpy."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs("regression_metrics_complete.ipynb")
    mean_absolute_error = funcs["mean_absolute_error"]
    mean_squared_error = funcs["mean_squared_error"]
    root_mean_squared_error = funcs["root_mean_squared_error"]
    r2_score = funcs["r2_score"]

    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.1, 1.9, 3.1, 3.9, 5.1])

    # Testa todas as métricas
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    # Verificar se são números válidos
    assert isinstance(mae, float), f"MAE deveria ser float, obtido: {type(mae)}"
    assert isinstance(mse, float), f"MSE deveria ser float, obtido: {type(mse)}"
    assert isinstance(rmse, float), f"RMSE deveria ser float, obtido: {type(rmse)}"
    assert isinstance(r2, float), f"R² deveria ser float, obtido: {type(r2)}"

    # Verificar valores aproximados
    assert abs(mae - 0.1) < 1e-10, f"MAE deveria ser ~0.1, obtido: {mae}"
    assert abs(mse - 0.01) < 1e-10, f"MSE deveria ser ~0.01, obtido: {mse}"
    assert abs(rmse - 0.1) < 1e-10, f"RMSE deveria ser ~0.1, obtido: {rmse}"
    assert r2 > 0.95, f"R² deveria ser > 0.95, obtido: {r2}"
