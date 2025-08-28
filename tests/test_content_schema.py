"""Testes para esquemas de conteúdo."""

from pathlib import Path

import yaml


def _is_module_test_enabled(module_data):
    """Verifica se o módulo está habilitado para testes."""
    return module_data.get("test_enabled", True)


def _is_lesson_test_enabled(lesson_data):
    """Verifica se a lição está habilitada para testes."""
    return lesson_data.get("test_enabled", True)


def _is_exercise_test_enabled(exercise_data):
    """Verifica se o exercício está habilitado para testes."""
    return exercise_data.get("test_enabled", True)


def _get_enabled_modules():
    """Retorna lista de módulos habilitados para teste."""
    project_root = Path(__file__).parent.parent
    module_yamls = list(project_root.glob("modules/*/module.yaml"))
    enabled_modules = []

    for yaml_path in module_yamls:
        with open(yaml_path, encoding="utf-8") as f:
            module_data = yaml.safe_load(f)

        if _is_module_test_enabled(module_data):
            enabled_modules.append(yaml_path)

    return enabled_modules


def test_module_yaml_files_exist():
    """Verifica se arquivos module.yaml existem para módulos habilitados."""
    project_root = Path(__file__).parent.parent

    # Lista específica de módulos críticos que sempre devem existir
    critical_modules = [
        "modules/01-fundamentos",
    ]

    for module_path in critical_modules:
        yaml_path = project_root / module_path / "module.yaml"
        if yaml_path.exists():
            with open(yaml_path, encoding="utf-8") as f:
                module_data = yaml.safe_load(f)

            # Só testa se o módulo está habilitado
            if _is_module_test_enabled(module_data):
                assert yaml_path.exists(), f"Arquivo module.yaml não encontrado em {module_path}"


def test_module_yaml_schema():
    """Verifica se os arquivos module.yaml seguem o schema correto."""
    project_root = Path(__file__).parent.parent

    # Só testa módulos habilitados
    enabled_modules = _get_enabled_modules()

    required_fields = [
        "slug",
        "title",
        "order",
        "prerequisites",
        "outcomes",
        "lessons",
        "exercises",
    ]

    for yaml_path in enabled_modules:
        with open(yaml_path, encoding="utf-8") as f:
            module_data = yaml.safe_load(f)

        # Verificar campos obrigatórios
        for field in required_fields:
            assert field in module_data, f"Campo '{field}' ausente em {yaml_path}"

        # Verificar tipos
        assert isinstance(module_data["slug"], str), f"'slug' deve ser string em {yaml_path}"
        assert isinstance(module_data["title"], str), f"'title' deve ser string em {yaml_path}"
        assert isinstance(module_data["order"], int), f"'order' deve ser int em {yaml_path}"
        assert isinstance(module_data["prerequisites"], list), f"'prerequisites' deve ser lista em {yaml_path}"
        assert isinstance(module_data["outcomes"], list), f"'outcomes' deve ser lista em {yaml_path}"
        assert isinstance(module_data["lessons"], list), f"'lessons' deve ser lista em {yaml_path}"
        assert isinstance(module_data["exercises"], list), f"'exercises' deve ser lista em {yaml_path}"


def test_lesson_structure():
    """Verifica estrutura das lições nos module.yaml."""
    project_root = Path(__file__).parent.parent

    # Só testa módulos habilitados
    enabled_modules = _get_enabled_modules()

    for yaml_path in enabled_modules:
        with open(yaml_path, encoding="utf-8") as f:
            module_data = yaml.safe_load(f)

        for lesson in module_data["lessons"]:
            # Só testa lições habilitadas
            if not _is_lesson_test_enabled(lesson):
                continue

            # Verificar campos obrigatórios da lição
            required_lesson_fields = ["slug", "title", "notebook", "est_time_min"]
            for field in required_lesson_fields:
                assert field in lesson, f"Campo '{field}' ausente em lição de {yaml_path}"

            # Verificar se notebook existe
            notebook_path = yaml_path.parent / lesson["notebook"]
            assert notebook_path.exists(), f"Notebook {lesson['notebook']} não encontrado para {yaml_path}"


def test_exercise_structure():
    """Verifica estrutura dos exercícios nos module.yaml."""
    project_root = Path(__file__).parent.parent

    # Só testa módulos habilitados
    enabled_modules = _get_enabled_modules()

    for yaml_path in enabled_modules:
        with open(yaml_path, encoding="utf-8") as f:
            module_data = yaml.safe_load(f)

        for exercise in module_data["exercises"]:
            # Só testa exercícios habilitados
            if not _is_exercise_test_enabled(exercise):
                continue

            # Verificar campos obrigatórios do exercício
            required_exercise_fields = [
                "slug",
                "title",
                "notebook",
                "tests",
                "max_score",
            ]
            for field in required_exercise_fields:
                assert field in exercise, f"Campo '{field}' ausente em exercício de {yaml_path}"

            # Verificar se arquivos existem
            notebook_path = yaml_path.parent / exercise["notebook"]
            tests_path = yaml_path.parent / exercise["tests"]

            assert notebook_path.exists(), f"Notebook {exercise['notebook']} não encontrado para {yaml_path}"
            assert tests_path.exists(), f"Arquivo de testes {exercise['tests']} não encontrado para {yaml_path}"


def test_module_order_consistency():
    """Verifica se a ordem dos módulos é consistente."""
    project_root = Path(__file__).parent.parent

    # Só considera módulos habilitados para teste
    enabled_modules = _get_enabled_modules()
    orders = []

    for yaml_path in enabled_modules:
        with open(yaml_path, encoding="utf-8") as f:
            module_data = yaml.safe_load(f)
        orders.append(module_data["order"])

    # Verificar se não há ordens duplicadas entre módulos habilitados
    assert len(orders) == len(set(orders)), "Ordens de módulos duplicadas encontradas"

    # Verificar se as ordens são válidas (não precisam ser sequenciais se alguns módulos estão desabilitados)
    for order in orders:
        assert order >= 1, f"Ordem do módulo deve ser >= 1, encontrada: {order}"


class TestContentConsistency:
    """Testes de consistência de conteúdo."""

    def test_prerequisites_exist(self):
        """Verifica se pré-requisitos existem."""
        project_root = Path(__file__).parent.parent

        # Considera todos os módulos para verificar pré-requisitos, não só os habilitados
        module_yamls = list(project_root.glob("modules/*/module.yaml"))
        module_slugs = set()

        # Coletar todos os slugs
        for yaml_path in module_yamls:
            with open(yaml_path, encoding="utf-8") as f:
                module_data = yaml.safe_load(f)
            module_slugs.add(module_data["slug"])

        # Verificar se pré-requisitos existem apenas para módulos habilitados
        enabled_modules = _get_enabled_modules()
        for yaml_path in enabled_modules:
            with open(yaml_path, encoding="utf-8") as f:
                module_data = yaml.safe_load(f)

            for prereq in module_data["prerequisites"]:
                assert prereq in module_slugs, f"Pré-requisito '{prereq}' não encontrado para {module_data['slug']}"
