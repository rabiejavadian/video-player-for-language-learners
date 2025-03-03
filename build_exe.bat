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

REM Build the executable with all required settings
echo Building executable...
pyinstaller --name="Language_Learning_Video_Player" ^
            --onefile ^
            --noconsole ^
            --add-data "LICENSE;." ^
            --add-data "README.md;." ^
            --icon="app_icon.ico" ^
            --hidden-import="PIL" ^
            --hidden-import="PIL._imagingtk" ^
            --hidden-import="PIL._tkinter_finder" ^
            src/video_player.py

echo.
echo Build process complete!
echo The executable can be found in the 'dist' folder
echo.
echo Next steps:
echo 1. Test the executable
echo 2. Create a GitHub release
echo 3. Upload the following files to the release:
echo    - dist/Language_Learning_Video_Player.exe
echo    - README.md
echo    - LICENSE
echo.
pause 