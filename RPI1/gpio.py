import RPi.GPIO as GPIO
import time

class PiHandler:
    def __init__(self):
        self.initGPIO()
        self.inputs = {
            'x1': [GPIO.input(3), 3],
            'x2': [GPIO.input(5), 5],
            'x3': [GPIO.input(7), 7],
            'x4': [GPIO.input(11), 11],
            'x5': [GPIO.input(13), 13],
            'x40': [GPIO.input(40), 40],
        }

        self.outs = {
            "y1": 15,
            "y2": 19,
            "y3": 21,
            "y4": 23,
            "y5": 29,
            "y6": 31,
            "y7": 33,
            "y8": 35,
            "y9": 37,
            "y10": 8,
            "y11": 10,
            "y12": 12,
            "y13": 16,
            "y14": 18,
            "y15": 22,
            "y16": 24,
            "y17": 26,
            "y18": 32,
            "y19": 36,
            "y38": 38,
        }

    @staticmethod
    def getInputs():
        inputs = {
            'x1': GPIO.input(3),
            'x2': GPIO.input(4),
            'x3': GPIO.input(5),
            'x4': GPIO.input(11),
            'x5': GPIO.input(13),
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

        GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(19, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(21, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(29, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(31, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(33, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(35, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(37, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(8, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(10, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(26, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(32, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(36, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(38, GPIO.OUT, initial=GPIO.HIGH)

    def resetOut(self, out, status):
        if status:
            GPIO.output(self.outs[out], GPIO.LOW)
        else:
            GPIO.output(self.outs[out], GPIO.HIGH)

    def resetInput(self, input, status):
        pass