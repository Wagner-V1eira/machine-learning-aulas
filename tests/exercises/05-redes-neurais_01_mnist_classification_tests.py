"""Testes para o exercício de classificação MNIST."""

from pathlib import Path

import numpy as np
import pandas as pd

from core.grading.api import load_notebook_funcs

# Caminho para o notebook do exercício (relativo ao projeto)
project_root = Path(__file__).parent.parent.parent
notebook_path = project_root / "modules/05-redes-neurais/exercises/01_mnist_classification_aluno.ipynb"

# Carregar funções do notebook do estudante
student = load_notebook_funcs(
    str(notebook_path),
    allowed_imports={"numpy", "pandas", "sklearn", "matplotlib", "seaborn"},
)


def test_data_loaded():
    """Verifica se os dados MNIST foram carregados corretamente."""
    assert "X" in student, "Variável 'X' não encontrada"
    assert "y" in student, "Variável 'y' não encontrada"

    X = student["X"]
    y = student["y"]

    # Verificar shape básico
    assert len(X.shape) == 2, "X deve ser 2D (n_samples, n_features)"
    assert X.shape[1] == 784, "X deve ter 784 features (28x28 pixels)"
    assert len(y.shape) == 1, "y deve ser 1D"
    assert len(X) == len(y), "X e y devem ter o mesmo número de amostras"

    # Verificar valores
    assert len(np.unique(y)) == 10, "Deve haver 10 classes (dígitos 0-9)"
    assert set(np.unique(y)) == set(range(10)), "Classes devem ser 0-9"


def test_train_test_split():
    """Verifica se os dados foram divididos em treino e teste."""
    required_vars = ["X_train", "X_test", "y_train", "y_test"]

    for var in required_vars:
        assert var in student, f"Variável '{var}' não encontrada"

    X_train = student["X_train"]
    X_test = student["X_test"]
    y_train = student["y_train"]
    y_test = student["y_test"]

    # Verificar que split foi feito
    assert len(X_train) > 0, "X_train está vazio"
    assert len(X_test) > 0, "X_test está vazio"

    # Verificar proporção aproximada (80/20)
    total = len(X_train) + len(X_test)
    train_ratio = len(X_train) / total
    assert 0.7 < train_ratio < 0.9, "Proporção de treino deve estar próxima de 80%"

    # Verificar consistência
    assert len(X_train) == len(y_train), "X_train e y_train devem ter mesmo tamanho"
    assert len(X_test) == len(y_test), "X_test e y_test devem ter mesmo tamanho"


def test_data_normalization():
    """Verifica se os dados foram normalizados."""
    # Verificar se existe versão normalizada
    assert (
        "X_train_norm" in student or "X_train_scaled" in student
    ), "Dados de treino normalizados não encontrados (X_train_norm ou X_train_scaled)"
    assert (
        "X_test_norm" in student or "X_test_scaled" in student
    ), "Dados de teste normalizados não encontrados (X_test_norm ou X_test_scaled)"

    # Pegar a versão normalizada (tentar ambos os nomes)
    X_train_norm = student.get("X_train_norm", student.get("X_train_scaled"))
    X_test_norm = student.get("X_test_norm", student.get("X_test_scaled"))

    assert X_train_norm is not None, "Dados normalizados não encontrados"

    # Converter para numpy array se necessário
    if hasattr(X_train_norm, "values"):
        X_train_norm_array = X_train_norm.values
    else:
        X_train_norm_array = np.array(X_train_norm)

    # Verificar range de valores (normalizado para [0,1] ou z-score)
    min_val = float(X_train_norm_array.min())
    max_val = float(X_train_norm_array.max())

    assert min_val >= -5, "Valores muito negativos, verificar normalização"
    assert max_val <= 5, "Valores muito altos, verificar normalização"

    # Se for normalização [0,1]
    if min_val >= 0 and max_val <= 1:
        assert abs(max_val - 1.0) < 0.01, "Máximo deve ser próximo de 1.0"
        assert abs(min_val - 0.0) < 0.01, "Mínimo deve ser próximo de 0.0"


def test_mlp_basic_trained():
    """Verifica se um MLP básico foi treinado."""
    assert "mlp_basic" in student, "Modelo 'mlp_basic' não encontrado"

    mlp_basic = student["mlp_basic"]

    # Verificar se é um MLPClassifier
    from sklearn.neural_network import MLPClassifier

    assert isinstance(mlp_basic, MLPClassifier), "mlp_basic deve ser um MLPClassifier"

    # Verificar se foi treinado (tem atributo n_iter_)
    assert hasattr(mlp_basic, "n_iter_"), "Modelo não foi treinado (falta atributo n_iter_)"

    # Verificar que tem pelo menos uma camada oculta
    if hasattr(mlp_basic, "hidden_layer_sizes"):
        hidden_layers = mlp_basic.hidden_layer_sizes  # type: ignore
        if isinstance(hidden_layers, int):
            assert hidden_layers > 0, "Deve ter pelo menos 1 neurônio na camada oculta"
        else:
            assert len(hidden_layers) > 0, "Deve ter pelo menos 1 camada oculta"


