from server import Server
import socket
import threading

import time
import random
from TimeBox import TimeBox

from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'window_state', 'maximized')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.write()

import kivy
from kivy.app import App

from kivy.properties import NumericProperty

from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.core.audio import SoundLoader

from kivy.clock import Clock
from functools import partial


class CenteredTextInput(TextInput):
	text_width = NumericProperty()

	def update_padding(self, *args):
	 	self.text_width = self._get_text_width(self.text,self.tab_width,self._label_cached)


class GridL(GridLayout):
	pass

class Tab(TabbedPanel):
	def __init__(self, **kwargs):
		super(Tab, self).__init__(**kwargs)

		self.set_standard_settings()

		self.timebox = TimeBox("Интервалы времени.txt")
		self.time_m = 10
		self.time_s = 0
		self.timer_on = None
		self.lastlen_text = 5
		self.timeUV_bt = [False, False, False]
		self.UV_activation_time = self.timebox.t21

		self.sensor_start = False
		self.sensor_fans = [False, False, False, False]

		self.uv_event = None
		self.strobe_event = None
		self.strobe_music_event = None
		self.music_play_event = None
		self.start_event = None
		self.shadow_lamp_enent = None
		self.shadow_event = None

		Clock.schedule_interval(self.sensors_loop, 0.1)


	def set_standard_settings(self):
		self.set_standart_outs()

		self.time_panel.text = "10:00"
		self.scripts = 0
		self.timer = "10:00"
		self.order = 1
		self.order_strobe = 1
		self.order_music = 1
		self.order_fans = [0,0,0,0]

		self.bonuses = {
		"UVlamps": False,
		"fans": False,
		"strobes": False,
		"settings": False
		}
		self.for_kids = False
		self.bonus_time = 1

		self.RUNSTOP = False
		self.shadow = False
		self.start_run_time = -1 
		self.fans_run_time = [0,0,0,0]
		self.fan_strobe = False

		self.staticUV = [False, False, False, False, False, False, False, False, False]


	def set_standart_outs(self):
		self.UVlamps = [False, False, False, False, False, False, False, False, False]
		self.Strobes = [False, False, False]
		self.Fans = [False, False, False, False]
		self.ShadowLamp = False
		self.RunStopLamp = False


	def sensors_loop(self, dt):
		self.sensor_fans[0] = s.sensor_fans[0]
		self.sensor_fans[1] = s.sensor_fans[1]
		self.sensor_fans[2] = s.sensor_fans[2]
		self.sensor_fans[3] = s.sensor_fans[3]
		self.sensor_btRS = s.sensor_btRS

		if self.sensor_btRS == False and not self.sensor_start:
			self.start_run_time = time.time()
			self.sensor_start = True
			
		if self.sensor_start:
			if self.timebox.t1 < time.time() - self.start_run_time < self.timebox.t1 + 0.2:
				self.bt_RUNSTOP_press()
				self.sensor_start = False
				self.start_run_time = -1
				
		if self.sensor_btRS == True:
			self.sensor_start = False
			self.start_run_time = -1
			self.time1 = time.time()
				
		if time.time() - self.time1 > 7 and self.RUNSTOP:
			self.bt_RUNSTOP_press()

		for i in range(4):
			if not self.sensor_fans[i] and time.time() - self.fans_run_time[i] > self.timebox.t17:
				self.order_fans[i]+=1
				self.fans_run_time[i] = time.time()
	
				if self.order_fans[i] == 3:
					self.order_fans[i]=0
	
					if i == 0:
						if self.bonuses["fans"]:
							self.action_fan1(0)
							Clock.schedule_once(self.action_fan1, 4)
	
					if i == 1:
						if self.bonuses["fans"]:
							self.action_fan2(0)
							Clock.schedule_once(self.action_fan2, 4)
	
					if i == 2:
						if self.bonuses["fans"]:
							self.action_fan3(0)
							Clock.schedule_once(self.action_fan3, 4)
	
					if i == 3:
						if self.bonuses["fans"]:
							self.action_fan4(0)
							Clock.schedule_once(self.action_fan4, 4)

		self.reset_sensors()

		if self.bonuses['settings']:
			self.set_dinamic_OnOff()
		else:
			self.set_static_OnOff()

		self.reset_OnOff_bt()
		
		if not self.RUNSTOP and not self.bonuses['settings']:
			self.off_all()
			self.set_standart_outs()      


	def bt_script1_press(self):
		self.scripts = 0
		self.change_scriptbt_color()

	def bt_script2_press(self):
		self.scripts = 1
		self.change_scriptbt_color()

	def bt_script3_press(self):
		self.scripts = 2
		self.change_scriptbt_color()

	def bt_script4_press(self):
		self.scripts = 3
		self.change_scriptbt_color()


	def bt_UVlamps_press(self):
		self.bonuses['UVlamps'] = not self.bonuses['UVlamps']
		self.refresh_settings_buttons()

	def bt_UVkids_press(self):
		self.for_kids = not self.for_kids

		if self.for_kids:
			self.UV_activation_time = self.timebox.t22
		else:
			self.UV_activation_time = self.timebox.t21

		self.refresh_settings_buttons()


	def bt_UVsec1_press(self):
		if self.bonuses['UVlamps']:
			self.timeUV_bt[0] = not self.timeUV_bt[0]

			if self.timeUV_bt[0]:
				self.bonus_time += self.timebox.t12
			else:
				self.bonus_time -= self.timebox.t12

			self.refresh_settings_buttons()

	def bt_UVsec2_press(self):
		if self.bonuses['UVlamps']:
			self.timeUV_bt[1] = not self.timeUV_bt[1]

			if self.timeUV_bt[1]:
				self.bonus_time += self.timebox.t13
			else:
				self.bonus_time -= self.timebox.t13

			self.refresh_settings_buttons()

	def bt_UVsec3_press(self):
		if self.bonuses['UVlamps']:
			self.timeUV_bt[2] = not self.timeUV_bt[2]

			if self.timeUV_bt[2]:
				self.bonus_time += self.timebox.t14
			else:
				self.bonus_time -= self.timebox.t14

			self.refresh_settings_buttons()


	def bt_fans_press(self):
		self.bonuses['fans'] = not self.bonuses['fans']
		self.refresh_settings_buttons()

	def bt_strobes_press(self):
		self.bonuses['strobes'] = not self.bonuses['strobes']
		self.refresh_settings_buttons()

	def bt_settings_press(self):
		self.bonuses['settings'] = not self.bonuses['settings']

		if self.bonuses['settings']:
			self.set_dinamic_OnOff()
		else:
			self.set_static_OnOff()

		self.refresh_settings_buttons()
		self.reset_OnOff_bt()

	def bt_reset_press(self):
		self.stop_events(0)

		self.set_standard_settings()
		self.off_UV_lamps()
		self.off_fans()
		self.off_strobes()

		self.reset_bt_colors()
		self.reset_time()

		self.disabling_buttons()
		self.disabled_settings()
		self.refresh_settings_buttons()
		self.reset_OnOff_bt()

		if self.RunStopLamp:
			self.action_runstop_lamp(0)


	def bt_RUNSTOP_press(self):
		if self.ShadowLamp:
			self.action_shadow_lamp(0)
				
		self.set_standart_outs()
		self.action_runstop_lamp(0)
		if self.RUNSTOP:
			self.play_end_music()

		self.RUNSTOP = not self.RUNSTOP
		self.change_RSbt_color()
		self.disabling_buttons()
		self.reset_OnOff_bt()

		if self.start_event != None:
			self.start_event.cancel()
		if self.shadow_event != None:
			self.shadow_event.cancel()

		if self.RUNSTOP:
			if self.scripts == 0:
				self.start_event = Clock.schedule_once(self.start_game, self.timebox.t2)
				try:
					s.connection[0].send("MG1;".encode('utf-8'))
				except:
					pass
			elif self.scripts == 1:
				self.start_game(0)
				self.shadow_event = Clock.schedule_once(self.action_shadow, 8)


	def bt_5min_press(self):
		if self.timer == "05:00":
			self.time_panel.text = "00:00"
			self.timer = "0"
		else:
			self.time_panel.text = "05:00"
			self.timer = "05:00"

		self.change_timebt_color()
		self.reset_time()

	def bt_8min_press(self):
		if self.timer == "08:00":
			self.time_panel.text = "00:00"
			self.timer = "0"
		else:
			self.time_panel.text = "08:00"
			self.timer = "08:00"

		self.change_timebt_color()
		self.reset_time()

	def bt_10min_press(self):
		if self.timer == "10:00":
			self.time_panel.text = "00:00"
			self.timer = "0"
		else:
			self.time_panel.text = "10:00"
			self.timer = "10:00"

		self.change_timebt_color()
		self.reset_time()

	def bt_12min_press(self):
		if self.timer == "12:00":
			self.time_panel.text = "00:00"
			self.timer = "0"
		else:
			self.time_panel.text = "12:00"
			self.timer = "12:00"

		self.change_timebt_color()
		self.reset_time()

	def bt_15min_press(self):
		if self.timer == "15:00":
			self.time_panel.text = "00:00"
			self.timer = "0"
		else:
			self.time_panel.text = "15:00"
			self.timer = "15:00"

		self.change_timebt_color()
		self.reset_time()

	def bt_18min_press(self):
		if self.timer == "18:00":
			self.time_panel.text = "00:00"
			self.timer = "0"
		else:
			self.time_panel.text = "18:00"
			self.timer = "18:00"

		self.change_timebt_color()
		self.reset_time()


	def timer_run(self, dt):
		if self.time_s - 1 >= 0:
			self.time_s -= 1
		elif self.time_m > 0:
			self.time_m -= 1
			self.time_s = 59

		if self.time_m < 10:
			m1 = f"0{str(self.time_m)}"
		else:
			m1 = str(self.time_m)

		if self.time_s < 10:
			s1 = f"0{str(self.time_s)}"
		else:
			s1 = str(self.time_s)

		self.time_panel.text = f"{m1}:{s1}"

		try:
			if self.time_m == 1 and self.time_s == 0 and self.scripts == 1 and self.timer != "05:00":
				s.connection[0].send('MH1;'.encode('utf-8'))
			elif self.time_m == 2 and self.time_s == 0 and self.scripts == 1:
				s.connection[0].send('MI1;'.encode('utf-8'))
			elif self.time_m == 3 and self.time_s == 0 and self.scripts == 1:
				s.connection[0].send('MJ1;'.encode('utf-8'))
			elif self.time_m == 4 and self.time_s == 0 and self.scripts == 1:
				s.connection[0].send('MK1;'.encode('utf-8'))
			elif self.time_m == 5 and self.time_s == 0 and self.scripts == 1:
				s.connection[0].send('ML1;'.encode('utf-8'))
		except:
			pass

		if self.time_m == 0 and self.time_s == 0 or not self.RUNSTOP:
			self.order = 1
			self.order_strobe = 1
			self.order_music = 1

			self.stop_events(0)

			self.RUNSTOP = False
			self.time_panel.text = self.timer
			self.reset_time()
			self.disabling_buttons()
			self.reset_bt_colors()
			self.play_end_music()

			if self.RunStopLamp:
				self.action_runstop_lamp(0)


	def reset_bt_colors(self):
		self.refresh_settings_buttons()
		self.change_timebt_color()
		self.change_scriptbt_color()
		self.change_RSbt_color()


	def reset_time(self):
		try:
			time = self.time_panel.text.split(':')
			self.time_m = int(time[0])
			self.time_s = int(time[1])

			if self.time_m > 18:
				self.time_m = 18

			if self.time_s > 59:
				self.time_s = 59

			if self.time_m == 18:
				self.time_s = 0

			if self.time_m < 5:
				self.time_m = 5
				self.time_s = 0

		except:
			self.time_m = 10
			self.time_s = 0


	def refresh_settings_buttons(self):
		if self.bonuses['UVlamps']:
			self.bt_UVlamps.background_color = "00ff00ff"

			if self.timeUV_bt[0]:
				self.bt_UVsec1.background_color = "ffff00ff"
			else:
				self.bt_UVsec1.background_color = "ffffffff"

			if self.timeUV_bt[1]:
				self.bt_UVsec2.background_color = "ffff00ff"
			else:
				self.bt_UVsec2.background_color = "ffffffff"

			if self.timeUV_bt[2]:
				self.bt_UVsec3.background_color = "ffff00ff"
			else:
				self.bt_UVsec3.background_color = "ffffffff"

		else:
			self.bt_UVlamps.background_color = "ffffffff"

			self.bt_UVsec1.background_color = "ffffffff"
			self.bt_UVsec2.background_color = "ffffffff"
			self.bt_UVsec3.background_color = "ffffffff"
			self.bonus_time = 1


		if self.for_kids:
			self.bt_UVkids.background_color = "00ff00ff"
		else:
			self.bt_UVkids.background_color = "ffffffff"


		if self.bonuses['fans']:
			self.bt_fans.background_color = "00ff00ff"
		else:
			self.bt_fans.background_color = "ffffffff"

		if self.bonuses['strobes']:
			self.bt_strobes.background_color = "00ff00ff"
		else:
			self.bt_strobes.background_color = "ffffffff"

		if self.bonuses['settings']:
			self.bt_settings.background_color = "00ff00ff"
		else:
			self.bt_settings.background_color = "ffffffff"

	def change_scriptbt_color(self):
		if self.scripts == 0:
			self.bt_script1.background_color = '00ff00ff'
			self.bt_script2.background_color = 'ffffffff'
			self.bt_script3.background_color = 'ffffffff'
			self.bt_script4.background_color = 'ffffffff'
		elif self.scripts == 1:
			self.bt_script1.background_color = 'ffffffff'
			self.bt_script2.background_color = '00ff00ff'
			self.bt_script3.background_color = 'ffffffff'
			self.bt_script4.background_color = 'ffffffff'
		elif self.scripts == 2:
			self.bt_script1.background_color = 'ffffffff'
			self.bt_script2.background_color = 'ffffffff'
			self.bt_script3.background_color = '00ff00ff'
			self.bt_script4.background_color = 'ffffffff'
		elif self.scripts == 3:
			self.bt_script1.background_color = 'ffffffff'
			self.bt_script2.background_color = 'ffffffff'
			self.bt_script3.background_color = 'ffffffff'
			self.bt_script4.background_color = '00ff00ff'

	def change_timebt_color(self):
		if self.timer == "0":
			self.bt_5min.background_color = 'ffffffff'
			self.bt_8min.background_color = 'ffffffff'
			self.bt_10min.background_color = 'ffffffff'
			self.bt_12min.background_color = 'ffffffff'
			self.bt_15min.background_color = 'ffffffff'
			self.bt_18min.background_color = 'ffffffff'
		elif self.timer == "05:00":
			self.bt_5min.background_color = 'ffff00ff'
			self.bt_8min.background_color = 'ffffffff'
			self.bt_10min.background_color = 'ffffffff'
			self.bt_12min.background_color = 'ffffffff'
			self.bt_15min.background_color = 'ffffffff'
			self.bt_18min.background_color = 'ffffffff'
		elif self.timer == "08:00":
			self.bt_5min.background_color = 'ffffffff'
			self.bt_8min.background_color = 'ffff00ff'
			self.bt_10min.background_color = 'ffffffff'
			self.bt_12min.background_color = 'ffffffff'
			self.bt_15min.background_color = 'ffffffff'
			self.bt_18min.background_color = 'ffffffff'
		elif self.timer == "10:00":
			self.bt_5min.background_color = 'ffffffff'
			self.bt_8min.background_color = 'ffffffff'
			self.bt_10min.background_color = 'ffff00ff'
			self.bt_12min.background_color = 'ffffffff'
			self.bt_15min.background_color = 'ffffffff'
			self.bt_18min.background_color = 'ffffffff'
		elif self.timer == "12:00":
			self.bt_5min.background_color = 'ffffffff'
			self.bt_8min.background_color = 'ffffffff'
			self.bt_10min.background_color = 'ffffffff'
			self.bt_12min.background_color = 'ffff00ff'
			self.bt_15min.background_color = 'ffffffff'
			self.bt_18min.background_color = 'ffffffff'
		elif self.timer == "15:00":
			self.bt_5min.background_color = 'ffffffff'
			self.bt_8min.background_color = 'ffffffff'
			self.bt_10min.background_color = 'ffffffff'
			self.bt_12min.background_color = 'ffffffff'
			self.bt_15min.background_color = 'ffff00ff'
			self.bt_18min.background_color = 'ffffffff'
		elif self.timer == "18:00":
			self.bt_5min.background_color = 'ffffffff'
			self.bt_8min.background_color = 'ffffffff'
			self.bt_10min.background_color = 'ffffffff'
			self.bt_12min.background_color = 'ffffffff'
			self.bt_15min.background_color = 'ffffffff'
			self.bt_18min.background_color = 'ffff00ff'


	def change_RSbt_color(self):
		if self.RUNSTOP:
			self.bt_RUNSTOP.background_color = "00ff00ff"
		else:
			self.bt_RUNSTOP.background_color = "ff0000ff"


	def change_time(self):
		text = self.time_panel.text

		if len(text) > 0 and len(text) != 3:
			if '0123456789'.find(text[-1]) == -1:
				text = text[:-1]

		if len(text) == 2 and self.lastlen_text == 1:
			text += ":"
			Clock.schedule_once(partial(self.time_panel.do_cursor_movement, 'cursor_end'))

		if len(text) == 6:
			text = text[0:5]

		if len(text) == 5 and not self.RUNSTOP:
			self.reset_time()

		timer = self.timer
		self.timer = "0"
		self.change_timebt_color()
		self.timer = timer
		self.lastlen_text = len(text)
		self.time_panel.text = text


	def disabling_buttons(self):
		if self.RUNSTOP:
			self.bt_script1.disabled = True
			self.bt_script2.disabled = True
			self.bt_script3.disabled = True
			self.bt_script4.disabled = True

			self.bt_5min.disabled = True
			self.bt_8min.disabled = True
			self.bt_10min.disabled = True
			self.bt_12min.disabled = True
			self.bt_15min.disabled = True
			self.bt_18min.disabled = True
			self.time_panel.disabled = True
		else:
			self.bt_script1.disabled = False
			self.bt_script2.disabled = False
			self.bt_script3.disabled = True
			self.bt_script4.disabled = True

			self.bt_5min.disabled = False
			self.bt_8min.disabled = False
			self.bt_10min.disabled = False
			self.bt_12min.disabled = False
			self.bt_15min.disabled = False
			self.bt_18min.disabled = False
			self.time_panel.disabled = False


	def disabled_settings(self):
		self.bt_UVlamps.disabled = False
		self.bt_UVsec1.disabled = False
		self.bt_UVsec2.disabled = False
		self.bt_UVsec3.disabled = False
		self.bt_UVkids.disabled = False
		self.bt_fans.disabled = False
		self.bt_strobes.disabled = False


	def reset_sensors(self):
		if self.sensor_btRS:
			self.sensRS.background_color = "ffffffff"
		else:
			self.sensRS.background_color = "ffff00ff"

		if self.sensor_fans[0]:
			self.sens1.background_color = "ffffffff"
		else:
			self.sens1.background_color = "ffff00ff"

		if self.sensor_fans[1]:
			self.sens2.background_color = "ffffffff"
		else:
			self.sens2.background_color = "ffff00ff"

		if self.sensor_fans[2]:
			self.sens3.background_color = "ffffffff"
		else:
			self.sens3.background_color = "ffff00ff"

		if self.sensor_fans[3]:
			self.sens4.background_color = "ffffffff"
		else:
			self.sens4.background_color = "ffff00ff"


	def reset_OnOff_bt(self):
		self.reset_OnOff_runstop()
		self.reset_OffOn_shadow()
		self.reset_OffOn_strobe()
		self.reset_OffOn_fan()
		self.reset_OffOn_uv()


	def reset_OnOff_runstop(self):
		if self.RunStopLamp:
			self.runstop_off.disabled = False
			self.runstop_on.disabled = True
		else:
			self.runstop_off.disabled = True
			self.runstop_on.disabled = False

		if not self.bonuses['settings']:
			self.runstop_off.disabled = True
			self.runstop_on.disabled = True


	def reset_OffOn_shadow(self):
		if self.ShadowLamp:
			self.shadow_off.disabled = False
			self.shadow_on.disabled = True
		else:
			self.shadow_off.disabled = True
			self.shadow_on.disabled = False

		if not self.bonuses['settings']:
			self.shadow_off.disabled = True
			self.shadow_on.disabled = True


	def reset_OffOn_strobe(self):
		if self.Strobes[0]:
			self.strobe1_off.disabled = False
			self.strobe1_on.disabled = True
		else:
			self.strobe1_off.disabled = True
			self.strobe1_on.disabled = False

		if self.Strobes[1]:
			self.strobe2_off.disabled = False
			self.strobe2_on.disabled = True
		else:
			self.strobe2_off.disabled = True
			self.strobe2_on.disabled = False

		if self.Strobes[2]:
			self.strobe3_off.disabled = False
			self.strobe3_on.disabled = True
		else:
			self.strobe3_off.disabled = True
			self.strobe3_on.disabled = False

		if not self.bonuses['settings']:
			self.strobe1_off.disabled = True
			self.strobe1_on.disabled = True
			self.strobe2_off.disabled = True
			self.strobe2_on.disabled = True
			self.strobe3_on.disabled = True
			self.strobe3_off.disabled = True


	def reset_OffOn_fan(self):
		if self.Fans[0]:
			self.fan1_off.disabled = False
			self.fan1_on.disabled = True
		else:
			self.fan1_off.disabled = True
			self.fan1_on.disabled = False

		if self.Fans[1]:
			self.fan2_off.disabled = False
			self.fan2_on.disabled = True
		else:
			self.fan2_off.disabled = True
			self.fan2_on.disabled = False

		if self.Fans[2]:
			self.fan3_off.disabled = False
			self.fan3_on.disabled = True
		else:
			self.fan3_off.disabled = True
			self.fan3_on.disabled = False

		if self.Fans[3]:
			self.fan4_off.disabled = False
			self.fan4_on.disabled = True
		else:
			self.fan4_off.disabled = True
			self.fan4_on.disabled = False

		if not self.bonuses['settings']:
			self.fan1_off.disabled = True
			self.fan1_on.disabled = True
			self.fan2_off.disabled = True
			self.fan2_on.disabled = True
			self.fan3_off.disabled = True
			self.fan3_on.disabled = True
			self.fan4_off.disabled = True
			self.fan4_on.disabled = True


	def reset_OffOn_uv(self):
		if self.UVlamps[0]:
			self.uv1_off.disabled = False
			self.uv1_on.disabled = True
		else:
			self.uv1_off.disabled = True
			self.uv1_on.disabled = False

		if self.UVlamps[1]:
			self.uv2_off.disabled = False
			self.uv2_on.disabled = True
		else:
			self.uv2_off.disabled = True
			self.uv2_on.disabled = False

		if self.UVlamps[2]:
			self.uv3_off.disabled = False
			self.uv3_on.disabled = True
		else:
			self.uv3_off.disabled = True
			self.uv3_on.disabled = False

		if self.UVlamps[3]:
			self.uv4_off.disabled = False
			self.uv4_on.disabled = True
		else:
			self.uv4_off.disabled = True
			self.uv4_on.disabled = False

		if self.UVlamps[4]:
			self.uv5_off.disabled = False
			self.uv5_on.disabled = True
		else:
			self.uv5_off.disabled = True
			self.uv5_on.disabled = False

		if self.UVlamps[5]:
			self.uv6_off.disabled = False
			self.uv6_on.disabled = True
		else:
			self.uv6_off.disabled = True
			self.uv6_on.disabled = False

		if self.UVlamps[6]:
			self.uv7_off.disabled = False
			self.uv7_on.disabled = True
		else:
			self.uv7_off.disabled = True
			self.uv7_on.disabled = False

		if self.UVlamps[7]:
			self.uv8_off.disabled = False
			self.uv8_on.disabled = True
		else:
			self.uv8_off.disabled = True
			self.uv8_on.disabled = False

		if self.UVlamps[8]:
			self.uv9_off.disabled = False
			self.uv9_on.disabled = True
		else:
			self.uv9_off.disabled = True
			self.uv9_on.disabled = False

		if not self.bonuses['settings']:
			self.uv1_off.disabled = True
			self.uv1_on.disabled = True
			self.uv2_off.disabled = True
			self.uv2_on.disabled = True
			self.uv3_off.disabled = True
			self.uv3_on.disabled = True
			self.uv4_off.disabled = True
			self.uv4_on.disabled = True
			self.uv5_off.disabled = True
			self.uv5_on.disabled = True
			self.uv6_off.disabled = True
			self.uv6_on.disabled = True
			self.uv7_off.disabled = True
			self.uv7_on.disabled = True
			self.uv8_off.disabled = True
			self.uv8_on.disabled = True
			self.uv9_off.disabled = True
			self.uv9_on.disabled = True


	def bt_runstop_press(self):
		self.action_runstop_lamp(0)
		self.reset_OnOff_bt()

	def bt_shadow_press(self):
		self.action_shadow_lamp(0)
		self.reset_OnOff_bt()


	def bt_strobe1_press(self):
		self.action_strobe1(0)
		self.reset_OnOff_bt()

	def bt_strobe2_press(self):
		self.action_strobe2(0)
		self.reset_OnOff_bt()

	def bt_strobe3_press(self):
		self.action_strobe3(0)
		self.reset_OnOff_bt()


	def bt_fan1_press(self):
		self.action_fan1(0)
		self.reset_OnOff_bt()

	def bt_fan2_press(self):
		self.action_fan2(0)
		self.reset_OnOff_bt()

	def bt_fan3_press(self):
		self.action_fan3(0)
		self.reset_OnOff_bt()

	def bt_fan4_press(self):
		self.action_fan4(0)
		self.reset_OnOff_bt()


	def bt_uv1_press(self):
		try:
			if not self.staticUV[0]:
				self.UVlamps[0] = not self.UVlamps[0]
			self.staticUV[0] = not self.staticUV[0]
			self.action_uv1(0)
			self.reset_OnOff_bt()
		except:
			self.staticUV[0] = not self.staticUV[0]
			self.UVlamps[0] = not self.UVlamps[0]

	def bt_uv2_press(self):
		try:
			if not self.staticUV[1]:
				self.UVlamps[1] = not self.UVlamps[1]
			self.staticUV[1] = not self.staticUV[1]
			self.action_uv2(0)
			self.reset_OnOff_bt()
		except:
			self.staticUV[1] = not self.staticUV[1]
			self.UVlamps[1] = not self.UVlamps[1]

	def bt_uv3_press(self):
		try:
			if not self.staticUV[2]:
				self.UVlamps[2] = not self.UVlamps[2]
			self.staticUV[2] = not self.staticUV[2]
			self.action_uv3(0)
			self.reset_OnOff_bt()
		except:
			self.staticUV[2] = not self.staticUV[2]
			self.UVlamps[2] = not self.UVlamps[2]

	def bt_uv4_press(self):
		try:
			if not self.staticUV[3]:
				self.UVlamps[3] = not self.UVlamps[3]
			self.staticUV[3] = not self.staticUV[3]
			self.action_uv4(0)
			self.reset_OnOff_bt()
		except:
			self.staticUV[3] = not self.staticUV[3]
			self.UVlamps[3] = not self.UVlamps[3]

	def bt_uv5_press(self):
		try:
			if not self.staticUV[4]:
				self.UVlamps[4] = not self.UVlamps[4]
			self.staticUV[4] = not self.staticUV[4]
			self.action_uv5(0)
			self.reset_OnOff_bt()
		except:
			self.staticUV[4] = not self.staticUV[4]
			self.UVlamps[4] = not self.UVlamps[4]

	def bt_uv6_press(self):
		try:
			if not self.staticUV[5]:
				self.UVlamps[5] = not self.UVlamps[5]
			self.staticUV[5] = not self.staticUV[5]
			self.action_uv6(0)
			self.reset_OnOff_bt()
		except:
			self.staticUV[5] = not self.staticUV[5]
			self.UVlamps[5] = not self.UVlamps[5]

	def bt_uv7_press(self):
		try:
			if not self.staticUV[6]:
				self.UVlamps[6] = not self.UVlamps[6]
			self.staticUV[6] = not self.staticUV[6]
			self.action_uv7(0)
			self.reset_OnOff_bt()
		except:
			self.staticUV[6] = not self.staticUV[6]
			self.UVlamps[6] = not self.UVlamps[6]

	def bt_uv8_press(self):
		try:
			if not self.staticUV[7]:
				self.UVlamps[7] = not self.UVlamps[7]
			self.staticUV[7] = not self.staticUV[7]
			self.action_uv8(0)
			self.reset_OnOff_bt()
		except:
			self.staticUV[7] = not self.staticUV[7]
			self.UVlamps[7] = not self.UVlamps[7]

	def bt_uv9_press(self):
		try:
			if not self.staticUV[8]:
				self.UVlamps[8] = not self.UVlamps[8]
			self.staticUV[8] = not self.staticUV[8]
			self.action_uv9(0)
			self.reset_OnOff_bt()
		except:
			self.staticUV[8] = not self.staticUV[8]
			self.UVlamps[8] = not self.UVlamps[8]




	def shadow_lamp_activation(self, dt):
		self.shadow_lamp_enent = Clock.schedule_interval(self.action_shadow_lamp, self.timebox.t10)


	def strobe_music_play(self, dt):
		try:
			if self.bonuses['strobes']:
				tmp = random.randint(1,3)
				print(tmp)
				if tmp == 1:
					s.connection[0].send("MD1;".encode('utf-8'))
				elif tmp == 2:
					s.connection[0].send("ME1;".encode('utf-8'))
				elif tmp == 3:
					s.connection[0].send("MF1;".encode('utf-8'))
		except:
			pass


	def strobe_activation(self, dt):
		if self.RUNSTOP:
			if self.order_strobe == 1:
				self.order_strobe+=1
				if self.bonuses['strobes']:
					Clock.schedule_once(self.action_strobe1)
					Clock.schedule_once(self.action_strobe1, self.timebox.t18)

				if (self.time_m*60 + self.time_s) - self.timebox.t19 > 5:
					self.strobe_music_event = Clock.schedule_once(self.strobe_music_play, self.timebox.t19 - self.timebox.t20)
					self.strobe_event = Clock.schedule_once(self.strobe_activation, self.timebox.t19)

			elif self.order_strobe == 2:
				self.order_strobe+=1
				if self.bonuses['strobes']:
					Clock.schedule_once(self.action_strobe2)
					Clock.schedule_once(self.action_strobe2, self.timebox.t18)

				if (self.time_m*60 + self.time_s) - self.timebox.t19 > 5:
					self.strobe_music_event = Clock.schedule_once(self.strobe_music_play, self.timebox.t19 - self.timebox.t20)
					self.strobe_event = Clock.schedule_once(self.strobe_activation, self.timebox.t19)

			elif self.order_strobe == 3:
				self.order_strobe=1
				if self.bonuses['strobes']:
					Clock.schedule_once(self.action_strobe3)
					Clock.schedule_once(self.action_strobe3, self.timebox.t18)

				if (self.time_m*60 + self.time_s) - self.timebox.t19 > 5:
					self.strobe_music_event = Clock.schedule_once(self.strobe_music_play, self.timebox.t19 - self.timebox.t20)
					self.strobe_event = Clock.schedule_once(self.strobe_activation, self.timebox.t19)


	def lamp_activation(self, dt):
		if self.RUNSTOP:
			if self.order % 60 == 1:
				self.order+=3

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv7)
					Clock.schedule_once(self.action_uv4, self.bonus_time)
					Clock.schedule_once(self.action_uv7, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*3 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*3)

			elif self.order % 60 == 4:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv3)
					Clock.schedule_once(self.action_uv3, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 5:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv6)
					Clock.schedule_once(self.action_uv6, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 6:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv9)
					Clock.schedule_once(self.action_uv9, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*2)

			elif self.order % 60 == 8:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv5)
					Clock.schedule_once(self.action_uv5, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*2)

			elif self.order % 60 == 10:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv7)
					Clock.schedule_once(self.action_uv7, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 11:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv4, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 12:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv2)
					Clock.schedule_once(self.action_uv2, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 13:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv1)
					Clock.schedule_once(self.action_uv8)
					Clock.schedule_once(self.action_uv1, self.bonus_time)
					Clock.schedule_once(self.action_uv8, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 14:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv6)
					Clock.schedule_once(self.action_uv6, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 15:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv3)
					Clock.schedule_once(self.action_uv3, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 16:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv7)
					Clock.schedule_once(self.action_uv7, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*2)

			elif self.order % 60 == 18:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv9)
					Clock.schedule_once(self.action_uv9, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 19:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv4, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*2)

			elif self.order % 60 == 21:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv2)
					Clock.schedule_once(self.action_uv8)
					Clock.schedule_once(self.action_uv2, self.bonus_time)
					Clock.schedule_once(self.action_uv8, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 22:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv5)
					Clock.schedule_once(self.action_uv5, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 23:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv1)
					Clock.schedule_once(self.action_uv1, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 24:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv2)
					Clock.schedule_once(self.action_uv6)
					Clock.schedule_once(self.action_uv2, self.bonus_time)
					Clock.schedule_once(self.action_uv6, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 25:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv3)
					Clock.schedule_once(self.action_uv3, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 26:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv4, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 27:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv5)
					Clock.schedule_once(self.action_uv5, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 28:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv6)
					Clock.schedule_once(self.action_uv6, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 29:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv3)
					Clock.schedule_once(self.action_uv7)
					Clock.schedule_once(self.action_uv3, self.bonus_time)
					Clock.schedule_once(self.action_uv7, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 30:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv1)
					Clock.schedule_once(self.action_uv8)
					Clock.schedule_once(self.action_uv1, self.bonus_time)
					Clock.schedule_once(self.action_uv8, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 31:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv9)
					Clock.schedule_once(self.action_uv9, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*2)

			elif self.order % 60 == 33:
				self.order+=3

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv2)
					Clock.schedule_once(self.action_uv6)
					Clock.schedule_once(self.action_uv2, self.bonus_time)
					Clock.schedule_once(self.action_uv6, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*3 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*3)

			elif self.order % 60 == 36:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv4, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 37:
				self.order+=3

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv1)
					Clock.schedule_once(self.action_uv3)
					Clock.schedule_once(self.action_uv5)
					Clock.schedule_once(self.action_uv7)
					Clock.schedule_once(self.action_uv9)
					Clock.schedule_once(self.action_uv1, self.bonus_time)
					Clock.schedule_once(self.action_uv3, self.bonus_time)
					Clock.schedule_once(self.action_uv5, self.bonus_time)
					Clock.schedule_once(self.action_uv7, self.bonus_time)
					Clock.schedule_once(self.action_uv9, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*3 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*3)

			elif self.order % 60 == 40:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv7)
					Clock.schedule_once(self.action_uv7, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 41:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv1)
					Clock.schedule_once(self.action_uv1, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 42:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv5)
					Clock.schedule_once(self.action_uv8)
					Clock.schedule_once(self.action_uv5, self.bonus_time)
					Clock.schedule_once(self.action_uv8, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 43:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv2)
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv2, self.bonus_time)
					Clock.schedule_once(self.action_uv4, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 44:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv9)
					Clock.schedule_once(self.action_uv9, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*2)

			elif self.order % 60 == 46:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv3)
					Clock.schedule_once(self.action_uv6)
					Clock.schedule_once(self.action_uv3, self.bonus_time)
					Clock.schedule_once(self.action_uv6, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*2)

			elif self.order % 60 == 48:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv8)
					Clock.schedule_once(self.action_uv4, self.bonus_time)
					Clock.schedule_once(self.action_uv8, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 50:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv3)
					Clock.schedule_once(self.action_uv7)
					Clock.schedule_once(self.action_uv3, self.bonus_time)
					Clock.schedule_once(self.action_uv7, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 51:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv1)
					Clock.schedule_once(self.action_uv5)
					Clock.schedule_once(self.action_uv1, self.bonus_time)
					Clock.schedule_once(self.action_uv5, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*2)

			elif self.order % 60 == 53:
				self.order+=2

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv9)
					Clock.schedule_once(self.action_uv4, self.bonus_time)
					Clock.schedule_once(self.action_uv9, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*2 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*2)

			elif self.order % 60 == 55:
				self.order+=3

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv2)
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv6)
					Clock.schedule_once(self.action_uv8)
					Clock.schedule_once(self.action_uv2, self.bonus_time)
					Clock.schedule_once(self.action_uv4, self.bonus_time)
					Clock.schedule_once(self.action_uv6, self.bonus_time)
					Clock.schedule_once(self.action_uv8, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time*3 > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time*3)

			elif self.order % 60 == 58:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv1)
					Clock.schedule_once(self.action_uv4)
					Clock.schedule_once(self.action_uv1, self.bonus_time)
					Clock.schedule_once(self.action_uv4, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 59:
				self.order+=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv6)
					Clock.schedule_once(self.action_uv6, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)

			elif self.order % 60 == 0:
				self.order=1

				if self.bonuses["UVlamps"] and not self.fan_strobe:
					Clock.schedule_once(self.action_uv2)
					Clock.schedule_once(self.action_uv8)
					Clock.schedule_once(self.action_uv2, self.bonus_time)
					Clock.schedule_once(self.action_uv8, self.bonus_time)

				if (self.time_m*60 + self.time_s) - self.UV_activation_time > self.UV_activation_time:
					self.uv_event = Clock.schedule_once(self.lamp_activation, self.UV_activation_time)



	def action_shadow(self, dt):
		try:
			self.shadow = not self.shadow

			if self.shadow:
				print("on shadow")
				s.connection[0].send("SH1;".encode('utf-8'))
			else:
				print("off shadow")
				s.connection[0].send("SH0;".encode('utf-8'))
		except:
			self.shadow = not self.shadow


	def action_runstop_lamp(self, dt):
		try:
			self.RunStopLamp = not self.RunStopLamp

			if self.RunStopLamp:
				print("on RunStopLamp")
				s.connection[0].send("RS1;".encode('utf-8'))
			else:
				print("off RunStopLamp")
				s.connection[0].send("RS0;".encode('utf-8'))
		except:
			self.RunStopLamp = not self.RunStopLamp


	def action_shadow_lamp(self, dt):
		try:
			self.ShadowLamp = not self.ShadowLamp

			if self.ShadowLamp:
				print("on ShadowLamp")
				s.connection[0].send("SL1;".encode('utf-8'))
			else:
				print("off ShadowLamp")
				s.connection[0].send("SL0;".encode('utf-8'))
		except:
			self.ShadowLamp = not self.ShadowLamp


	def action_uv1(self, dt):
		try:
			if not self.staticUV[0]:
				self.UVlamps[0] = not self.UVlamps[0]

			if self.UVlamps[0]:
				print("on uv1")
				s.connection[0].send("U11;".encode('utf-8'))
			elif not self.staticUV[0]:
				print("off uv1")
				s.connection[0].send("U10;".encode('utf-8'))
		except:
			self.bt_reset_press()

	def action_uv2(self, dt):
		try:
			if not self.staticUV[1]:
				self.UVlamps[1] = not self.UVlamps[1]

			if self.UVlamps[1]:
				print("on uv2")
				s.connection[0].send("U21;".encode('utf-8'))
			elif not self.staticUV[1]:
				print("off uv2")
				s.connection[0].send("U20;".encode('utf-8'))
		except:
			self.bt_reset_press()

	def action_uv3(self, dt):
		try:
			if not self.staticUV[2]:
				self.UVlamps[2] = not self.UVlamps[2]

			if self.UVlamps[2]:
				print("on uv3")
				s.connection[0].send("U31;".encode('utf-8'))
			elif not self.staticUV[2]:
				print("off uv3")
				s.connection[0].send("U30;".encode('utf-8'))
		except:
			self.bt_reset_press()

	def action_uv4(self, dt):
		try:
			if not self.staticUV[3]:
				self.UVlamps[3] = not self.UVlamps[3]

			if self.UVlamps[3]:
				print("on uv4")
				s.connection[0].send("U41;".encode('utf-8'))
			elif not self.staticUV[3]:
				print("off uv4")
				s.connection[0].send("U40;".encode('utf-8'))
		except:
			self.bt_reset_press()

	def action_uv5(self, dt):
		try:
			if not self.staticUV[4]:
				self.UVlamps[4] = not self.UVlamps[4]

			if self.UVlamps[4]:
				print("on uv5")
				s.connection[0].send("U51;".encode('utf-8'))
			elif not self.staticUV[4]:
				print("off uv5")
				s.connection[0].send("U50;".encode('utf-8'))
		except:
			self.bt_reset_press()

	def action_uv6(self, dt):
		try:
			if not self.staticUV[5]:
				self.UVlamps[5] = not self.UVlamps[5]

			if self.UVlamps[5]:
				print("on uv6")
				s.connection[0].send("U61;".encode('utf-8'))
			elif not self.staticUV[5]:
				print("off uv6")
				s.connection[0].send("U60;".encode('utf-8'))
		except:
			self.bt_reset_press()

	def action_uv7(self, dt):
		try:
			if not self.staticUV[6]:
				self.UVlamps[6] = not self.UVlamps[6]

			if self.UVlamps[6]:
				print("on uv7")
				s.connection[0].send("U71;".encode('utf-8'))
			elif not self.staticUV[6]:
				print("off uv7")
				s.connection[0].send("U70;".encode('utf-8'))
		except:
			self.bt_reset_press()

	def action_uv8(self, dt):
		try:
			if not self.staticUV[7]:
				self.UVlamps[7] = not self.UVlamps[7]

			if self.UVlamps[7]:
				print("on uv8")
				s.connection[0].send("U81;".encode('utf-8'))
			elif not self.staticUV[7]:
				print("off uv8")
				s.connection[0].send("U80;".encode('utf-8'))
		except:
			self.bt_reset_press()

	def action_uv9(self, dt):
		try:
			if not self.staticUV[8]:
				self.UVlamps[8] = not self.UVlamps[8]

			if self.UVlamps[8]:
				print("on uv9")
				s.connection[0].send("U91;".encode('utf-8'))
			elif not self.staticUV[8]:
				print("off uv9")
				s.connection[0].send("U90;".encode('utf-8'))
		except:
			self.bt_reset_press()


	def action_strobe1(self, dt):
		try:
			self.Strobes[0] = not self.Strobes[0]

			if self.Strobes[0]:
				print("on strobe1")
				s.connection[0].send("S11;".encode('utf-8'))

				self.fan_strobe = True
				self.off_UV_lamps()
			else:
				print("off strobe1")
				s.connection[0].send("S10;".encode('utf-8'))
				self.fan_strobe = False
		except:
			self.Strobes[0] = not self.Strobes[0]

	def action_strobe2(self, dt):
		try:
			self.Strobes[1] = not self.Strobes[1]

			if self.Strobes[1]:
				print("on strobe2")
				s.connection[0].send("S21;".encode('utf-8'))

				self.fan_strobe = True
				self.off_UV_lamps()
			else:
				print("off strobe2")
				s.connection[0].send("S20;".encode('utf-8'))
				self.fan_strobe = False
		except:
			self.Strobes[1] = not self.Strobes[1]

	def action_strobe3(self, dt):
		try:
			self.Strobes[2] = not self.Strobes[2]

			if self.Strobes[2]:
				print("on strobe3")
				s.connection[0].send("S31;".encode('utf-8'))

				self.fan_strobe = True
				self.off_UV_lamps()
			else:
				print("off strobe3")
				s.connection[0].send("S30;".encode('utf-8'))
				self.fan_strobe = False
		except:
			self.Strobes[2] = not self.Strobes[2]


	def action_fan1(self, dt):
		try:
			self.Fans[0] = not self.Fans[0]

			if self.Fans[0]:
				print("on fan1")
				s.connection[0].send("F11;".encode('utf-8'))

				self.fan_strobe = True
				self.off_UV_lamps()
			else:
				print("off fan1")
				s.connection[0].send("F10;".encode('utf-8'))
				self.fan_strobe = False
		except:
			self.Fans[0] = not self.Fans[0]

	def action_fan2(self, dt):
		try:
			self.Fans[1] = not self.Fans[1]

			if self.Fans[1]:
				print("on fan2")
				s.connection[0].send("F21;".encode('utf-8'))

				self.fan_strobe = True
				self.off_UV_lamps()
			else:
				print("off fan2")
				s.connection[0].send("F20;".encode('utf-8'))
				self.fan_strobe = False
		except:
			self.Fans[1] = not self.Fans[1]

	def action_fan3(self, dt):
		try:
			self.Fans[2] = not self.Fans[2]

			if self.Fans[2]:
				print("on fan3")
				s.connection[0].send("F31;".encode('utf-8'))

				self.fan_strobe = True
				self.off_UV_lamps()
			else:
				print("off fan3")
				s.connection[0].send("F30;".encode('utf-8'))
				self.fan_strobe = False
		except:
			self.Fans[2] = not self.Fans[2]

	def action_fan4(self, dt):
		try:
			self.Fans[3] = not self.Fans[3]

			if self.Fans[3]:
				print("on fan4")
				s.connection[0].send("F41;".encode('utf-8'))

				self.fan_strobe = True
				self.off_UV_lamps()
			else:
				print("off fan4")
				s.connection[0].send("F40;".encode('utf-8'))
				self.fan_strobe = False
		except:
			self.Fans[3] = not self.Fans[3]


	def off_UV_lamps(self):
		try:
			s.connection[0].send("U10;".encode('utf-8'))
			s.connection[0].send("U20;".encode('utf-8'))
			s.connection[0].send("U30;".encode('utf-8'))
			s.connection[0].send("U40;".encode('utf-8'))
			s.connection[0].send("U50;".encode('utf-8'))
			s.connection[0].send("U60;".encode('utf-8'))
			s.connection[0].send("U70;".encode('utf-8'))
			s.connection[0].send("U80;".encode('utf-8'))
			s.connection[0].send("U90;".encode('utf-8'))
		except:
			pass

	def off_fans(self):
		try:
			s.connection[0].send("F10;".encode('utf-8'))
			s.connection[0].send("F20;".encode('utf-8'))
			s.connection[0].send("F30;".encode('utf-8'))
			s.connection[0].send("F40;".encode('utf-8'))
		except:
			pass

	def off_strobes(self):
		try:
			s.connection[0].send("S10;".encode('utf-8'))
			s.connection[0].send("S20;".encode('utf-8'))
			s.connection[0].send("S30;".encode('utf-8'))
		except:
			pass

		
	def off_all(self):
		self.off_UV_lamps()
		self.off_fans()
		self.off_strobes()


	def music_play(self, dt):
		try:
			if self.RUNSTOP:
				if self.scripts == 0:
					if self.order_music == 1:
						self.order_music+=1

						s.connection[0].send("M11;".encode('utf-8'))
						self.music_play_event = Clock.schedule_once(self.music_play, 6)

					elif self.order_music == 2:
						self.order_music+=1
						
						tmp = random.randint(1,4)
						if tmp == 1:
							s.connection[0].send("M21;".encode('utf-8'))
						elif tmp == 2:
							s.connection[0].send("M31;".encode('utf-8'))
						elif tmp == 3:
							s.connection[0].send("M41;".encode('utf-8'))
						elif tmp == 4:
							s.connection[0].send("M51;".encode('utf-8'))

						if self.time_m*60 + self.time_s > 15*60:
							self.order_music-=1
							self.music_play_event = Clock.schedule_once(self.music_play, 15*60 - 0.1)
						else:
							self.music_play_event = Clock.schedule_once(self.music_play, self.time_m*60 + self.time_s - 0.1)

					elif self.order_music == 3:
						self.order_music=1

				elif self.scripts == 1:
					if self.order_music == 1:
						self.order_music+=1
						
						s.connection[0].send("M71;".encode('utf-8'))
						self.music_play_event = Clock.schedule_once(self.music_play, 11)

					elif self.order_music == 2:
						self.order_music+=1
						
						tmp = random.randint(1,4)
						if tmp == 1:
							s.connection[0].send("M81;".encode('utf-8'))
						elif tmp == 2:
							s.connection[0].send("M91;".encode('utf-8'))
						elif tmp == 3:
							s.connection[0].send("MA1;".encode('utf-8'))
						elif tmp == 4:
							s.connection[0].send("MB1;".encode('utf-8'))

						if self.time_m*60 + self.time_s> 15*60:
							self.order_music-=1
							self.music_play_event = Clock.schedule_once(self.music_play, 15*60 - 0.1)
						else:
							self.music_play_event = Clock.schedule_once(self.music_play, self.time_m*60 + self.time_s - 0.1)

					elif self.order_music == 3:
						self.order_music=1
		except:
			pass


	def start_game(self, dt):
		if self.RUNSTOP:
			if self.time_m != 0 or self.time_s != 0:
				if self.timer_on != None:
					self.timer_on.cancel()
				self.timer_on = Clock.schedule_interval(self.timer_run, 1)
				self.action_shadow_lamp(0)

		if self.music_play_event != None:
			self.music_play_event.cancel()
		self.music_play_event = Clock.schedule_once(self.music_play)

		if self.uv_event != None:
			self.uv_event.cancel()
		if self.RUNSTOP:
			self.uv_event = Clock.schedule_once(self.lamp_activation)

		if self.strobe_event != None:
			self.strobe_event.cancel()
		if self.strobe_music_event != None:
			self.strobe_music_event.cancel()			
		if self.RUNSTOP:
			self.strobe_music_event = Clock.schedule_once(self.strobe_music_play, self.timebox.t19 - self.timebox.t20)
			self.strobe_event = Clock.schedule_once(self.strobe_activation, self.timebox.t19)

			if self.scripts == 0:
				self.shadow_lamp_enent = Clock.schedule_once(self.shadow_lamp_activation, self.time_m*60 + self.time_s - self.timebox.t4)

			elif self.scripts == 1:
				self.shadow_lamp_enent = Clock.schedule_once(self.shadow_lamp_activation, self.time_m*60 + self.time_s - self.timebox.t9)


	def stop_events(self, dt):
		if self.start_event != None:
			self.start_event.cancel()

		if self.timer_on != None:
			self.timer_on.cancel()

		if self.music_play_event != None:
			self.music_play_event.cancel()

		if self.uv_event != None:
			self.uv_event.cancel()

		if self.strobe_event != None:
			self.strobe_event.cancel()

		if self.strobe_music_event != None:
			self.strobe_music_event.cancel()

		if self.shadow_lamp_enent != None:
			self.shadow_lamp_enent.cancel()

		if self.shadow_event != None:
			self.action_shadow(0)
			self.shadow_event.cancel()

		if self.ShadowLamp:
			self.action_shadow_lamp(0)

		if self.RunStopLamp:
			self.action_runstop_lamp(0)

		try:
			s.connection[0].send("M00;".encode('utf-8'))
		except:
			pass

		if self.RUNSTOP:
			self.play_end_music()


	def play_end_music(self):
		try:
			if self.scripts == 0:
				s.connection[0].send("M61;".encode('utf-8'))

			if self.scripts == 1:
				s.connection[0].send("MC1;".encode('utf-8'))
		except:
			pass


	def set_dinamic_OnOff(self):
		self.runstop_off.background_disabled_normal = "red.jpg"
		self.runstop_off.background_normal = "off.jpg"
		self.runstop_on.background_disabled_normal = "green.jpg"
		self.runstop_on.background_normal = "on.jpg"

		self.shadow_off.background_disabled_normal = "red.jpg"
		self.shadow_off.background_normal = "off.jpg"
		self.shadow_on.background_disabled_normal = "green.jpg"
		self.shadow_on.background_normal = "on.jpg"

		self.strobe1_off.background_disabled_normal = "red.jpg"
		self.strobe1_off.background_normal = "off.jpg"
		self.strobe1_on.background_disabled_normal = "green.jpg"
		self.strobe1_on.background_normal = "on.jpg"

		self.strobe2_off.background_disabled_normal = "red.jpg"
		self.strobe2_off.background_normal = "off.jpg"
		self.strobe2_on.background_disabled_normal = "green.jpg"
		self.strobe2_on.background_normal = "on.jpg"

		self.strobe3_off.background_disabled_normal = "red.jpg"
		self.strobe3_off.background_normal = "off.jpg"
		self.strobe3_on.background_disabled_normal = "green.jpg"
		self.strobe3_on.background_normal = "on.jpg"

		self.fan1_off.background_disabled_normal = "red.jpg"
		self.fan1_off.background_normal = "off.jpg"
		self.fan1_on.background_disabled_normal = "green.jpg"
		self.fan1_on.background_normal = "on.jpg"

		self.fan2_off.background_disabled_normal = "red.jpg"
		self.fan2_off.background_normal = "off.jpg"
		self.fan2_on.background_disabled_normal = "green.jpg"
		self.fan2_on.background_normal = "on.jpg"

		self.fan3_off.background_disabled_normal = "red.jpg"
		self.fan3_off.background_normal = "off.jpg"
		self.fan3_on.background_disabled_normal = "green.jpg"
		self.fan3_on.background_normal = "on.jpg"

		self.fan4_off.background_disabled_normal = "red.jpg"
		self.fan4_off.background_normal = "off.jpg"
		self.fan4_on.background_disabled_normal = "green.jpg"
		self.fan4_on.background_normal = "on.jpg"

		self.uv1_off.background_disabled_normal = "red.jpg"
		self.uv1_off.background_normal = "off.jpg"
		self.uv1_on.background_disabled_normal = "green.jpg"
		self.uv1_on.background_normal = "on.jpg"

		self.uv2_off.background_disabled_normal = "red.jpg"
		self.uv2_off.background_normal = "off.jpg"
		self.uv2_on.background_disabled_normal = "green.jpg"
		self.uv2_on.background_normal = "on.jpg"

		self.uv3_off.background_disabled_normal = "red.jpg"
		self.uv3_off.background_normal = "off.jpg"
		self.uv3_on.background_disabled_normal = "green.jpg"
		self.uv3_on.background_normal = "on.jpg"

		self.uv4_off.background_disabled_normal = "red.jpg"
		self.uv4_off.background_normal = "off.jpg"
		self.uv4_on.background_disabled_normal = "green.jpg"
		self.uv4_on.background_normal = "on.jpg"

		self.uv5_off.background_disabled_normal = "red.jpg"
		self.uv5_off.background_normal = "off.jpg"
		self.uv5_on.background_disabled_normal = "green.jpg"
		self.uv5_on.background_normal = "on.jpg"

		self.uv6_off.background_disabled_normal = "red.jpg"
		self.uv6_off.background_normal = "off.jpg"
		self.uv6_on.background_disabled_normal = "green.jpg"
		self.uv6_on.background_normal = "on.jpg"

		self.uv7_off.background_disabled_normal = "red.jpg"
		self.uv7_off.background_normal = "off.jpg"
		self.uv7_on.background_disabled_normal = "green.jpg"
		self.uv7_on.background_normal = "on.jpg"

		self.uv8_off.background_disabled_normal = "red.jpg"
		self.uv8_off.background_normal = "off.jpg"
		self.uv8_on.background_disabled_normal = "green.jpg"
		self.uv8_on.background_normal = "on.jpg"

		self.uv9_off.background_disabled_normal = "red.jpg"
		self.uv9_off.background_normal = "off.jpg"
		self.uv9_on.background_disabled_normal = "green.jpg"
		self.uv9_on.background_normal = "on.jpg"


	def set_static_OnOff(self):
		if self.RunStopLamp:
			self.runstop_off.background_disabled_normal = "off.jpg"
			self.runstop_on.background_disabled_normal = "green.jpg"
		else:
			self.runstop_off.background_disabled_normal = "red.jpg"
			self.runstop_on.background_disabled_normal = "on.jpg"

		if self.ShadowLamp:
			self.shadow_off.background_disabled_normal = "off.jpg"
			self.shadow_on.background_disabled_normal = "green.jpg"
		else:
			self.shadow_off.background_disabled_normal = "red.jpg"
			self.shadow_on.background_disabled_normal = "on.jpg"

		if self.Strobes[0]:
			self.strobe1_off.background_disabled_normal = "off.jpg"
			self.strobe1_on.background_disabled_normal = "green.jpg"
		else:
			self.strobe1_off.background_disabled_normal = "red.jpg"
			self.strobe1_on.background_disabled_normal = "on.jpg"

		if self.Strobes[1]:
			self.strobe2_off.background_disabled_normal = "off.jpg"
			self.strobe2_on.background_disabled_normal = "green.jpg"
		else:
			self.strobe2_off.background_disabled_normal = "red.jpg"
			self.strobe2_on.background_disabled_normal = "on.jpg"

		if self.Strobes[2]:
			self.strobe3_off.background_disabled_normal = "off.jpg"
			self.strobe3_on.background_disabled_normal = "green.jpg"
		else:
			self.strobe3_off.background_disabled_normal = "red.jpg"
			self.strobe3_on.background_disabled_normal = "on.jpg"

		if self.Fans[0]:
			self.fan1_off.background_disabled_normal = "off.jpg"
			self.fan1_on.background_disabled_normal = "green.jpg"
		else:
			self.fan1_off.background_disabled_normal = "red.jpg"
			self.fan1_on.background_disabled_normal = "on.jpg"

		if self.Fans[1]:
			self.fan2_off.background_disabled_normal = "off.jpg"
			self.fan2_on.background_disabled_normal = "green.jpg"
		else:
			self.fan2_off.background_disabled_normal = "red.jpg"
			self.fan2_on.background_disabled_normal = "on.jpg"

		if self.Fans[2]:
			self.fan3_off.background_disabled_normal = "off.jpg"
			self.fan3_on.background_disabled_normal = "green.jpg"
		else:
			self.fan3_off.background_disabled_normal = "red.jpg"
			self.fan3_on.background_disabled_normal = "on.jpg"

		if self.Fans[3]:
			self.fan4_off.background_disabled_normal = "off.jpg"
			self.fan4_on.background_disabled_normal = "green.jpg"
		else:
			self.fan4_off.background_disabled_normal = "red.jpg"
			self.fan4_on.background_disabled_normal = "on.jpg"

		if self.UVlamps[0]:
			self.uv1_off.background_disabled_normal = "off.jpg"
			self.uv1_on.background_disabled_normal = "green.jpg"
		else:
			self.uv1_off.background_disabled_normal = "red.jpg"
			self.uv1_on.background_disabled_normal = "on.jpg"

		if self.UVlamps[1]:
			self.uv2_off.background_disabled_normal = "off.jpg"
			self.uv2_on.background_disabled_normal = "green.jpg"
		else:
			self.uv2_off.background_disabled_normal = "red.jpg"
			self.uv2_on.background_disabled_normal = "on.jpg"

		if self.UVlamps[2]:
			self.uv3_off.background_disabled_normal = "off.jpg"
			self.uv3_on.background_disabled_normal = "green.jpg"
		else:
			self.uv3_off.background_disabled_normal = "red.jpg"
			self.uv3_on.background_disabled_normal = "on.jpg"

		if self.UVlamps[3]:
			self.uv4_off.background_disabled_normal = "off.jpg"
			self.uv4_on.background_disabled_normal = "green.jpg"
		else:
			self.uv4_off.background_disabled_normal = "red.jpg"
			self.uv4_on.background_disabled_normal = "on.jpg"

		if self.UVlamps[4]:
			self.uv5_off.background_disabled_normal = "off.jpg"
			self.uv5_on.background_disabled_normal = "green.jpg"
		else:
			self.uv5_off.background_disabled_normal = "red.jpg"
			self.uv5_on.background_disabled_normal = "on.jpg"

		if self.UVlamps[5]:
			self.uv6_off.background_disabled_normal = "off.jpg"
			self.uv6_on.background_disabled_normal = "green.jpg"
		else:
			self.uv6_off.background_disabled_normal = "red.jpg"
			self.uv6_on.background_disabled_normal = "on.jpg"

		if self.UVlamps[6]:
			self.uv7_off.background_disabled_normal = "off.jpg"
			self.uv7_on.background_disabled_normal = "green.jpg"
		else:
			self.uv7_off.background_disabled_normal = "red.jpg"
			self.uv7_on.background_disabled_normal = "on.jpg"

		if self.UVlamps[7]:
			self.uv8_off.background_disabled_normal = "off.jpg"
			self.uv8_on.background_disabled_normal = "green.jpg"
		else:
			self.uv8_off.background_disabled_normal = "red.jpg"
			self.uv8_on.background_disabled_normal = "on.jpg"

		if self.UVlamps[8]:
			self.uv9_off.background_disabled_normal = "off.jpg"
			self.uv9_on.background_disabled_normal = "green.jpg"
		else:
			self.uv9_off.background_disabled_normal = "red.jpg"
			self.uv9_on.background_disabled_normal = "on.jpg"

	def exit(self):
		pass


class MyApp(App):
	def build(self):
		return Tab()


if __name__ == "__main__":
	#Window.fullscreen = True
	
	s = Server()
	threading.Thread(target=s.serverFunction, daemon=True).start()
	MyApp().run()