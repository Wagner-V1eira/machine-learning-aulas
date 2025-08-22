# 📚 Guia do Aluno - Machine Learning

## 🚀 Setup Inicial

```bash
# 1. Clone o repositório
git clone https://github.com/chiarorosa/machine-learning-aulas.git
cd machine-learning-aulas

# 2. Instale dependências com UV
uv sync

# 3. Configure seus arquivos de trabalho
uv run scripts/setup-student.py

# 4. Verifique a configuração
uv run scripts/check-structure.py
```

## 📁 Estrutura dos Exercícios

```
modules/01-fundamentos/exercises/
├── 01_preprocess.ipynb         # 📖 Template do professor (NÃO EDITE)
├── 01_preprocess_aluno.ipynb   # ✏️  SEU arquivo de trabalho
├── 01_preprocess_tests.py      # 🧪 Testes automáticos
└── 01_guia_exercicio.md        # 📋 Instruções detalhadas
```

## ⚖️ Regras de Ouro

### ✅ PODE FAZER:

- ✏️ Editar qualquer arquivo `*_aluno.ipynb`
- 🧪 Executar testes com `uv run pytest`
- 📊 Rodar scripts de avaliação
- 🔄 Fazer git commit dos seus `*_aluno.ipynb`

### ❌ NUNCA FAÇA:

- 🚫 Editar templates originais (sem `_aluno`)
- 🚫 Modificar arquivos em `lessons/`
- 🚫 Alterar arquivos `*_tests.py`
- 🚫 Fazer commit de arquivos temporários

## 🔄 Recebendo Atualizações

### Atualização Automática (Recomendado)

```bash
# Execute semanalmente
./update-course.sh
```

### Atualização Manual

```bash
git pull origin main
uv sync
uv run scripts/setup-student.py
```

## 🧪 Trabalhando com Exercícios

### Iniciar um Exercício

```bash
# 1. Verificar se tem arquivo _aluno
uv run check-structure.py

# 2. Abrir Jupyter Lab
uv run jupyter lab

# 3. Trabalhar no arquivo *_aluno.ipynb
```

### Testar Sua Solução

```bash
# Testar exercício específico
uv run pytest modules/01-fundamentos/exercises/01_preprocess_tests.py

# Testar todos os exercícios
uv run pytest

# Avaliar com sistema de notas
uv run scripts/grade_exercise.py modules/01-fundamentos/exercises/01_preprocess_aluno.ipynb
```

### Salvar Seu Trabalho

```bash
# Adicionar apenas seus arquivos
git add **/*_aluno.ipynb

# Fazer commit
git commit -m "Exercício 01-fundamentos concluído"

# Enviar para seu fork (opcional)
git push origin main
```

## 🆘 Resolução de Problemas

### "Não tenho arquivo \_aluno"

```bash
uv run scripts/setup-student.py
```

### "Conflitos no git pull"

```bash
# Seus arquivos _aluno estão protegidos pelo .gitignore
# mas se acontecer:
git stash
git pull origin main
git stash pop
uv run scripts/setup-student.py
```

### "Testes não passam"

```bash
# 1. Verificar se implementou todas as funções
# 2. Ler o guia do exercício (*_guia_exercicio.md)
# 3. Rodar célula por célula no Jupyter
# 4. Verificar mensagens de erro específicas
```

### "Dependências desatualizadas"

```bash
uv sync --upgrade
```

## 📊 Sistema de Avaliação

### Autoavaliação

```bash
# Verificar implementação
uv run scripts/grade_exercise.py <arquivo_aluno.ipynb>

# Exemplo de saída:
# ✅ fill_missing_values: 100%
# ✅ detect_outliers_iqr: 95%
# ⚠️  normalize_data: 75% (edge case falhou)
# ❌ train_test_split_custom: 0% (não implementado)
```

### Entrega Final

- Faça commit dos arquivos `*_aluno.ipynb`
- Certifique-se que todos os testes passam
- Professor avaliará automaticamente via GitHub

## 🔧 Comandos Úteis

```bash
# Configuração
uv run scripts/setup-student.py     # Configurar exercícios
uv run scripts/check-structure.py   # Verificar estrutura
./update-course.sh                  # Atualizar tudo

# Desenvolvimento
uv run jupyter lab               # Abrir Jupyter
uv run pytest                   # Executar testes
uv run scripts/grade_exercise.py # Avaliar exercício

# Dados
uv run scripts/make_dataset_synth.py  # Gerar datasets sintéticos
```

## 📞 Suporte

- 📖 Leia primeiro o `*_guia_exercicio.md` de cada exercício
- 🔍 Use `uv run check-structure.py` para diagnósticos
- 💬 Dúvidas: abra issue no GitHub ou contacte o professor
- 📚 Documentação adicional: `/docs/`
