# Language Learning Video Player v1.1.1

A specialized video player designed for language learning, featuring dual subtitle support and navigation controls. Perfect for studying languages through movies and TV shows. 
If your subtitles are not synchronized with the video, you can sync them using VLC, PotPlayer, or any other video player, then save the modified subtitle files to use in this application.

## Release Contents
- `Language_Learning_Video_Player.exe` - Standalone executable (Windows 64-bit)
- `README.md` - Documentation and usage instructions
- `LICENSE` - MIT License

## What's New in v1.1.1

### Improved VLC Detection
- Better error handling when VLC is not found
- User-friendly error message with direct download link if VLC is missing

### Enhanced Practice Sequence
- More consistent behavior in the practice sequence:
  1. Hide both subtitles and play from current time to end of current subtitle - Test pure listening
  2. Show English subtitle and play from start to end of current subtitle - Check comprehension
  3. Show both subtitles and play from start to end of current subtitle - Compare translations
  4. Hide both subtitles and play from end of current subtitle to end of next subtitle - Continue practice with next subtitle
- Improved timing between practice steps
- Better state management during practice sequence

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
- **Up Arrow**: Practice sequence:
  1. Hide subtitles, play current subtitle from current position
  2. Show English, replay current subtitle from start
  3. Show both subtitles, replay current subtitle from start
  4. Hide subtitles, play from end of current to end of next subtitle
- **Right Arrow**: Play until end of next subtitle line (shows both subtitles)
- **Ctrl + Right Arrow**: Jump to start of next subtitle line and begin playing (shows both subtitles)
- **Left Arrow**: Go to previous subtitle line and auto-resume playback (shows both subtitles)
- **Down Arrow**: Repeat current subtitle line
- **F**: Toggle fullscreen mode
- **Escape**: Exit fullscreen mode

## Practical Tips
- Use Right Arrow (➡️) multiple times to playback until a number of subtitles
- Use Ctrl+Right (`Ctrl` + ➡️) multiple times to fast-track video playback
- Use Up Arrow (⬆️) for practice sequence: hide subtitles → English only → both subtitles → next subtitle
- Use Down Arrow (⬇️) to listen again
- Press Up Arrow (⬆️) once to hide subtitles, then use Down Arrow (⬇️) to replay the subtitle while keeping it hidden - perfect for testing your listening comprehension!

## Important Notes
1. VLC Media Player 64-bit must be installed before running the application
2. The application will help you locate or download VLC if needed
3. Practice sequence is designed for systematic language learning
4. Auto-pause feature helps maintain a steady learning pace

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