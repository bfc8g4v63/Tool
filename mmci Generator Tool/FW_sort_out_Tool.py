import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QRadioButton, QListWidget,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

class DragDropListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                self.parent().add_file(file_path)
            event.acceptProposedAction()

class MMCIGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MMCIGenerator")
        self.resize(600, 400)
        self.mode = 'USB'
        self.file_list = []
        self.output_dir = ''
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        mode_layout = QHBoxLayout()
        self.usb_radio = QRadioButton("USB")
        self.pcuid_radio = QRadioButton("PC UID")
        self.usb_radio.setChecked(True)

        self.usb_radio.toggled.connect(self.set_mode)
        self.pcuid_radio.toggled.connect(self.set_mode)

        mode_layout.addWidget(self.usb_radio)
        mode_layout.addWidget(self.pcuid_radio)
        layout.addLayout(mode_layout)

        self.file_list_widget = DragDropListWidget(self)
        layout.addWidget(self.file_list_widget)

        save_name_layout = QHBoxLayout()
        self.save_name_label = QLabel("存名:")
        self.save_name_input = QLineEdit()
        save_name_layout.addWidget(self.save_name_label)
        save_name_layout.addWidget(self.save_name_input)
        layout.addLayout(save_name_layout)

        output_dir_layout = QHBoxLayout()
        self.output_dir_label = QLabel("輸出資料夾:")
        self.output_dir_input = QLineEdit()
        self.select_output_button = QPushButton("選擇")
        self.select_output_button.clicked.connect(self.select_output_dir)
        output_dir_layout.addWidget(self.output_dir_label)
        output_dir_layout.addWidget(self.output_dir_input)
        output_dir_layout.addWidget(self.select_output_button)
        layout.addLayout(output_dir_layout)

        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("生成")
        self.generate_button.clicked.connect(self.generate_mmci)

        button_layout.addWidget(self.generate_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def set_mode(self):
        if self.usb_radio.isChecked():
            self.mode = 'USB'
        else:
            self.mode = 'PCUID'

    def add_file(self, file_path):
        if os.path.isdir(file_path):
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    self.file_list.append(full_path)
                    self.file_list_widget.addItem(full_path)
        else:
            self.file_list.append(file_path)
            self.file_list_widget.addItem(file_path)

    def get_target_folder(self, file_path):

        parent_dir = os.path.dirname(file_path)
        folder_name = os.path.basename(parent_dir)
        return folder_name

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "選擇輸出資料夾")
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_input.setText(dir_path)

    def generate_mmci(self):
        if not self.file_list:
            QMessageBox.warning(self, "警告", "請先加入檔案！")
            return

        save_name = self.save_name_input.text().strip()
        if not save_name:
            QMessageBox.warning(self, "警告", "請輸入存名！")
            return

        if not self.output_dir:
            QMessageBox.warning(self, "警告", "請選擇輸出資料夾！")
            return

        output_lines = []

        for path in self.file_list:
            folder_name = self.get_target_folder(path)
            filename = os.path.basename(path)

            dest_folder = os.path.join(self.output_dir, folder_name)
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, filename)

            shutil.copy2(path, dest_path)

            if self.mode == 'USB':
                output_path_line = f"{folder_name}/{filename}"
            else:
                output_path_line = f"{folder_name}\\{filename}"

            output_lines.append(output_path_line)

        output_content = '\n'.join(output_lines)
        mmci_path = os.path.join(self.output_dir, f"{save_name}.mmci")

        try:
            with open(mmci_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            QMessageBox.information(self, "成功", f"成功生成 {mmci_path}")
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"生成失敗: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MMCIGenerator()
    window.show()
    sys.exit(app.exec())