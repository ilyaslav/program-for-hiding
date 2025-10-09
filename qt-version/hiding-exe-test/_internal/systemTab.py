import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QIntValidator
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QSlider, QLineEdit, QFrame, QGroupBox, QSpacerItem, QSizePolicy
)


# Кастомный виджет для кружка-индикатора
class CircleIndicator(QWidget):
    def __init__(self, color=QColor("red"), parent=None):
        super().__init__(parent)
        self._color = color
        self.setFixedSize(40, 40)
        self.rsb_blocks = {}

    def setColor(self, color: QColor):
        self._color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self._color)
        painter.setPen(Qt.black)
        painter.drawEllipse(0, 0, self.width(), self.height())


class SystemTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # Верхние кнопки (в ряд)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        button_style = "font-size: 14px; font-weight: bold; padding: 6px; min-height: 40px;"

        self.start_btn = QPushButton("Запустить\nсистему")
        self.start_btn.setFixedWidth(170)
        self.start_btn.setStyleSheet("background-color: red;" + button_style)

        self.stop_btn = QPushButton("Остановить\nсистему")
        self.stop_btn.setFixedWidth(170)
        self.stop_btn.setStyleSheet("background-color: red;" + button_style)

        self.check_btn = QPushButton("Проверка связи")
        self.check_btn.setFixedWidth(170)
        self.check_btn.setStyleSheet("background-color: yellow;" + button_style)

        self.status_label = QLabel("------")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFrameShape(QFrame.Box)
        self.status_label.setFixedWidth(340)
        self.status_label.setMinimumHeight(40)
        self.status_label.setStyleSheet("font-size: 14px; padding: 6px; background-color: white;")

        self.skip_btn = QPushButton("Пропуск\nпроверки")
        self.skip_btn.setFixedWidth(170)
        self.skip_btn.setStyleSheet("background-color: red;" + button_style)

        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.stop_btn)
        buttons_layout.addWidget(self.check_btn)
        buttons_layout.addWidget(self.status_label)
        buttons_layout.addWidget(self.skip_btn)

        main_layout.addLayout(buttons_layout)

        # Секция RSB и Резервов
        devices_layout = QHBoxLayout()
        devices_layout.setSpacing(15)

        # Словарь для блоков с отдельными виджетами
        self.rsb_blocks = {}

        for idx, name in enumerate(["RSB1", "RSB2", "RSB3", "Резерв", "Резерв", "Резерв"]):
            block = self.createDeviceBlock(name, active=("RSB" in name))
            self.rsb_blocks[name] = block
            devices_layout.addWidget(block["group"])

        main_layout.addLayout(devices_layout)
        self.setLayout(main_layout)

    def createDeviceBlock(self, name, active=True):
        group = QGroupBox()
        group.setFixedWidth(170)
        group.setStyleSheet("QGroupBox { background-color: #f0f0f0; border: 1px solid gray; }")

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        lbl_name = QLabel(name)
        lbl_name.setAlignment(Qt.AlignCenter)
        lbl_name.setStyleSheet("font-size: 14px; font-weight: bold;")

        indicator = CircleIndicator(QColor("red") if active else QColor("gray"))

        spacer_top = QSpacerItem(20, 120, QSizePolicy.Minimum, QSizePolicy.Preferred)

        lbl_vol = QLabel("Громкость")
        lbl_vol.setAlignment(Qt.AlignCenter)
        lbl_vol.setStyleSheet("font-size: 14px; font-weight: bold;")

        slider = QSlider(Qt.Vertical)
        slider.setRange(0, 100)
        slider.setValue(80)
        slider.setFixedHeight(150)

        percent_layout = QHBoxLayout()
        line = QLineEdit("80")
        line.setValidator(QIntValidator(0, 100))
        line.setAlignment(Qt.AlignCenter)
        line.setFixedWidth(50)
        line.setStyleSheet("font-size: 14px; font-weight: bold;")
        lbl_percent = QLabel("%")
        lbl_percent.setStyleSheet("font-size: 14px; font-weight: bold;")
        percent_layout.addStretch()
        percent_layout.addWidget(line)
        percent_layout.addWidget(lbl_percent)
        percent_layout.addStretch()

        vbox.addWidget(lbl_name)
        vbox.addWidget(indicator, alignment=Qt.AlignHCenter)
        vbox.addItem(spacer_top)
        vbox.addWidget(lbl_vol)
        vbox.addWidget(slider, alignment=Qt.AlignHCenter)
        vbox.addLayout(percent_layout)

        group.setLayout(vbox)

        # Возвращаем словарь с нужными виджетами
        return {
            "group": group,
            "indicator": indicator,
            "slider": slider,
            "line_edit": line,
            "label": lbl_name
        }

    def get_indicator_rsb1(self):
        return self.rsb_blocks["RSB1"]["indicator"]

    def get_indicator_rsb2(self):
        return self.rsb_blocks["RSB2"]["indicator"]

    def get_indicator_rsb3(self):
        return self.rsb_blocks["RSB3"]["indicator"]

    def get_slider_rsb1(self):
        return self.rsb_blocks["RSB1"]["slider"]

    def get_slider_rsb2(self):
        return self.rsb_blocks["RSB2"]["slider"]

    def get_slider_rsb3(self):
        return self.rsb_blocks["RSB3"]["slider"]

    def get_line_edit_rsb1(self):
        return self.rsb_blocks["RSB1"]["line_edit"]

    def get_line_edit_rsb2(self):
        return self.rsb_blocks["RSB2"]["line_edit"]

    def get_line_edit_rsb3(self):
        return self.rsb_blocks["RSB3"]["line_edit"]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemTab()
    window.setWindowTitle("Система")
    window.resize(1126, 627)
    window.show()
    sys.exit(app.exec_())
