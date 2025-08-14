#!/usr/bin/env python3
"""Generate synthetic datasets for the course."""

# Add project root to path
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs, make_classification, make_regression

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils.seeds import fix_random_seeds


def generate_regression_dataset() -> pd.DataFrame:
    """Generate synthetic regression dataset."""
    fix_random_seeds(42)

    X, y = make_regression(n_samples=500, n_features=5, noise=0.1, random_state=42)

    # Create feature names
    feature_names = [f"feature_{i+1}" for i in range(X.shape[1])]

    # Create DataFrame
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y

    return df


def generate_classification_dataset() -> pd.DataFrame:
    """Generate synthetic classification dataset."""
    fix_random_seeds(42)

    X, y = make_classification(
        n_samples=500, n_features=8, n_classes=3, n_redundant=2, n_informative=6, random_state=42
    )

    # Create feature names
    feature_names = [f"feature_{i+1}" for i in range(X.shape[1])]

    # Create DataFrame
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y

    return df


def generate_clustering_dataset() -> pd.DataFrame:
    """Generate synthetic clustering dataset."""
    fix_random_seeds(42)

    X, y = make_blobs(n_samples=300, centers=4, n_features=2, random_state=42, cluster_std=1.5)

    # Create DataFrame
    df = pd.DataFrame(X, columns=["x", "y"])
    df["true_cluster"] = y

    return df


def generate_time_series_dataset() -> pd.DataFrame:
    """Generate synthetic time series dataset."""
    fix_random_seeds(42)

    # Generate dates
    dates = pd.date_range("2020-01-01", periods=365, freq="D")

    # Generate trend + seasonality + noise
    trend = np.linspace(100, 200, len(dates))
    seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    noise = np.random.normal(0, 5, len(dates))

    values = trend + seasonal + noise

    df = pd.DataFrame({"date": dates, "value": values})

    return df


def main() -> None:
    """Generate all synthetic datasets."""
    project_root = Path(__file__).parent.parent
    datasets_dir = project_root / "datasets" / "synthetic"
    datasets_dir.mkdir(parents=True, exist_ok=True)

    print("Generating synthetic datasets...")

    # Generate datasets
    datasets = {
        "regression_dataset.csv": generate_regression_dataset(),
        "classification_dataset.csv": generate_classification_dataset(),
        "clustering_dataset.csv": generate_clustering_dataset(),
        "timeseries_dataset.csv": generate_time_series_dataset(),
    }

    # Save datasets
    for filename, df in datasets.items():
        filepath = datasets_dir / filename
        df.to_csv(filepath, index=False)
        print(f"✓ Generated {filename} ({len(df)} rows, {len(df.columns)} columns)")

    print(f"\nAll datasets saved to: {datasets_dir}")


if __name__ == "__main__":
    main()
