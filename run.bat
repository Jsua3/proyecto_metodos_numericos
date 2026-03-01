@echo off
echo ==========================================
echo Calculadora de Metodos Numericos - Launcher
echo ==========================================
echo.

:: Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH.
    pause
    exit /b
)

:: Crear entorno virtual si no existe
if not exist .venv (
    echo [INFO] Creando entorno virtual .venv...
    python -m venv .venv
)

:: Activar entorno virtual e instalar dependencias
echo [INFO] Activando entorno virtual...
call .venv\Scripts\activate

if exist requirements.txt (
    echo [INFO] Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt
)

:: Iniciar aplicacion
echo [INFO] Iniciando aplicacion...
python main.py

echo.
echo [INFO] Aplicacion cerrada con exito.
pause
