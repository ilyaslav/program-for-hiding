from mainWindow import Ui_MainWindow
import settings
import game

import time
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication

class ThreadClass(QThread):
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent = None):
        super(ThreadClass, self).__init__(parent)
        self.is_running = True
    def run(self):
        while True:
            self.any_signal.emit(1)
            time.sleep(0.1)
    def stop(self):
        self.is_running = False
        self.terminate()

class MyWindow(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super(MyWindow, self).setupUi(MainWindow)
        self.start_worker()
        self.connect_functions()

    def connect_functions(self):
        self.bt_script1.pressed.connect(self.bt_script1_press)
        self.bt_script2.pressed.connect(self.bt_script2_press)
        self.bt_script3.pressed.connect(self.bt_script3_press)
        self.bt_script4.pressed.connect(self.bt_script4_press)
        self.bt_UV.pressed.connect(self.bt_UVlamps_press)
        self.bt_fan.pressed.connect(self.bt_fans_press)
        self.bt_strobe.pressed.connect(self.bt_strobes_press)
        self.bt_1.pressed.connect(self.bt_UVsec1_press)
        self.bt_2.pressed.connect(self.bt_UVsec2_press)
        self.bt_3.pressed.connect(self.bt_UVsec3_press)
        self.bt_children.pressed.connect(self.bt_UVkids_press)
        self.bt_diagnostic.pressed.connect(self.bt_settings_press)
        self.bt_5min.pressed.connect(self.bt_5min_press)
        self.bt_8min.pressed.connect(self.bt_8min_press)
        self.bt_10min.pressed.connect(self.bt_10min_press)
        self.bt_12min.pressed.connect(self.bt_12min_press)
        self.bt_15min.pressed.connect(self.bt_15min_press)
        self.bt_18min.pressed.connect(self.bt_18min_press)
        self.bt_reset.pressed.connect(self.bt_reset_press)
        self.bt_runstop.pressed.connect(self.bt_RUNSTOP_press)
        self.bt_uv1_off.pressed.connect(partial(game.action_uv1, 0))
        self.bt_uv1_on.pressed.connect(partial(game.action_uv1, 0))
        self.bt_uv2_off.pressed.connect(partial(game.action_uv2, 0))
        self.bt_uv2_on.pressed.connect(partial(game.action_uv2, 0))
        self.bt_uv3_off.pressed.connect(partial(game.action_uv3, 0))
        self.bt_uv3_on.pressed.connect(partial(game.action_uv3, 0))
        self.bt_uv4_off.pressed.connect(partial(game.action_uv4, 0))
        self.bt_uv4_on.pressed.connect(partial(game.action_uv4, 0))
        self.bt_uv5_off.pressed.connect(partial(game.action_uv5, 0))
        self.bt_uv5_on.pressed.connect(partial(game.action_uv5, 0))
        self.bt_uv6_off.pressed.connect(partial(game.action_uv6, 0))
        self.bt_uv6_on.pressed.connect(partial(game.action_uv6, 0))
        self.bt_uv7_off.pressed.connect(partial(game.action_uv7, 0))
        self.bt_uv7_on.pressed.connect(partial(game.action_uv7, 0))
        self.bt_uv8_off.pressed.connect(partial(game.action_uv8, 0))
        self.bt_uv8_on.pressed.connect(partial(game.action_uv8, 0))
        self.bt_uv9_off.pressed.connect(partial(game.action_uv9, 0))
        self.bt_uv9_on.pressed.connect(partial(game.action_uv9, 0))
        self.bt_fan1_off.pressed.connect(partial(game.action_fan1, 0))
        self.bt_fan1_on.pressed.connect(partial(game.action_fan1, 0))
        self.bt_fan2_off.pressed.connect(partial(game.action_fan2, 0))
        self.bt_fan2_on.pressed.connect(partial(game.action_fan2, 0))
        self.bt_fan3_off.pressed.connect(partial(game.action_fan3, 0))
        self.bt_fan3_on.pressed.connect(partial(game.action_fan3, 0))
        self.bt_fan4_off.pressed.connect(partial(game.action_fan4, 0))
        self.bt_fan4_on.pressed.connect(partial(game.action_fan4, 0))
        self.bt_strobe1_off.pressed.connect(partial(game.action_strobe1, 0))
        self.bt_strobe1_on.pressed.connect(partial(game.action_strobe1, 0))
        self.bt_strobe2_off.pressed.connect(partial(game.action_strobe2, 0))
        self.bt_strobe2_on.pressed.connect(partial(game.action_strobe2, 0))
        self.bt_strobe3_off.pressed.connect(partial(game.action_strobe3, 0))
        self.bt_strobe3_on.pressed.connect(partial(game.action_strobe3, 0))
        self.bt_shadow_off.pressed.connect(partial(game.action_shadow_lamp, 0))
        self.bt_shadow_on.pressed.connect(partial(game.action_shadow_lamp, 0))
        self.bt_start_off.pressed.connect(partial(game.action_runstop_lamp, 0))
        self.bt_start_on.pressed.connect(partial(game.action_runstop_lamp, 0))
        self.timer.textEdited.connect(self.change_time)

    def start_worker(self):
        self.thread = ThreadClass(parent=None)
        self.thread.start()
        self.thread.any_signal.connect(self.main_loop)

    def stop_worker(self):
        self.thread.stop()

    def main_loop(self):
        if game.check_start():
            self.bt_RUNSTOP_press()
        game.check_fans()
        self.reset_sensors()

        if settings.bonuses['settings']:
            self.set_dinamic_OnOff()
        else:
            self.set_static_OnOff()

        self.reset_OnOff_bt()
        if settings.time_event:
            settings.time_event = False
            self.timer.setText(settings.time)

        if not settings.runstop and not settings.bonuses['settings']:
            game.off_all()
            game.set_standart_outs()

        if settings.end_timer_event:
            settings.end_timer_event = False
            self.reset_time()
            self.disabling_buttons()
            self.reset_bt_colors()

    def bt_RUNSTOP_press(self):
        game.stop_events()
        if settings.outs['ShadowLamp']:
            game.action_shadow_lamp(0)

        game.set_standart_outs()
        game.action_runstop_lamp(0)
        if settings.runstop:
            game.play_end_music()

        settings.runstop = not settings.runstop
        self.change_RSbt_color()
        self.disabling_buttons()
        self.reset_OnOff_bt()
        game.init_game()
        if not settings.runstop:
            time = settings.timer.split(':')
            settings.time_m = int(time[0])
            settings.time_s = int(time[1])
            settings.time = settings.timer
            settings.time_event = True

    def bt_reset_press(self):
        game.stop_events()
        game.set_standard_settings()
        game.off_all()
        self.reset_bt_colors()
        self.disabling_buttons()
        self.disabled_settings()
        self.refresh_settings_buttons()
        self.reset_OnOff_bt()
        if settings.outs['RunStopLamp']:
            game.action_runstop_lamp(0)
        settings.time_event = True

    def reset_bt_colors(self):
        self.refresh_settings_buttons()
        self.change_timebt_color()
        self.change_scriptbt_color()
        self.change_RSbt_color()

    def change_RSbt_color(self):
        if settings.runstop:
            self.bt_runstop.setStyleSheet('background-color: #00ff00')
        else:
            self.bt_runstop.setStyleSheet('background-color: #ff0000')

    def bt_script1_press(self):
        settings.scripts = 0
        self.change_scriptbt_color()

    def bt_script2_press(self):
        settings.scripts = 1
        self.change_scriptbt_color()

    def bt_script3_press(self):
        settings.scripts = 2
        self.change_scriptbt_color()

    def bt_script4_press(self):
        settings.scripts = 3
        self.change_scriptbt_color()

    def bt_UVlamps_press(self):
        settings.bonuses['UVlamps'] = not settings.bonuses['UVlamps']
        self.refresh_settings_buttons()

    def bt_UVkids_press(self):
        settings.for_kids = not settings.for_kids
        if settings.for_kids:
            settings.UV_activation_time = settings.timebox.t22
        else:
            settings.UV_activation_time = settings.timebox.t21
        self.refresh_settings_buttons()

    def bt_UVsec1_press(self):
        if settings.bonuses['UVlamps']:
            settings.timeUV_bt[0] = not settings.timeUV_bt[0]
            if settings.timeUV_bt[0]:
                settings.bonus_time += settings.timebox.t12
            else:
                settings.bonus_time -= settings.timebox.t12
            self.refresh_settings_buttons()

    def bt_UVsec2_press(self):
        if settings.bonuses['UVlamps']:
            settings.timeUV_bt[1] = not settings.timeUV_bt[1]
            if settings.timeUV_bt[1]:
                settings.bonus_time += settings.timebox.t13
            else:
                settings.bonus_time -= settings.timebox.t13
            self.refresh_settings_buttons()

    def bt_UVsec3_press(self):
        if settings.bonuses['UVlamps']:
            settings.timeUV_bt[2] = not settings.timeUV_bt[2]
            if settings.timeUV_bt[2]:
                settings.bonus_time += settings.timebox.t14
            else:
                settings.bonus_time -= settings.timebox.t14
            self.refresh_settings_buttons()

    def bt_fans_press(self):
        settings.bonuses['fans'] = not settings.bonuses['fans']
        self.refresh_settings_buttons()

    def bt_strobes_press(self):
        settings.bonuses['strobes'] = not settings.bonuses['strobes']
        self.refresh_settings_buttons()

    def bt_settings_press(self):
        settings.bonuses['settings'] = not settings.bonuses['settings']
        if settings.bonuses['settings']:
            self.set_dinamic_OnOff()
        else:
            self.set_static_OnOff()
        self.refresh_settings_buttons()
        self.reset_OnOff_bt()

    def bt_5min_press(self):
        if settings.timer == "05:00":
            self.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.timer.setText("05:00")
            settings.timer = "05:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_8min_press(self):
        if settings.timer == "08:00":
            self.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.timer.setText("08:00")
            settings.timer = "08:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_10min_press(self):
        if settings.timer == "10:00":
            self.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.timer.setText("10:00")
            settings.timer = "10:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_12min_press(self):
        if settings.timer == "12:00":
            self.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.timer.setText("12:00")
            settings.timer = "12:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_15min_press(self):
        if settings.timer == "15:00":
            self.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.timer.setText("15:00")
            settings.timer = "15:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_18min_press(self):
        if settings.timer == "18:00":
            self.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.timer.setText("18:00")
            settings.timer = "18:00"

        self.change_timebt_color()
        self.reset_time()

    def change_timebt_color(self):
        time_list = ['05:00', '08:00', '10:00', '12:00', '15:00', '18:00']
        bt_list = [self.bt_5min, self.bt_8min, self.bt_10min, self.bt_12min, self.bt_15min, self.bt_18min]
        for i in range(len(time_list)):
            if settings.timer == time_list[i]:
                bt_list[i].setStyleSheet('background-color: #ffff00')
            else:
                bt_list[i].setStyleSheet('background-color: #ffffff')

    def change_time(self):
        try:
            time = self.timer.text().split(':')
            settings.time_m = int(time[0])
            settings.time_s = int(time[1])
            if settings.time_m > 18:
                settings.time_m = 18
            if settings.time_s > 59:
                settings.time_s = 59
            if settings.time_m == 18:
                settings.time_s = 0
            if settings.time_m < 5:
                settings.time_m = 5
                settings.time_s = 0
            if settings.time_m < 10:
                m1 = f"0{str(settings.time_m)}"
            else:
                m1 = str(settings.time_m)
            if settings.time_s < 10:
                s1 = f"0{str(settings.time_s)}"
            else:
                s1 = str(settings.time_s)
            settings.time = f"{m1}:{s1}"
        except Exception as e:
            settings.time_m = 10
            settings.time_s = 0
            settings.time = '10:00'

    def reset_time(self):
        self.change_time()
        settings.time_event = True

    def refresh_settings_buttons(self):
        if settings.bonuses['UVlamps']:
            self.bt_UV.setStyleSheet('background-color: #00ff00')
            if settings.timeUV_bt[0]:
                self.bt_1.setStyleSheet('background-color: #ffff00')
            else:
                self.bt_1.setStyleSheet('background-color: #ffffff')
            if settings.timeUV_bt[1]:
                self.bt_2.setStyleSheet('background-color: #ffff00')
            else:
                self.bt_2.setStyleSheet('background-color: #ffffff')
            if settings.timeUV_bt[2]:
                self.bt_3.setStyleSheet('background-color: #ffff00')
            else:
                self.bt_3.setStyleSheet('background-color: #ffffff')
            if settings.for_kids:
                self.bt_children.setStyleSheet('background-color: #ffff00')
            else:
                self.bt_children.setStyleSheet('background-color: #ffffff')
        else:
            self.bt_UV.setStyleSheet('background-color: #ffffff')
            self.bt_1.setStyleSheet('background-color: #ffffff')
            self.bt_2.setStyleSheet('background-color: #ffffff')
            self.bt_3.setStyleSheet('background-color: #ffffff')
            self.bt_children.setStyleSheet('background-color: #ffffff')
            self.bonus_time = 1
        if settings.bonuses['fans']:
            self.bt_fan.setStyleSheet('background-color: #00ff00')
        else:
            self.bt_fan.setStyleSheet('background-color: #ffffff')
        if settings.bonuses['strobes']:
            self.bt_strobe.setStyleSheet('background-color: #00ff00')
        else:
            self.bt_strobe.setStyleSheet('background-color: #ffffff')
        if settings.bonuses['settings']:
            self.bt_diagnostic.setStyleSheet('background-color: #00ff00')
        else:
            self.bt_diagnostic.setStyleSheet('background-color: #ffffff')

    def change_scriptbt_color(self):
        scripts_list = [self.bt_script1, self.bt_script2, self.bt_script3, self.bt_script4]
        for i in range(len(scripts_list)):
            if i == settings.scripts:
                scripts_list[i].setStyleSheet('background-color:#00ff00;')
            else:
                scripts_list[i].setStyleSheet('background-color:#ffffff;')

    def set_dinamic_OnOff(self):
        off_list = [self.bt_start_off, self.bt_shadow_off,
                    self.bt_strobe1_off, self.bt_strobe2_off, self.bt_strobe3_off,
                    self.bt_fan1_off, self.bt_fan2_off, self.bt_fan3_off,self.bt_fan4_off,
                    self.bt_uv1_off, self.bt_uv2_off, self.bt_uv3_off,
                    self.bt_uv4_off, self.bt_uv5_off, self.bt_uv6_off,
                    self.bt_uv7_off, self.bt_uv8_off, self.bt_uv9_off
                    ]
        on_list = [self.bt_start_on, self.bt_shadow_on,
                    self.bt_strobe1_on, self.bt_strobe2_on, self.bt_strobe3_on,
                    self.bt_fan1_on, self.bt_fan2_on, self.bt_fan3_on, self.bt_fan4_on,
                    self.bt_uv1_on, self.bt_uv2_on, self.bt_uv3_on,
                    self.bt_uv4_on, self.bt_uv5_on, self.bt_uv6_on,
                    self.bt_uv7_on, self.bt_uv8_on, self.bt_uv9_on
                    ]
        for bt in off_list:
            bt.setStyleSheet('''
QPushButton {
background-color:#ffffff;
}
QPushButton:disabled {
background-color:#ff0000;
}''')
        for bt in on_list:
            bt.setStyleSheet('''
QPushButton {
background-color:#ffffff;
}
QPushButton:disabled {
background-color:#00ff00;
}''')

    def set_static_OnOff(self):
        settings_list = [settings.outs['RunStopLamp'], settings.outs['ShadowLamp'],
                         settings.outs['Strobes'][0], settings.outs['Strobes'][1], settings.outs['Strobes'][2],
                         settings.outs['Fans'][0], settings.outs['Fans'][1], settings.outs['Fans'][2], settings.outs['Fans'][3],
                         settings.outs['UVlamps'][0], settings.outs['UVlamps'][1], settings.outs['UVlamps'][2],
                         settings.outs['UVlamps'][3], settings.outs['UVlamps'][4], settings.outs['UVlamps'][5],
                         settings.outs['UVlamps'][6], settings.outs['UVlamps'][7], settings.outs['UVlamps'][8],]
        off_list = [self.bt_start_off, self.bt_shadow_off,
                    self.bt_strobe1_off, self.bt_strobe2_off, self.bt_strobe3_off,
                    self.bt_fan1_off, self.bt_fan2_off, self.bt_fan3_off, self.bt_fan4_off,
                    self.bt_uv1_off, self.bt_uv2_off, self.bt_uv3_off,
                    self.bt_uv4_off, self.bt_uv5_off, self.bt_uv6_off,
                    self.bt_uv7_off, self.bt_uv8_off, self.bt_uv9_off
                    ]
        on_list = [self.bt_start_on, self.bt_shadow_on,
                    self.bt_strobe1_on, self.bt_strobe2_on, self.bt_strobe3_on,
                    self.bt_fan1_on, self.bt_fan2_on, self.bt_fan3_on, self.bt_fan4_on,
                    self.bt_uv1_on, self.bt_uv2_on, self.bt_uv3_on,
                    self.bt_uv4_on, self.bt_uv5_on, self.bt_uv6_on,
                    self.bt_uv7_on, self.bt_uv8_on, self.bt_uv9_on
                    ]
        for i in range(len(settings_list)):
            if settings_list[i]:
                off_list[i].setStyleSheet('''
QPushButton {
background-color:#ffffff;
}
QPushButton:disabled {
background-color:#ffffff;
}''')
                on_list[i].setStyleSheet('''
QPushButton {
background-color:#ffffff;
}
QPushButton:disabled {
background-color:#00ff00;
}''')
            else:
                off_list[i].setStyleSheet('''
QPushButton {
background-color:#ffffff;
}
QPushButton:disabled {
background-color:#ff0000;
}''')
                on_list[i].setStyleSheet('''
QPushButton {
background-color:#ffffff;
}
QPushButton:disabled {
background-color:#ffffff;
}''')

    def reset_sensors(self):
        if settings.inputs['runstop']:
            self.sensor_runstop.setStyleSheet("background-color: rgb(117, 123, 127);")
        else:
            self.sensor_runstop.setStyleSheet("background-color: rgb(255, 255, 0);")

        if settings.inputs['fans'][0]:
            self.sensor_1.setStyleSheet("background-color: rgb(117, 123, 127);")
        else:
            self.sensor_1.setStyleSheet("background-color: rgb(255, 255, 0);")

        if settings.inputs['fans'][1]:
            self.sensor_2.setStyleSheet("background-color: rgb(117, 123, 127);")
        else:
            self.sensor_2.setStyleSheet("background-color: rgb(255, 255, 0);")

        if settings.inputs['fans'][2]:
            self.sensor_3.setStyleSheet("background-color: rgb(117, 123, 127);")
        else:
            self.sensor_3.setStyleSheet("background-color: rgb(255, 255, 0);")

        if settings.inputs['fans'][3]:
            self.sensor_4.setStyleSheet("background-color: rgb(117, 123, 127);")
        else:
            self.sensor_4.setStyleSheet("background-color: rgb(255, 255, 0);")

    def reset_OnOff_bt(self):
        settings_list = [settings.outs['RunStopLamp'], settings.outs['ShadowLamp'],
                         settings.outs['Strobes'][0], settings.outs['Strobes'][1], settings.outs['Strobes'][2],
                         settings.outs['Fans'][0], settings.outs['Fans'][1], settings.outs['Fans'][2], settings.outs['Fans'][3],
                         settings.outs['UVlamps'][0], settings.outs['UVlamps'][1], settings.outs['UVlamps'][2],
                         settings.outs['UVlamps'][3], settings.outs['UVlamps'][4], settings.outs['UVlamps'][5],
                         settings.outs['UVlamps'][6], settings.outs['UVlamps'][7], settings.outs['UVlamps'][8],]
        off_list = [self.bt_start_off, self.bt_shadow_off,
                    self.bt_strobe1_off, self.bt_strobe2_off, self.bt_strobe3_off,
                    self.bt_fan1_off, self.bt_fan2_off, self.bt_fan3_off, self.bt_fan4_off,
                    self.bt_uv1_off, self.bt_uv2_off, self.bt_uv3_off,
                    self.bt_uv4_off, self.bt_uv5_off, self.bt_uv6_off,
                    self.bt_uv7_off, self.bt_uv8_off, self.bt_uv9_off
                    ]
        on_list = [self.bt_start_on, self.bt_shadow_on,
                    self.bt_strobe1_on, self.bt_strobe2_on, self.bt_strobe3_on,
                    self.bt_fan1_on, self.bt_fan2_on, self.bt_fan3_on, self.bt_fan4_on,
                    self.bt_uv1_on, self.bt_uv2_on, self.bt_uv3_on,
                    self.bt_uv4_on, self.bt_uv5_on, self.bt_uv6_on,
                    self.bt_uv7_on, self.bt_uv8_on, self.bt_uv9_on
                    ]
        if not settings.bonuses['settings']:
            for i in range(len(settings_list)):
                off_list[i].setDisabled(True)
                on_list[i].setDisabled(True)
        else:
            for i in range(len(settings_list)):
                if settings_list[i]:
                    off_list[i].setDisabled(False)
                    on_list[i].setDisabled(True)
                else:
                    off_list[i].setDisabled(True)
                    on_list[i].setDisabled(False)

    def disabling_buttons(self):
        if settings.runstop:
            self.bt_script1.setDisabled(True)
            self.bt_script2.setDisabled(True)
            self.bt_script3.setDisabled(True)
            self.bt_script4.setDisabled(True)
            self.bt_5min.setDisabled(True)
            self.bt_8min.setDisabled(True)
            self.bt_10min.setDisabled(True)
            self.bt_12min.setDisabled(True)
            self.bt_15min.setDisabled(True)
            self.bt_18min.setDisabled(True)
            self.timer.setDisabled(True)
        else:
            self.bt_script1.setDisabled(False)
            self.bt_script2.setDisabled(False)
            self.bt_script3.setDisabled(True)
            self.bt_script4.setDisabled(True)
            self.bt_5min.setDisabled(False)
            self.bt_8min.setDisabled(False)
            self.bt_10min.setDisabled(False)
            self.bt_12min.setDisabled(False)
            self.bt_15min.setDisabled(False)
            self.bt_18min.setDisabled(False)
            self.timer.setDisabled(False)

    def disabled_settings(self):
        self.bt_UV.setDisabled(False)
        self.bt_1.setDisabled(False)
        self.bt_2.setDisabled(False)
        self.bt_3.setDisabled(False)
        self.bt_children.setDisabled(False)
        self.bt_fan.setDisabled(False)
        self.bt_strobe.setDisabled(False)

if __name__ == "__main__":
    import sys
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
