#!/usr/bin/env python3
"""
Script para configurar área de trabalho do aluno.
Copia templates dos exercícios para versões _aluno.

Uso: uv run setup-student.py
"""

import shutil
from pathlib import Path


def setup_student_workspace():
    """Copia templates para arquivos _aluno onde o aluno pode trabalhar"""
    modules_dir = Path("modules")
    copied_files = 0

    print("🚀 Configurando área de trabalho do aluno...")

    for module in modules_dir.iterdir():
        if not module.is_dir():
            continue

        exercises_dir = module / "exercises"
        if not exercises_dir.exists():
            continue

        print(f"\n📁 Processando {module.name}...")

        # Procurar por notebooks que NÃO sejam _aluno
        for template_file in exercises_dir.glob("*.ipynb"):
            if "_aluno" in template_file.name:
                continue  # Pular arquivos que já são do aluno

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
