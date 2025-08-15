#!/usr/bin/env python3
"""
Script de tarefas para o projeto ML Curso.
Substitui o Makefile com comandos baseados em Python/UV.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(
    cmd: list[str], cwd: Path | None = None, check: bool = True
) -> subprocess.CompletedProcess[bytes]:
    """Executa um comando e retorna o resultado."""
    print(f"→ Executando: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=check)


def clean() -> None:
    """Limpa arquivos temporários e cache."""
    print("🧹 Limpando arquivos temporários...")

    # Definir padrões para limpeza
    patterns_to_remove = [
        "**/__pycache__",
        "**/*.pyc",
        "**/.pytest_cache",
        ".coverage",
        "htmlcov",
        ".mypy_cache",
        "**/.ipynb_checkpoints",
    ]

    project_root = Path.cwd()

    for pattern in patterns_to_remove:
        for path in project_root.glob(pattern):
            if path.is_file():
                path.unlink()
                print(f"  Removido arquivo: {path}")
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"  Removido diretório: {path}")

    print("✅ Limpeza concluída!")


def setup() -> None:
    """Configura o ambiente usando UV."""
    print("⚙️ Configurando ambiente com UV...")

    # Verificar se UV está instalado
    if not shutil.which("uv"):
        print("❌ UV não encontrado! Instale com: pip install uv")
        sys.exit(1)

    # Sincronizar dependências
    run_command(["uv", "sync", "--all-extras"])
    print("✅ Ambiente configurado com sucesso!")


def lint() -> None:
    """Verifica código com ruff, black e isort."""
    print("🔍 Verificando código...")

    try:
        run_command(["uv", "run", "python", "-m", "ruff", "check", "."])
        run_command(["uv", "run", "python", "-m", "black", "--check", "."])
        run_command(["uv", "run", "python", "-m", "isort", "--check-only", "."])
        print("✅ Código está conforme as regras!")
    except subprocess.CalledProcessError:
        print("❌ Problemas encontrados no código!")
        sys.exit(1)


def fmt() -> None:
    """Formata código com black e isort."""
    print("🎨 Formatando código...")

    run_command(["uv", "run", "python", "-m", "black", "."])
    run_command(["uv", "run", "python", "-m", "isort", "."])
    print("✅ Código formatado!")


def typecheck() -> None:
    """Verifica tipos com mypy."""
    print("🔬 Verificando tipos...")

    try:
        run_command(["uv", "run", "python", "-m", "mypy", "core/", "scripts/"])
        print("✅ Verificação de tipos passou!")
    except subprocess.CalledProcessError:
        print("❌ Problemas de tipo encontrados!")
        sys.exit(1)


def test() -> None:
    """Executa testes unitários."""
    print("🧪 Executando testes...")

    run_command(
        [
            "uv",
            "run",
            "python",
            "-m",
            "pytest",
            "tests/",
            "--cov=core",
            "--cov-report=term-missing",
            "--cov-report=xml",
        ]
    )
    print("✅ Testes concluídos!")


def run_notebooks() -> None:
    """Executa todos os notebooks."""
    print("📚 Executando notebooks...")

    run_command(["uv", "run", "python", "scripts/run_all_notebooks.py"])
    print("✅ Notebooks executados!")


def grade(module: str, exercise: str) -> None:
    """Executa autograder para um exercício específico."""
    print(f"📝 Avaliando exercício {exercise} do módulo {module}...")

    notebook_path = f"modules/{module}/exercises/{exercise}.ipynb"
    tests_path = f"modules/{module}/exercises/{exercise}_tests.py"

    # Verificar se arquivos existem
    if not Path(notebook_path).exists():
        print(f"❌ Notebook não encontrado: {notebook_path}")
        sys.exit(1)

    if not Path(tests_path).exists():
        print(f"❌ Arquivo de testes não encontrado: {tests_path}")
        sys.exit(1)

    run_command(
        ["uv", "run", "python", "scripts/grade_exercise.py", notebook_path, tests_path]
    )
    print("✅ Avaliação concluída!")


def install() -> None:
    """Instala o projeto em modo desenvolvimento."""
    print("📦 Instalando projeto em modo desenvolvimento...")
    run_command(["uv", "pip", "install", "-e", "."])
    print("✅ Projeto instalado!")


def update() -> None:
    """Atualiza dependências."""
    print("⬆️ Atualizando dependências...")
    run_command(["uv", "lock", "--upgrade"])
    run_command(["uv", "sync"])
    print("✅ Dependências atualizadas!")


def help_cmd() -> None:
    """Mostra ajuda."""
    print(
        """
🚀 ML Curso - Sistema de Tarefas

Comandos disponíveis:

  setup         Configurar ambiente com UV
  lint          Verificar código (ruff + black + isort)
  fmt           Formatar código
  typecheck     Verificação de tipos (mypy)
  test          Executar testes unitários
  run-notebooks Executar todos notebooks
  grade         Executar autograder (use --module e --exercise)
  clean         Limpar arquivos temporários
  install       Instalar projeto em modo desenvolvimento
  update        Atualizar dependências
  help          Mostrar esta ajuda

Exemplos:
  python scripts/tasks.py setup
  python scripts/tasks.py grade --module 02-regressao --exercise 01_mae_metric
  python scripts/tasks.py lint

Ou com UV:
  uv run python scripts/tasks.py setup
  uv run ml-curso grade --module 02-regressao --exercise 01_mae_metric
"""
    )


def main() -> None:
    """Função principal."""
    parser = argparse.ArgumentParser(description="ML Curso Task Runner")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comandos sem argumentos
    subparsers.add_parser("setup", help="Configurar ambiente")
    subparsers.add_parser("lint", help="Verificar código")
    subparsers.add_parser("fmt", help="Formatar código")
    subparsers.add_parser("typecheck", help="Verificar tipos")
    subparsers.add_parser("test", help="Executar testes")
    subparsers.add_parser("run-notebooks", help="Executar notebooks")
    subparsers.add_parser("clean", help="Limpar arquivos temporários")
    subparsers.add_parser("install", help="Instalar em modo desenvolvimento")
    subparsers.add_parser("update", help="Atualizar dependências")
    subparsers.add_parser("help", help="Mostrar ajuda")

    # Comando grade com argumentos
    grade_parser = subparsers.add_parser("grade", help="Executar autograder")
    grade_parser.add_argument(
        "--module", "-m", required=True, help="Módulo (ex: 02-regressao)"
    )
    grade_parser.add_argument(
        "--exercise", "-e", required=True, help="Exercício (ex: 01_mae_metric)"
    )

    args = parser.parse_args()

    if not args.command or args.command == "help":
        help_cmd()
        return

    # Mapeamento de comandos
    commands = {
        "setup": setup,
        "lint": lint,
        "fmt": fmt,
        "typecheck": typecheck,
        "test": test,
        "run-notebooks": run_notebooks,
        "clean": clean,
        "install": install,
        "update": update,
    }

    if args.command == "grade":
        grade(args.module, args.exercise)
    elif args.command in commands:
        commands[args.command]()
    else:
        print(f"❌ Comando desconhecido: {args.command}")
        help_cmd()
        sys.exit(1)


if __name__ == "__main__":
    main()
