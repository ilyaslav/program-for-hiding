import RPi.GPIO as GPIO
import time

class PiHandler:
    def __init__(self):
        self.initGPIO()
        self.inputs = {
            'x1': [GPIO.input(7), 7],
            'x2': [GPIO.input(11), 11],
            'x40': [GPIO.input(40), 40],
        }

        self.outs = {
            "y1": 8,
            "y2": 10,
            "y38": 38,
        }

    @staticmethod
    def getInputs():
        inputs = {
            'x1': GPIO.input(8),
            'x2': GPIO.input(10),
            'x40': GPIO.input(40),
        }
        return inputs

    def sensorsLoop(self):
        while True:
            try:
                for input in self.inputs:
                    status = GPIO.input(self.inputs[input][1])
                    if self.inputs[input][0] != status:
                        self.inputs[input][0] = status
                        self.resetInput(input, int(status))
                time.sleep(0.1)
            except:
                pass

    def initGPIO(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)

    def resetOut(self, out, status):
        if status:
            GPIO.output(self.outs[out], GPIO.HIGH)
        else:
            GPIO.output(self.outs[out], GPIO.LOW)

    def resetInput(self, input, status):
        pass
