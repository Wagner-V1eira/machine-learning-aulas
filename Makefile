.PHONY: setup lint fmt typecheck test run-notebooks grade clean help

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help:
	@echo "Comandos disponíveis:"
	@echo "  setup         - Criar venv e instalar dependências"
	@echo "  lint          - Verificar código (ruff + black + isort)"
	@echo "  fmt           - Formatar código"
	@echo "  typecheck     - Verificação de tipos (mypy)"
	@echo "  test          - Executar testes unitários"
	@echo "  run-notebooks - Executar todos notebooks"
	@echo "  grade         - Executar autograder (use MOD=module EX=exercise)"
	@echo "  clean         - Limpar arquivos temporários"

setup:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m black --check .
	$(PYTHON) -m isort --check-only .

fmt:
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

typecheck:
	$(PYTHON) -m mypy core/ scripts/

test:
	$(PYTHON) -m pytest tests/ --cov=core --cov-report=term-missing --cov-report=xml

run-notebooks:
	$(PYTHON) scripts/run_all_notebooks.py

grade:
	@if [ -z "$(MOD)" ] || [ -z "$(EX)" ]; then \
		echo "Uso: make grade MOD=02-regressao EX=01_mae_metric"; \
		exit 1; \
	fi
	$(PYTHON) scripts/grade_exercise.py modules/$(MOD)/exercises/$(EX).ipynb modules/$(MOD)/exercises/$(EX)_tests.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .mypy_cache/
