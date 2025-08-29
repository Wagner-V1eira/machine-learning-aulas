#!/usr/bin/env python3
"""
Script para verificar se a estrutura do aluno está correta.
Apenas verifica exercícios marcados com create: true no module.yaml.

Uso: uv run check-structure.py
"""

from pathlib import Path

import yaml


def check_student_structure():
    """Verifica se os arquivos _aluno estão configurados corretamente"""
    modules_dir = Path("modules")
    issues = []
    all_good = []

    print("🔍 Verificando estrutura do aluno...\n")

    for module in modules_dir.iterdir():
        if not module.is_dir():
            continue

        # Verificar se existe module.yaml
        yaml_path = module / "module.yaml"
        if not yaml_path.exists():
            print(f"⚠️  {module.name}: sem module.yaml, pulando...")
            continue

        # Carregar configuração do módulo
        try:
            with open(yaml_path, encoding="utf-8") as f:
                module_data = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Erro ao ler {yaml_path}: {e}")
            continue

        exercises_dir = module / "exercises"
        if not exercises_dir.exists():
            continue

        module_issues = []
        module_good = []
        module_skipped = []

        # Obter lista de exercícios que devem ser criados
        exercises = module_data.get("exercises", [])
        exercises_to_create = {}

        for exercise in exercises:
            if isinstance(exercise, dict):
                # Extrair nome do notebook do slug ou notebook field
                notebook_name = exercise.get("notebook", f"{exercise['slug']}.ipynb")
                if notebook_name.startswith("exercises/"):
                    notebook_name = notebook_name.replace("exercises/", "")

                if exercise.get("create", False):
                    exercises_to_create[notebook_name] = exercise

        # Verificar templates e arquivos do aluno
        templates = list(exercises_dir.glob("*.ipynb"))
        templates = [f for f in templates if "_aluno" not in f.name]

        for template in templates:
            stem = template.stem
            aluno_file = exercises_dir / f"{stem}_aluno.ipynb"

            # Verificar se este exercício deve ser criado
            if template.name not in exercises_to_create:
                module_skipped.append(f"⏭️  {template.name} (não habilitado para criação)")
                continue

            if aluno_file.exists():
                module_good.append(f"✅ {aluno_file.name}")
            else:
                module_issues.append(f"❌ Faltando: {aluno_file.name}")

        if module_issues or module_good or module_skipped:
            print(f"📁 {module.name}:")
            for item in module_good:
                print(f"   {item}")
            for item in module_issues:
                print(f"   {item}")
            for item in module_skipped:
                print(f"   {item}")
            print()

        issues.extend(module_issues)
        all_good.extend(module_good)

    # Resumo final
    if issues:
        print("⚠️  Problemas encontrados:")
        for issue in issues:
            print(f"   {issue}")
        print(f"\n💡 Execute 'uv run setup-student.py' para corrigir automaticamente.")
    else:
        print("🎉 Todos os exercícios habilitados estão configurados corretamente!")

    print(f"\n📊 Resumo: {len(all_good)} exercícios prontos, {len(issues)} pendentes")
    if len(all_good) > 0 or len(issues) == 0:
        print("ℹ️  Exercícios não habilitados (create: false) são ignorados na verificação")

    return len(issues) == 0


def check_gitignore():
    """Verifica se .gitignore está configurado corretamente"""
    gitignore_path = Path(".gitignore")

    if not gitignore_path.exists():
        print("⚠️  Arquivo .gitignore não encontrado!")
        return False

    content = gitignore_path.read_text()

    required_patterns = ["*_aluno.ipynb", "*_aluno.py", "*_student.*"]
    missing = [pattern for pattern in required_patterns if pattern not in content]

    if missing:
        print("⚠️  .gitignore não está configurado corretamente!")
        print("   Padrões faltando:", ", ".join(missing))
        return False

    print("✅ .gitignore configurado corretamente")
    return True


if __name__ == "__main__":
    structure_ok = check_student_structure()
    gitignore_ok = check_gitignore()

    if structure_ok and gitignore_ok:
        print("\n🚀 Tudo pronto para começar!")
    else:
        print("\n🔧 Algumas configurações precisam ser ajustadas.")
