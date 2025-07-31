from audioplayer import AudioPlayer
import alsaaudio

class Music():
	def __init__(self):
		self.tracks = {} # 'track': [state, AudioPlayer()]
		self.mix = alsaaudio.Mixer()

	def changeVolume(self, vol):
		self.mix.setvolume(vol)

	def play(self, track):
		try:
			music = self.tracks.get(track)
			if music:
				if not music[0]:
					music[0] = True
					music[1].resume()
				else:
					music[1].play()
			else:
				self.tracks[track] = [True, AudioPlayer(f'/home/user/Desktop/RPI1/mp3/{track}.mp3')]
				self.tracks[track][1].play()
		except:
			pass

	def stop(self, track):
		try:
			if self.tracks.get(track):
				self.tracks[track][1].stop()
				del self.tracks[track]
		except:
			pass

	def pause(self, track):
		try:
			music = self.tracks.get(track)
			if music:
				music[0] = False
				music[1].pause()
		except:
			pass