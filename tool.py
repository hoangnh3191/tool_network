import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quản lý Switch Cisco")

        # Đặt kích thước ban đầu cho cửa sổ
        self.resize(900, 600)  # Tăng kích thước cửa sổ lên 800x600

        # Tạo widget tab
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tạo tab "Switch"
        self.switch_tab = QWidget()
        self.tabs.addTab(self.switch_tab, "Switch")
        self.switch_tab_layout = QVBoxLayout()
        self.switch_tab.setLayout(self.switch_tab_layout)
        self.switch_tab_layout.addWidget(QLabel("Nội dung cho tab Switch"))

        # Tạo tab "Wifi"
        self.wifi_tab = QWidget()
        self.tabs.addTab(self.wifi_tab, "Wifi")
        self.wifi_tab_layout = QVBoxLayout()
        self.wifi_tab.setLayout(self.wifi_tab_layout)
        self.wifi_tab_layout.addWidget(QLabel("Nội dung cho tab Wifi"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
