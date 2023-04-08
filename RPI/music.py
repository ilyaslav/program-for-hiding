from kivy.core.audio import SoundLoader

class Music:
	def __init__(self):
		self.loadMusic()

	def loadMusic(self):
		self.music = SoundLoader.load('mp3/трек 01.mp3')
		self.music_HandS = {
		"Прятки 1": SoundLoader.load('mp3/трек 02.mp3'),
		"Прятки 2": SoundLoader.load('mp3/трек 03.mp3'),
		"Прятки 3": SoundLoader.load('mp3/трек 04.mp3'),
		"Прятки 4": SoundLoader.load('mp3/трек 05.mp3'),
		"Тени в городе": SoundLoader.load('mp3/трек 01.mp3'),
		"Рассвет": SoundLoader.load('mp3/трек 06.mp3')
		}
		self.music_souls = {
		"Души 1": SoundLoader.load('mp3/трек 08.mp3'),
		"Души 2": SoundLoader.load('mp3/трек 09.mp3'),
		"Души 3": SoundLoader.load('mp3/трек 10.mp3'),
		"Души 4": SoundLoader.load('mp3/трек 11.mp3'),
		"Поиск душ. Начало": SoundLoader.load('mp3/трек 07.mp3'),
		"Поиск душ. Конец": SoundLoader.load('mp3/трек 12.mp3')
		}
		self.music_strobe = {
		"Строб 1": SoundLoader.load('mp3/трек 13.mp3'),
		"Строб 2": SoundLoader.load('mp3/трек 14.mp3'),
		"Строб 3": SoundLoader.load('mp3/трек 15.mp3')
		}
		self.music_start = SoundLoader.load('mp3/трек 16.mp3')
		self.music_minutes = {
		"1 минута": SoundLoader.load('mp3/трек 17.mp3'),
		"2 минуты": SoundLoader.load('mp3/трек 18.mp3'),
		"3 минуты": SoundLoader.load('mp3/трек 19.mp3'),
		"4 минуты": SoundLoader.load('mp3/трек 20.mp3'),
		"5 минут": SoundLoader.load('mp3/трек 21.mp3'),
		}

	def stopTrack(self):
		self.music.stop()

	def playTrack1(self):
		self.music.stop()
		self.music = self.music_HandS['Тени в городе']
		self.music.play()

	def playTrack2(self):
		self.music.stop()
		self.music = self.music_HandS['Прятки 1']
		self.music.play()

	def playTrack3(self):
		self.music.stop()
		self.music = self.music_HandS['Прятки 2']
		self.music.play()

	def playTrack4(self):
		self.music.stop()
		self.music = self.music_HandS['Прятки 3']
		self.music.play()

	def playTrack5(self):
		self.music.stop()
		self.music = self.music_HandS['Прятки 4']
		self.music.play()

	def playTrack6(self):
		self.music.stop()
		self.music = self.music_HandS['Рассвет']
		self.music.play()

	def playTrack7(self):
		self.music.stop()
		self.music = self.music_souls['Поиск душ. Начало']
		self.music.play()

	def playTrack8(self):
		self.music.stop()
		self.music = self.music_souls['Души 1']
		self.music.play()

	def playTrack9(self):
		self.music.stop()
		self.music = self.music_souls['Души 2']
		self.music.play()

	def playTrack10(self):
		self.music.stop()
		self.music = self.music_souls['Души 3']
		self.music.play()

	def playTrack11(self):
		self.music.stop()
		self.music = self.music_souls['Души 4']
		self.music.play()

	def playTrack12(self):
		self.music.stop()
		self.music = self.music_souls['Поиск душ. Конец']
		self.music.play()

	def playTrack13(self):
		self.music_strobe['Строб 1'].play()

	def playTrack14(self):
		self.music_strobe['Строб 2'].play()

	def playTrack15(self):
		self.music_strobe['Строб 3'].play()

	def playTrack16(self):
		self.music.stop()
		self.music = self.music_start
		self.music.play()

	def playTrack17(self):
		self.music_minutes['1 минута'].play()

	def playTrack18(self):
		self.music_minutes['2 минуты'].play()

	def playTrack19(self):
		self.music_minutes['3 минуты'].play()

	def playTrack20(self):
		self.music_minutes['4 минуты'].play()

	def playTrack21(self):
		self.music_minutes['5 минут'].play()
