import time
from enum import Enum

import settings
from blinker import Blinker
from game import reset_out, play_music, stop_music, thread_wraper
from singleTimer import SingleTimer
from rpiPing import PingRpi


class PingStatus(Enum):
    DO_FULL_PING = "Запуск системы"
    DO_SHORT_PING = "Выполняется проверка связи"
    NOT_READY = "Связь не установлена"
    READY = "Связь установлена"
    SKIP = "Проверка связи отключена"
    WAITING = "Нажмите – Запустить систему"


class Ping:
    def __init__(self):
        self.stop_event = False
        self.display_ping_event = False
        self.ping_event = False
        self.status = PingStatus.NOT_READY
        self.start_button_out = 'r1:y1'
        self.r2_blinked_outs = [
            "r2:y1",
            "r2:y2",
            "r2:y4",
            "r2:y6",
            "r2:y8",
            "r2:y10",
            "r2:y12",
            "r2:y14",
        ]
        self.r2_other_outs = [
            "r2:y3",
            "r2:y5",
            "r2:y7",
            "r2:y9",
            "r2:y11",
            "r2:y13",
        ]
        self.ping_out = 'y38'
        self.ping_input = 'x40'
        self.rpi_2 = "r2"
        self.ping_timout = settings.timebox['t24']
        self.ping_range = int(settings.timebox['t25'])
        # self.ping_range = 3
        self.start_blink_interval = settings.timebox['t26']
        self.r2_blink_interval = settings.timebox['t27']
        self.start_blinker = Blinker(self.blink_start_button, self.start_blink_interval)
        self.r2_blinker = Blinker(self.blink_r2_outs, self.r2_blink_interval)
        self.connection_success_play = SingleTimer(self.play_track_connection_success)
        self.ping_r2_event = SingleTimer(self.ping_r2)

    @thread_wraper
    def start_short_ping(self):
        print(PingStatus.DO_SHORT_PING)
        self.status = PingStatus.DO_SHORT_PING
        self.display_ping_event = True
        self.init_pings()
        for ping_number in range(self.ping_range):
            print(f"{ping_number} {self.ping_range}")
            if self.stop_event:
                if self.status != PingStatus.SKIP:
                    self.status = PingStatus.NOT_READY
                    self.display_ping_event = True
                self.stop_event = False
                return
            time.sleep(self.ping_timout)
            self.calculate_ping()
            if self.check_status():
                self.status = PingStatus.READY
                self.display_ping_event = True
                return
        else:
            self.status = PingStatus.NOT_READY
            self.display_ping_event = True
            return

    @thread_wraper
    def start_full_ping(self):
        self.status = PingStatus.DO_FULL_PING
        self.display_ping_event = True
        self.init_pings()
        for ping_number in range(self.ping_range):
            print(f"{ping_number} {self.ping_range}")
            self.calculate_ping()
            time.sleep(self.ping_timout)
            if self.check_status():
                self.status = PingStatus.READY
                self.display_ping_event = True
                self.connection_success_play.start()
                self.start_blinker.start()
                self.ping_r2_event.start()
                return
        else:
            self.status = PingStatus.NOT_READY
            self.display_ping_event = True
            return

    def skip(self):
        if self.status != PingStatus.SKIP:
            self.status = PingStatus.SKIP
        else:
            self.status = PingStatus.WAITING
        self.display_ping_event = True

    def do_ping_out(self, rpi: PingRpi):
        rpi.ping_status = not rpi.ping_status
        reset_out(f"{rpi.name}:{self.ping_out}", int(rpi.ping_status))
        self.ping_event = True

    def init_pings(self):
        for rpi_name in settings.pings:
            rpi = settings.pings[rpi_name]
            rpi.__init__(rpi_name)
            self.do_ping_out(rpi)

    def calculate_ping(self):
        for rpi_name in settings.pings:
            rpi = settings.pings[rpi_name]
            if not rpi.rpi_status:
                if self.check_input(rpi_name):
                    rpi.ping_number += 1
                else:
                    rpi.ping_number = 0
                if rpi.ping_number == 5:
                    rpi.rpi_status = True
                    self.display_ping_event = True
                    continue
                self.do_ping_out(rpi)

    def check_input(self, rpi_name: str) -> bool:
        return settings.inputs[f"{rpi_name}:{self.ping_input}"] == settings.pings[rpi_name].ping_status

    def check_status(self) -> bool:
        for rpi_name in settings.pings:
            rpi = settings.pings[rpi_name]
            if not rpi.rpi_status:
                return False
        return True

    def blink_r2_outs(self):
        for out in self.r2_blinked_outs:
            settings.outs[out] = not settings.outs[out]
            reset_out(out, settings.outs[out])
        return True

    def reset_r2_blinked_outs(self, status: bool):
        for out in self.r2_blinked_outs:
            settings.outs[out] = status
            reset_out(out, settings.outs[out])

    def reset_r2_other_outs(self, status: bool):
        for out in self.r2_other_outs:
            settings.outs[out] = status
            reset_out(out, settings.outs[out])

    def blink_start_button(self):
        settings.outs[self.start_button_out] = not settings.outs[self.start_button_out]
        reset_out(self.start_button_out, settings.outs[self.start_button_out])

    def play_track_connection_success(self):
        play_music(self.rpi_2, 15)
        time.sleep(3)
        stop_music(self.rpi_2, 15)
        time.sleep(6)
        play_music(self.rpi_2, 15)
        time.sleep(3)
        stop_music(self.rpi_2, 15)
        time.sleep(3)
        play_music(self.rpi_2, 16)

    def ping_r2(self):
        reset_out(f"{self.rpi_2}:y16", 1)
        self.r2_blinker.start()
        time.sleep(8)
        self.reset_r2_blinked_outs(True)
        time.sleep(1)
        self.reset_r2_other_outs(True)
        time.sleep(5)
        self.reset_r2_other_outs(False)
        time.sleep(1)
        self.reset_r2_blinked_outs(True)


if __name__ == "__main__":
    pass
