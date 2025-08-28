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

import yaml


def run_command(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[bytes]:
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


def test_status() -> None:
    """Mostra status dos módulos para testes."""
    print("📊 Status dos Módulos para Testes:")
    print("=" * 60)

    project_root = Path.cwd()
    modules_dir = project_root / "modules"

    enabled_count = 0
    disabled_count = 0

    for module_dir in sorted(modules_dir.iterdir()):
        if module_dir.is_dir():
            yaml_path = module_dir / "module.yaml"
            if yaml_path.exists():
                with open(yaml_path, encoding="utf-8") as f:
                    module_data = yaml.safe_load(f)

                test_enabled = module_data.get("test_enabled", True)
                if test_enabled:
                    status = "✅ HABILITADO"
                    enabled_count += 1
                else:
                    status = "❌ DESABILITADO"
                    disabled_count += 1

                print(f"{module_data['slug']:20} | {status:15} | {module_data['title']}")
            else:
                print(f"{module_dir.name:20} | ⚠️  SEM YAML     | (module.yaml não encontrado)")

    print("=" * 60)
    print(f"Total: {enabled_count} habilitados, {disabled_count} desabilitados")

    if disabled_count > 0:
        print("\n💡 Para gerenciar status: uv run python scripts/manage_tests.py [enable|disable] <module-slug>")


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

    run_command(["uv", "run", "python", "scripts/grade_exercise.py", notebook_path, tests_path])
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
  test-status   Mostrar status dos módulos para testes
  run-notebooks Executar todos notebooks
  grade         Executar autograder (use --module e --exercise)
  clean         Limpar arquivos temporários
  install       Instalar projeto em modo desenvolvimento
  update        Atualizar dependências
  help          Mostrar esta ajuda

Exemplos:
  uv run python scripts/tasks.py setup
  uv run python scripts/tasks.py grade --module 03-classificacao --exercise 01_classification_metrics
  uv run python scripts/tasks.py lint

Ou com UV (modo direto após install):
  uv run ml-curso setup
  uv run ml-curso grade --module 03-classificacao --exercise 01_classification_metrics
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
    subparsers.add_parser("test-status", help="Mostrar status dos módulos para testes")
    subparsers.add_parser("run-notebooks", help="Executar notebooks")
    subparsers.add_parser("clean", help="Limpar arquivos temporários")
    subparsers.add_parser("install", help="Instalar em modo desenvolvimento")
    subparsers.add_parser("update", help="Atualizar dependências")
    subparsers.add_parser("help", help="Mostrar ajuda")

    # Comando grade com argumentos
    grade_parser = subparsers.add_parser("grade", help="Executar autograder")
    grade_parser.add_argument("--module", "-m", required=True, help="Módulo (ex: 03-classificacao)")
    grade_parser.add_argument("--exercise", "-e", required=True, help="Exercício (ex: 01_classification_metrics)")

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
        "test-status": test_status,
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
