import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QTimer

class AddDeviceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Thiết Bị Mới")
        
        self.layout = QFormLayout(self)
        
        # Tạo các trường nhập liệu
        self.host_input = QLineEdit(self)
        self.device_name_input = QLineEdit(self)
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.secret_input = QLineEdit(self)
        self.device_type_input = QLineEdit(self)
        self.location_input = QLineEdit(self)
        
        # Thêm các trường vào layout
        self.layout.addRow("Host:", self.host_input)
        self.layout.addRow("Device Name:", self.device_name_input)
        self.layout.addRow("Username:", self.username_input)
        self.layout.addRow("Password:", self.password_input)
        self.layout.addRow("Secret:", self.secret_input)
        self.layout.addRow("Device Type:", self.device_type_input)
        self.layout.addRow("Location:", self.location_input)
        
        # Thêm nút OK và Cancel
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quản lý FLW")
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
        self.inner_tabs.addTab(self.control_tab, "Check Switch Status")
        self.control_tab_layout = QVBoxLayout()
        self.control_tab.setLayout(self.control_tab_layout)
        self.control_tab_layout.addWidget(QLabel("Nội dung cho tab Control"))

        # Tạo tab "Device List" bên trong tab "Switch"
        self.setting_tab = QWidget()
        self.inner_tabs.addTab(self.setting_tab, "Device List")
        self.setting_tab_layout = QVBoxLayout()
        self.setting_tab.setLayout(self.setting_tab_layout)

        # Thêm nút "Add Device" phía trên bảng
        self.add_device_button = QPushButton("Add Device")
        self.add_device_button.clicked.connect(self.add_device)
        self.setting_tab_layout.addWidget(self.add_device_button)

        # Tạo bảng trong tab "Device List"
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(8)  # Tăng số lượng cột lên 8
        self.device_table.setHorizontalHeaderLabels([
            "Host", "Device Name", "Username", "Password", 
            "Secret", "Device Type", "Location", "Action"
        ])
        self.setting_tab_layout.addWidget(self.device_table)

        # Đọc dữ liệu từ file CSV và hiển thị trong bảng
        self.load_device_data()

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

        # Thêm một thanh trạng thái khác ở phía bên phi
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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Xác nhận thoát', 
                                     'Bạn có chắc chắn muốn thoát không?', 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def load_device_data(self):
        with open('SW/sw_all.csv', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Bỏ qua dòng tiêu đề
            for row in csvreader:
                row_position = self.device_table.rowCount()
                self.device_table.insertRow(row_position)
                for column, data in enumerate(row):  # Không bỏ qua cột nào
                    self.device_table.setItem(row_position, column, QTableWidgetItem(data))
                
                # Thêm nút "Delete" vào cột thứ 8
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=row_position: self.confirm_delete(row))
                self.device_table.setCellWidget(row_position, 7, delete_button)  # Cột thứ 8 có chỉ số 7
        
        # Giãn đều các cột theo kích thước chiều ngang của bảng
        header = self.device_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Sắp xếp dữ liệu theo cột "Device Name" (cột thứ 1, chỉ số 1)
        self.device_table.sortItems(1, Qt.AscendingOrder)

    def confirm_delete(self, row):
        reply = QMessageBox.question(self, 'Xác nhận xóa', 
                                     'Bạn có chắc chắn muốn xóa hàng này không?', 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.delete_row(row)

    def delete_row(self, row):
        self.device_table.removeRow(row)

    def add_device(self):
        dialog = AddDeviceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Lấy dữ liệu từ hộp thoại
            new_device = [
                dialog.host_input.text(),
                dialog.device_name_input.text(),
                dialog.username_input.text(),
                dialog.password_input.text(),
                dialog.secret_input.text(),
                dialog.device_type_input.text(),
                dialog.location_input.text()
            ]
            
            # Ghi dữ liệu vào file CSV
            with open('SW/sw_all.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(new_device)
            
            # Thêm dữ liệu vào bảng
            row_position = self.device_table.rowCount()
            self.device_table.insertRow(row_position)
            for column, data in enumerate(new_device):
                self.device_table.setItem(row_position, column, QTableWidgetItem(data))
            
            # Thêm nút "Delete" vào cột thứ 8
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, row=row_position: self.confirm_delete(row))
            self.device_table.setCellWidget(row_position, 7, delete_button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())