"""Testes para execução de notebooks."""

from pathlib import Path


def test_notebooks_exist():
    """Verifica se os notebooks existem."""
    project_root = Path(__file__).parent.parent

    # Notebooks de lições
    lesson_notebooks = [
        "modules/01-fundamentos/lessons/01_intro.ipynb",
        "modules/01-fundamentos/lessons/02_fluxo_ml.ipynb",
    ]

    for notebook_path in lesson_notebooks:
        full_path = project_root / notebook_path
        assert full_path.exists(), f"Notebook não encontrado: {notebook_path}"


def test_notebooks_have_valid_json():
    """Verifica se os notebooks têm JSON válido."""
    import json

    project_root = Path(__file__).parent.parent

    notebook_files = list(project_root.glob("modules/**/lessons/*.ipynb"))
    notebook_files.extend(list(project_root.glob("modules/**/exercises/*.ipynb")))

    for notebook_path in notebook_files:
        with open(notebook_path, encoding="utf-8") as f:
            try:
                json.load(f)
            except json.JSONDecodeError as e:
                raise AssertionError(f"JSON inválido em {notebook_path}: {e}") from e


def test_exercise_notebooks_have_solutions():
    """Verifica se exercícios têm código implementado."""
    project_root = Path(__file__).parent.parent

    exercise_notebooks = list(project_root.glob("modules/**/exercises/*.ipynb"))

    for notebook_path in exercise_notebooks:
        # Pular arquivos "complete" que são gabaritos
        if "complete" in notebook_path.name:
            continue

        with open(notebook_path, encoding="utf-8") as f:
            content = f.read()
            # Verificar se não há apenas TODOs vazios
            assert "TODO" in content, f"Notebook {notebook_path} deve ter TODOs para exercícios"


class TestNotebookStructure:
    """Testes de estrutura dos notebooks."""

    def test_lesson_notebooks_structure(self):
        """Verifica estrutura dos notebooks de lições."""
        import json

        project_root = Path(__file__).parent.parent

        lesson_notebooks = list(project_root.glob("modules/**/lessons/*.ipynb"))

        for notebook_path in lesson_notebooks:
            with open(notebook_path, encoding="utf-8") as f:
                notebook = json.load(f)

            # Verificar se tem células
            assert "cells" in notebook, f"Notebook {notebook_path} deve ter células"
            assert len(notebook["cells"]) > 0, f"Notebook {notebook_path} deve ter pelo menos uma célula"

            # Verificar se primeira célula é markdown com título
            first_cell = notebook["cells"][0]
            assert first_cell["cell_type"] == "markdown", f"Primeira célula de {notebook_path} deve ser markdown"

            # Verificar se há células de código
            code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
            assert len(code_cells) > 0, f"Notebook {notebook_path} deve ter pelo menos uma célula de código"
