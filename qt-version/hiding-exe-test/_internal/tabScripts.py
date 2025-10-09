from PyQt5 import QtCore, QtGui, QtWidgets


class TabScripts(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("tab_scripts")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(15)

        font = QtGui.QFont()
        font.setPointSize(16)

        # ====== Сетка для 8 кнопок (2 ряда по 4) ======
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(20)

        self.buttons = []
        self.labels = []

        button_width = 240  # фиксированная ширина для всех кнопок
        button_height = 60

        for i in range(8):
            # Кнопка
            button = QtWidgets.QPushButton(f"Сценарий {i + 1}")
            button.setFixedSize(button_width, button_height)
            button.setFont(font)

            if i == 0:
                button.setStyleSheet('''
QPushButton {
background-color:#00ff00;
}
QPushButton:disabled {
background-color:#00ff00;
}''')
            else:
                button.setStyleSheet('''
QPushButton {
background-color:#ffffff;
}
QPushButton:disabled {
background-color:#ffffff;
}''')

            # Подпись
            label = QtWidgets.QLabel("\n------------------")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setStyleSheet("background-color: white; font-size: 16px; padding: 2px;")
            label.setMinimumHeight(24)
            label.setFixedWidth(button_width)

            # Минимальное расстояние между кнопкой и подписью
            button_layout = QtWidgets.QVBoxLayout()
            button_layout.setSpacing(4)
            button_layout.addWidget(button, alignment=QtCore.Qt.AlignHCenter)
            button_layout.addWidget(label, alignment=QtCore.Qt.AlignHCenter)

            container = QtWidgets.QWidget()
            container.setLayout(button_layout)

            row = i // 4
            col = i % 4
            grid_layout.addWidget(container, row, col, alignment=QtCore.Qt.AlignCenter)

            self.buttons.append(button)
            self.labels.append(label)

        self.verticalLayout.addLayout(grid_layout)

        spacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacer)

    # ===== Методы доступа к кнопкам =====
    def get_script1_bt(self): return self.buttons[0]
    def get_script2_bt(self): return self.buttons[1]
    def get_script3_bt(self): return self.buttons[2]
    def get_script4_bt(self): return self.buttons[3]
    def get_script5_bt(self): return self.buttons[4]
    def get_script6_bt(self): return self.buttons[5]
    def get_script7_bt(self): return self.buttons[6]
    def get_script8_bt(self): return self.buttons[7]

    # ===== Методы доступа к лейблам =====
    def get_script1_label(self): return self.labels[0]
    def get_script2_label(self): return self.labels[1]
    def get_script3_label(self): return self.labels[2]
    def get_script4_label(self): return self.labels[3]
    def get_script5_label(self): return self.labels[4]
    def get_script6_label(self): return self.labels[5]
    def get_script7_label(self): return self.labels[6]
    def get_script8_label(self): return self.labels[7]
