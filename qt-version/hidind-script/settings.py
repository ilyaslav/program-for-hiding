from database import Database
from rpiPing import PingRpi

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
order_fans = [0, 0, 0, 0]
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
fans_run_time = [0, 0, 0, 0]
fan_strobe = False
staticUV = [False, False, False, False, False, False, False, False, False]

outs = {
    "r1:y1": False,  # RunStopLamp
    "r1:y2": False,  # ShadowLamp
    "r1:y3": False,  # UVlamps
    "r1:y4": False,  # UVlamps
    "r1:y5": False,  # UVlamps
    "r1:y6": False,  # UVlamps
    "r1:y7": False,  # UVlamps
    "r1:y8": False,  # UVlamps
    "r1:y9": False,  # UVlamps
    "r1:y10": False,  # UVlamps
    "r1:y11": False,  # UVlamps
    "r1:y12": False,  # Fans
    "r1:y13": False,  # Fans
    "r1:y14": False,  # Fans
    "r1:y15": False,  # Fans
    "r1:y16": False,  # Strobes
    "r1:y17": False,  # Strobes
    "r1:y18": False,  # Strobes
    "r1:y19": False,  # Souls
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
    "r2:y38": True,
    "r3:y1": False,
    "r3:y2": False,
    "r3:y38": True,
}
inputs = {
    "r1:x1": False,
    "r1:x2": False,
    "r1:x3": False,
    "r1:x4": False,
    "r1:x5": False,
    "r1:x40": True,
    "r2:x1": False,
    "r2:x40": False,
    "r3:x1": False,
    "r3:x2": False,
    "r3:x40": False,
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

pings = {
    'r1': PingRpi('r1'),
    'r2': PingRpi('r2'),
    'r3': PingRpi('r3'),
}

button_config = [
    {'outputs': ['r1:y1'], 'tab': 'tab_diagnostic', 'buttons': ['bt_start_off', 'bt_start_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y2'], 'tab': 'tab_diagnostic', 'buttons': ['bt_shadow_off', 'bt_shadow_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y16'], 'tab': 'tab_diagnostic', 'buttons': ['bt_strobe1_off', 'bt_strobe1_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y17'], 'tab': 'tab_diagnostic', 'buttons': ['bt_strobe2_off', 'bt_strobe2_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y18'], 'tab': 'tab_diagnostic', 'buttons': ['bt_strobe3_off', 'bt_strobe3_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y12'], 'tab': 'tab_diagnostic', 'buttons': ['bt_fan1_off', 'bt_fan1_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y13'], 'tab': 'tab_diagnostic', 'buttons': ['bt_fan2_off', 'bt_fan2_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y14'], 'tab': 'tab_diagnostic', 'buttons': ['bt_fan3_off', 'bt_fan3_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y15'], 'tab': 'tab_diagnostic', 'buttons': ['bt_fan4_off', 'bt_fan4_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y3'], 'tab': 'tab_diagnostic', 'buttons': ['bt_uv1_off', 'bt_uv1_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y4'], 'tab': 'tab_diagnostic', 'buttons': ['bt_uv2_off', 'bt_uv2_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y5'], 'tab': 'tab_diagnostic', 'buttons': ['bt_uv3_off', 'bt_uv3_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y6'], 'tab': 'tab_diagnostic', 'buttons': ['bt_uv4_off', 'bt_uv4_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y7'], 'tab': 'tab_diagnostic', 'buttons': ['bt_uv5_off', 'bt_uv5_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y8'], 'tab': 'tab_diagnostic', 'buttons': ['bt_uv6_off', 'bt_uv6_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y9'], 'tab': 'tab_diagnostic', 'buttons': ['bt_uv7_off', 'bt_uv7_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y10'], 'tab': 'tab_diagnostic', 'buttons': ['bt_uv8_off', 'bt_uv8_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y11'], 'tab': 'tab_diagnostic', 'buttons': ['bt_uv9_off', 'bt_uv9_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y19'], 'tab': 'tab_diagnostic', 'buttons': ['bt_shadow_box_off', 'bt_shadow_box_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r1:y38'], 'tab': 'tab_diagnostic', 'buttons': ['bt_ping_off', 'bt_ping_on', None], 'logic': 'standard', 'inverted': False},

    {'outputs': ['r2:y1'], 'tab': 'tab_diagnostic_r2', 'buttons': ['spot_off', 'spot_on', None], 'logic': 'standard', 'inverted': True},
    {'outputs': ['r2:y16'], 'tab': 'tab_diagnostic_r2', 'buttons': ['blinker_off', 'blinker_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r2:y17'], 'tab': 'tab_diagnostic_r2', 'buttons': ['animator_start_off', 'animator_start_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r2:y38'], 'tab': 'tab_diagnostic_r2', 'buttons': ['ping_off', 'ping_on', None], 'logic': 'standard', 'inverted': True},
    # Специальные кнопки с blink
    {'outputs': ['r2:y2', 'r2:y3'], 'tab': 'tab_diagnostic_r2', 'buttons': ['light1_off', 'light1_on', 'light1_blink'], 'logic': 'special', 'inverted': False},
    {'outputs': ['r2:y4', 'r2:y5'], 'tab': 'tab_diagnostic_r2', 'buttons': ['light2_off', 'light2_on', 'light2_blink'], 'logic': 'special', 'inverted': False},
    {'outputs': ['r2:y6', 'r2:y7'], 'tab': 'tab_diagnostic_r2', 'buttons': ['light3_off', 'light3_on', 'light3_blink'], 'logic': 'special', 'inverted': False},
    {'outputs': ['r2:y8', 'r2:y9'], 'tab': 'tab_diagnostic_r2', 'buttons': ['light4_off', 'light4_on', 'light4_blink'], 'logic': 'special', 'inverted': False},
    {'outputs': ['r2:y10', 'r2:y11'], 'tab': 'tab_diagnostic_r2', 'buttons': ['light5_off', 'light5_on', 'light5_blink'], 'logic': 'special', 'inverted': False},
    {'outputs': ['r2:y12', 'r2:y13'], 'tab': 'tab_diagnostic_r2', 'buttons': ['light6_off', 'light6_on', 'light6_blink'], 'logic': 'special', 'inverted': False},
    {'outputs': ['r2:y14', 'r2:y18'], 'tab': 'tab_diagnostic_r2', 'buttons': ['light7_off', 'light7_on', 'light7_blink'], 'logic': 'special', 'inverted': False},

    {'outputs': ['r3:y1'], 'tab': 'tab_diagnostic_r3', 'buttons': ['mask_off', 'mask_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r3:y2'], 'tab': 'tab_diagnostic_r3', 'buttons': ['light_off', 'light_on', None], 'logic': 'standard', 'inverted': False},
    {'outputs': ['r3:y38'], 'tab': 'tab_diagnostic_r3', 'buttons': ['ping_off', 'ping_on', None], 'logic': 'standard', 'inverted': True},
]
