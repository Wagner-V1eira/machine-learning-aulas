#!/usr/bin/env python3
"""Run all notebooks in the course."""

import sys
from pathlib import Path

import nbclient
from nbformat import read as nbread
from nbformat import write as nbwrite
from tqdm import tqdm

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils.seeds import fix_random_seeds


def execute_notebook(notebook_path: Path) -> bool:
    """
    Execute a single notebook.

    Args:
        notebook_path: Path to notebook

    Returns:
        True if execution succeeded, False otherwise
    """
    try:
        # Read notebook
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = nbread(f, as_version=4)

        # Execute notebook
        client = nbclient.NotebookClient(nb, timeout=300, kernel_name="python3")  # 5 minutes max per notebook

        with client.setup_kernel():
            client.execute()

        print(f"✓ {notebook_path.relative_to(Path.cwd())}")
        return True

    except Exception as e:
        print(f"✗ {notebook_path.relative_to(Path.cwd())}: {e}")
        return False


def main() -> None:
    """Main function to run all notebooks."""
    project_root = Path(__file__).parent.parent

    # Find all lesson notebooks
    lesson_notebooks = list(project_root.glob("modules/*/lessons/*.ipynb"))

    if not lesson_notebooks:
        print("No lesson notebooks found!")
        return

    print(f"Found {len(lesson_notebooks)} notebooks to execute")
    print("=" * 50)

    # Fix random seeds for reproducibility
    fix_random_seeds(42)

    # Execute notebooks
    failed_notebooks = []

    for notebook_path in tqdm(lesson_notebooks, desc="Executing notebooks"):
        if not execute_notebook(notebook_path):
            failed_notebooks.append(notebook_path)

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    total = len(lesson_notebooks)
    succeeded = total - len(failed_notebooks)

    print(f"Total notebooks: {total}")
    print(f"Succeeded: {succeeded}")
    print(f"Failed: {len(failed_notebooks)}")

    if failed_notebooks:
        print("\nFailed notebooks:")
        for nb in failed_notebooks:
            print(f"  - {nb.relative_to(project_root)}")
        sys.exit(1)
    else:
        print("\n✓ All notebooks executed successfully!")


if __name__ == "__main__":
    main()
