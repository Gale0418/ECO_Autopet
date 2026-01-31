import sys
import time
import threading
import win32gui
import win32con
import win32api
import win32process
import psutil
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QInputDialog,
    QFrame,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, QTimer


# 按鍵對應
KEYS = {
    "F9": 0x78,
    "F10": 0x79,
    "F11": 0x7A,
    "F12": 0x7B,
}


def send_key(hwnd, keycode):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, keycode, 0)
    time.sleep(0.05)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, keycode, 0)


def find_eco_windows():
    hwnds = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                if process.name().lower() == "eco.exe":
                    hwnds.append(hwnd)
            except Exception:
                pass

    win32gui.EnumWindows(callback, None)
    return hwnds


class FloatingUI(QWidget):
    def __init__(self, cycle_time):
        super().__init__()
        self.cycle_time = cycle_time
        self.remaining = cycle_time

        # 浮窗設定
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 頂部按鈕列 F9-F12 + X
        self.key_buttons = {}
        x_offset = 10
        for key in KEYS.keys():
            btn = QPushButton(key, self)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(100,100,100,180);
                    color:white;
                    border-radius:6px;
                    padding:4px 6px;
                }
                QPushButton:checked {
                    background-color: rgba(0,200,120,220);
                    font-weight:bold;
                }
            """)
            btn.move(x_offset, 5)
            btn.setFixedSize(45, 28)
            btn.setChecked(key in ["F9", "F12"])
            self.key_buttons[key] = btn
            x_offset += 50

        # 關閉按鈕 X
        self.close_btn = QPushButton("X", self)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(200,50,50,180);
                color:white;
                border:none;
                border-radius:6px;
                font-weight:bold;
                font-size:14px;
            }
            QPushButton:hover {
                background-color: rgba(255,80,80,220);
            }
        """)
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.clicked.connect(self.close_app)
        self.close_btn.move(x_offset, 5)

        # 大框框，用 QFrame 包裹資訊
        self.info_frame = QFrame(self)
        self.info_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(50,50,50,220);
                border-radius:10px;
            }
        """)
        self.info_frame.setGeometry(10, 40, x_offset + 10, 80)

        # 時間設定區域
        time_layout = QHBoxLayout()
        
        self.time_label = QLabel("循環時間:", self.info_frame)
        self.time_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
            }
        """)
        
        self.time_input = QLineEdit(str(cycle_time), self.info_frame)
        self.time_input.setFixedWidth(60)
        self.time_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255,255,255,200);
                border-radius:4px;
                padding:2px 4px;
            }
        """)
        
        self.set_time_btn = QPushButton("設定", self.info_frame)
        self.set_time_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0,150,255,180);
                color:white;
                border-radius:4px;
                padding:2px 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(0,180,255,220);
            }
        """)
        self.set_time_btn.clicked.connect(self.set_cycle_time)
        
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_input)
        time_layout.addWidget(self.set_time_btn)
        time_layout.addStretch()

        # ECO視窗數量
        self.label_count = QLabel("ECO視窗數量: 0", self.info_frame)
        self.label_count.setStyleSheet("""
            QLabel {
                color: #00FFAA;
                font-weight: bold;
                font-size: 16px;
            }
        """)

        # 倒數
        self.label_timer = QLabel(
            f"下一次執行倒數: {self.remaining}秒", self.info_frame
        )
        self.label_timer.setStyleSheet("""
            QLabel {
                color: #FFFF66;
                font-weight: bold;
                font-size: 16px;
            }
        """)

        # 佈局
        main_layout = QVBoxLayout(self.info_frame)
        main_layout.addLayout(time_layout)
        main_layout.addWidget(self.label_count)
        main_layout.addWidget(self.label_timer)
        main_layout.addStretch()
        
        # 設定浮窗大小
        self.resize(self.info_frame.width() + 20, 160)
        self.show()

        # 拖曳
        self.drag_pos = None

        # UI 更新
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

        # 背景自動執行
        threading.Thread(target=self.auto_runner, daemon=True).start()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(event.globalPosition().toPoint() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def close_app(self):
        QApplication.quit()

    def get_selected_keys(self):
        return [k for k, btn in self.key_buttons.items() if btn.isChecked()]

    def set_cycle_time(self):
        try:
            new_time = int(self.time_input.text())
            if new_time > 0:
                self.cycle_time = new_time
                self.remaining = new_time
                self.label_timer.setText(f"下一次執行倒數: {self.remaining}秒")
        except ValueError:
            pass

    def update_ui(self):
        hwnds = find_eco_windows()
        eco_count = len(hwnds)
        self.label_count.setText(f"ECO視窗數量: {eco_count}")
        self.label_count.adjustSize()
        self.label_timer.setText(f"下一次執行倒數: {self.remaining}秒")
        self.label_timer.adjustSize()

    def auto_runner(self):
        while True:
            hwnds = find_eco_windows()
            selected_keys = self.get_selected_keys()
            if hwnds and selected_keys:
                for key in selected_keys:
                    for hwnd in hwnds:
                        send_key(hwnd, KEYS[key])
                    time.sleep(10)
                self.remaining = self.cycle_time
                while self.remaining > 0:
                    time.sleep(1)
                    self.remaining -= 1
            else:
                time.sleep(2)
                self.remaining = self.cycle_time


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cycle_time = 180  # 預設循環時間
    ui = FloatingUI(cycle_time)
    sys.exit(app.exec())
