"""Testes específicos para exercícios de métricas de classificação."""

import numpy as np

from core.grading.api import load_notebook_funcs


def test_accuracy_score():
    """Testa a implementação da acurácia."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs(
        "modules/03-classificacao/exercises/01_classification_metrics.ipynb"
    )
    accuracy_score = funcs["accuracy_score"]

    # Teste com classificação perfeita
    y_true = [1, 0, 1, 1, 0]
    y_pred = [1, 0, 1, 1, 0]

    accuracy = accuracy_score(y_true, y_pred)
    assert (
        accuracy == 1.0
    ), f"Acurácia deveria ser 1.0 para classificação perfeita, obtido: {accuracy}"

    # Teste com 50% de acertos
    y_true = [1, 0, 1, 0]
    y_pred = [1, 1, 1, 1]

    accuracy = accuracy_score(y_true, y_pred)
    assert accuracy == 0.5, f"Acurácia deveria ser 0.5, obtido: {accuracy}"


def test_precision_score():
    """Testa a implementação da precisão."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs(
        "modules/03-classificacao/exercises/01_classification_metrics.ipynb"
    )
    precision_score = funcs["precision_score"]

    # Teste básico
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 0, 0]

    precision = precision_score(y_true, y_pred)
    assert precision == 1.0, f"Precisão deveria ser 1.0, obtido: {precision}"

    # Teste com falsos positivos
    y_true = [1, 0, 0, 0]
    y_pred = [1, 1, 0, 0]

    precision = precision_score(y_true, y_pred)
    assert precision == 0.5, f"Precisão deveria ser 0.5, obtido: {precision}"


def test_recall_score():
    """Testa a implementação do recall."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs(
        "modules/03-classificacao/exercises/01_classification_metrics.ipynb"
    )
    recall_score = funcs["recall_score"]

    # Teste básico
    y_true = [1, 1, 0, 0]
    y_pred = [1, 1, 0, 0]

    recall = recall_score(y_true, y_pred)
    assert recall == 1.0, f"Recall deveria ser 1.0, obtido: {recall}"

    # Teste com falsos negativos
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 0, 0]

    recall = recall_score(y_true, y_pred)
    assert recall == 0.5, f"Recall deveria ser 0.5, obtido: {recall}"


def test_f1_score():
    """Testa a implementação do F1-Score."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs(
        "modules/03-classificacao/exercises/01_classification_metrics.ipynb"
    )
    f1_score = funcs["f1_score"]

    # Teste com classificação perfeita
    y_true = [1, 1, 0, 0]
    y_pred = [1, 1, 0, 0]

    f1 = f1_score(y_true, y_pred)
    assert (
        f1 == 1.0
    ), f"F1-Score deveria ser 1.0 para classificação perfeita, obtido: {f1}"

    # Teste com valores conhecidos
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 0, 0]

    f1 = f1_score(y_true, y_pred)
    expected_f1 = (
        2 * (1.0 * 0.5) / (1.0 + 0.5)
    )  # 2 * (precision * recall) / (precision + recall)
    assert (
        abs(f1 - expected_f1) < 1e-10
    ), f"F1-Score deveria ser {expected_f1:.3f}, obtido: {f1}"


