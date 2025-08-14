#!/bin/bash
# Script de instalação rápida para ML Curso

set -e  # Parar em caso de erro

echo "🚀 Instalando ML Curso..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado! Instale Python 3.10+ primeiro."
    exit 1
fi

# Verificar versão do Python
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.10"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "❌ Python $required_version+ requerido. Versão atual: $python_version"
    exit 1
fi

echo "✅ Python $python_version detectado"

# Instalar UV se não estiver instalado
if ! command -v uv &> /dev/null; then
    echo "📦 Instalando UV..."
    pip install uv
fi

echo "✅ UV instalado"

# Configurar ambiente
echo "⚙️ Configurando ambiente..."
uv sync --all-extras

echo "📚 Instalando projeto em modo desenvolvimento..."
uv run python scripts/tasks.py install

echo ""
echo "🎉 Instalação concluída!"
echo ""
echo "Comandos disponíveis:"
echo "  uv run python scripts/tasks.py help     # Ver todos os comandos"
echo "  uv run python scripts/tasks.py test     # Executar testes"
echo "  ml-curso lint                           # Verificar código"
echo ""
echo "Para começar:"
echo "  cd modules/01-fundamentos/lessons/"
echo "  jupyter notebook"
