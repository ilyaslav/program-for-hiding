import threading

from client import Client
from music import Music
from gpio import PiHandler


class GameHandler(PiHandler):
    def __init__(self):
        super().__init__()
        self.client = Client(self.sendInputs, self.messageHandler)
        self.gm = Music()
        self.rsb_name = 'r1'

    def messageHandler(self, message: str):
        rpi, command, value =  message.split(":")

        if rpi != self.rsb_name:
            return
        
        if command.__contains__('x'):
            self.resetOut(command, int(value))
        
        if command == 'play':
            self.gm.play(value)
        elif command == 'stop':
            self.gm.stop(value)
        elif command == 'pause':
            self.gm.pause(value)
        elif command == 'volume':
            self.gm.changeVolume(int(value))

    def resetInput(self, input, status):
        self.client.sendMessage(f'{input}:{status};')

    def sendInputs(self):
        inputs = PiHandler.getInputs()
        for inputName in inputs:
            self.client.sendMessage(f'{self.rsb_name}:{inputName}:{int(inputs[inputName])};')


def main():
    gh = GameHandler()
    threading.Thread(target=gh.client.clientFunction, daemon=True).start()
    gh.sensorsLoop()


if __name__ == '__main__':
    main()