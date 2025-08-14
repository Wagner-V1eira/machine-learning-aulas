"""I/O utilities for the ML course."""

import json
from pathlib import Path
from typing import Any

import yaml


def load_yaml(file_path: Path | str) -> dict[str, Any]:
    """Load YAML file."""
    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(data: dict[str, Any], file_path: Path | str) -> None:
    """Save data to YAML file."""
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)


def load_json(file_path: Path | str) -> dict[str, Any]:
    """Load JSON file."""
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict[str, Any], file_path: Path | str) -> None:
    """Save data to JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
