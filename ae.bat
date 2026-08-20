echo off
REM Default is Python 3.11

if "%1"=="3.7" goto py_37
if "%1"=="3.8" goto py_38
if "%1"=="3.9" goto py_39
if "%1"=="3.10" goto py_310
if "%1"=="3.11" goto py_311
if "%1"=="3.12" goto py_312
if "%1"=="3.13" goto py_313
if "%1"=="3.14" goto py_314
if "%1"=="units" goto units
if "%1"=="ipython" goto ipython

goto py_311

:py_37
venv-ideas3.7\scripts\activate
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

:py_311
venv-ideas3.11\scripts\activate
goto end

:py_312
venv-ideas3.12\scripts\activate
goto end

:py_313
venv-ideas3.13\scripts\activate
goto end

:py_314
venv-ideas3.14\scripts\activate
goto end


REM Separate since it requires pint and astropy
:units
venv-units\scripts\activate

:ipython
venv-ipython\scripts\activate

:end