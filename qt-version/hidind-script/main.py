import time
from functools import partial

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication

import game
import settings
from mainWindow import Ui_MainWindow
from ping import Ping, PingStatus
from blinker import Blinker


class ThreadClass(QThread):
    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
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
    def __init__(self):
        self.thread = ThreadClass(parent=None)
        self.ping = Ping()
        self.ping.start_full_ping()
        self.start_system_btn_blinker = Blinker(self.blink_system_btn, 1)
        self.start_system_btn_color = 'red'

    def setupUi(self, MainWindow):
        super(MyWindow, self).setupUi(MainWindow)
        self.start_worker()
        self.connect_functions()
        self.update_volumes()

    def connect_functions(self):
        self.tab_scripts.get_script1_bt().pressed.connect(self.bt_script1_press)
        self.tab_scripts.get_script2_bt().pressed.connect(self.bt_script2_press)
        # self.tabScripts.get_script3_bt().pressed.connect(self.bt_script3_press)
        # self.tabScripts.get_script4_bt().pressed.connect(self.bt_script4_press)
        # self.tabScripts.get_script5_bt().pressed.connect(self.bt_script5_press)
        self.tab_operator.bt_UV.pressed.connect(self.bt_UVlamps_press)
        self.tab_operator.bt_fan.pressed.connect(self.bt_fans_press)
        self.tab_operator.bt_strobe.pressed.connect(self.bt_strobes_press)
        self.tab_operator.bt_1.pressed.connect(self.bt_UVsec1_press)
        self.tab_operator.bt_2.pressed.connect(self.bt_UVsec2_press)
        self.tab_operator.bt_3.pressed.connect(self.bt_UVsec3_press)
        self.tab_operator.bt_children.pressed.connect(self.bt_UVkids_press)
        self.tab_operator.bt_diagnostic.pressed.connect(self.bt_settings_press)
        self.tab_operator.bt_5min.pressed.connect(self.bt_5min_press)
        self.tab_operator.bt_8min.pressed.connect(self.bt_8min_press)
        self.tab_operator.bt_10min.pressed.connect(self.bt_10min_press)
        self.tab_operator.bt_12min.pressed.connect(self.bt_12min_press)
        self.tab_operator.bt_15min.pressed.connect(self.bt_15min_press)
        self.tab_operator.bt_18min.pressed.connect(self.bt_18min_press)
        self.tab_operator.bt_reset.pressed.connect(self.bt_reset_press)
        self.tab_operator.bt_runstop.pressed.connect(self.bt_RUNSTOP_press)
        self.tab_operator.timer.textEdited.connect(self.change_time)

        self.tab_diagnostic.bt_uv1_off.pressed.connect(partial(game.action_uv1, 0))
        self.tab_diagnostic.bt_uv1_on.pressed.connect(partial(game.action_uv1, 0))
        self.tab_diagnostic.bt_uv2_off.pressed.connect(partial(game.action_uv2, 0))
        self.tab_diagnostic.bt_uv2_on.pressed.connect(partial(game.action_uv2, 0))
        self.tab_diagnostic.bt_uv3_off.pressed.connect(partial(game.action_uv3, 0))
        self.tab_diagnostic.bt_uv3_on.pressed.connect(partial(game.action_uv3, 0))
        self.tab_diagnostic.bt_uv4_off.pressed.connect(partial(game.action_uv4, 0))
        self.tab_diagnostic.bt_uv4_on.pressed.connect(partial(game.action_uv4, 0))
        self.tab_diagnostic.bt_uv5_off.pressed.connect(partial(game.action_uv5, 0))
        self.tab_diagnostic.bt_uv5_on.pressed.connect(partial(game.action_uv5, 0))
        self.tab_diagnostic.bt_uv6_off.pressed.connect(partial(game.action_uv6, 0))
        self.tab_diagnostic.bt_uv6_on.pressed.connect(partial(game.action_uv6, 0))
        self.tab_diagnostic.bt_uv7_off.pressed.connect(partial(game.action_uv7, 0))
        self.tab_diagnostic.bt_uv7_on.pressed.connect(partial(game.action_uv7, 0))
        self.tab_diagnostic.bt_uv8_off.pressed.connect(partial(game.action_uv8, 0))
        self.tab_diagnostic.bt_uv8_on.pressed.connect(partial(game.action_uv8, 0))
        self.tab_diagnostic.bt_uv9_off.pressed.connect(partial(game.action_uv9, 0))
        self.tab_diagnostic.bt_uv9_on.pressed.connect(partial(game.action_uv9, 0))
        self.tab_diagnostic.bt_fan1_off.pressed.connect(partial(game.action_fan1, 0))
        self.tab_diagnostic.bt_fan1_on.pressed.connect(partial(game.action_fan1, 0))
        self.tab_diagnostic.bt_fan2_off.pressed.connect(partial(game.action_fan2, 0))
        self.tab_diagnostic.bt_fan2_on.pressed.connect(partial(game.action_fan2, 0))
        self.tab_diagnostic.bt_fan3_off.pressed.connect(partial(game.action_fan3, 0))
        self.tab_diagnostic.bt_fan3_on.pressed.connect(partial(game.action_fan3, 0))
        self.tab_diagnostic.bt_fan4_off.pressed.connect(partial(game.action_fan4, 0))
        self.tab_diagnostic.bt_fan4_on.pressed.connect(partial(game.action_fan4, 0))
        self.tab_diagnostic.bt_strobe1_off.pressed.connect(partial(game.action_strobe1, 0))
        self.tab_diagnostic.bt_strobe1_on.pressed.connect(partial(game.action_strobe1, 0))
        self.tab_diagnostic.bt_strobe2_off.pressed.connect(partial(game.action_strobe2, 0))
        self.tab_diagnostic.bt_strobe2_on.pressed.connect(partial(game.action_strobe2, 0))
        self.tab_diagnostic.bt_strobe3_off.pressed.connect(partial(game.action_strobe3, 0))
        self.tab_diagnostic.bt_strobe3_on.pressed.connect(partial(game.action_strobe3, 0))
        self.tab_diagnostic.bt_shadow_off.pressed.connect(partial(game.action_shadow_lamp, 0))
        self.tab_diagnostic.bt_shadow_on.pressed.connect(partial(game.action_shadow_lamp, 0))
        self.tab_diagnostic.bt_start_off.pressed.connect(partial(game.action_runstop_lamp, 0))
        self.tab_diagnostic.bt_start_on.pressed.connect(partial(game.action_runstop_lamp, 0))
        self.tab_diagnostic.bt_shadow_box_off.pressed.connect(partial(self.reset_shadow_box, 0))
        self.tab_diagnostic.bt_shadow_box_on.pressed.connect(partial(self.reset_shadow_box, 1))
        self.tab_diagnostic.bt_ping_off.pressed.connect(partial(self.reset_ping_r1, 0))
        self.tab_diagnostic.bt_ping_on.pressed.connect(partial(self.reset_ping_r1, 1))

        self.tab_diagnostic_r2.spot_off.pressed.connect(partial(self.reset_spot, 1))
        self.tab_diagnostic_r2.spot_on.pressed.connect(partial(self.reset_spot, 0))
        self.tab_diagnostic_r2.blinker_off.pressed.connect(partial(self.reset_blinker, 0))
        self.tab_diagnostic_r2.blinker_on.pressed.connect(partial(self.reset_blinker, 1))
        self.tab_diagnostic_r2.animator_start_off.pressed.connect(partial(self.reset_animator_start, 0))
        self.tab_diagnostic_r2.animator_start_on.pressed.connect(partial(self.reset_animator_start, 1))
        self.tab_diagnostic_r2.wardrobe_off.pressed.connect(partial(self.reset_wardrobe, 0))
        self.tab_diagnostic_r2.wardrobe_on.pressed.connect(partial(self.reset_wardrobe, 1))
        self.tab_diagnostic_r2.ping_off.pressed.connect(partial(self.reset_ping_r2, 0))
        self.tab_diagnostic_r2.ping_on.pressed.connect(partial(self.reset_ping_r2, 1))
        self.tab_diagnostic_r2.light1_off.pressed.connect(partial(self.reset_light, 1, 0, 1))
        self.tab_diagnostic_r2.light1_on.pressed.connect(partial(self.reset_light, 0, 0, 1))
        self.tab_diagnostic_r2.light1_blink.pressed.connect(partial(self.reset_light, 1, 1, 1))
        self.tab_diagnostic_r2.light2_off.pressed.connect(partial(self.reset_light, 1, 0, 2))
        self.tab_diagnostic_r2.light2_on.pressed.connect(partial(self.reset_light, 0, 0, 2))
        self.tab_diagnostic_r2.light2_blink.pressed.connect(partial(self.reset_light, 1, 1, 2))
        self.tab_diagnostic_r2.light3_off.pressed.connect(partial(self.reset_light, 1, 0, 3))
        self.tab_diagnostic_r2.light3_on.pressed.connect(partial(self.reset_light, 0, 0, 3))
        self.tab_diagnostic_r2.light3_blink.pressed.connect(partial(self.reset_light, 1, 1, 3))
        self.tab_diagnostic_r2.light4_off.pressed.connect(partial(self.reset_light, 1, 0, 4))
        self.tab_diagnostic_r2.light4_on.pressed.connect(partial(self.reset_light, 0, 0, 4))
        self.tab_diagnostic_r2.light4_blink.pressed.connect(partial(self.reset_light, 1, 1, 4))
        self.tab_diagnostic_r2.light5_off.pressed.connect(partial(self.reset_light, 1, 0, 5))
        self.tab_diagnostic_r2.light5_on.pressed.connect(partial(self.reset_light, 0, 0, 5))
        self.tab_diagnostic_r2.light5_blink.pressed.connect(partial(self.reset_light, 1, 1, 5))
        self.tab_diagnostic_r2.light6_off.pressed.connect(partial(self.reset_light, 1, 0, 6))
        self.tab_diagnostic_r2.light6_on.pressed.connect(partial(self.reset_light, 0, 0, 6))
        self.tab_diagnostic_r2.light6_blink.pressed.connect(partial(self.reset_light, 1, 1, 6))
        self.tab_diagnostic_r2.light7_off.pressed.connect(partial(self.reset_light, 1, 0, 7))
        self.tab_diagnostic_r2.light7_on.pressed.connect(partial(self.reset_light, 0, 0, 7))
        self.tab_diagnostic_r2.light7_blink.pressed.connect(partial(self.reset_light, 1, 1, 7))

        self.tab_diagnostic_r3.mask_on.pressed.connect(partial(self.reset_mask, 1))
        self.tab_diagnostic_r3.mask_off.pressed.connect(partial(self.reset_mask, 0))
        self.tab_diagnostic_r3.light_on.pressed.connect(partial(self.reset_light_r3, 1))
        self.tab_diagnostic_r3.light_off.pressed.connect(partial(self.reset_light_r3, 0))
        self.tab_diagnostic_r3.ping_on.pressed.connect(partial(self.reset_ping_r3, 1))
        self.tab_diagnostic_r3.ping_off.pressed.connect(partial(self.reset_ping_r3, 0))

        self.tab_system.start_btn.pressed.connect(self.bt_start_system_press)
        self.tab_system.stop_btn.pressed.connect(self.bt_stop_system_press)
        self.tab_system.check_btn.pressed.connect(self.bt_connection_check_press)
        self.tab_system.skip_btn.pressed.connect(self.bt_skipping_press)
        self.tab_system.get_slider_rsb1().sliderReleased.connect(self.release_volume_rsb1)
        self.tab_system.get_slider_rsb2().sliderReleased.connect(self.release_volume_rsb2)
        self.tab_system.get_slider_rsb3().sliderReleased.connect(self.release_volume_rsb3)
        self.tab_system.get_slider_rsb1().sliderMoved.connect(self.change_volume_rsb1)
        self.tab_system.get_slider_rsb2().sliderMoved.connect(self.change_volume_rsb2)
        self.tab_system.get_slider_rsb3().sliderMoved.connect(self.change_volume_rsb3)
        self.tab_system.get_line_edit_rsb1().textEdited.connect(self.edit_volume_rsb1)
        self.tab_system.get_line_edit_rsb2().textEdited.connect(self.edit_volume_rsb2)
        self.tab_system.get_line_edit_rsb3().textEdited.connect(self.edit_volume_rsb3)

    def start_worker(self):
        self.thread.start()
        self.thread.any_signal.connect(self.main_loop)

    def stop_worker(self):
        self.thread.stop()

    def main_loop(self):
        self.display_ping_event()
        self.ping_event()
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
            self.tab_operator.timer.setText(settings.time)

        if settings.end_timer_event:
            settings.end_timer_event = False
            self.reset_time()
            self.disabling_buttons()
            self.reset_bt_colors()
            self.ping.start_blinker.start()

        self.reset_system_tab()

    def reset_shadow_box(self, value = 0):
        game.reset_out('r1:y19', value)
        self.reset_OnOff_bt()

    def reset_ping_r1(self, value = 0):
        game.reset_out('r1:y38', value)
        self.reset_OnOff_bt()

    def reset_spot(self, value = 0):
        game.reset_out('r2:y1', value)
        self.reset_OnOff_bt()

    def reset_blinker(self, value = 0):
        game.reset_out('r2:y16', value)
        self.reset_OnOff_bt()

    def reset_animator_start(self, value = 0):
        game.reset_out('r2:y17', value)
        self.reset_OnOff_bt()

    def reset_ping_r2(self, value = 0):
        game.reset_out('r2:y38', value)
        self.reset_OnOff_bt()

    def reset_wardrobe(self, value = 0):
        game.reset_out('r2:y15', value)
        self.reset_OnOff_bt()

    def reset_light(self, value1: int, value2: int, order: int):
        order_map = {
            1: {'out1_name': 'r2:y2', 'out2_name': 'r2:y3'},
            2: {'out1_name': 'r2:y4', 'out2_name': 'r2:y5'},
            3: {'out1_name': 'r2:y6', 'out2_name': 'r2:y7'},
            4: {'out1_name': 'r2:y8', 'out2_name': 'r2:y9'},
            5: {'out1_name': 'r2:y10', 'out2_name': 'r2:y11'},
            6: {'out1_name': 'r2:y12', 'out2_name': 'r2:y13'},
            7: {'out1_name': 'r2:y14', 'out2_name': 'r2:y18'},
        }
        game.reset_light_outs(order_map[order]['out1_name'], value1, order_map[order]['out2_name'], value2)
        self.reset_OnOff_bt()

    def reset_mask(self, value = 0):
        game.reset_out('r3:y1', value)
        self.reset_OnOff_bt()

    def reset_light_r3(self, value = 0):
        game.reset_out('r3:y2', value)
        self.reset_OnOff_bt()

    def reset_ping_r3(self, value = 0):
        game.reset_out('r3:y38', value)
        self.reset_OnOff_bt()

    def bt_start_system_press(self):
        self.ping.start_full_ping()

    def bt_connection_check_press(self):
        self.ping.start_short_ping()

    def bt_skipping_press(self):
        if self.ping.status == PingStatus.DO_SHORT_PING:
            self.ping.stop_event = True
        self.ping.skip()

    def ping_event(self):
        if self.ping.ping_event:
            self.ping.ping_event = False
            for ping_name in settings.pings:
                match ping_name:
                    case 'r1':
                        indicator = self.tab_system.get_indicator_rsb1()
                    case 'r2':
                        indicator = self.tab_system.get_indicator_rsb2()
                    case 'r3':
                        indicator = self.tab_system.get_indicator_rsb3()

                if settings.pings[ping_name].rpi_status:
                    indicator.setColor(QColor("green"))
                else:
                    if settings.pings[ping_name].ping_status:
                        indicator.setColor(QColor("white"))
                    else:
                        indicator.setColor(QColor("red"))

    def set_red_indicators_color(self):
        for ping_name in settings.pings:
            match ping_name:
                case 'r1':
                    indicator = self.tab_system.get_indicator_rsb1()
                case 'r2':
                    indicator = self.tab_system.get_indicator_rsb2()
                case 'r3':
                    indicator = self.tab_system.get_indicator_rsb3()

            if not settings.pings[ping_name].rpi_status:
                indicator.setColor(QColor("red"))

    def set_ping_scripts(self):
        actions = {
            (False, False, False): lambda: self.set_ping_script1(),
            (True, False, False): lambda: self.set_ping_script2(),
            (False, True, False): lambda: self.set_ping_script3(),
            (False, False, True): lambda: self.set_ping_script4(),
            (True, True, False): lambda: self.set_ping_script5(),
            (True, False, True): lambda: self.set_ping_script6(),
            (False, True, True): lambda: self.set_ping_script7(),
            (True, True, True): lambda: self.set_ping_script8()
        }
        result = (settings.pings['r1'].rpi_status, settings.pings['r2'].rpi_status, settings.pings['r3'].rpi_status)
        actions[result]()

    def set_ping_script1(self):
        self.tab_scripts.get_script1_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №1")
        self.tab_scripts.get_script2_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №2")
        self.tab_scripts.get_script3_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №3")
        self.tab_scripts.get_script4_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №4")
        self.tab_scripts.get_script1_label().setStyleSheet("background-color: red; font-size: 13px; padding: 2px;")
        self.tab_scripts.get_script2_label().setStyleSheet("background-color: red; font-size: 13px; padding: 2px;")
        self.tab_scripts.get_script3_label().setStyleSheet("background-color: red; font-size: 13px; padding: 2px;")
        self.tab_scripts.get_script4_label().setStyleSheet("background-color: red; font-size: 13px; padding: 2px;")

    def set_ping_script2(self):
        self.tab_scripts.get_script1_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script2_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script3_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №9")
        self.tab_scripts.get_script4_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №10")
        self.tab_scripts.get_script1_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script2_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script3_label().setStyleSheet("background-color: orange;")
        self.tab_scripts.get_script4_label().setStyleSheet("background-color: orange;")

    def set_ping_script3(self):
        self.tab_scripts.get_script1_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №1")
        self.tab_scripts.get_script2_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №2")
        self.tab_scripts.get_script3_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №11")
        self.tab_scripts.get_script4_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №12")
        self.tab_scripts.get_script1_label().setStyleSheet("background-color: red;")
        self.tab_scripts.get_script2_label().setStyleSheet("background-color: red;")
        self.tab_scripts.get_script3_label().setStyleSheet("background-color: orange;")
        self.tab_scripts.get_script4_label().setStyleSheet("background-color: orange;")

    def set_ping_script4(self):
        self.tab_scripts.get_script1_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №1")
        self.tab_scripts.get_script2_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №2")
        self.tab_scripts.get_script3_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №13")
        self.tab_scripts.get_script4_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №14")
        self.tab_scripts.get_script1_label().setStyleSheet("background-color: red;")
        self.tab_scripts.get_script2_label().setStyleSheet("background-color: red;")
        self.tab_scripts.get_script3_label().setStyleSheet("background-color: orange;")
        self.tab_scripts.get_script4_label().setStyleSheet("background-color: orange;")

    def set_ping_script5(self):
        self.tab_scripts.get_script1_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script2_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script3_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №7")
        self.tab_scripts.get_script4_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №8")
        self.tab_scripts.get_script1_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script2_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script3_label().setStyleSheet("background-color: orange;")
        self.tab_scripts.get_script4_label().setStyleSheet("background-color: orange;")

    def set_ping_script6(self):
        self.tab_scripts.get_script1_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script2_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script3_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №5")
        self.tab_scripts.get_script4_label().setText("Сценарий доступен с ограничениями.\nСм. «Ошибка №6")
        self.tab_scripts.get_script1_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script2_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script3_label().setStyleSheet("background-color: orange;")
        self.tab_scripts.get_script4_label().setStyleSheet("background-color: orange;")

    def set_ping_script7(self):
        self.tab_scripts.get_script1_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №1")
        self.tab_scripts.get_script2_label().setText("Сценарий НЕ доступен. Есть вариации\nСм. «Ошибка №2")
        self.tab_scripts.get_script3_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script4_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script1_label().setStyleSheet("background-color: red;")
        self.tab_scripts.get_script2_label().setStyleSheet("background-color: red;")
        self.tab_scripts.get_script3_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script4_label().setStyleSheet("background-color: white;")

    def set_ping_script8(self):
        self.tab_scripts.get_script1_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script2_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script3_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script4_label().setText("\nСценарий доступен")
        self.tab_scripts.get_script1_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script2_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script3_label().setStyleSheet("background-color: white;")
        self.tab_scripts.get_script4_label().setStyleSheet("background-color: white;")

    def display_ping_event(self):
        if self.ping.display_ping_event:
            self.ping.display_ping_event = False
            self.display_rpi_statuses()
            self.tab_system.status_label.setText(self.ping.status.value)
            match self.ping.status:
                case PingStatus.DO_FULL_PING:
                    self.start_system_btn_blinker.stop()
                    self.tabWidget.setTabEnabled(1, False)
                    self.tabWidget.setTabEnabled(2, False)
                    settings.bonuses['settings'] = False
                    self.refresh_settings_buttons()
                    self.tab_system.start_btn.setDisabled(True)
                    self.tab_system.stop_btn.setDisabled(True)
                    self.tab_system.check_btn.setDisabled(True)
                    self.tab_system.skip_btn.setDisabled(True)
                case PingStatus.DO_SHORT_PING:
                    self.start_system_btn_blinker.stop()
                    self.tab_system.start_btn.setDisabled(True)
                    self.tab_system.check_btn.setDisabled(True)
                case PingStatus.READY:
                    self.start_system_btn_blinker.stop()
                    self.tab_system.start_btn.setStyleSheet(
                        "font-size: 14px; font-weight: bold; padding: 6px; min-height: 40px; background-color: green;")
                    self.set_ping_scripts()
                    self.tabWidget.setTabEnabled(1, True)
                    self.tabWidget.setTabEnabled(2, True)
                    self.tab_system.start_btn.setDisabled(True)
                    self.tab_system.stop_btn.setDisabled(False)
                    self.tab_system.check_btn.setDisabled(False)
                    self.tab_system.skip_btn.setDisabled(True)
                case PingStatus.NOT_READY:
                    self.set_red_indicators_color()
                    self.set_ping_scripts()
                    self.start_system_btn_blinker.start()
                    self.tab_system.skip_btn.setStyleSheet(
                        "font-size: 14px; font-weight: bold; padding: 6px; min-height: 40px; background-color: yellow;")
                    self.tab_system.start_btn.setDisabled(False)
                    self.tab_system.stop_btn.setDisabled(False)
                    self.tab_system.check_btn.setDisabled(False)
                    self.tab_system.skip_btn.setDisabled(False)
                case PingStatus.SKIP:
                    self.tabWidget.setTabEnabled(1, True)
                    self.tabWidget.setTabEnabled(2, True)
                    self.start_system_btn_blinker.stop()
                    self.tab_system.skip_btn.setStyleSheet(
                        "font-size: 14px; font-weight: bold; padding: 6px; min-height: 40px; background-color: green;")
                    self.tab_system.start_btn.setDisabled(True)
                    self.tab_system.stop_btn.setDisabled(True)
                    self.tab_system.check_btn.setDisabled(False)
                    self.tab_system.skip_btn.setDisabled(False)
                case PingStatus.WAITING:
                    self.tabWidget.setTabEnabled(1, False)
                    self.tabWidget.setTabEnabled(2, False)
                    self.start_system_btn_blinker.start()
                    self.tab_system.skip_btn.setStyleSheet(
                        "font-size: 14px; font-weight: bold; padding: 6px; min-height: 40px; background-color: red;")
                    self.tab_system.start_btn.setDisabled(True)
                    self.tab_system.stop_btn.setDisabled(False)
                    self.tab_system.check_btn.setDisabled(False)
                    self.tab_system.skip_btn.setDisabled(True)

    def display_rpi_statuses(self):
        if settings.pings['r1'].rpi_status:
            self.tab_system.get_indicator_rsb1().setColor(QColor("green"))
        else:
            self.tab_system.get_indicator_rsb1().setColor(QColor("red"))
        if settings.pings['r2'].rpi_status:
            self.tab_system.get_indicator_rsb2().setColor(QColor("green"))
        else:
            self.tab_system.get_indicator_rsb2().setColor(QColor("red"))
        if settings.pings['r3'].rpi_status:
            self.tab_system.get_indicator_rsb3().setColor(QColor("green"))
        else:
            self.tab_system.get_indicator_rsb3().setColor(QColor("red"))

    def change_volume_rsb1(self):
        self.tab_system.get_line_edit_rsb1().setText(str(self.tab_system.get_slider_rsb1().value()))

    def change_volume_rsb2(self):
        self.tab_system.get_line_edit_rsb2().setText(str(self.tab_system.get_slider_rsb2().value()))

    def change_volume_rsb3(self):
        self.tab_system.get_line_edit_rsb3().setText(str(self.tab_system.get_slider_rsb3().value()))

    def validate_edited_volume(self, line_edit):
        if line_edit.text() == '':
            line_edit.setText("0")
        value = int(line_edit.text())
        if value > 100:
            line_edit.setText("100")
            value = 100
        return value

    def edit_volume_rsb1(self):
        value = self.validate_edited_volume(self.tab_system.get_line_edit_rsb1())
        self.tab_system.get_slider_rsb1().setValue(value)
        settings.volumes['r1'] = value
        self.update_volumes()

    def edit_volume_rsb2(self):
        value = self.validate_edited_volume(self.tab_system.get_line_edit_rsb2())
        self.tab_system.get_slider_rsb2().setValue(value)
        settings.volumes['r2'] = value
        self.update_volumes()

    def edit_volume_rsb3(self):
        value = self.validate_edited_volume(self.tab_system.get_line_edit_rsb3())
        self.tab_system.get_slider_rsb3().setValue(value)
        settings.volumes['r3'] = value
        self.update_volumes()

    def release_volume_rsb1(self):
        settings.volumes['r1'] = self.tab_system.get_slider_rsb1().value()
        self.update_volumes()

    def release_volume_rsb2(self):
        settings.volumes['r2'] = self.tab_system.get_slider_rsb2().value()
        self.update_volumes()

    def release_volume_rsb3(self):
        settings.volumes['r3'] = self.tab_system.get_slider_rsb3().value()
        self.update_volumes()

    def blink_system_btn(self):
        if self.start_system_btn_color == 'red':
            self.start_system_btn_color = 'white'
        else:
            self.start_system_btn_color = 'red'
        self.tab_system.start_btn.setStyleSheet(
            f"font-size: 14px; font-weight: bold; padding: 6px; min-height: 40px; background-color: {self.start_system_btn_color};")

    def bt_RUNSTOP_press(self):
        game.stop_events()
        if settings.outs['r1:y2']:
            game.action_shadow_lamp(0)

        if settings.runstop:
            game.play_end_music()
            self.ping.start_blinker.start()
        else:
            self.ping.stop_events()
        game.set_standart_outs()
        game.action_runstop_lamp(0)

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

    def bt_stop_system_press(self):
        self.tab_system.start_btn.setDisabled(False)
        self.bt_reset_press()
        self.ping.start_blinker.stop()
        self.ping.play_stop_music()

    def bt_reset_press(self):
        game.stop_events()
        self.ping.stop_events()
        game.set_standard_settings()
        game.off_all()
        self.reset_bt_colors()
        self.disabling_buttons()
        self.disabled_settings()
        self.refresh_settings_buttons()
        self.reset_OnOff_bt()
        if settings.outs['r1:y1']:
            game.action_runstop_lamp(0)
        settings.time_event = True
        if self.ping.status == PingStatus.DO_SHORT_PING:
            self.ping.stop_event = True
        self.ping.start_blinker.start()

    def reset_bt_colors(self):
        self.refresh_settings_buttons()
        self.change_timebt_color()
        self.change_scriptbt_color()
        self.change_RSbt_color()

    def change_RSbt_color(self):
        if settings.runstop:
            self.tab_operator.bt_runstop.setStyleSheet('background-color: #00ff00')
        else:
            self.tab_operator.bt_runstop.setStyleSheet('background-color: #ff0000')

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

    def bt_script5_press(self):
        settings.scripts = 4
        self.change_scriptbt_color()

    def bt_UVlamps_press(self):
        settings.bonuses['UVlamps'] = not settings.bonuses['UVlamps']
        self.refresh_settings_buttons()

    def bt_UVkids_press(self):
        settings.for_kids = not settings.for_kids
        if settings.for_kids:
            settings.UV_activation_time = settings.timebox['t43']
        else:
            settings.UV_activation_time = settings.timebox['t42']
        self.refresh_settings_buttons()

    def bt_UVsec1_press(self):
        if settings.bonuses['UVlamps']:
            settings.timeUV_bt[0] = not settings.timeUV_bt[0]
            if settings.timeUV_bt[0]:
                settings.bonus_time += settings.timebox['t12']
            else:
                settings.bonus_time -= settings.timebox['t12']
            self.refresh_settings_buttons()

    def bt_UVsec2_press(self):
        if settings.bonuses['UVlamps']:
            settings.timeUV_bt[1] = not settings.timeUV_bt[1]
            if settings.timeUV_bt[1]:
                settings.bonus_time += settings.timebox['t13']
            else:
                settings.bonus_time -= settings.timebox['t13']
            self.refresh_settings_buttons()

    def bt_UVsec3_press(self):
        if settings.bonuses['UVlamps']:
            settings.timeUV_bt[2] = not settings.timeUV_bt[2]
            if settings.timeUV_bt[2]:
                settings.bonus_time += settings.timebox['t14']
            else:
                settings.bonus_time -= settings.timebox['t14']
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
            self.tab_operator.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.tab_operator.timer.setText("05:00")
            settings.timer = "05:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_8min_press(self):
        if settings.timer == "08:00":
            self.tab_operator.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.tab_operator.timer.setText("08:00")
            settings.timer = "08:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_10min_press(self):
        if settings.timer == "10:00":
            self.tab_operator.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.tab_operator.timer.setText("10:00")
            settings.timer = "10:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_12min_press(self):
        if settings.timer == "12:00":
            self.tab_operator.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.tab_operator.timer.setText("12:00")
            settings.timer = "12:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_15min_press(self):
        if settings.timer == "15:00":
            self.tab_operator.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.tab_operator.timer.setText("15:00")
            settings.timer = "15:00"

        self.change_timebt_color()
        self.reset_time()

    def bt_18min_press(self):
        if settings.timer == "18:00":
            self.tab_operator.timer.setText("00:00")
            settings.timer = "0"
        else:
            self.tab_operator.timer.setText("18:00")
            settings.timer = "18:00"

        self.change_timebt_color()
        self.reset_time()

    def change_timebt_color(self):
        time_list = ['05:00', '08:00', '10:00', '12:00', '15:00', '18:00']
        bt_list = [self.tab_operator.bt_5min, self.tab_operator.bt_8min, self.tab_operator.bt_10min,
                   self.tab_operator.bt_12min, self.tab_operator.bt_15min, self.tab_operator.bt_18min]
        for i in range(len(time_list)):
            if settings.timer == time_list[i]:
                bt_list[i].setStyleSheet('background-color: #ffff00')
            else:
                bt_list[i].setStyleSheet('background-color: #ffffff')

    def change_time(self):
        try:
            time = self.tab_operator.timer.text().split(':')
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
            self.tab_operator.bt_UV.setStyleSheet('background-color: #00ff00')
            if settings.timeUV_bt[0]:
                self.tab_operator.bt_1.setStyleSheet('background-color: #ffff00')
            else:
                self.tab_operator.bt_1.setStyleSheet('background-color: #ffffff')
            if settings.timeUV_bt[1]:
                self.tab_operator.bt_2.setStyleSheet('background-color: #ffff00')
            else:
                self.tab_operator.bt_2.setStyleSheet('background-color: #ffffff')
            if settings.timeUV_bt[2]:
                self.tab_operator.bt_3.setStyleSheet('background-color: #ffff00')
            else:
                self.tab_operator.bt_3.setStyleSheet('background-color: #ffffff')
            if settings.for_kids:
                self.tab_operator.bt_children.setStyleSheet('background-color: #ffff00')
            else:
                self.tab_operator.bt_children.setStyleSheet('background-color: #ffffff')
        else:
            self.tab_operator.bt_UV.setStyleSheet('background-color: #ffffff')
            self.tab_operator.bt_1.setStyleSheet('background-color: #ffffff')
            self.tab_operator.bt_2.setStyleSheet('background-color: #ffffff')
            self.tab_operator.bt_3.setStyleSheet('background-color: #ffffff')
            self.tab_operator.bt_children.setStyleSheet('background-color: #ffffff')
            self.bonus_time = 1
        if settings.bonuses['fans']:
            self.tab_operator.bt_fan.setStyleSheet('background-color: #00ff00')
        else:
            self.tab_operator.bt_fan.setStyleSheet('background-color: #ffffff')
        if settings.bonuses['strobes']:
            self.tab_operator.bt_strobe.setStyleSheet('background-color: #00ff00')
        else:
            self.tab_operator.bt_strobe.setStyleSheet('background-color: #ffffff')
        if settings.bonuses['settings']:
            self.tab_operator.bt_diagnostic.setStyleSheet('background-color: #00ff00')
        else:
            self.tab_operator.bt_diagnostic.setStyleSheet('background-color: #ffffff')

    def change_scriptbt_color(self):
        scripts_list = [self.tab_scripts.get_script1_bt(), self.tab_scripts.get_script2_bt(),
                        self.tab_scripts.get_script3_bt(), self.tab_scripts.get_script4_bt(),
                        self.tab_scripts.get_script5_bt()]
        for i in range(len(scripts_list)):
            if i == settings.scripts:
                scripts_list[i].setStyleSheet('background-color:#00ff00;')
            else:
                scripts_list[i].setStyleSheet('background-color:#ffffff;')

    def set_dinamic_OnOff(self):
        # Стили для кнопок
        style_off_active = '''
            QPushButton {
                background-color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #ff0000;
            }'''

        style_on_active = '''
            QPushButton {
                background-color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #00ff00;
            }'''

        # Стили для blink кнопок
        style_blink_active = '''
            QPushButton {
                background-color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #ffff00;
            }'''

        for config in settings.button_config:
            tab_widget = getattr(self, config['tab'])
            off_btn, on_btn, blink_btn = config['buttons']
            off_button = getattr(tab_widget, off_btn)
            on_button = getattr(tab_widget, on_btn)

            if config['logic'] == 'standard':
                # Для стандартных кнопок устанавливаем оба стиля
                off_button.setStyleSheet(style_off_active)
                on_button.setStyleSheet(style_on_active)

            elif config['logic'] == 'special':
                # Для special кнопок добавляем blink стиль
                blink_button = getattr(tab_widget, blink_btn)
                off_button.setStyleSheet(style_off_active)
                on_button.setStyleSheet(style_on_active)
                blink_button.setStyleSheet(style_blink_active)

    def set_static_OnOff(self):
        # Стили для кнопок
        style_enabled = '''
            QPushButton {
                background-color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #ffffff;
            }'''

        style_off_active = '''
            QPushButton {
                background-color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #ff0000;
            }'''

        style_on_active = '''
            QPushButton {
                background-color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #00ff00;
            }'''

        # Стили для blink кнопок
        style_blink_active = '''
            QPushButton {
                background-color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #ffff00;
            }'''

        for config in settings.button_config:
            if config['logic'] == 'standard':  # Пропускаем special кнопки
                tab_widget = getattr(self, config['tab'])
                off_btn, on_btn, _ = config['buttons']
                off_button = getattr(tab_widget, off_btn)
                on_button = getattr(tab_widget, on_btn)

                is_active = settings.outs[config['outputs'][0]] if not config['inverted'] else not settings.outs[config['outputs'][0]]

                if is_active:
                    # Включено - красный на OFF, белый на ON
                    off_button.setStyleSheet(style_enabled)
                    on_button.setStyleSheet(style_on_active)
                else:
                    # Выключено - белый на OFF, зеленый на ON
                    off_button.setStyleSheet(style_off_active)
                    on_button.setStyleSheet(style_enabled)
            elif config['logic'] == 'special':
                tab_widget = getattr(self, config['tab'])
                off_btn, on_btn, blink_btn = config['buttons']
                off_button = getattr(tab_widget, off_btn)
                on_button = getattr(tab_widget, on_btn)
                blink_button = getattr(tab_widget, blink_btn)

                key1, key2 = config['outputs']
                val1, val2 = settings.outs[key1], settings.outs[key2]

                if not val1 and not val2:  # on
                    off_button.setStyleSheet(style_enabled)
                    on_button.setStyleSheet(style_on_active)
                    blink_button.setStyleSheet(style_enabled)
                elif val1 and not val2:  # off
                    off_button.setStyleSheet(style_off_active)
                    on_button.setStyleSheet(style_enabled)
                    blink_button.setStyleSheet(style_enabled)
                elif val1 and val2:  # blink
                    off_button.setStyleSheet(style_enabled)
                    on_button.setStyleSheet(style_enabled)
                    blink_button.setStyleSheet(style_blink_active)

    def reset_sensors(self):
        style_off = "background-color: rgb(117, 123, 127);"
        style_on = "background-color: rgb(255, 255, 0);"
        sensor_mapping = [
            ('r1:x1', 'tab_diagnostic', 'sensor_runstop', False),
            ('r1:x2', 'tab_diagnostic', 'sensor_1', False),
            ('r1:x3', 'tab_diagnostic', 'sensor_2', False),
            ('r1:x4', 'tab_diagnostic', 'sensor_3', False),
            ('r1:x5', 'tab_diagnostic', 'sensor_4', False),
            ('r1:x40', 'tab_diagnostic', 'sensor_5', True),
            ('r2:x1', 'tab_diagnostic_r2', 'sensor_door', False),
            ('r2:x40', 'tab_diagnostic_r2', 'ping_input', False),
            ('r3:x1', 'tab_diagnostic_r3', 'animator_input', False),
            ('r3:x2', 'tab_diagnostic_r3', 'light_input', False),
            ('r3:x40', 'tab_diagnostic_r3', 'ping_input', False),
        ]

        for input_key, tab_name, sensor_name, inverted in sensor_mapping:
            tab_widget = getattr(self, tab_name)
            sensor_widget = getattr(tab_widget, sensor_name)
            input_value = settings.inputs[input_key]
            if inverted:
                input_value = not input_value
            sensor_widget.setStyleSheet(style_on if input_value else style_off)


    def reset_OnOff_bt(self):
        for config in settings.button_config:
            tab_widget = getattr(self, config['tab'])
            off_btn, on_btn, blink_btn = config['buttons']
            off_button = getattr(tab_widget, off_btn)
            on_button = getattr(tab_widget, on_btn)
            
            if not settings.bonuses['settings']:
                off_button.setDisabled(True)
                on_button.setDisabled(True)
                if blink_btn:
                    getattr(tab_widget, blink_btn).setDisabled(True)
            else:
                if config['logic'] == 'standard':
                    is_active = settings.outs[config['outputs'][0]] if not config['inverted'] else not settings.outs[config['outputs'][0]]
                    off_button.setDisabled(not is_active)
                    on_button.setDisabled(is_active)
                    
                elif config['logic'] == 'special':
                    key1, key2 = config['outputs']
                    val1, val2 = settings.outs[key1], settings.outs[key2]
                    blink_button = getattr(tab_widget, blink_btn)
                    
                    # on: False, False
                    # off: True, False  
                    # blink: True, True
                    off_button.setDisabled(val1 and not val2)
                    on_button.setDisabled(not val1 and not val2)
                    blink_button.setDisabled(val1 and val2)

    def disabling_buttons(self):
        if settings.runstop:
            self.tab_scripts.get_script1_bt().setDisabled(True)
            self.tab_scripts.get_script2_bt().setDisabled(True)
            self.tab_scripts.get_script3_bt().setDisabled(True)
            self.tab_scripts.get_script4_bt().setDisabled(True)
            self.tab_scripts.get_script5_bt().setDisabled(True)
            self.tab_operator.bt_5min.setDisabled(True)
            self.tab_operator.bt_8min.setDisabled(True)
            self.tab_operator.bt_10min.setDisabled(True)
            self.tab_operator.bt_12min.setDisabled(True)
            self.tab_operator.bt_15min.setDisabled(True)
            self.tab_operator.bt_18min.setDisabled(True)
            self.tab_operator.timer.setDisabled(True)
        else:
            self.tab_scripts.get_script1_bt().setDisabled(False)
            self.tab_scripts.get_script2_bt().setDisabled(False)
            self.tab_scripts.get_script3_bt().setDisabled(True)
            self.tab_scripts.get_script4_bt().setDisabled(True)
            self.tab_scripts.get_script5_bt().setDisabled(True)
            self.tab_operator.bt_5min.setDisabled(False)
            self.tab_operator.bt_8min.setDisabled(False)
            self.tab_operator.bt_10min.setDisabled(False)
            self.tab_operator.bt_12min.setDisabled(False)
            self.tab_operator.bt_15min.setDisabled(False)
            self.tab_operator.bt_18min.setDisabled(False)
            self.tab_operator.timer.setDisabled(False)

    def disabled_settings(self):
        self.tab_operator.bt_UV.setDisabled(False)
        self.tab_operator.bt_1.setDisabled(False)
        self.tab_operator.bt_2.setDisabled(False)
        self.tab_operator.bt_3.setDisabled(False)
        self.tab_operator.bt_children.setDisabled(False)
        self.tab_operator.bt_fan.setDisabled(False)
        self.tab_operator.bt_strobe.setDisabled(False)

    def reset_system_tab(self):
        pass

    def update_volumes(self):
        self.tab_system.get_slider_rsb1().setValue(settings.volumes['r1'])
        self.tab_system.get_slider_rsb2().setValue(settings.volumes['r2'])
        self.tab_system.get_slider_rsb3().setValue(settings.volumes['r3'])
        self.tab_system.get_line_edit_rsb1().setText(str(settings.volumes['r1']))
        self.tab_system.get_line_edit_rsb2().setText(str(settings.volumes['r2']))
        self.tab_system.get_line_edit_rsb3().setText(str(settings.volumes['r3']))

        for rpi_name in settings.volumes:
            game.change_volume(rpi_name, settings.volumes[rpi_name])


if __name__ == "__main__":
    import sys

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setFixedSize(1126, 627)
    ui = MyWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
