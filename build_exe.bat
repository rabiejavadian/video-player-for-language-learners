@echo off
echo Setting up build environment...

REM Activate virtual environment
call .venv\Scripts\activate

REM Install required packages
echo Installing required packages...
pip install pillow
pip install pyinstaller

REM Create application icon
echo Creating application icon...
python create_icon.py

echo Cleaning previous builds...
rmdir /s /q "build" 2>nul
rmdir /s /q "dist" 2>nul
del /f /q "*.spec" 2>nul

echo Building executable...
pyinstaller --clean ^
    --noconfirm ^
    --noconsole ^
    --name "Language_Learning_Video_Player" ^
    --add-data "LICENSE;." ^
    --hidden-import=vlc ^
    --hidden-import=pysrt ^
    --hidden-import=PyQt6 ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --collect-all vlc ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module PIL ^
    --exclude-module tkinter ^
    src/video_player.py

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo Build successful!
echo Executable is in the dist folder
pause