def test_confusion_matrix():
    """Testa a implementação da matriz de confusão."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs(
        "modules/03-classificacao/exercises/01_classification_metrics.ipynb"
    )
    confusion_matrix = funcs["confusion_matrix"]

    # Teste básico
    y_true = [1, 1, 0, 0]
    y_pred = [1, 0, 0, 1]

    cm = confusion_matrix(y_true, y_pred)
    expected_cm = np.array([[1, 1], [1, 1]])  # [[TN, FP], [FN, TP]]

    assert np.array_equal(
        cm, expected_cm
    ), f"Matriz de confusão incorreta. Esperado:\n{expected_cm}\nObtido:\n{cm}"

    # Verificar formato
    assert cm.shape == (2, 2), f"Matriz de confusão deveria ser 2x2, obtido: {cm.shape}"


def test_classification_report():
    """Testa a função de relatório completo."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs(
        "modules/03-classificacao/exercises/01_classification_metrics.ipynb"
    )
    classification_report = funcs["classification_report"]

    y_true = [1, 1, 0, 0]
    y_pred = [1, 1, 0, 0]

    report = classification_report(y_true, y_pred)

    # Verificar se todas as métricas estão presentes
    expected_keys = {"accuracy", "precision", "recall", "f1", "confusion_matrix"}
    assert (
        set(report.keys()) == expected_keys
    ), f"Métricas esperadas: {expected_keys}, obtidas: {set(report.keys())}"

    # Verificar valores para classificação perfeita
    assert (
        report["accuracy"] == 1.0
    ), f"Acurácia deveria ser 1.0, obtido: {report['accuracy']}"
    assert (
        report["precision"] == 1.0
    ), f"Precisão deveria ser 1.0, obtido: {report['precision']}"
    assert (
        report["recall"] == 1.0
    ), f"Recall deveria ser 1.0, obtido: {report['recall']}"
    assert report["f1"] == 1.0, f"F1-Score deveria ser 1.0, obtido: {report['f1']}"


def test_multiclass_accuracy():
    """Testa a acurácia multiclasse."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs(
        "modules/03-classificacao/exercises/01_classification_metrics.ipynb"
    )
    accuracy_multiclass = funcs["accuracy_multiclass"]

    # Teste com 3 classes
    y_true = [0, 1, 2, 0, 1, 2]
    y_pred = [0, 1, 2, 0, 1, 1]  # 1 erro na última predição

    accuracy = accuracy_multiclass(y_true, y_pred)
    expected_accuracy = 5 / 6  # 5 acertos de 6 total

    assert (
        abs(accuracy - expected_accuracy) < 1e-10
    ), f"Acurácia multiclasse deveria ser {expected_accuracy:.3f}, obtido: {accuracy}"


def test_precision_recall_per_class():
    """Testa métricas por classe."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs(
        "modules/03-classificacao/exercises/01_classification_metrics.ipynb"
    )
    precision_recall_per_class = funcs["precision_recall_per_class"]

    # Teste simples com 2 classes
    y_true = [0, 1, 0, 1]
    y_pred = [0, 1, 0, 1]

    per_class = precision_recall_per_class(y_true, y_pred)

    # Verificar se todas as classes estão presentes
    expected_classes = {"class_0", "class_1"}
    assert (
        set(per_class.keys()) == expected_classes
    ), f"Classes esperadas: {expected_classes}, obtidas: {set(per_class.keys())}"

    # Verificar valores para classificação perfeita
    for class_name in expected_classes:
        assert (
            per_class[class_name]["precision"] == 1.0
        ), f"Precisão da {class_name} deveria ser 1.0"
        assert (
            per_class[class_name]["recall"] == 1.0
        ), f"Recall da {class_name} deveria ser 1.0"
        assert per_class[class_name]["f1"] == 1.0, f"F1 da {class_name} deveria ser 1.0"


def test_edge_cases():
    """Testa casos extremos."""
    # Carregar funções do notebook
    funcs = load_notebook_funcs(
        "modules/03-classificacao/exercises/01_classification_metrics.ipynb"
    )
    precision_score = funcs["precision_score"]
    recall_score = funcs["recall_score"]

    # Teste com todos negativos preditos (nenhum positivo predito)
    y_true = [1, 1, 0, 0]
    y_pred = [0, 0, 0, 0]

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)

    assert (
        precision == 0.0
    ), f"Precisão deveria ser 0.0 quando não há positivos preditos, obtido: {precision}"
    assert (
        recall == 0.0
    ), f"Recall deveria ser 0.0 quando não há positivos preditos, obtido: {recall}"
