# Language Learning Video Player v1.1.0

A specialized video player designed for language learning, featuring dual subtitle support (English and Persian) and smart navigation controls.

## Release Contents
- `Language_Learning_Video_Player.exe` - Standalone executable (Windows 64-bit)
- `README.md` - Documentation and usage instructions
- `LICENSE` - MIT License

## System Requirements
- Windows 10 or newer (64-bit)
- VLC Media Player 64-bit must be installed
  - Download from: https://www.videolan.org/vlc/
  - Make sure to install 64-bit version

## Installation
1. Download and install VLC Media Player 64-bit
2. Download `Language_Learning_Video_Player.exe`
3. Run the executable - no additional installation required

## Key Features
- Play MKV and MP4 videos with dual subtitle support
- Auto-pause at subtitle endings for practice
- Smart subtitle navigation
- Fullscreen support
- Dark theme interface
- Adjustable video/subtitle layout

## Controls
- **Spacebar**: Toggle play/pause
- **Up Arrow**: Practice sequence (1. Hide subtitles → 2. English only → 3. Both subtitles → 4. Next subtitle)
- **Right Arrow**: Play from current position until the end of next subtitle line (shows both subtitles)
- **Ctrl + Right Arrow**: Jump to start of next subtitle line and begin playing (shows both subtitles)
- **Left Arrow**: Go to previous subtitle line and auto-resume playback (shows both subtitles)
- **Down Arrow**: Repeat current subtitle line
- **F**: Toggle fullscreen mode
- **Escape**: Exit fullscreen mode

## Important Notes
1. VLC Media Player 64-bit must be installed before running the application
2. If subtitles become out of sync, please restart the application
3. Load video file first, then subtitle files
4. Press spacebar to start playback

## Changes in v1.0.0
- Initial release
- Dual subtitle support (English and Persian)
- Smart navigation controls
- Auto-pause feature
- Fullscreen mode
- Dark theme interface
- Keyboard shortcuts
- Improved subtitle synchronization

## Known Issues
- VLC Media Player 64-bit is required for proper operation

## Support
If you encounter any issues:
1. Ensure VLC Media Player 64-bit is installed
2. Check that both video and subtitle files are valid
3. Try restarting the application
4. Report issues on our GitHub page

## Credits
- Built with Python and VLC Media Player
- Uses PyQt6 for the user interface
- Developed with Cursor.sh and Claude by RabieJavadian