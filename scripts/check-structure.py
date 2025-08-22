#!/usr/bin/env python3
"""
Script para verificar se a estrutura do aluno está correta.

Uso: uv run check-structure.py
"""

from pathlib import Path


def check_student_structure():
    """Verifica se os arquivos _aluno estão configurados corretamente"""
    modules_dir = Path("modules")
    issues = []
    all_good = []
    
    print("🔍 Verificando estrutura do aluno...\n")
    
    for module in modules_dir.iterdir():
        if not module.is_dir():
            continue
            
        exercises_dir = module / "exercises"
        if not exercises_dir.exists():
            continue
        
        module_issues = []
        module_good = []
        
        # Verificar templates e arquivos do aluno
        templates = list(exercises_dir.glob("*.ipynb"))
        templates = [f for f in templates if "_aluno" not in f.name]
        
        for template in templates:
            stem = template.stem
            aluno_file = exercises_dir / f"{stem}_aluno.ipynb"
            
            if aluno_file.exists():
                module_good.append(f"✅ {aluno_file.name}")
            else:
                module_issues.append(f"❌ Faltando: {aluno_file.name}")
        
        if module_issues or module_good:
            print(f"📁 {module.name}:")
            for item in module_good:
                print(f"   {item}")
            for item in module_issues:
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
        print("🎉 Tudo configurado corretamente!")
    
    print(f"\n📊 Resumo: {len(all_good)} arquivos prontos, {len(issues)} pendentes")
    
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
