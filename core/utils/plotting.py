"""Plotting utilities for the ML course."""


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def setup_plotting_style() -> None:
    """Set up consistent plotting style."""
    plt.style.use("default")
    sns.set_palette("husl")
    plt.rcParams.update(
        {
            "figure.figsize": (10, 6),
            "font.size": 12,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 11,
        }
    )


def plot_regression_results(
    y_true: np.ndarray, y_pred: np.ndarray, title: str | None = None
) -> plt.Figure:
    """
    Plot regression results (actual vs predicted).

    Args:
        y_true: True values
        y_pred: Predicted values
        title: Plot title

    Returns:
        matplotlib Figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Scatter plot
    ax1.scatter(y_true, y_pred, alpha=0.6)
    ax1.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], "r--", lw=2)
    ax1.set_xlabel("Valores Reais")
    ax1.set_ylabel("Valores Preditos")
    ax1.set_title("Predito vs Real")

    # Residuals
    residuals = y_true - y_pred
    ax2.scatter(y_pred, residuals, alpha=0.6)
    ax2.axhline(y=0, color="r", linestyle="--")
    ax2.set_xlabel("Valores Preditos")
    ax2.set_ylabel("Resíduos")
    ax2.set_title("Resíduos vs Preditos")

    if title:
        fig.suptitle(title, fontsize=16)

    plt.tight_layout()
    return fig


def plot_classification_results(
    y_true: np.ndarray, y_pred: np.ndarray, class_names: list | None = None
) -> plt.Figure:
    """
    Plot classification results (confusion matrix).

    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: Names of classes

    Returns:
        matplotlib Figure object
    """
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        ax=ax,
        xticklabels=class_names,
        yticklabels=class_names,
    )
    ax.set_xlabel("Predito")
    ax.set_ylabel("Real")
    ax.set_title("Matriz de Confusão")

    return fig
