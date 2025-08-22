# 🎓 Machine Learning - Curso Prático

> Repositório didático e executável para aprendizado progressivo de Machine Learning com Python e UV.

## 👨‍🏫 Sobre o Projeto

Este repositório foi criado pelo **Prof. Pablo De Chiaro** para a unidade curricular **FIA (Fundamentos de Inteligência Artificial)**. O objetivo principal é **guiar os estudos fundamentais** da unidade curricular, fornecendo uma base sólida e prática para o aprendizado de Machine Learning.

### 🌟 Propósito e Uso

- **🎯 Principal**: Material de apoio para a unidade curricular FIA
- **🌍 Aberto**: Disponível para **qualquer aluno ou professor** que deseje utilizá-lo
- **🆓 Livre**: Uso completamente gratuito e sem restrições
- **🤝 Colaborativo**: Contribuições de novos materiais são muito bem-vindas

> **Nota**: Embora criado para FIA, este material serve como recurso universal para o ensino e aprendizado de Machine Learning.

## 🚀 Início Rápido para Alunos

```bash
# 1. Clone o repositório
git clone https://github.com/chiarorosa/machine-learning-aulas.git
cd machine-learning-aulas

# 2. Configure o ambiente (UV será instalado automaticamente)
uv sync

# 3. Configure seus arquivos de exercícios
uv run scripts/setup-student.py

# 4. Abra o Jupyter Lab
uv run jupyter lab
```

✅ **Pronto!** Agora você pode trabalhar nos exercícios em arquivos `*_aluno.ipynb`

## 📚 Estrutura do Curso

| Módulo | Tópico                             | Status |
| ------ | ---------------------------------- | ------ |
| **01** | 🔧 Fundamentos e Pré-processamento | ✅     |
| **02** | 📈 Regressão Linear                | ✅     |
| **03** | 🎯 Classificação                   | ✅     |
| **04** | ✅ Validação e Otimização          | ✅     |
| **05** | ⚙️ Feature Engineering             | 🚧     |
| **06** | 🔍 Aprendizado Não-Supervisionado  | 🚧     |
| **07** | 📊 Séries Temporais                | 🚧     |
| **08** | 🧠 Redes Neurais                   | ✅     |
| **09** | 🤖 Deep Learning                   | 🚧     |
| **10** | 🎯 Projetos Práticos               | 🚧     |

## 🎯 Como Estudar

### Para Alunos:

1. **📖 Estude as lições**: `modules/*/lessons/*.ipynb`
2. **✏️ Faça os exercícios**: Edite apenas arquivos `*_aluno.ipynb`
3. **🧪 Teste seu código**: `uv run pytest`
4. **📊 Avalie progresso**: `uv run scripts/grade_exercise.py <arquivo_aluno.ipynb>`
5. **🔄 Receba atualizações**: `./update-course.sh`

### Comandos Essenciais:

```bash
# Configuração inicial
uv run scripts/setup-student.py      # Criar arquivos de trabalho
uv run scripts/check-structure.py    # Verificar configuração

# Trabalho diário
uv run jupyter lab                   # Abrir Jupyter
uv run pytest                       # Executar testes
./update-course.sh                  # Receber atualizações do professor

# Avaliação
uv run scripts/grade_exercise.py modules/01-fundamentos/exercises/01_preprocess_aluno.ipynb
```

## ⚠️ Regras Importantes

### ✅ PODE:

- ✏️ Editar arquivos `*_aluno.ipynb`
- 🔄 Fazer `git commit` dos seus arquivos `*_aluno.ipynb`
- 🧪 Executar testes e scripts de avaliação

### ❌ NÃO PODE:

- 🚫 Editar templates originais (sem `_aluno`)
- 🚫 Modificar arquivos em `lessons/`
- 🚫 Alterar `*_tests.py`

## 🔄 Recebendo Atualizações

O professor pode adicionar novos conteúdos. Para receber:

```bash
./update-course.sh
```

Este script:

- 📡 Baixa novos conteúdos do professor
- 📦 Atualiza dependências
- 📚 Configura novos exercícios automaticamente
- ✅ Verifica que tudo está funcionando

## 🤝 Contribuições e Colaboração

Este projeto é **aberto e colaborativo**! Professores, alunos e entusiastas de Machine Learning são encorajados a:

- 📚 **Adicionar novos módulos** ou lições
- 🛠️ **Melhorar exercícios** existentes
- 🐛 **Reportar bugs** ou problemas
- 💡 **Sugerir melhorias** pedagógicas
- 📖 **Contribuir com documentação**

Consulte o [Guia de Contribuição](docs/CONTRIBUTING.md) para mais detalhes.

## 📖 Documentação Completa

- **👨‍🎓 [Guia Completo do Aluno](docs/STUDENT-GUIDE.md)** - Tutorial detalhado
- **📝 [Esquema de Conteúdo](docs/CONTENT_SCHEMA.md)** - Estrutura dos módulos
- **🔧 [Guia de Extensão](docs/EXTENDING.md)** - Para professores/contribuidores
- **🤝 [Como Contribuir](docs/CONTRIBUTING.md)** - Contribuições são bem-vindas

## 🚧 Para Desenvolvedores/Professores

<details>
<summary>Comandos Avançados</summary>

```bash
# Desenvolvimento
uv run scripts/tasks.py setup          # Configurar ambiente de dev
uv run scripts/tasks.py lint           # Verificar código
uv run scripts/tasks.py test           # Executar todos os testes

# Gerenciar módulos
uv run scripts/manage_tests.py enable 08-redes-neurais
uv run scripts/manage_tests.py disable 03-classificacao
uv run scripts/manage_tests.py list

# Executar notebooks
uv run scripts/run_all_notebooks.py

# Gerar datasets
uv run scripts/make_dataset_synth.py
```

</details>

## ❓ Problemas Comuns

| Problema                     | Solução                                    |
| ---------------------------- | ------------------------------------------ |
| "Não tenho arquivo `_aluno`" | `uv run scripts/setup-student.py`          |
| "Conflitos no git pull"      | `./update-course.sh`                       |
| "Testes não passam"          | Verifique implementação no `*_aluno.ipynb` |
| "Jupyter não abre"           | `uv sync && uv run jupyter lab`            |

## 🏆 Por que UV?

- ⚡ **Ultra-rápido**: 10-100x mais rápido que pip
- 🔒 **Reprodutível**: Ambientes idênticos para todos
- 🌍 **Multiplataforma**: Windows, macOS, Linux
- 🎯 **Moderno**: Padrão atual da comunidade Python

---

**🎯 Meta**: Aprender ML de forma prática, progressiva e reprodutível!

**🎓 Criado por**: Prof. Pablo De Chiaro para FIA - Fundamentos de Inteligência Artificial

**🌍 Uso Livre**: Material aberto para toda a comunidade acadêmica

💡 **Dúvidas?** Abra uma issue ou consulte o [Guia do Aluno](docs/STUDENT-GUIDE.md)
