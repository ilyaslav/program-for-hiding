import RPi.GPIO as GPIO
import socket
import threading
from music import Music

class Client:
	def __init__(self):
		self.m = Music()
		self.server = []
		self.messages = []
		self.HOST = "192.168.0."
		self.PORT = 1111

	def clientFunction(self):
		i = 0
		while True:
			try:
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
					s.settimeout(0.01)
					print(self.HOST+f'{i}')
					s.connect((self.HOST+f'{i}', self.PORT))
					s.settimeout(None)
					self.server.append(s)

					while True:
						data = s.recv(1024).decode('utf-8')
						self.messages.extend(data.split(';')[:-1])

						while self.messages:
							self.messageHandler(self.messages.pop(0))

			except TimeoutError as e:
				print(i)
				if i == 254:
					i = 1
				else:
					i+=1

				if self.server:
					self.server.pop()
				continue
					
			except OSError as e:
				print(e)
				if i == 254:
					i = 1
				else:
					i+=1

				self.m.stopTrack()
				self.set_default_settings()

				if self.server:
					self.server.pop()
				s.close()

	def set_default_settings(self):
		GPIO.output(15, GPIO.HIGH)
		GPIO.output(19, GPIO.HIGH)
		GPIO.output(21, GPIO.HIGH)
		GPIO.output(23, GPIO.HIGH)
		GPIO.output(29, GPIO.HIGH)
		GPIO.output(31, GPIO.HIGH)
		GPIO.output(33, GPIO.HIGH)
		GPIO.output(35, GPIO.HIGH)
		GPIO.output(37, GPIO.HIGH)
		GPIO.output(8, GPIO.HIGH)
		GPIO.output(10, GPIO.HIGH)
		GPIO.output(12, GPIO.HIGH)
		GPIO.output(16, GPIO.HIGH)
		GPIO.output(18, GPIO.HIGH)
		GPIO.output(22, GPIO.HIGH)
		GPIO.output(24, GPIO.HIGH)
		GPIO.output(26, GPIO.HIGH)
		GPIO.output(32, GPIO.HIGH)
		GPIO.output(38, GPIO.HIGH)


	def messageHandler(self, message):
		if message == 'SH1':
			print(message)
			GPIO.output(38, GPIO.LOW)
		elif message == 'SH0':
			print(message)
			GPIO.output(38, GPIO.HIGH)
		elif message == 'RS1':
			print(message)
			GPIO.output(15, GPIO.LOW)
		elif message == 'RS0':
			print(message)
			GPIO.output(15, GPIO.HIGH)
		elif message == 'SL1':
			print(message)
			GPIO.output(19, GPIO.LOW)
		elif message == 'SL0':
			print(message)
			GPIO.output(19, GPIO.HIGH)

		elif message == 'U11':
			print(message)
			GPIO.output(21, GPIO.LOW)
		elif message == 'U10':
			print(message)
			GPIO.output(21, GPIO.HIGH)
		elif message == 'U21':
			print(message)
			GPIO.output(23, GPIO.LOW)
		elif message == 'U20':
			print(message)
			GPIO.output(23, GPIO.HIGH)
		elif message == 'U31':
			print(message)
			GPIO.output(29, GPIO.LOW)
		elif message == 'U30':
			print(message)
			GPIO.output(29, GPIO.HIGH)
		elif message == 'U41':
			print(message)
			GPIO.output(31, GPIO.LOW)
		elif message == 'U40':
			print(message)
			GPIO.output(31, GPIO.HIGH)
		elif message == 'U51':
			print(message)
			GPIO.output(33, GPIO.LOW)
		elif message == 'U50':
			print(message)
			GPIO.output(33, GPIO.HIGH)
		elif message == 'U61':
			print(message)
			GPIO.output(35, GPIO.LOW)
		elif message == 'U60':
			print(message)
			GPIO.output(35, GPIO.HIGH)
		elif message == 'U71':
			print(message)
			GPIO.output(37, GPIO.LOW)
		elif message == 'U70':
			print(message)
			GPIO.output(37, GPIO.HIGH)
		elif message == 'U81':
			print(message)
			GPIO.output(8, GPIO.LOW)
		elif message == 'U80':
			print(message)
			GPIO.output(8, GPIO.HIGH)
		elif message == 'U91':
			print(message)
			GPIO.output(10, GPIO.LOW)
		elif message == 'U90':
			print(message)
			GPIO.output(10, GPIO.HIGH)

		elif message == 'F11':
			print(message)
			GPIO.output(12, GPIO.LOW)
		elif message == 'F10':
			print(message)
			GPIO.output(12, GPIO.HIGH)
		elif message == 'F21':
			print(message)
			GPIO.output(16, GPIO.LOW)
		elif message == 'F20':
			print(message)
			GPIO.output(16, GPIO.HIGH)
		elif message == 'F31':
			print(message)
			GPIO.output(18, GPIO.LOW)
		elif message == 'F30':
			print(message)
			GPIO.output(18, GPIO.HIGH)
		elif message == 'F41':
			print(message)
			GPIO.output(22, GPIO.LOW)
		elif message == 'F40':
			print(message)
			GPIO.output(22, GPIO.HIGH)

		elif message == 'S11':
			print(message)
			GPIO.output(24, GPIO.LOW)
		elif message == 'S10':
			print(message)
			GPIO.output(24, GPIO.HIGH)
		elif message == 'S21':
			print(message)
			GPIO.output(26, GPIO.LOW)
		elif message == 'S20':
			print(message)
			GPIO.output(26, GPIO.HIGH)
		elif message == 'S31':
			print(message)
			GPIO.output(32, GPIO.LOW)
		elif message == 'S30':
			print(message)
			GPIO.output(32, GPIO.HIGH)

		elif message == 'M00':
			print(message)
			self.m.stopTrack()
		elif message == 'M11':
			print(message)
			self.m.playTrack1()
		elif message == 'M21':
			print(message)
			self.m.playTrack2()
		elif message == 'M31':
			print(message)
			self.m.playTrack3()
		elif message == 'M41':
			print(message)
			self.m.playTrack4()
		elif message == 'M51':
			print(message)
			self.m.playTrack5()
		elif message == 'M61':
			print(message)
			self.m.playTrack6()
		elif message == 'M71':
			print(message)
			self.m.playTrack7()
		elif message == 'M81':
			print(message)
			self.m.playTrack8()
		elif message == 'M91':
			print(message)
			self.m.playTrack9()
		elif message == 'MA1':
			print(message)
			self.m.playTrack10()
		elif message == 'MB1':
			print(message)
			self.m.playTrack11()
		elif message == 'MC1':
			print(message)
			self.m.playTrack12()
		elif message == 'MD1':
			print(message)
			self.m.playTrack13()
		elif message == 'ME1':
			print(message)
			self.m.playTrack14()
		elif message == 'MF1':
			print(message)
			self.m.playTrack15()
		elif message == 'MG1':
			print(message)
			self.m.playTrack16()
		elif message == 'MH1':
			print(message)
			self.m.playTrack17()
		elif message == 'MI1':
			print(message)
			self.m.playTrack18()
		elif message == 'MJ1':
			print(message)
			self.m.playTrack19()
		elif message == 'MK1':
			print(message)
			self.m.playTrack20()
		elif message == 'ML1':
			print(message)
			self.m.playTrack21()



if __name__ == "__main__":
	client = Client()
	client.clientFunction()
