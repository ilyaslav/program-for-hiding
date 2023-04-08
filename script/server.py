import socket
import threading
import time

class Server():
	def __init__(self):
		self.connection = []
		self.messenges = []
		self.sensor_fans = [True, True, True, True]
		self.sensor_btRS = True
		self.HOST = socket.gethostbyname(socket.gethostname())
		self.PORT = 1111

	def serverFunction(self):	
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((self.HOST,self.PORT))
			s.listen()

			while True:
				try:
					conn, addr = s.accept()
					with conn:
						self.connection.append(conn)
						print(f"Connected by {addr}")
						print(self.connection)
			
						while True:
							data = conn.recv(1024).decode('utf-8')
							self.messenges.extend(data.split(';')[:-1])

							while self.messenges:
								ms = self.messenges.pop()

								if ms == 'F10':
									self.sensor_fans[0] = True
								elif ms == 'F11':
									self.sensor_fans[0] = False
								elif ms == 'F20':
									self.sensor_fans[1] = True
								elif ms == 'F21':
									self.sensor_fans[1] = False
								elif ms == 'F30':
									self.sensor_fans[2] = True
								elif ms == 'F31':
									self.sensor_fans[2] = False
								elif ms == 'F40':
									self.sensor_fans[3] = True
								elif ms == 'F41':
									self.sensor_fans[3] = False

								elif ms == 'RS0':
									self.sensor_btRS = True
								elif ms == 'RS1':
									self.sensor_btRS = False

				except TimeoutError as e:
					print(e)
					continue
			
				except OSError as e:
					print(e)
					self.connection.pop()