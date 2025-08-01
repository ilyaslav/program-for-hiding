from database import Database

db = Database("settings.db")
timebox = db.select_times()
volumes = db.select_volumes()

scripts = 0
timer = "10:00"
time = "10:00"
time_m = 10
time_s = 0

pressed_time = 0
timeUV_bt = [False, False, False]
UV_activation_time = timebox['t42']

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

oust1 = {
    "r1:y1": False,
    "r1:y2": False,
    "r1:y3": False,
    "r1:y4": False,
    "r1:y5": False,
    "r1:y6": False,
    "r1:y7": False,
    "r1:y8": False,
    "r1:y9": False,
    "r1:y10": False,
    "r1:y11": False,
    "r1:y12": False,
    "r1:y13": False,
    "r1:y14": False,
    "r1:y15": False,
    "r1:y16": False,
    "r1:y17": False,
    "r1:y18": False,
    "r1:y19": False,
    "r1:y38": False,
    "r2:y1": False,
    "r2:y2": False,
    "r2:y3": False,
    "r2:y4": False,
    "r2:y5": False,
    "r2:y6": False,
    "r2:y7": False,
    "r2:y8": False,
    "r2:y9": False,
    "r2:y10": False,
    "r2:y11": False,
    "r2:y12": False,
    "r2:y13": False,
    "r2:y14": False,
    "r2:y15": False,
    "r2:y16": False,
    "r2:y17": False,
    "r2:y18": False,
    "r2:y38": False,
    "r3:y1": False,
    "r3:y2": False,
    "r3:y38": False,
}
inputs1 = {
    "r1:x1": False,
    "r1:x2": False,
    "r1:x3": False,
    "r1:x4": False,
    "r1:x5": False,
    "r1:x40": False,
    "r2:x1": False,
    "r2:x40": False,
    "r3:x1": False,
    "r3:x2": False,
    "r3:x40": False,
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
