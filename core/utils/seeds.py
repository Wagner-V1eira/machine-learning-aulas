"""Utility functions for the ML course."""

import random

import numpy as np


def fix_random_seeds(seed: int = 42) -> None:
    """
    Fix random seeds for reproducibility.

    Args:
        seed: Random seed value
    """
    random.seed(seed)
    np.random.seed(seed)

    # Set PyTorch seeds if available
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass
