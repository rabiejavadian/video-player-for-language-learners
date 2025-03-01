@echo off
echo Checking requirements...

REM Check if dependencies are already installed by testing if python-vlc works
python -c "import vlc" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Dependencies are already working, skipping checks...
    goto START_APP
)

REM Check for Visual C++ Build Tools using registry and other methods
set FOUND_CPP=0

REM Check registry for VS installation paths
for /f "tokens=*" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\VisualStudio\SxS\VS7" 2^>nul') do (
    if exist "%%i\VC\Tools\MSVC" set FOUND_CPP=1
)
for /f "tokens=*" %%i in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\VisualStudio\SxS\VS7" 2^>nul') do (
    if exist "%%i\VC\Tools\MSVC" set FOUND_CPP=1
)

REM Check if cl.exe is in PATH as a backup check
where cl.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 set FOUND_CPP=1

REM Check if we can compile anything as final check
echo int main(){return 0;} > test.cpp 2>nul
cl /nologo test.cpp >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set FOUND_CPP=1
    del test.cpp >nul 2>&1
    del test.obj >nul 2>&1
    del test.exe >nul 2>&1
)

if %FOUND_CPP% EQU 0 (
    echo ERROR: Microsoft Visual C++ Build Tools not found!
    echo Please follow these steps to install the required tools:
    echo 1. Download Visual Studio Build Tools from:
    echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo 2. Run the installer
    echo 3. Select "Desktop development with C++"
    echo 4. Install the selected components
    echo 5. After installation, run this script again
    echo.
    echo Press any key to open the download page...
    pause >nul
    start "" "https://visualstudio.microsoft.com/visual-cpp-build-tools/"
    exit /b 1
)

echo Setting up Python virtual environment...

if not exist .venv (
    python -m venv .venv
    call .venv\Scripts\activate
    python -m pip install --upgrade pip
    echo Installing wheel and setuptools first...
    pip install wheel setuptools
    echo Installing requirements...
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate
)

if %ERRORLEVEL% NEQ 0 (
    echo Error during installation. Please check the error messages above.
    pause
    exit /b 1
)

:START_APP
echo Starting Video Player...
python video_player.py
pause 