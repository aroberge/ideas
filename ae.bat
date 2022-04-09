echo off
REM Default is Python 3.7

if "%1"=="3.9" goto py_39
if "%1"=="units" goto units

:py_37
venv-ideas3.7\scripts\activate
goto end

:units
venv-units\scripts\activate
goto end

:py_39
venv-ideas3.9\scripts\activate

:end
