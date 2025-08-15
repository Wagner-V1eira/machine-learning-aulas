"""Grading API for notebook exercises."""

from pathlib import Path
from typing import Any

from nbformat import read as nbread

from .sandbox import execute_with_timeout


def load_notebook_funcs(notebook_path: str, allowed_imports: set[str] | None = None) -> dict[str, Any]:
    """
    Load functions from a notebook after executing it in a sandboxed environment.

    Args:
        notebook_path: Path to the notebook file
        allowed_imports: Set of allowed import modules

    Returns:
        Dictionary mapping function names to function objects

    Raises:
        ImportError: If notebook uses forbidden imports
        RuntimeError: If notebook execution fails
    """
    if allowed_imports is None:
        allowed_imports = {
            "numpy",
            "pandas",
            "sklearn",
            "matplotlib",
            "scipy",
            "seaborn",
            "typing",
        }

    notebook_path_obj = Path(notebook_path)
    if not notebook_path_obj.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    # Read notebook
    nb = nbread(notebook_path_obj, as_version=4)  # type: ignore[no-untyped-call]

    # Extract code cells
    code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]

    # Validate imports
    all_code = "\n".join(cell.source for cell in code_cells)
    _validate_imports(all_code, allowed_imports)

    # Execute notebook in controlled environment
    globals_dict = {"__name__": "__main__"}

    try:
        for cell in code_cells:
            if cell.source.strip():
                execute_with_timeout(cell.source, globals_dict, timeout=30)
    except Exception as e:
        raise RuntimeError(f"Notebook execution failed: {e}") from e

    # Extract functions
    functions = {}
    for name, obj in globals_dict.items():
        if callable(obj) and not name.startswith("_"):
            functions[name] = obj

    return functions


def _validate_imports(code: str, allowed_imports: set[str]) -> None:
    """Validate that code only uses allowed imports."""
    import ast

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise RuntimeError(f"Syntax error in code: {e}") from e

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]
                if module not in allowed_imports:
                    raise ImportError(f"Import not allowed: {module}")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module = node.module.split(".")[0]
                if module not in allowed_imports:
                    raise ImportError(f"Import not allowed: {module}")


def grade_exercise(notebook_path: str, tests_path: str, allowed_imports: set[str] | None = None) -> dict[str, Any]:
    """
    Grade a student exercise notebook.

    Args:
        notebook_path: Path to student notebook
        tests_path: Path to test file
        allowed_imports: Set of allowed import modules

    Returns:
        Dictionary with grading results
    """
    try:
        # Load student functions
        student_funcs = load_notebook_funcs(notebook_path, allowed_imports)

        # Execute tests
        test_results = _execute_tests(tests_path, student_funcs)

        # Calculate score
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results if result["passed"])
        score = int((passed_tests / total_tests) * 100) if total_tests > 0 else 0

        return {
            "score": score,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "test_results": test_results,
            "status": "success",
        }

    except Exception as e:
        return {
            "score": 0,
            "total_tests": 0,
            "passed_tests": 0,
            "test_results": [],
            "status": "error",
            "error": str(e),
        }


def _execute_tests(tests_path: str, student_funcs: dict[str, Any]) -> list[dict[str, Any]]:
    """Execute test file and return results."""
    import importlib.util

    # Load test module
    spec = importlib.util.spec_from_file_location("test_module", tests_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load test file: {tests_path}")

    test_module = importlib.util.module_from_spec(spec)

    # Inject student functions into test module
    for name, func in student_funcs.items():
        setattr(test_module, name, func)

    # Load the module
    spec.loader.exec_module(test_module)

    # Find and execute test functions
    test_results = []
    for attr_name in dir(test_module):
        if attr_name.startswith("test_"):
            test_func = getattr(test_module, attr_name)
            if callable(test_func):
                try:
                    test_func()
                    test_results.append({"name": attr_name, "passed": True, "error": None})
                except Exception as e:
                    test_results.append({"name": attr_name, "passed": False, "error": str(e)})

    return test_results