def test_mlp_basic_accuracy():
    """Verifica se o MLP básico alcançou uma acurácia mínima."""
    assert (
        "acc_basic" in student or "y_pred_basic" in student
    ), "Acurácia ou predições do modelo básico não encontradas"

    if "acc_basic" in student:
        acc_basic = student["acc_basic"]
        assert acc_basic > 0.80, "Acurácia do MLP básico deve ser > 80%"
        assert acc_basic <= 1.0, "Acurácia não pode ser > 100%"
    else:
        # Calcular acurácia a partir das predições
        y_pred_basic = student["y_pred_basic"]
        y_test = student["y_test"]
        from sklearn.metrics import accuracy_score

        acc_basic = accuracy_score(y_test, y_pred_basic)
        assert acc_basic > 0.80, "Acurácia do MLP básico deve ser > 80%"


def test_architecture_comparison():
    """Verifica se diferentes arquiteturas foram testadas."""
    # Procurar por variáveis que indiquem comparação
    possible_vars = ["resultados", "df_resultados", "arquiteturas"]

    found = False
    for var in possible_vars:
        if var in student:
            found = True
            resultados = student[var]

            # Se for DataFrame, verificar se tem múltiplas arquiteturas
            if isinstance(resultados, pd.DataFrame):
                assert len(resultados) >= 3, "Deve testar pelo menos 3 arquiteturas diferentes"
                assert (
                    "acuracia" in resultados.columns or "acurácia" in resultados.columns
                ), "DataFrame deve conter coluna de acurácia"
            elif isinstance(resultados, list):
                assert len(resultados) >= 3, "Deve testar pelo menos 3 arquiteturas diferentes"
            break

    assert found, "Comparação de arquiteturas não encontrada (procure por 'resultados' ou 'df_resultados')"


def test_confusion_matrix_created():
    """Verifica se a matriz de confusão foi criada."""
    assert "cm" in student, "Matriz de confusão 'cm' não encontrada"

    cm = student["cm"]

    # Verificar shape (deve ser 10x10 para MNIST)
    assert cm.shape == (10, 10), "Matriz de confusão deve ser 10x10"

    # Verificar que é numérica
    assert np.issubdtype(cm.dtype, np.integer), "Matriz de confusão deve conter inteiros"

    # Verificar que a soma é razoável
    total_predictions = cm.sum()
    assert total_predictions > 0, "Matriz de confusão está vazia"


def test_error_analysis():
    """Verifica se a análise de erros foi realizada."""
    # Procurar por índices de erros
    possible_vars = ["erros_idx", "indices_erros", "wrong_predictions"]

    found = False
    for var in possible_vars:
        if var in student:
            found = True
            erros = student[var]
            assert len(erros) > 0, "Deve haver alguns erros para análise"
            break

    # Aceitar se não encontrado explicitamente, mas deve ter matriz de confusão
    if not found:
        assert "cm" in student, "Deve ter matriz de confusão ou índices de erros"


def test_regularization_tested():
    """Verifica se diferentes valores de regularização foram testados."""
    # Procurar por variáveis de resultados de regularização
    possible_vars = ["resultados_reg", "df_reg", "alphas"]

    found = False
    for var in possible_vars:
        if var in student:
            found = True
            reg_results = student[var]

            if isinstance(reg_results, pd.DataFrame):
                assert len(reg_results) >= 3, "Deve testar pelo menos 3 valores de alpha"
                # Verificar colunas esperadas
                possible_cols = ["alpha", "acuracia_teste", "acuracia_treino", "acurácia_teste", "acurácia_treino"]
                has_alpha = any(col in reg_results.columns for col in ["alpha"])
                has_acc = any(col in reg_results.columns for col in possible_cols[1:])
                assert has_alpha, "DataFrame deve conter coluna 'alpha'"
                assert has_acc, "DataFrame deve conter colunas de acurácia"
            elif isinstance(reg_results, list):
                assert len(reg_results) >= 3, "Deve testar pelo menos 3 valores de alpha"
            break

    assert found, "Experimentação com regularização não encontrada"


def test_best_model_performance():
    """Verifica se o melhor modelo tem performance aceitável."""
    # Procurar pelo melhor modelo ou suas métricas
    possible_models = ["melhor_mlp", "best_mlp", "final_model"]

    found_model = False
    for var in possible_models:
        if var in student:
            found_model = True
            model = student[var]

            # Fazer predições se tivermos dados de teste
            if "X_test_norm" in student and "y_test" in student:
                X_test_norm = student["X_test_norm"]
                y_test = student["y_test"]

                y_pred = model.predict(X_test_norm)
                from sklearn.metrics import accuracy_score

                acc = accuracy_score(y_test, y_pred)

                assert acc > 0.85, f"Melhor modelo deve ter acurácia > 85%, obteve {acc:.2%}"
            break

    # Se não encontrou modelo, verificar se tem acurácia reportada
    if not found_model:
        possible_acc = ["melhor_acc", "best_accuracy", "final_accuracy"]
        for var in possible_acc:
            if var in student:
                acc = student[var]
                assert acc > 0.85, f"Melhor acurácia deve ser > 85%, obteve {acc:.2%}"
                found_model = True
                break

    # Aceitar se fez todo o exercício mas não salvou como "melhor"
    if not found_model:
        assert "mlp_basic" in student, "Pelo menos o modelo básico deve existir"
