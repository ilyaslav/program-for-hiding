import threading
import time

class Blinker:
    def __init__(self, method, interval : float, total_time = None):
        self.total_time = total_time
        self.interval = float(interval)
        self.start_time = None
        self.timer = None
        self.running = False
        self.method = method

    def _blink(self):
        if not self.running:
            return

        elapsed = time.time() - self.start_time
        if self.total_time and elapsed >= self.total_time:
            self.running = False
            return

        self.method()
        self.timer = threading.Timer(self.interval, self._blink)
        self.timer.daemon = True
        self.timer.start()

    def start(self):
        if self.running:
            return

        self.running = True
        self.start_time = time.time()
        self._blink()

    def stop(self):
        if self.timer:
            self.timer.cancel()
        self.running = False