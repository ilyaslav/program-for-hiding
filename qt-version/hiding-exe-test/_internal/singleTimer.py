import threading

class SingleTimer:
    def __init__(self, callback, delay = None):
        self.delay = delay
        self.callback = callback
        self.timer = None
        self.running = False

    def _run(self):
        self.running = False
        self.callback()

    def start(self):
        if self.running:
            self.stop()

        if self.delay is None:
            self.delay = 0

        self.timer = threading.Timer(self.delay, self._run)
        self.timer.daemon = True
        self.timer.start()
        self.running = True

    def stop(self):
        if self.timer:
            self.timer.cancel()
            self.running = False