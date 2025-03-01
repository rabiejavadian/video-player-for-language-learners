import sys
import vlc
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QFileDialog, QLabel,
                            QSplitter, QDialog, QTextBrowser)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
import pysrt

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player for Language Learners")
        self.setGeometry(100, 100, 1280, 720)

        # Create VLC instance with proper parameters
        vlc_args = [
            '--no-xlib',  # Don't use Xlib
            '--quiet',    # No output
            '--no-sub-autodetect-file',  # Don't auto-load subtitles
            '--no-spu',   # Disable subpictures/subtitles
            '--no-osd',   # Disable on-screen display
            '--no-video-title-show'  # Don't show video title
        ]
        self.instance = vlc.Instance(' '.join(vlc_args))
        self.media_player = self.instance.media_player_new()

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create main splitter
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2A2A2A;
            }
        """)
        layout.addWidget(self.splitter)

        # Create video frame with proper attributes
        self.video_frame = QWidget()
        self.video_frame.setStyleSheet("background-color: black;")
        self.video_frame.setMinimumHeight(400)
        self.video_frame.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)  # Prevent flickering
        self.splitter.addWidget(self.video_frame)

        # Create subtitle container with dark background
        subtitle_container = QWidget()
        subtitle_container.setStyleSheet("background-color: #2A2A2A;")
        subtitle_layout = QVBoxLayout(subtitle_container)
        subtitle_layout.setContentsMargins(10, 10, 10, 10)
        subtitle_layout.setSpacing(10)  # Space between English and Persian subtitles
        self.splitter.addWidget(subtitle_container)

        # Create subtitle labels
        self.english_subtitle_label = QLabel()
        self.persian_subtitle_label = QLabel()
        
        # Style subtitle labels with larger font and semi-transparent background
        subtitle_style = """
            QLabel {
                color: white;
                background-color: rgba(42, 42, 42, 180);
                padding: 8px;
                border-radius: 8px;
            }
        """
        self.english_subtitle_label.setStyleSheet(subtitle_style)
        self.persian_subtitle_label.setStyleSheet(subtitle_style)
        
        # Set larger fonts for subtitles
        english_font = QFont("Calibri", 22)  # Increased from 14 to 16
        persian_font = QFont("Calibri", 22)  # Increased from 14 to 16
        english_font.setBold(True)  # Make English subtitles bold
        persian_font.setBold(True)
        self.english_subtitle_label.setFont(english_font)
        self.persian_subtitle_label.setFont(persian_font)
        
        self.english_subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.persian_subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add word wrap to handle long subtitles
        self.english_subtitle_label.setWordWrap(True)
        self.persian_subtitle_label.setWordWrap(True)
        
        subtitle_layout.addWidget(self.english_subtitle_label)
        subtitle_layout.addWidget(self.persian_subtitle_label)

        # Set initial splitter sizes (90% video, 10% subtitles)
        self.splitter.setSizes([int(self.height() * 0.9), int(self.height() * 0.1)])

        # Create button container with matching dark theme
        button_container = QWidget()
        button_container.setStyleSheet("background-color: #2A2A2A;")
        button_layout = self.create_buttons()  # Use the create_buttons method
        button_container.setLayout(button_layout)
        layout.addWidget(button_container)

        # Initialize variables
        self.media = None
        self.english_subtitles = None
        self.persian_subtitles = None
        self.current_subtitle_index = 0
        self.current_persian_index = 0
        self.is_playing = False
        self.is_fullscreen = False
        self.current_video_path = None
        self.current_english_subtitle_path = None
        self.current_persian_subtitle_path = None
        self.next_subtitle_end_time = None

        # Timer for updating subtitle display
        self.timer = QTimer(self)
        self.timer.setInterval(100)  # 100ms interval
        self.timer.timeout.connect(self.update_subtitle)

        # Set up key event handling
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def load_video(self, video_path):
        self.current_video_path = video_path
        
        # Create media with subtitle disabled
        media_opts = [
            'no-sub-autodetect-file',
            'no-spu',
            'no-osd'
        ]
        self.media = self.instance.media_new(video_path)
        for opt in media_opts:
            self.media.add_option(f'--{opt}')
            
        self.media_player.set_media(self.media)
        
        # Disable all subtitle/SPU tracks
        self.media_player.video_set_spu(-1)
        self.media_player.video_set_spu_delay(0)
        self.media_player.video_set_subtitle_file("")
        
        if sys.platform.startswith('win'):
            self.media_player.set_hwnd(self.video_frame.winId())
        else:
            self.media_player.set_xwindow(self.video_frame.winId())
        
        # Play briefly to load the video then pause
        self.media_player.play()
        self.media_player.set_pause(1)
        self.is_playing = False
        self.timer.start()

    def open_file(self):
        dialog = QFileDialog()
        video_path, _ = dialog.getOpenFileName(self, "Open Video File", "",
                                             "Video Files (*.mp4 *.mkv *.avi)")
        if video_path:
            self.load_video(video_path)

    def open_subtitle_file(self, language):
        dialog = QFileDialog()
        subtitle_path, _ = dialog.getOpenFileName(self, f"Open {language.title()} Subtitle File", "",
                                                "Subtitle Files (*.srt)")
        if subtitle_path:
            self.load_subtitle(subtitle_path, language)

    def load_subtitle(self, subtitle_path, language):
        try:
            if language == 'english':
                self.english_subtitles = pysrt.open(subtitle_path)
                self.current_english_subtitle_path = subtitle_path
                # Make sure VLC subtitles are still disabled
                self.media_player.video_set_spu(-1)
                self.media_player.video_set_subtitle_file("")
            else:
                self.persian_subtitles = pysrt.open(subtitle_path)
                self.current_persian_subtitle_path = subtitle_path
            
            # Find correct subtitle index based on current video position
            if language == 'english':
                self.find_current_subtitle_index()
                self.update_subtitle_text()
        except Exception:
            pass

    def find_current_subtitle_index(self):
        if not self.english_subtitles:
            return

        current_time = self.media_player.get_time()
        
        # Find the appropriate subtitle index for the current time
        for i, subtitle in enumerate(self.english_subtitles):
            start_time = (subtitle.start.hours * 3600 + 
                         subtitle.start.minutes * 60 +
                         subtitle.start.seconds) * 1000 + subtitle.start.milliseconds
            end_time = (subtitle.end.hours * 3600 + 
                       subtitle.end.minutes * 60 +
                       subtitle.end.seconds) * 1000 + subtitle.end.milliseconds
            
            if start_time <= current_time <= end_time:
                self.current_subtitle_index = i
                return
            elif current_time < start_time:
                self.current_subtitle_index = max(0, i - 1)
                return
        
        self.current_subtitle_index = len(self.english_subtitles) - 1

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.toggle_play_pause()
        elif event.key() == Qt.Key.Key_Right:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                self.start_from_next_subtitle()
            else:
                self.play_until_next_subtitle()
        elif event.key() == Qt.Key.Key_Left:
            self.previous_subtitle()
            if not self.media_player.is_playing():
                self.media_player.play()
                self.is_playing = True
        elif event.key() == Qt.Key.Key_Down:
            self.repeat_current_subtitle()
            if not self.media_player.is_playing():
                self.media_player.play()
                self.is_playing = True
        elif event.key() == Qt.Key.Key_F:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key.Key_Escape and self.is_fullscreen:
            self.toggle_fullscreen()

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            self.normal_geometry = self.geometry()
            self.open_button.hide()
            self.open_english_subtitle_button.hide()
            self.open_persian_subtitle_button.hide()
            self.help_button.hide()
            self.showFullScreen()
            self.is_fullscreen = True
        else:
            self.open_button.show()
            self.open_english_subtitle_button.show()
            self.open_persian_subtitle_button.show()
            self.help_button.show()
            self.showNormal()
            self.setGeometry(self.normal_geometry)
            self.is_fullscreen = False

    def toggle_play_pause(self):
        if not self.media:
            return
            
        if self.media_player.is_playing():
            self.media_player.set_pause(1)
            self.is_playing = False
        else:
            if self.media_player.get_length() > 0:
                self.media_player.play()
                self.is_playing = True
                self.next_subtitle_end_time = None

    def next_subtitle(self):
        if self.english_subtitles and self.current_subtitle_index < len(self.english_subtitles) - 1:
            self.current_subtitle_index += 1
            self.jump_to_subtitle(self.current_subtitle_index)

    def previous_subtitle(self):
        if self.english_subtitles and self.current_subtitle_index > 0:
            self.current_subtitle_index -= 1
            self.jump_to_subtitle(self.current_subtitle_index)

    def repeat_current_subtitle(self):
        if self.english_subtitles:
            self.jump_to_subtitle(self.current_subtitle_index)

    def jump_to_subtitle(self, index):
        if self.english_subtitles:
            subtitle = self.english_subtitles[index]
            start_time = (subtitle.start.hours * 3600 + 
                         subtitle.start.minutes * 60 +
                         subtitle.start.seconds) * 1000 + subtitle.start.milliseconds
            self.media_player.set_time(start_time)
            self.update_subtitle_text()

    def update_subtitle_text(self):
        # Update English subtitle
        if self.english_subtitles and 0 <= self.current_subtitle_index < len(self.english_subtitles):
            self.english_subtitle_label.setText(self.english_subtitles[self.current_subtitle_index].text)
        else:
            self.english_subtitle_label.setText("")

        # Update Persian subtitle
        if self.persian_subtitles and 0 <= self.current_subtitle_index < len(self.persian_subtitles):
            self.persian_subtitle_label.setText(self.persian_subtitles[self.current_subtitle_index].text)
        else:
            self.persian_subtitle_label.setText("")

    def update_subtitle(self):
        if not self.media_player.is_playing():
            return

        current_time = self.media_player.get_time()

        # Check if we need to stop at next subtitle's end
        if self.next_subtitle_end_time and current_time >= self.next_subtitle_end_time:
            self.media_player.pause()
            self.is_playing = False
            self.next_subtitle_end_time = None
            return

        # Update English subtitle based on current index
        if self.english_subtitles:
            current_subtitle = self.english_subtitles[self.current_subtitle_index]
            self.english_subtitle_label.setText(current_subtitle.text)

            # Only auto-pause at current subtitle end if not playing until next subtitle
            if not self.next_subtitle_end_time:
                end_time = (current_subtitle.end.hours * 3600 + 
                          current_subtitle.end.minutes * 60 +
                          current_subtitle.end.seconds) * 1000 + current_subtitle.end.milliseconds

                if current_time >= end_time:
                    self.media_player.pause()
                    self.is_playing = False

        # Update Persian subtitle based on current video time
        persian_subtitle = self.find_persian_subtitle(current_time)
        if persian_subtitle:
            self.persian_subtitle_label.setText(persian_subtitle.text)
        else:
            self.persian_subtitle_label.setText("")

    def find_persian_subtitle(self, current_time):
        if not self.persian_subtitles:
            return None
            
        # Binary search for the appropriate Persian subtitle
        left, right = 0, len(self.persian_subtitles) - 1
        
        while left <= right:
            mid = (left + right) // 2
            subtitle = self.persian_subtitles[mid]
            
            start_time = (subtitle.start.hours * 3600 + 
                         subtitle.start.minutes * 60 +
                         subtitle.start.seconds) * 1000 + subtitle.start.milliseconds
            end_time = (subtitle.end.hours * 3600 + 
                       subtitle.end.minutes * 60 +
                       subtitle.end.seconds) * 1000 + subtitle.end.milliseconds
            
            if start_time <= current_time <= end_time:
                return subtitle
            elif current_time < start_time:
                right = mid - 1
            else:
                left = mid + 1
                
        return None

    def play_until_next_subtitle(self):
        if not self.english_subtitles or not self.media:
            return

        # Find the next subtitle's end time
        if self.current_subtitle_index < len(self.english_subtitles) - 1:
            next_subtitle = self.english_subtitles[self.current_subtitle_index + 1]
            self.next_subtitle_end_time = (next_subtitle.end.hours * 3600 + 
                                         next_subtitle.end.minutes * 60 +
                                         next_subtitle.end.seconds) * 1000 + next_subtitle.end.milliseconds
            self.current_subtitle_index += 1
            
            # Start playing if not already playing
            if not self.media_player.is_playing():
                self.media_player.play()
                self.is_playing = True

    def start_from_next_subtitle(self):
        if not self.english_subtitles or not self.media:
            return

        if self.current_subtitle_index < len(self.english_subtitles) - 1:
            next_subtitle = self.english_subtitles[self.current_subtitle_index + 1]
            start_time = (next_subtitle.start.hours * 3600 + 
                         next_subtitle.start.minutes * 60 +
                         next_subtitle.start.seconds) * 1000 + next_subtitle.start.milliseconds
            
            self.media_player.set_time(start_time)
            self.current_subtitle_index += 1
            self.update_subtitle_text()
            
            if not self.media_player.is_playing():
                self.media_player.play()
                self.is_playing = True
                self.next_subtitle_end_time = None

    def closeEvent(self, event):
        super().closeEvent(event)

    def create_buttons(self):
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 5, 10, 5)
        button_layout.setSpacing(10)
        
        # Create buttons
        open_button = QPushButton("Open Video")
        open_button.clicked.connect(self.open_file)
        
        open_english_subtitle = QPushButton("Open English Subtitles")
        open_english_subtitle.clicked.connect(lambda: self.open_subtitle_file('english'))
        
        open_persian_subtitle = QPushButton("Open Persian Subtitles")
        open_persian_subtitle.clicked.connect(lambda: self.open_subtitle_file('persian'))

        help_button = QPushButton("Keyboard Shortcuts")
        help_button.clicked.connect(self.show_shortcuts)
        
        # Store buttons as instance variables for fullscreen toggle
        self.open_button = open_button
        self.open_english_subtitle_button = open_english_subtitle
        self.open_persian_subtitle_button = open_persian_subtitle
        self.help_button = help_button
        
        # Add buttons to layout
        button_layout.addWidget(open_button)
        button_layout.addWidget(open_english_subtitle)
        button_layout.addWidget(open_persian_subtitle)
        button_layout.addWidget(help_button)
        
        # Style the buttons
        for button in [open_button, open_english_subtitle, open_persian_subtitle, help_button]:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2A2A2A;
                    color: white;
                    border: none;
                    padding: 5px 15px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #404040;
                }
                QPushButton:pressed {
                    background-color: #505050;
                }
            """)
        
        return button_layout

    def show_shortcuts(self):
        shortcuts_text = """
<h2>Keyboard Shortcuts</h2>
<table style='border-collapse: collapse; width: 100%;'>
    <tr style='background-color: #2A2A2A;'>
        <th style='padding: 8px; text-align: left; border: 1px solid #404040;'>Key</th>
        <th style='padding: 8px; text-align: left; border: 1px solid #404040;'>Action</th>
    </tr>
    <tr>
        <td style='padding: 8px; border: 1px solid #404040;'>Spacebar</td>
        <td style='padding: 8px; border: 1px solid #404040;'>Play/Pause video</td>
    </tr>
    <tr style='background-color: #2A2A2A;'>
        <td style='padding: 8px; border: 1px solid #404040;'>Right Arrow</td>
        <td style='padding: 8px; border: 1px solid #404040;'>Play until end of next subtitle</td>
    </tr>
    <tr>
        <td style='padding: 8px; border: 1px solid #404040;'>Ctrl + Right</td>
        <td style='padding: 8px; border: 1px solid #404040;'>Skip to start of next subtitle</td>
    </tr>
    <tr style='background-color: #2A2A2A;'>
        <td style='padding: 8px; border: 1px solid #404040;'>Left Arrow</td>
        <td style='padding: 8px; border: 1px solid #404040;'>Go to previous subtitle</td>
    </tr>
    <tr>
        <td style='padding: 8px; border: 1px solid #404040;'>Down Arrow</td>
        <td style='padding: 8px; border: 1px solid #404040;'>Repeat current subtitle</td>
    </tr>
    <tr style='background-color: #2A2A2A;'>
        <td style='padding: 8px; border: 1px solid #404040;'>F</td>
        <td style='padding: 8px; border: 1px solid #404040;'>Toggle fullscreen</td>
    </tr>
    <tr>
        <td style='padding: 8px; border: 1px solid #404040;'>Escape</td>
        <td style='padding: 8px; border: 1px solid #404040;'>Exit fullscreen</td>
    </tr>
</table>

<h3 style='margin-top: 15px;'>Tips:</h3>
<ul>
    <li>Use Right Arrow to continue from current position</li>
    <li>Use Ctrl+Right to jump to next subtitle immediately</li>
    <li>Use Down Arrow to practice current subtitle</li>
    <li>Use Left Arrow to review previous subtitles</li>
</ul>
"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Keyboard Shortcuts")
        dialog.setFixedSize(500, 600)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Create text browser for rich text
        text_browser = QTextBrowser()
        text_browser.setHtml(shortcuts_text)
        text_browser.setStyleSheet("""
            QTextBrowser {
                background-color: #1A1A1A;
                color: white;
                border: none;
                padding: 10px;
            }
        """)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #2A2A2A;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton:pressed {
                background-color: #505050;
            }
        """)
        
        # Add widgets to layout
        layout.addWidget(text_browser)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set dialog style
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1A1A1A;
                color: white;
            }
        """)
        
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec()) 