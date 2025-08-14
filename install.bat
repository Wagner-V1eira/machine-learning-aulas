@echo off
REM Script de instalação rápida para ML Curso (Windows)

echo 🚀 Instalando ML Curso...

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.10+ primeiro.
    exit /b 1
)

echo ✅ Python detectado

REM Instalar UV se não estiver instalado
uv --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando UV...
    pip install uv
)

echo ✅ UV instalado

REM Configurar ambiente
echo ⚙️ Configurando ambiente...
uv sync --all-extras

echo 📚 Instalando projeto em modo desenvolvimento...
uv run python scripts/tasks.py install

echo.
echo 🎉 Instalação concluída!
echo.
echo Comandos disponíveis:
echo   uv run python scripts/tasks.py help     # Ver todos os comandos
echo   uv run python scripts/tasks.py test     # Executar testes
echo   ml-curso lint                           # Verificar código
echo.
echo Para começar:
echo   cd modules/01-fundamentos/lessons/
echo   jupyter notebook

pause
