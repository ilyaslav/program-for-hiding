from TimeBox import TimeBox

timebox = TimeBox("Интервалы времени.txt")
scripts = 0
timer = "10:00"
time = "10:00"
time_m = 10
time_s = 0

pressed_time = 0
timeUV_bt = [False, False, False]
UV_activation_time = timebox.t21

order = 1
order_strobe = 1
order_music = 1
order_fans = [0,0,0,0]
bonuses = {
"UVlamps": False,
"fans": False,
"strobes": False,
"settings": False
}
for_kids = False
bonus_time = 1
runstop = False
start_run_time = -1
fans_run_time = [0,0,0,0]
fan_strobe = False
staticUV = [False, False, False, False, False, False, False, False, False]
outs = {
    'UVlamps': [False, False, False, False, False, False, False, False, False],
    'Strobes': [False, False, False],
    'Fans': [False, False, False, False],
    'ShadowLamp': False,
    'RunStopLamp':  False,
    'Souls': False
}
inputs = {
    'fans': [True, True, True, True],
    'runstop': True
}
game_status = False

uv_event = False
strobe_event = False
strobe_music_event = False
music_play_event = False
start_event = False
shadow_lamp_enent = False
shadow_event = False
timer_event = False
end_timer_event = False
time_event = False
