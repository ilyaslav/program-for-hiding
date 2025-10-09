import socket
from select import select
import itertools


class Server:
	def __init__(self):
		self.HOST = self.get_local_ip()
		self.PORT = 1111
		self.connections = []
		self.messages = []

	def get_local_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			# doesn't even have to be reachable
			s.connect(('192.255.255.255', 1))
			IP = s.getsockname()[0]
		except:
			IP = '127.0.0.1'
		finally:
			s.close()
		return IP


	def start_server(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.bind((self.HOST,self.PORT))
			sock.listen()
			sock.settimeout(0.1)

			self.connections_handler(sock)


	def connections_handler(self, sock):
		while True:
			try:
				conn, addr = sock.accept()

			except OSError:
				pass

			else:
				print(f"Connected by {addr}")
				self.connections.append(conn)
				self.init_settings()

			finally:
				for conn in self.connections:
					redy_to_read = []
					redy_to_read, _, _ = select(self.connections, [], [], 0)
					if conn in redy_to_read:
						try:
							data = conn.recv(1024).decode('utf-8')
							self.messages.extend(data.split(';')[:-1])
							while self.messages:
								mes = self.messages.pop(0)
								self.message_handler(mes)
						except:
							ind = self.connections.index(conn)
							self.connections.pop(ind)
							

	def init_settings(self):
		pass


	def message_handler(self, mes):
		self.send_message(mes)


	def send_message(self, message):
		for conn in self.connections:
			try:
				conn.send(message.encode('utf-8'))
			except:
				ind = self.connections.index(conn)
				self.connections.pop(ind)

if __name__ == '__main__':
	s = Server()
	s.start_server()