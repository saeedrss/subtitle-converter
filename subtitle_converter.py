import re
import sys
import os
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLabel, QComboBox, QPushButton, 
                            QFileDialog, QMessageBox, QLineEdit, QAction, QDialog,
                            QDialogButtonBox)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QIcon
from pathlib import Path


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Subtitle Frame Rate Converter")
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Subtitle Frame Rate Converter")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Icon
        icon_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")

        self.setWindowIcon(QIcon(icon_path))
        QApplication.setWindowIcon(QIcon(icon_path))
        # Version
        version = QLabel("Version 1.0")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)
        
        # Links
        github_link = QLabel('<a href="https://github.com/saeedrss/subtitle-converter">GitHub Repository</a>')
        github_link.setOpenExternalLinks(True)
        github_link.setAlignment(Qt.AlignCenter)
        layout.addWidget(github_link)
        
        telegram_link = QLabel('<a href="https://t.me/Digi_Chanel">Telegram Channel</a>')
        telegram_link.setOpenExternalLinks(True)
        telegram_link.setAlignment(Qt.AlignCenter)
        layout.addWidget(telegram_link)
        
        # Feedback
        feedback = QLabel("Suggestions and feedback welcome!")
        feedback.setAlignment(Qt.AlignCenter)
        layout.addWidget(feedback)
        
        # Close button
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
        
        self.setLayout(layout)

        def set_application_icon(self):
            """Try to set application icon from available files"""
            icon_paths = [
                "app_icon.ico",  # Windows preferred format
                "app_icon.png",  # Cross-platform format
                "icons/app_icon.ico",  # Common alternative locations
                "icons/app_icon.png",
                "resources/app_icon.ico",
                "resources/app_icon.png"
            ]

            for path in icon_paths:
                if Path(path).exists():
                    self.setWindowIcon(QIcon(path))
                    QApplication.setWindowIcon(QIcon(path))  # Also set for the application
                    print(f"Using icon from: {path}")
                    return

            print("Warning: No application icon found (tried app_icon.ico and app_icon.png)")

    
class SubtitleConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = 'en'
        self.translations = {
            'en': {
                'window_title': "Subtitle Frame Rate Converter",
                'file_menu': "File",
                'exit': "Exit",
                'language_menu': "Language",
                'input_label': "Input File:",
                'output_label': "Output File:",
                'source_label': "Source FPS:",
                'target_label': "Target FPS:",
                'browse': "Browse...",
                'convert': "Convert Subtitles",
                'select_input': "Select Input Subtitle File",
                'select_output': "Select Output Subtitle File",
                'error': "Error",
                'no_input': "Please select an input file",
                'no_output': "Please select an output file",
                'same_fps': "Source and target FPS are the same",
                'success': "Success",
                'converted': "Successfully converted from {}fps to {}fps",
                'conversion_failed': "Conversion failed: {}",
                'file_types': "Subtitle Files (*.srt *.ass *.ssa);;All Files (*)",
                'unknown': "Unknown"
            },
            'fa': {
                'window_title': "مبدل نرخ فریم زیرنویس",
                'file_menu': "فایل",
                'exit': "خروج",
                'language_menu': "زبان",
                'input_label': "فایل ورودی:",
                'output_label': "فایل خروجی:",
                'source_label': "نرخ فریم مبدأ:",
                'target_label': "نرخ فریم مقصد:",
                'browse': "مرور...",
                'convert': "تبدیل زیرنویس‌ها",
                'select_input': "انتخاب فایل زیرنویس ورودی",
                'select_output': "انتخاب فایل زیرنویس خروجی",
                'error': "خطا",
                'no_input': "لطفاً فایل ورودی را انتخاب کنید",
                'no_output': "لطفاً فایل خروجی را انتخاب کنید",
                'same_fps': "نرخ فریم مبدأ و مقصد یکسان هستند",
                'success': "موفقیت",
                'converted': "تبدیل با موفقیت انجام شد از {}فریم بر ثانیه به {}فریم بر ثانیه",
                'conversion_failed': "تبدیل ناموفق: {}",
                'file_types': "فایل‌های زیرنویس (*.srt *.ass *.ssa);;تمام فایل‌ها (*)",
                'unknown': "ناشناخته"
            }
        }
        
        # Available frame rates
        self.frame_rates = ["23.976", "24", "25", "29.97", "30"]
        
        # Create UI
        self.setup_ui()
        self.retranslate_ui()

        # Set window icon
        icon_path = self.get_icon_path()
        self.setWindowIcon(QIcon(icon_path))

        # Set window properties
        self.setFixedSize(500, 300)

    def get_icon_path(self):
        """Return the best available icon path for the current platform"""
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Try .ico first (better for Windows)
        ico_path = os.path.join(base_dir, 'app_icon.ico')
        if os.path.exists(ico_path):
            return ico_path

        # Fall back to .png
        png_path = os.path.join(base_dir, 'app_icon.png')
        if os.path.exists(png_path):
            return png_path

        return ""  # No icon found
    def setup_ui(self):
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Create UI elements
        self.create_menu()
        self.create_file_selection()
        self.create_frame_rate_selection()
        self.create_convert_button()
        self.create_help_menu()
    def create_help_menu(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu(self.translate("Help"))
        
        about_action = QAction(self.translate("About"), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        feedback_action = QAction(self.translate("Send Feedback"), self)
        feedback_action.triggered.connect(self.send_feedback)
        help_menu.addAction(feedback_action)

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def send_feedback(self):
        telegram_url = QUrl("https://t.me/Digi_Chanel")
        QDesktopServices.openUrl(telegram_url)
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # File menu
        self.file_menu = menubar.addMenu("")
        self.exit_action = QAction("", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)
        
        # Language menu
        self.language_menu = menubar.addMenu("")
        
        self.english_action = QAction("English", self)
        self.english_action.triggered.connect(lambda: self.set_language('en'))
        
        self.farsi_action = QAction("فارسی", self)
        self.farsi_action.triggered.connect(lambda: self.set_language('fa'))
        
        self.language_menu.addAction(self.english_action)
        self.language_menu.addAction(self.farsi_action)
    
    def create_file_selection(self):
        # Input file selection
        input_layout = QHBoxLayout()
        self.input_label = QLabel()
        self.input_line = QLineEdit()
        self.input_line.setReadOnly(True)
        self.input_button = QPushButton()
        self.input_button.clicked.connect(self.select_input_file)
        
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.input_button)
        self.main_layout.addLayout(input_layout)
        
        # Output file selection
        output_layout = QHBoxLayout()
        self.output_label = QLabel()
        self.output_line = QLineEdit()
        self.output_button = QPushButton()
        self.output_button.clicked.connect(self.select_output_file)
        
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_line)
        output_layout.addWidget(self.output_button)
        self.main_layout.addLayout(output_layout)
    
    def create_frame_rate_selection(self):
        # Source frame rate
        source_layout = QHBoxLayout()
        self.source_label = QLabel()
        self.source_combo = QComboBox()
        self.source_combo.addItem(self.translate('unknown'))  # Add "Unknown" option
        self.source_combo.addItems(self.frame_rates)
        
        source_layout.addWidget(self.source_label)
        source_layout.addWidget(self.source_combo)
        self.main_layout.addLayout(source_layout)
        
        # Target frame rate
        target_layout = QHBoxLayout()
        self.target_label = QLabel()
        self.target_combo = QComboBox()
        self.target_combo.addItem(self.translate('unknown'))  # Add "Unknown" option
        self.target_combo.addItems(self.frame_rates)
        self.target_combo.setCurrentIndex(1)  # Default to first frame rate
        
        target_layout.addWidget(self.target_label)
        target_layout.addWidget(self.target_combo)
        self.main_layout.addLayout(target_layout)
    
    def create_convert_button(self):
        self.convert_button = QPushButton()
        self.convert_button.clicked.connect(self.convert_subtitles)
        self.main_layout.addWidget(self.convert_button)
    
    def retranslate_ui(self):
        # Window title
        self.setWindowTitle(self.translate('window_title'))
        
        # Menu items
        self.file_menu.setTitle(self.translate('file_menu'))
        self.exit_action.setText(self.translate('exit'))
        self.language_menu.setTitle(self.translate('language_menu'))

        # File selection
        self.input_label.setText(self.translate('input_label'))
        self.output_label.setText(self.translate('output_label'))
        self.input_button.setText(self.translate('browse'))
        self.output_button.setText(self.translate('browse'))
        
        # Frame rate selection
        self.source_label.setText(self.translate('source_label'))
        self.target_label.setText(self.translate('target_label'))
        
        # Convert button
        self.convert_button.setText(self.translate('convert'))
        
        # Update combo boxes
        self.update_combo_boxes()
    
    def update_combo_boxes(self):
        # Save current selections
        source_index = self.source_combo.currentIndex()
        target_index = self.target_combo.currentIndex()
        
        # Update source combo
        self.source_combo.clear()
        self.source_combo.addItem(self.translate('unknown'))
        self.source_combo.addItems(self.frame_rates)
        self.source_combo.setCurrentIndex(min(source_index, len(self.frame_rates)))
        
        # Update target combo
        self.target_combo.clear()
        self.target_combo.addItem(self.translate('unknown'))
        self.target_combo.addItems(self.frame_rates)
        self.target_combo.setCurrentIndex(min(target_index, len(self.frame_rates)))
    
    def set_language(self, language):
        self.current_language = language
        if language == 'fa':
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)
        self.retranslate_ui()
    
    def translate(self, text):
        """Get translation for the current language"""
        return self.translations.get(self.current_language, {}).get(text, text)
    
    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, self.translate('select_input'), "", 
            self.translate('file_types'))
        if file_name:
            self.input_line.setText(file_name)
            # Suggest output filename
            if not self.output_line.text():
                base_name = os.path.splitext(file_name)[0]
                self.output_line.setText(f"{base_name}_converted.srt")
    
    def select_output_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, self.translate('select_output'), self.output_line.text(), 
            self.translate('file_types'))
        if file_name:
            self.output_line.setText(file_name)
    
    def convert_subtitles(self):
        input_file = self.input_line.text()
        output_file = self.output_line.text()
        
        # Validate inputs
        if not input_file:
            QMessageBox.warning(self, self.translate('error'), self.translate('no_input'))
            return
        
        # Get selected FPS options
        source_selection = self.source_combo.currentText()
        target_selection = self.target_combo.currentText()
        
        # Determine source and target FPS lists
        if source_selection == self.translate('unknown'):
            source_fps_list = self.frame_rates
        else:
            source_fps_list = [source_selection]
        
        if target_selection == self.translate('unknown'):
            target_fps_list = self.frame_rates
        else:
            target_fps_list = [target_selection]
        
        # Get base output filename
        base_output = os.path.splitext(output_file)[0] if output_file else os.path.splitext(input_file)[0]
        
        # Convert all combinations
        success_count = 0
        for source_fps in source_fps_list:
            for target_fps in target_fps_list:
                if source_fps == target_fps:
                    continue
                
                # Generate output filename
                if source_selection == self.translate('unknown') and target_selection == self.translate('unknown'):
                    out_file = f"{base_output}_{source_fps}to{target_fps}.srt"
                elif source_selection == self.translate('unknown'):
                    out_file = f"{base_output}_{source_fps}to{target_selection}.srt"
                elif target_selection == self.translate('unknown'):
                    out_file = f"{base_output}_{source_selection}to{target_fps}.srt"
                else:
                    out_file = output_file
                
                try:
                    self.convert_subtitle_file(input_file, out_file, float(source_fps), float(target_fps))
                    success_count += 1
                except Exception as e:
                    QMessageBox.critical(self, self.translate('error'), 
                                      self.translate('conversion_failed').format(f"{source_fps}->{target_fps}: {str(e)}"))
        
        if success_count > 0:
            QMessageBox.information(self, self.translate('success'), 
                                 self.translate('converted').format(f"{len(source_fps_list)} sources", 
                                                                  f"{len(target_fps_list)} targets"))
    
    def time_to_ms(self, h, m, s, ms):
        return h * 3600000 + m * 60000 + s * 1000 + ms
    
    def ms_to_time(self, ms):
        h = ms // 3600000
        ms %= 3600000
        m = ms // 60000
        ms %= 60000
        s = ms // 1000
        ms %= 1000
        return h, m, s, ms
    
    def convert_time(self, time_str, source_fps, target_fps):
        # Parse time string (support both , and . as millisecond separator)
        match = re.match(r'(\d{2}):(\d{2}):(\d{2})[,.](\d{3})', time_str)
        if not match:
            return time_str
        
        h, m, s, ms = map(int, match.groups())
        ms_total = self.time_to_ms(h, m, s, ms)
        
        # Convert frame rates
        converted_ms = ms_total * (target_fps / source_fps)
        
        # Convert back to time format
        h, m, s, ms = self.ms_to_time(int(converted_ms))
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    
    def convert_subtitle_file(self, input_file, output_file, source_fps, target_fps):
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                # Check if line contains timecodes
                if '-->' in line:
                    parts = line.strip().split(' --> ')
                    if len(parts) == 2:
                        start, end = parts
                        new_start = self.convert_time(start, source_fps, target_fps)
                        new_end = self.convert_time(end, source_fps, target_fps)
                        outfile.write(f"{new_start} --> {new_end}\n")
                    else:
                        outfile.write(line)
                else:
                    outfile.write(line)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = SubtitleConverter()
    converter.show()
    sys.exit(app.exec_())
