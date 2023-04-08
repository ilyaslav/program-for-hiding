import RPi.GPIO as GPIO
import socket
import threading
import time
from client import Client

class PiHandler():
	def __init__(self):
		self.sensor_fans = [True, True, True, True]
		self.sensor_btRS = True

		self.sensors_loop()

	def sensors_loop(self):
		while True:
			if GPIO.input(3) != self.sensor_btRS:
				self.sensor_btRS = GPIO.input(3)
				if self.sensor_btRS:
					client.server[0].send("RS0;".encode('utf-8'))
				else:
					client.server[0].send("RS1;".encode('utf-8'))

			if GPIO.input(5) != self.sensor_fans[0]:
				self.sensor_fans[0] = GPIO.input(5)
				if self.sensor_fans[0]:
					client.server[0].send("F10;".encode('utf-8'))
				else:
					client.server[0].send("F11;".encode('utf-8'))

			if GPIO.input(7) != self.sensor_fans[1]:
				self.sensor_fans[1] = GPIO.input(7)
				if self.sensor_fans[1]:
					client.server[0].send("F20;".encode('utf-8'))
				else:
					client.server[0].send("F21;".encode('utf-8'))


			if GPIO.input(11) != self.sensor_fans[2]:
				self.sensor_fans[2] = GPIO.input(11)
				if self.sensor_fans[2]:
					client.server[0].send("F30;".encode('utf-8'))
				else:
					client.server[0].send("F31;".encode('utf-8'))


			if GPIO.input(13) != self.sensor_fans[3]:
				self.sensor_fans[3] = GPIO.input(13)
				if self.sensor_fans[3]:
					client.server[0].send("F40;".encode('utf-8'))
				else:
					client.server[0].send("F41;".encode('utf-8'))


			time.sleep(0.1)
			
def set_GPIO_settings():
	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)

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
	GPIO.setup(38, GPIO.OUT, initial=GPIO.HIGH)

if __name__ == "__main__":
	set_GPIO_settings()
	client = Client()
	threading.Thread(target=client.clientFunction, daemon=True).start()
	ph = PiHandler()
