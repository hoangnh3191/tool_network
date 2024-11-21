import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quản lý Switch Cisco")
        self.resize(900, 600)  # Tăng kích thước cửa sổ lên 800x600

        # Tạo widget tab chính
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tạo tab "Switch"
        self.switch_tab = QWidget()
        self.tabs.addTab(self.switch_tab, "Switch")
        self.switch_tab_layout = QVBoxLayout()
        self.switch_tab.setLayout(self.switch_tab_layout)

        # Tạo widget tab bên trong tab "Switch"
        self.inner_tabs = QTabWidget()
        self.switch_tab_layout.addWidget(self.inner_tabs)

        # Tạo tab "Control" bên trong tab "Switch"
        self.control_tab = QWidget()
        self.inner_tabs.addTab(self.control_tab, "Control")
        self.control_tab_layout = QVBoxLayout()
        self.control_tab.setLayout(self.control_tab_layout)
        self.control_tab_layout.addWidget(QLabel("Nội dung cho tab Control"))

        # Tạo tab "Setting" bên trong tab "Switch"
        self.setting_tab = QWidget()
        self.inner_tabs.addTab(self.setting_tab, "Setting")
        self.setting_tab_layout = QVBoxLayout()
        self.setting_tab.setLayout(self.setting_tab_layout)
        self.setting_tab_layout.addWidget(QLabel("Nội dung cho tab Setting"))

        # Tạo tab "Wifi"
        self.wifi_tab = QWidget()
        self.tabs.addTab(self.wifi_tab, "Wifi")
        self.wifi_tab_layout = QVBoxLayout()
        self.wifi_tab.setLayout(self.wifi_tab_layout)
        self.wifi_tab_layout.addWidget(QLabel("Nội dung cho tab Wifi"))

        # Tạo hình tròn màu xanh lá cây sáng hơn
        self.green_circle = QPixmap(10, 10)
        self.update_circle_opacity(1.0)  # Bắt đầu với độ trong suốt 1.0

        # Tạo QLabel cho hình tròn và thêm vào thanh trạng thái
        self.circle_label = QLabel()
        self.circle_label.setPixmap(self.green_circle)
        self.statusBar().addWidget(self.circle_label)

        # Tạo QTimer để chớp tắt hình tròn
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_circle_opacity)
        self.blink_timer.start(500)  # Chớp tắt mỗi 500ms

        # Cập nhật thông điệp thanh trạng thái
        self.statusBar().addWidget(QLabel("Server: Sẵn sàng"))

        # Thêm một thanh trạng thái khác ở phía bên phải
        self.statusBar().addPermanentWidget(QLabel("Đã kết nối"))

    def update_circle_opacity(self, opacity):
        self.green_circle.fill(Qt.transparent)
        painter = QPainter(self.green_circle)
        color = QColor('#00FF00')
        color.setAlphaF(opacity)  # Đặt độ trong suốt
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 10, 10)
        painter.end()

    def toggle_circle_opacity(self):
        current_opacity = self.green_circle.toImage().pixelColor(5, 5).alphaF()
        new_opacity = 0.0 if current_opacity > 0 else 1.0
        self.update_circle_opacity(new_opacity)
        self.circle_label.setPixmap(self.green_circle)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
