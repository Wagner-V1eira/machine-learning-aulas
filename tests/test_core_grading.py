"""Testes para o sistema de grading."""

import tempfile
from pathlib import Path

import pytest

from core.grading.api import grade_exercise, load_notebook_funcs
from core.grading.sandbox import execute_with_timeout


def test_execute_with_timeout_basic():
    """Teste básico de execução com timeout."""
    code = "x = 1 + 1"
    globals_dict = {}

    execute_with_timeout(code, globals_dict, timeout=5)
    assert globals_dict["x"] == 2


def test_execute_with_timeout_restricted():
    """Teste de restrições de segurança."""
    # Código que tenta importar módulo perigoso
    code = "import os"
    globals_dict = {}

    # Não deve quebrar, mas 'os' não deve estar disponível
    execute_with_timeout(code, globals_dict, timeout=5)


def test_grade_exercise_success():
    """Teste de grading com exercício simples."""
    # Criar notebook temporário
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".ipynb", delete=False
    ) as nb_file:
        notebook_content = {
            "nbformat": 4,
            "nbformat_minor": 4,
            "metadata": {},
            "cells": [
                {
                    "cell_type": "code",
                    "metadata": {},
                    "execution_count": None,
                    "outputs": [],
                    "source": ["def add_numbers(a, b):\n", "    return a + b"],
                }
            ],
        }
        import json

        json.dump(notebook_content, nb_file)
        nb_path = nb_file.name

    # Criar arquivo de testes temporário
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as test_file:
        test_content = """
from core.grading.api import load_notebook_funcs

student = load_notebook_funcs("{}", allowed_imports={{"numpy", "pandas"}})
add_numbers = student["add_numbers"]

def test_basic():
    assert add_numbers(2, 3) == 5
""".format(
            nb_path.replace("\\", "\\\\")
        )
        test_file.write(test_content)
        test_path = test_file.name

    try:
        # Executar grading
        result = grade_exercise(nb_path, test_path, {"numpy", "pandas"})

        assert result["status"] == "success"
        assert result["score"] > 0

    finally:
        # Limpar arquivos temporários
        Path(nb_path).unlink()
        Path(test_path).unlink()


def test_load_notebook_funcs_error():
    """Teste de erro ao carregar notebook inexistente."""
    with pytest.raises(FileNotFoundError):
        load_notebook_funcs("nonexistent.ipynb")


class TestGradingIntegration:
    """Testes de integração do sistema de grading."""

    def test_simple_function_extraction(self):
        """Teste de extração de função simples."""
        # Criar notebook temporário
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ipynb", delete=False
        ) as nb_file:
            notebook_content = {
                "nbformat": 4,
                "nbformat_minor": 4,
                "metadata": {},
                "cells": [
                    {
                        "cell_type": "code",
                        "metadata": {},
                        "execution_count": None,
                        "outputs": [],
                        "source": [
                            "import numpy as np\n",
                            "def multiply(x, y):\n",
                            "    return x * y\n",
                            "def square(x):\n",
                            "    return x ** 2",
                        ],
                    }
                ],
            }
            import json

            json.dump(notebook_content, nb_file)
            nb_path = nb_file.name

        try:
            functions = load_notebook_funcs(nb_path, {"numpy"})

            assert "multiply" in functions
            assert "square" in functions
            assert functions["multiply"](3, 4) == 12
            assert functions["square"](5) == 25

        finally:
            Path(nb_path).unlink()

    def test_forbidden_import(self):
        """Teste de import proibido."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ipynb", delete=False
        ) as nb_file:
            notebook_content = {
                "nbformat": 4,
                "nbformat_minor": 4,
                "metadata": {},
                "cells": [
                    {
                        "cell_type": "code",
                        "metadata": {},
                        "execution_count": None,
                        "outputs": [],
                        "source": [
                            "import os\n",
                            "def bad_function():\n",
                            "    return os.getcwd()",
                        ],
                    }
                ],
            }
            import json

            json.dump(notebook_content, nb_file)
            nb_path = nb_file.name

        try:
            with pytest.raises(ImportError):
                load_notebook_funcs(nb_path, {"numpy"})

        finally:
            Path(nb_path).unlink()
