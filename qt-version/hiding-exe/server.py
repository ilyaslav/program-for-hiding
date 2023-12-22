import socket
import threading
import settings

class Server():
    def __init__(self):
        self.connection = []
        self.messenges = []
        self.HOST = self.get_local_ip()
        self.PORT = 1111

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

        print(IP)
        return IP

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
                                    settings.inputs['fans'][0] = True
                                elif ms == 'F11':
                                    settings.inputs['fans'][0] = False
                                elif ms == 'F20':
                                    settings.inputs['fans'][1] = True
                                elif ms == 'F21':
                                    settings.inputs['fans'][1] = False
                                elif ms == 'F30':
                                    settings.inputs['fans'][2] = True
                                elif ms == 'F31':
                                    settings.inputs['fans'][2] = False
                                elif ms == 'F40':
                                    settings.inputs['fans'][3] = True
                                elif ms == 'F41':
                                    settings.inputs['fans'][3] = False

                                elif ms == 'RS0':
                                    settings.inputs['runstop'] = True
                                elif ms == 'RS1':
                                    settings.inputs['runstop'] = False

                except TimeoutError as e:
                    print(e)
                    continue

                except OSError as e:
                    print(e)
                    self.connection.pop()
