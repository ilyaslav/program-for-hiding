from PyQt5 import QtWidgets, QtGui

LABEL_WIDTH = 180

def scale_font(widget, factor=1.3):
    font = widget.font()
    font.setPointSizeF(font.pointSizeF() * factor)
    widget.setFont(font)


class PlayerRow(QtWidgets.QWidget):
    def __init__(self, rsb_name, with_volume=False, parent=None):
        super().__init__(parent)

        self.rsb_name = rsb_name

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("""
            background-color: #f4b400;
            padding: 10px;
        """)
        self.label.setMinimumHeight(40)
        self.label.setFixedWidth(LABEL_WIDTH)
        scale_font(self.label)

        layout.addWidget(self.label)

        if with_volume:
            self.volume_edit = QtWidgets.QLineEdit("80")
            self.volume_edit.setMinimumHeight(40)
            scale_font(self.volume_edit)
            validator = QtGui.QIntValidator(0, 100, self)
            self.volume_edit.setValidator(validator)
            self.volume_edit.textChanged.connect(self.fix_value)
            layout.addWidget(self.volume_edit)

            percent = QtWidgets.QLabel("%")
            percent.setStyleSheet("color: white;")
            percent.setMinimumHeight(40)
            scale_font(percent)
            layout.addWidget(percent)

            self.save_btn = QtWidgets.QPushButton("Сохранить")
            self.save_btn.setStyleSheet("background-color: #00c853;")
            self.save_btn.setMinimumHeight(40)
            scale_font(self.save_btn)
            layout.addWidget(self.save_btn)

        else:
            self.combo = QtWidgets.QComboBox()
            self.combo.setMinimumHeight(40)
            scale_font(self.combo)
            layout.addWidget(self.combo, 2)

            self.play_btn = QtWidgets.QPushButton("Play")
            self.pause_btn = QtWidgets.QPushButton("Pause")
            self.stop_btn = QtWidgets.QPushButton("Stop")

            for btn in [self.play_btn, self.pause_btn, self.stop_btn]:
                btn.setMinimumHeight(40)
                scale_font(btn)
                layout.addWidget(btn)

        layout.addStretch()

    def fix_value(self):
        text = self.volume_edit.text()
        if text == "":
            self.volume_edit.setText("0")
        else:
            value = max(0, min(100, int(text)))
            self.volume_edit.setText(str(value))


class MainSettingsTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(12)

        # Хранилища
        self.volume_rows = {}
        self.player_rows = {}

        # === Громкость ===
        for i in range(1, 5):
            row = PlayerRow(f"r{i}", with_volume=True)
            self.volume_rows[i] = row
            main_layout.addWidget(row)

        # === Плееры ===
        for i in range(1, 5):
            row = PlayerRow(f"r{i}")
            self.player_rows[i] = row
            main_layout.addWidget(row)

        main_layout.addStretch()