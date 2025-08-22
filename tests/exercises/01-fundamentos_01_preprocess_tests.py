"""Testes para o exercício de pré-processamento básico."""

from pathlib import Path

import numpy as np
import pandas as pd

from core.grading.api import load_notebook_funcs

# Caminho para o notebook do exercício (relativo ao projeto)
project_root = Path(__file__).parent.parent.parent
notebook_path = project_root / "modules/01-fundamentos/exercises/01_preprocess_aluno.ipynb"

# Carregar funções do notebook do estudante
student = load_notebook_funcs(
    str(notebook_path),
    allowed_imports={"numpy", "pandas"},
)

# Extrair funções
fill_missing_values = student["fill_missing_values"]
detect_outliers_iqr = student["detect_outliers_iqr"]
normalize_data = student["normalize_data"]
train_test_split_custom = student["train_test_split_custom"]


def test_fill_missing_values_mean():
    """Teste básico para preenchimento com média."""
    data = pd.DataFrame({"A": [1, 2, np.nan, 4, 5], "B": [10, np.nan, 30, 40, 50]})

    result = fill_missing_values(data, "mean")

    # Verificar se não há valores ausentes
    assert not result.isnull().any().any(), "Ainda existem valores ausentes"

    # Verificar se a média foi usada corretamente
    expected_A = data["A"].mean()  # (1+2+4+5)/4 = 3.0
    assert abs(result.iloc[2]["A"] - expected_A) < 0.001, "Média incorreta para coluna A"


def test_fill_missing_values_median():
    """Teste para preenchimento com mediana."""
    data = pd.DataFrame({"A": [1, 2, np.nan, 4, 5], "B": [10, np.nan, 30, 40, 50]})

    result = fill_missing_values(data, "median")

    # Verificar se não há valores ausentes
    assert not result.isnull().any().any(), "Ainda existem valores ausentes"

    # Verificar se a mediana foi usada corretamente
    expected_A = data["A"].median()  # 2.5
    assert abs(result.iloc[2]["A"] - expected_A) < 0.001, "Mediana incorreta para coluna A"


def test_detect_outliers_iqr_basic():
    """Teste básico para detecção de outliers."""
    data = pd.DataFrame({"values": [1, 2, 3, 4, 5, 100]})  # 100 é claramente um outlier

    outliers = detect_outliers_iqr(data, "values")

    # Verificar se é uma série booleana
    assert isinstance(outliers, pd.Series), "Retorno deve ser uma pd.Series"
    assert outliers.dtype == bool, "Série deve ser booleana"

    # Verificar se 100 foi detectado como outlier
    assert outliers.iloc[-1] == True, "Valor 100 deveria ser detectado como outlier"

    # Verificar se os outros valores não são outliers
    assert outliers.iloc[0] == False, "Valor 1 não deveria ser outlier"


def test_detect_outliers_iqr_no_outliers():
    """Teste para dados sem outliers."""
    data = pd.DataFrame({"values": [1, 2, 3, 4, 5]})  # Dados normais

    outliers = detect_outliers_iqr(data, "values")

    # Nenhum valor deve ser outlier
    assert not outliers.any(), "Não deveria haver outliers em dados normais"


def test_normalize_data_min_max():
    """Teste para normalização min-max."""
    data = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})

    result = normalize_data(data, "min_max")

    # Verificar se valores estão entre 0 e 1
    for col in result.select_dtypes(include=[np.number]).columns:
        assert result[col].min() >= 0, f"Valor mínimo da coluna {col} deve ser >= 0"
        assert result[col].max() <= 1, f"Valor máximo da coluna {col} deve ser <= 1"
        assert abs(result[col].min() - 0) < 0.001, f"Valor mínimo da coluna {col} deve ser 0"
        assert abs(result[col].max() - 1) < 0.001, f"Valor máximo da coluna {col} deve ser 1"


def test_normalize_data_z_score():
    """Teste para normalização z-score."""
    data = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})

    result = normalize_data(data, "z_score")

    # Verificar se média é aproximadamente 0 e desvio é aproximadamente 1
    for col in result.select_dtypes(include=[np.number]).columns:
        assert abs(result[col].mean()) < 0.001, f"Média da coluna {col} deve ser ~0"
        assert abs(result[col].std() - 1) < 0.001, f"Desvio da coluna {col} deve ser ~1"


def test_train_test_split_basic():
    """Teste básico para divisão treino/teste."""
    X = pd.DataFrame({"feature1": range(100), "feature2": range(100, 200)})
    y = pd.Series(range(50, 150))

    X_train, X_test, y_train, y_test = train_test_split_custom(X, y, test_size=0.2, random_state=42)

    # Verificar tamanhos
    assert len(X_train) == 80, "Tamanho do treino deve ser 80"
    assert len(X_test) == 20, "Tamanho do teste deve ser 20"
    assert len(y_train) == 80, "Tamanho do y_train deve ser 80"
    assert len(y_test) == 20, "Tamanho do y_test deve ser 20"

    # Verificar se são DataFrames/Series
    assert isinstance(X_train, pd.DataFrame), "X_train deve ser DataFrame"
    assert isinstance(X_test, pd.DataFrame), "X_test deve ser DataFrame"
    assert isinstance(y_train, pd.Series), "y_train deve ser Series"
    assert isinstance(y_test, pd.Series), "y_test deve ser Series"


def test_train_test_split_reproducibility():
    """Teste de reprodutibilidade da divisão."""
    X = pd.DataFrame({"feature1": range(50), "feature2": range(50, 100)})
    y = pd.Series(range(25, 75))

    # Duas execuções com mesmo random_state
    X_train1, X_test1, y_train1, y_test1 = train_test_split_custom(X, y, test_size=0.3, random_state=42)
    X_train2, X_test2, y_train2, y_test2 = train_test_split_custom(X, y, test_size=0.3, random_state=42)

    # Verificar se os resultados são idênticos
    pd.testing.assert_frame_equal(X_train1, X_train2, "Divisões com mesmo random_state devem ser idênticas")
    pd.testing.assert_frame_equal(X_test1, X_test2, "Divisões com mesmo random_state devem ser idênticas")
    pd.testing.assert_series_equal(y_train1, y_train2, "Divisões com mesmo random_state devem ser idênticas")
    pd.testing.assert_series_equal(y_test1, y_test2, "Divisões com mesmo random_state devem ser idênticas")


def test_hidden_edge_cases():
    """Testes ocultos para casos extremos."""
    # Teste com dados constantes para normalização
    constant_data = pd.DataFrame({"A": [5, 5, 5, 5, 5]})

    # Normalização min-max com dados constantes
    result_minmax = normalize_data(constant_data, "min_max")
    assert not result_minmax["A"].isnull().any(), "Normalização de dados constantes não deve gerar NaN"

    # Normalização z-score com dados constantes
    result_zscore = normalize_data(constant_data, "z_score")
    assert not result_zscore["A"].isnull().any(), "Normalização de dados constantes não deve gerar NaN"

    # Teste outliers com dados todos iguais
    outliers = detect_outliers_iqr(constant_data, "A")
    assert not outliers.any(), "Dados constantes não devem ter outliers"
