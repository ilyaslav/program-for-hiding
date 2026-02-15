import RPi.GPIO as GPIO
import time

class PiHandler:
    def __init__(self):
        self.initGPIO()
        self.inputs = {
            'x1': [GPIO.input(22), 22],
            'x40': [GPIO.input(40), 40],
        }

        self.outs = {
            "y1": 7,
            "y2": 11,
            "y3": 13,
            "y4": 15,
            "y5": 19,
            "y6": 21,
            "y7": 23,
            "y8": 29,
            "y9": 31,
            "y10": 33,
            "y11": 35,
            "y12": 37,
            "y13": 8,
            "y14": 10,
            "y18": 24,
            "y16": 18,
            "y17": 24,
            "y38": 38,
        }

    @staticmethod
    def getInputs():
        inputs = {
            'x1': GPIO.input(22),
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

        GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(40, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH)
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
        GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(38, GPIO.OUT, initial=GPIO.HIGH)

    def resetOut(self, out, status):
        if status:
            GPIO.output(self.outs[out], GPIO.LOW)
        else:
            GPIO.output(self.outs[out], GPIO.HIGH)

    def resetInput(self, input, status):
        pass