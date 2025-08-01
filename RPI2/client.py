import socket


class Client:
    def __init__(self, sendInputsMethod, messageHandler):
        self.server = []
        self.messages = []
        self.HOST = self.getLocalIp()
        self.PORT = 1111
        self.sendInputsMethod = sendInputsMethod
        self.handler = messageHandler

    def getLocalIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('192.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()

        a, b, c, _ = IP.split('.')
        IP = f'{a}.{b}.{c}.'
        print(IP)
        return IP

    def clientFunction(self):
        i = 0
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.01)
                    print(self.HOST + f'{i}')
                    s.connect((self.HOST + f'{i}', self.PORT))
                    s.settimeout(None)
                    self.server.append(s)
                    self.sendInputs()

                    while True:
                        data = s.recv(1024).decode('utf-8')
                        self.messages.extend(data.split(';')[:-1])

                        while self.messages:
                            self.messageHandler(self.messages.pop(0), self.handler)

            except TimeoutError as e:
                print(i)
                if i == 254:
                    i = 1
                else:
                    i += 1

                if self.server:
                    self.server.pop()
                continue

            except OSError as e:
                print(e)
                if i == 254:
                    i = 1
                else:
                    i += 1

                if self.server:
                    self.server.pop()
                s.close()

    def sendMessage(self, message):
        for s in self.server:
            try:
                s.send(message.encode('utf-8'))
            except:
                self.server.pop()

    def messageHandler(self, message, handler):
        print(f'Принято сообщение: {message}')
        if handler:
            handler(message)

    def sendInputs(self):
        self.sendInputsMethod()