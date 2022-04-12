echo off
REM Default is Python 3.7

if "%1"=="3.6" goto py_36
if "%1"=="3.8" goto py_38
if "%1"=="3.9" goto py_39
if "%1"=="3.10" goto py_310
if "%1"=="units" goto units

:py_37
venv-ideas3.7\scripts\activate
goto end

:py_36
venv-ideas3.6\scripts\activate
goto end

:py_38
venv-ideas3.8\scripts\activate
goto end

:py_39
venv-ideas3.9\scripts\activate
goto end

:py_310
venv-ideas3.10\scripts\activate
goto end

REM Separate since it requires pint and astropy
:units
venv-units\scripts\activate


:end
