@echo off
setlocal

echo Creating Python virtual environment...
python -m venv .venv
if errorlevel 1 goto :error

echo Activating virtual environment...
call .venv\Scripts\activate
if errorlevel 1 goto :error

echo Installing dependencies...
python -m pip install --upgrade pip
if errorlevel 1 goto :error

pip install -r requirements.txt
if errorlevel 1 goto :error

echo Running automated tests...
pytest AutoTesting -q
if errorlevel 1 goto :error

echo.
echo Setup complete.
echo Run locally with: python -m flask --app app.main run --host=0.0.0.0 --port=5000
echo Or with Docker: docker compose up --build
goto :eof

:error
echo Setup failed. Please check the error messages above.
exit /b 1

