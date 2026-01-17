@echo off
setlocal

set FORCE_BUILD=0
if "%1"=="--force" set FORCE_BUILD=1

echo Creating results directory...
if not exist "results" mkdir results

echo.
echo ==========================================
echo Building and Running Python Benchmarks...
echo ==========================================
set SHOULD_BUILD=0
if "%FORCE_BUILD%"=="1" (
    set SHOULD_BUILD=1
) else (
    docker image inspect nbody-python >nul 2>&1
    if %ERRORLEVEL% NEQ 0 set SHOULD_BUILD=1
)

if "%SHOULD_BUILD%"=="0" (
    echo Image nbody-python found, skipping build.
) else (
    echo Building nbody-python...
    docker build -f docker/python.Dockerfile -t nbody-python .
    if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%
)
docker run --rm -v %cd%/results:/app/results nbody-python

echo.
echo ==========================================
echo Building and Running C/C++ Benchmarks...
echo ==========================================
set SHOULD_BUILD=0
if "%FORCE_BUILD%"=="1" (
    set SHOULD_BUILD=1
) else (
    docker image inspect nbody-c-cpp >nul 2>&1
    if %ERRORLEVEL% NEQ 0 set SHOULD_BUILD=1
)

if "%SHOULD_BUILD%"=="0" (
    echo Image nbody-c-cpp found, skipping build.
) else (
    echo Building nbody-c-cpp...
    docker build -f docker/c_cpp.Dockerfile -t nbody-c-cpp .
    if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%
)
docker run --rm -v %cd%/results:/app/results nbody-c-cpp

echo.
echo ==========================================
echo Building and Running Rust Benchmarks...
echo ==========================================
set SHOULD_BUILD=0
if "%FORCE_BUILD%"=="1" (
    set SHOULD_BUILD=1
) else (
    docker image inspect nbody-rust >nul 2>&1
    if %ERRORLEVEL% NEQ 0 set SHOULD_BUILD=1
)

if "%SHOULD_BUILD%"=="0" (
    echo Image nbody-rust found, skipping build.
) else (
    echo Building nbody-rust...
    docker build -f docker/rust.Dockerfile -t nbody-rust .
    if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%
)
docker run --rm -v %cd%/results:/app/results nbody-rust

echo.
echo ==========================================
echo Building and Running Go Benchmarks...
echo ==========================================
set SHOULD_BUILD=0
if "%FORCE_BUILD%"=="1" (
    set SHOULD_BUILD=1
) else (
    docker image inspect nbody-go >nul 2>&1
    if %ERRORLEVEL% NEQ 0 set SHOULD_BUILD=1
)

if "%SHOULD_BUILD%"=="0" (
    echo Image nbody-go found, skipping build.
) else (
    echo Building nbody-go...
    docker build -f docker/go.Dockerfile -t nbody-go .
    if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%
)
docker run --rm -v %cd%/results:/app/results nbody-go

echo.
echo ==========================================
echo All Benchmarks Completed!
echo Results saved to results/latest_run.json
echo ==========================================


