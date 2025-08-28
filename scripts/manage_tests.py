#!/usr/bin/env python3
"""Script para gerenciar status de teste de módulos."""

import argparse
from pathlib import Path

import yaml


def list_modules_status():
    """Lista o status de teste de todos os módulos."""
    project_root = Path(__file__).parent.parent
    modules_dir = project_root / "modules"

    print("📊 Status dos Módulos para Testes:")
    print("=" * 60)

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


def toggle_module(module_slug, enable):
    """Habilita ou desabilita testes para um módulo específico."""
    project_root = Path(__file__).parent.parent

    # Encontrar o módulo
    module_path = None
    for module_dir in (project_root / "modules").iterdir():
        if module_dir.is_dir():
            yaml_path = module_dir / "module.yaml"
            if yaml_path.exists():
                with open(yaml_path, encoding="utf-8") as f:
                    module_data = yaml.safe_load(f)
                if module_data.get("slug") == module_slug:
                    module_path = yaml_path
                    break

    if not module_path:
        print(f"❌ Módulo '{module_slug}' não encontrado!")
        return False

    # Ler o conteúdo atual
    with open(module_path, encoding="utf-8") as f:
        lines = f.readlines()

    # Procurar e atualizar test_enabled
    test_enabled_line = f"test_enabled: {str(enable).lower()}"
    updated = False

    for i, line in enumerate(lines):
        if line.strip().startswith("test_enabled:"):
            lines[i] = test_enabled_line + "\n"
            updated = True
            break

    # Se não encontrou, adicionar após prerequisites
    if not updated:
        for i, line in enumerate(lines):
            if line.strip().startswith("prerequisites:"):
                # Encontrar o final da seção prerequisites
                j = i + 1
                while j < len(lines) and (lines[j].startswith("  ") or lines[j].strip() == ""):
                    j += 1
                # Adicionar test_enabled com comentário explicativo
                comment = f"# Controle de testes - {'habilitado' if enable else 'desabilitado temporariamente'}\n"
                lines.insert(j, comment)
                lines.insert(j + 1, test_enabled_line + "\n")
                updated = True
                break

    if updated:
        with open(module_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        action = "habilitado" if enable else "desabilitado"
        emoji = "✅" if enable else "❌"
        print(f"{emoji} Módulo '{module_slug}' {action} para testes!")
        return True
    else:
        print(f"⚠️  Não foi possível atualizar o módulo '{module_slug}'")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Gerenciar status de testes de módulos",
        epilog="Exemplos:\n"
        "  uv run python scripts/manage_tests.py list\n"
        "  uv run python scripts/manage_tests.py enable 01-fundamentos\n"
        "  uv run python scripts/manage_tests.py disable 07-redes-neurais",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando list
    subparsers.add_parser("list", help="Lista status de todos os módulos")

    # Comando enable
    enable_parser = subparsers.add_parser("enable", help="Habilita testes para um módulo")
    enable_parser.add_argument("module_slug", help="Slug do módulo (ex: 01-fundamentos)")

    # Comando disable
    disable_parser = subparsers.add_parser("disable", help="Desabilita testes para um módulo")
    disable_parser.add_argument("module_slug", help="Slug do módulo (ex: 01-fundamentos)")

    args = parser.parse_args()

    if args.command == "list":
        list_modules_status()
    elif args.command == "enable":
        toggle_module(args.module_slug, True)
    elif args.command == "disable":
        toggle_module(args.module_slug, False)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
