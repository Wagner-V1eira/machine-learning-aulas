#!/usr/bin/env python3
"""Run all notebooks in the course."""

import sys
from pathlib import Path

from tqdm import tqdm

# Setup path before core imports
sys.path.insert(0, str(Path(__file__).parent.parent))  # noqa: E402

from core.utils.seeds import fix_random_seeds  # noqa: E402


def execute_notebook(notebook_path: Path) -> bool:
    """
    Execute a single notebook.

    Args:
        notebook_path: Path to notebook

    Returns:
        True if execution succeeded, False otherwise
    """
    try:
        import shutil
        import subprocess
        import tempfile

        # Create a temporary copy to avoid modifying the original
        with tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False) as tmp:
            shutil.copy2(notebook_path, tmp.name)
            tmp_path = Path(tmp.name)

        try:
            # Execute notebook using nbconvert
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "jupyter",
                    "nbconvert",
                    "--to",
                    "notebook",
                    "--execute",
                    "--inplace",
                    "--ExecutePreprocessor.timeout=300",
                    "--ExecutePreprocessor.kernel_name=python3",
                    str(tmp_path),
                ],
                capture_output=True,
                text=True,
                timeout=360,
            )

            if result.returncode == 0:
                print(f"✓ {notebook_path.relative_to(Path.cwd())}")
                return True
            else:
                error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown error"
                print(f"✗ {notebook_path.relative_to(Path.cwd())}: {error_msg}")
                return False

        finally:
            # Clean up temporary file
            tmp_path.unlink(missing_ok=True)

    except subprocess.TimeoutExpired:
        print(f"✗ {notebook_path.relative_to(Path.cwd())}: Timeout after 5 minutes")
        return False
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
