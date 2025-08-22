# Testes dos Exercícios

Esta pasta contém todos os arquivos de teste para os exercícios dos módulos do curso.

## Estrutura e Nomenclatura

Os arquivos de teste seguem o padrão:

```
{módulo}_{exercício}_tests.py
```

### Exemplos:

- `01-fundamentos_01_preprocess_tests.py` - Testes para o exercício de pré-processamento do módulo 01

**Nota:** Atualmente apenas o exercício de pré-processamento básico (01-fundamentos) possui testes implementados. Outros exercícios terão testes adicionados conforme necessário.

**Importante:** Os testes avaliam o notebook `*_aluno.ipynb` onde o estudante implementa as funções.

## Por que esta estrutura?

1. **Organização centralizada**: Todos os testes ficam em um local específico, não misturados com os exercícios
2. **Evita confusão**: Alunos não veem arquivos de teste quando navegam pelos exercícios
3. **Nomenclatura clara**: O sufixo `_aluno` indica que são testes para validar o código do aluno
4. **Facilita manutenção**: Estrutura consistente e previsível

## Como usar

Os testes são executados automaticamente pelos scripts do curso. Para executar manualmente:

```bash
# Executar teste específico
uv run pytest tests/exercises/01-fundamentos_01_preprocess_tests.py

# Executar todos os testes de exercícios
uv run pytest tests/exercises/

# Usar o script de avaliação
uv run python scripts/grade_exercise.py \
  modules/01-fundamentos/exercises/01_preprocess_aluno.ipynb \
  tests/exercises/01-fundamentos_01_preprocess_tests.py
```

## Caminhos dos Notebooks

Os arquivos de teste referenciam os notebooks dos exercícios usando caminhos relativos e apontam para o arquivo `_aluno.ipynb`:

```python
# Dentro de tests/exercises/*_tests.py
project_root = Path(__file__).parent.parent.parent
notebook_path = project_root / "modules/01-fundamentos/exercises/01_preprocess_aluno.ipynb"

student = load_notebook_funcs(
    str(notebook_path),
    allowed_imports={"numpy", "pandas"},
)
```
