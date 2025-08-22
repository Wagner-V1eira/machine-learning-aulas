#!/bin/bash

echo "🔄 Atualizando repositório do curso..."

uv run scripts/tasks.py clean

# Sincronizar dependências
echo "📦 Atualizando dependências..."
uv sync

# Restaurar notebooks de lessons/exercises (evitar conflitos de formatação)
echo "🔄 Restaurando notebooks para estado original..."
git restore modules/*/lessons/*.ipynb modules/*/exercises/*.ipynb
# Preservar arquivos _aluno que o estudante pode ter modificado
git restore modules/*/exercises/*_aluno.ipynb modules/*/exercises/*_aluno.py 2>/dev/null || true

# Sincronizar com repositório do professor
echo "📡 Baixando atualizações do professor..."
git fetch origin main

# Verificar se há conflitos potenciais
if git diff --name-only origin/main | grep -E "_aluno\.(ipynb|py)$"; then
    echo "⚠️  ATENÇÃO: Arquivos _aluno foram modificados no repositório remoto!"
    echo "   Isso não deveria acontecer. Contacte o professor."
    exit 1
fi

# Fazer merge das atualizações
echo "🔀 Aplicando atualizações..."
git merge origin/main

# Sincronizar dependências
echo "📦 Atualizando dependências..."
uv sync

# Configurar novos exercícios (se houver)
echo "📚 Configurando novos exercícios..."
uv run scripts/setup-student.py

# Verificar estrutura
echo "🔍 Verificando configuração..."
uv run scripts/check-structure.py

echo "✅ Atualização concluída!"
echo ""
echo "📋 Resumo:"
echo "   • Notebooks restaurados ao estado original"
echo "   • Novos conteúdos sincronizados"
echo "   • Dependências atualizadas"  
echo "   • Exercícios configurados"
echo ""
echo "🚀 Use 'uv run jupyter lab' para continuar estudando!"
