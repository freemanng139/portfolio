@echo off
title Portfolio Freeman - Flask
echo ==============================================
echo   Lancement du Portfolio Freeman...
echo ==============================================
echo.

if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" app.py
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python app.py
    goto end
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py app.py
    goto end
)

echo [ERREUR] Python introuvable.
pause

:end
