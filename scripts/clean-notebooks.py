#!/usr/bin/env python3
"""
Script para limpar outputs dos notebooks antes de commits.
Usado para manter repositório limpo e evitar conflitos.

Uso: uv run scripts/clean-notebooks.py [--check-only]
"""

import subprocess
import sys
from pathlib import Path


def clean_notebooks(check_only=False):
    """Limpa outputs dos notebooks no repositório"""
    print("🧹 Limpando outputs dos notebooks...")
    
    # Encontrar todos os notebooks (exceto _aluno)
    notebook_patterns = [
        "modules/*/lessons/*.ipynb",
        "modules/*/exercises/*.ipynb"
    ]
    
    notebooks_to_clean = []
    for pattern in notebook_patterns:
        notebooks = list(Path(".").glob(pattern))
        # Filtrar notebooks que NÃO são do aluno
        notebooks = [nb for nb in notebooks if "_aluno" not in nb.name]
        notebooks_to_clean.extend(notebooks)
    
    if not notebooks_to_clean:
        print("✅ Nenhum notebook encontrado para limpar")
        return True
    
    print(f"📝 Encontrados {len(notebooks_to_clean)} notebooks para processar")
    
    # Executar nbstripout
    try:
        if check_only:
            print("🔍 Verificando se notebooks têm outputs...")
            # Usar --dry-run para verificar sem modificar
            cmd = ["uv", "run", "nbstripout", "--dry-run"]
        else:
            print("🧹 Removendo outputs dos notebooks...")
            cmd = ["uv", "run", "nbstripout"]
        
        cmd.extend([str(nb) for nb in notebooks_to_clean])
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if check_only:
                if result.stdout.strip():
                    print("⚠️  Alguns notebooks têm outputs que deveriam ser removidos:")
                    print(result.stdout)
                    print("\n💡 Execute: uv run scripts/clean-notebooks.py")
                    return False
                else:
                    print("✅ Todos os notebooks estão limpos (sem outputs)")
                    return True
            else:
                print("✅ Outputs removidos com sucesso")
                if result.stdout.strip():
                    print("� Arquivos processados:")
                    print(result.stdout)
                return True
        else:
            print("❌ Erro ao processar notebooks:")
            print(result.stderr)
            return False
                
    except FileNotFoundError:
        print("❌ nbstripout não encontrado. Execute: uv sync")
        return False


def setup_git_hooks():
    """Configura git hooks para limpeza automática"""
    print("🔧 Configurando git hooks...")
    
    # Pre-commit hook
    pre_commit_path = Path(".git/hooks/pre-commit")
    pre_commit_content = """#!/bin/bash
# Pre-commit hook para limpar notebooks

echo "🧹 Limpando outputs dos notebooks..."
uv run scripts/clean-notebooks.py

if [ $? -ne 0 ]; then
    echo "❌ Falha ao limpar notebooks. Commit cancelado."
    exit 1
fi

echo "✅ Notebooks limpos com sucesso"
"""
    
    pre_commit_path.parent.mkdir(exist_ok=True)
    pre_commit_path.write_text(pre_commit_content)
    pre_commit_path.chmod(0o755)
    
    print("✅ Git hook configurado em .git/hooks/pre-commit")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Limpar outputs dos notebooks")
    parser.add_argument("--check-only", action="store_true", 
                       help="Apenas verificar se notebooks têm outputs")
    parser.add_argument("--setup-hooks", action="store_true",
                       help="Configurar git hooks automáticos")
    
    args = parser.parse_args()
    
    if args.setup_hooks:
        setup_git_hooks()
    else:
        success = clean_notebooks(check_only=args.check_only)
        sys.exit(0 if success else 1)
