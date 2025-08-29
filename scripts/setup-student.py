#!/usr/bin/env python3
"""
Script para configurar área de trabalho do aluno.
Copia templates dos exercícios para versões _aluno.
Apenas cria arquivos _aluno para exercícios marcados com create: true no module.yaml.

Uso: uv run setup-student.py
"""

import shutil
from pathlib import Path

import yaml


def setup_student_workspace():
    """Copia templates para arquivos _aluno onde o aluno pode trabalhar"""
    modules_dir = Path("modules")
    copied_files = 0

    print("🚀 Configurando área de trabalho do aluno...")

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

        print(f"\n📁 Processando {module.name}...")

        # Obter lista de exercícios que devem ser criados
        exercises = module_data.get("exercises", [])
        exercises_to_create = {}

        for exercise in exercises:
            if isinstance(exercise, dict) and exercise.get("create", False):
                # Extrair nome do notebook do slug ou notebook field
                notebook_name = exercise.get("notebook", f"{exercise['slug']}.ipynb")
                if notebook_name.startswith("exercises/"):
                    notebook_name = notebook_name.replace("exercises/", "")
                exercises_to_create[notebook_name] = exercise

        if not exercises_to_create:
            print(f"   ℹ️  Nenhum exercício marcado com create: true")
            continue

        # Procurar por notebooks que NÃO sejam _aluno
        for template_file in exercises_dir.glob("*.ipynb"):
            if "_aluno" in template_file.name:
                continue  # Pular arquivos que já são do aluno

            # Verificar se este exercício deve ser criado
            if template_file.name not in exercises_to_create:
                print(f"   ⏭️  {template_file.name} não marcado para criação")
                continue

            # Criar nome do arquivo do aluno
            stem = template_file.stem  # nome sem extensão
            aluno_file = exercises_dir / f"{stem}_aluno.ipynb"

            # Copiar apenas se ainda não existir
            if not aluno_file.exists():
                print(f"   📝 Copiando {template_file.name} → {aluno_file.name}")
                shutil.copy2(template_file, aluno_file)
                copied_files += 1
            else:
                print(f"   ✅ {aluno_file.name} já existe")

    print(f"\n🎉 Configuração concluída! {copied_files} arquivos copiados.")
    print("\n📋 Próximos passos:")
    print("   1. Execute 'uv run jupyter lab' para abrir o Jupyter")
    print("   2. Trabalhe apenas em arquivos *_aluno.ipynb")
    print("   3. Use 'uv run scripts/check-structure.py' para verificar sua configuração")


if __name__ == "__main__":
    setup_student_workspace()
