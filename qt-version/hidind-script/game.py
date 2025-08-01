import threading
import time
import random

import settings
from server import Server

class GameServer(Server): # TODO
    def message_handler(mes: str):
        if mes == 'F10':
            settings.inputs['fans'][0] = True
        elif mes == 'F11':
            settings.inputs['fans'][0] = False
        elif mes == 'F20':
            settings.inputs['fans'][1] = True
        elif mes == 'F21':
            settings.inputs['fans'][1] = False
        elif mes == 'F30':
            settings.inputs['fans'][2] = True
        elif mes == 'F31':
            settings.inputs['fans'][2] = False
        elif mes == 'F40':
            settings.inputs['fans'][3] = True
        elif mes == 'F41':
            settings.inputs['fans'][3] = False

        elif mes == 'RS0':
            settings.inputs['runstop'] = True
        elif mes == 'RS1':
            settings.inputs['runstop'] = False

game_server = Server()
threading.Thread(target=game_server.start_server, daemon=True).start()

def thread_wraper(func):
    def wraper(*args, **kwargs):
        try:
            threading.Thread(target=func, args=args, daemon=True).start()
        except:
            pass
    return wraper

def set_standard_settings():
    settings.scripts = 0
    settings.timer = "10:00"
    settings.time = "10:00"
    settings.time_m = 10
    settings.time_s = 0
    settings.pressed_time = 0
    settings.order = 1
    settings.order_strobe = 1
    settings.order_music = 1
    settings.order_fans = [0,0,0,0]
    settings.bonuses = {
    "UVlamps": False,
    "fans": False,
    "strobes": False,
    "settings": False
    }
    settings.for_kids = False
    settings.bonus_time = 1
    settings.runstop = False
    settings.start_run_time = -1
    settings.fans_run_time = [0,0,0,0]
    settings.fan_strobe = False
    settings.staticUV = [False, False, False, False, False, False, False, False, False]
    set_standart_outs()
    settings.inputs = {
        'fans': [True, True, True, True],
        'runstop': True
    }
    settings.game_status = False

def set_standart_outs():
    settings.outs = {
    'UVlamps': [False, False, False, False, False, False, False, False, False],
    'Strobes': [False, False, False],
    'Fans': [False, False, False, False],
    'ShadowLamp': False,
    'RunStopLamp':  False,
    'Souls': False
}

def check_start():
    if settings.inputs['runstop'] == False and not settings.game_status:
        settings.start_run_time = time.time()
        settings.game_status = True

    if settings.game_status:
        if settings.timebox['t1'] < time.time() - settings.start_run_time < settings.timebox['t1'] + 0.2:
            settings.game_status = False
            settings.start_run_time = -1
            return True

    if settings.inputs['runstop'] == True:
        settings.game_status = False
        settings.start_run_time = -1
        settings.pressed_time = time.time()

    return time.time() - settings.pressed_time > 7 and settings.runstop

def check_fans():
    for i in range(4):
        if not settings.inputs['fans'][i] and time.time() - settings.fans_run_time[i] > settings.timebox['t17']:
            settings.order_fans[i]+=1
            settings.fans_run_time[i] = time.time()

            if settings.order_fans[i] == 3:
                settings.order_fans[i]=0

                if i == 0:
                    if settings.bonuses["fans"]:
                        action_fan1(0)
                        action_fan1(4)
                if i == 1:
                    if settings.bonuses["fans"]:
                        action_fan2(0)
                        action_fan2(4)
                if i == 2:
                    if settings.bonuses["fans"]:
                        action_fan3(0)
                        action_fan3(4)
                if i == 3:
                    if settings.bonuses["fans"]:
                        action_fan4(0)
                        action_fan4(4)

def init_game():
    if settings.runstop:
        if settings.scripts == 0:
            settings.start_event = True
            start_game(settings.timebox['t2'])
            try:
                play_music("r1", 1)
            except:
                pass
        elif settings.scripts == 1:
            settings.start_event = True
            settings.shadow_event = True
            start_game(0)
            action_shadow(8)

@thread_wraper
def start_game(dt):
    try:
        while True:
            dt -= 0.1
            time.sleep(0.1)
            if not settings.start_event:
                return
            if dt <= 0:
                break
        settings.start_event = False
        if settings.runstop:
            if settings.time_m != 0 or settings.time_s != 0:
                settings.timer_event = True
                timer_run(1)
                action_shadow_lamp(0)

        settings.music_play_event = True
        music_play(0)

        if settings.runstop:
            settings.uv_event = True
            lamp_activation(0)

        if settings.runstop:
            settings.strobe_music_event = True
            settings.strobe_event = True
            strobe_music_play(settings.timebox['t19'] - settings.timebox['t20'])
            strobe_activation(settings.timebox['t19'])

            if settings.scripts == 0:
                settings.shadow_lamp_enent = True
                shadow_lamp_activation(settings.time_m*60 + settings.time_s - settings.timebox['t4'])

            elif settings.scripts == 1:
                settings.shadow_lamp_enent = True
                shadow_lamp_activation(settings.time_m*60 + settings.time_s - settings.timebox['t9'])
    except Exception as e:
        print(e)
@thread_wraper
def action_runstop_lamp(dt):
    try:
        time.sleep(dt)
        settings.outs['RunStopLamp'] = not settings.outs['RunStopLamp']
        if settings.outs['RunStopLamp']:
            print("on RunStopLamp")
            game_server.send_message("r1:y1:1;")
        else:
            print("off RunStopLamp")
            game_server.send_message("r1:y1:0;")
    except:
        settings.outs['RunStopLamp'] = not settings.outs['RunStopLamp']
@thread_wraper
def action_shadow_lamp(dt):
    try:
        time.sleep(dt)
        settings.outs['ShadowLamp'] = not settings.outs['ShadowLamp']
        if settings.outs['ShadowLamp']:
            print("on ShadowLamp")
            game_server.send_message("r1:y2:1;")
        else:
            print("off ShadowLamp")
            game_server.send_message("r1:y2:0;")
    except:
        settings.outs['ShadowLamp'] = not settings.outs['ShadowLamp']
@thread_wraper
def action_shadow(dt):
    try:
        time.sleep(dt)
        settings.outs['Souls'] = not settings.outs['Souls']
        if settings.outs['Souls']:
            print("on shadow")
            game_server.send_message("r1:y19:1;")
        else:
            print("off shadow")
            game_server.send_message("r1:y19:0;")
    except:
        settings.outs['Souls'] = not settings.outs['Souls']
@thread_wraper
def action_strobe1(dt):
    time.sleep(dt)
    try:
        settings.outs['Strobes'][0] = not settings.outs['Strobes'][0]
        if settings.outs['Strobes'][0]:
            print("on strobe1")
            game_server.send_message("r1:y16:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off strobe1")
            game_server.send_message("r1:y16:0;")
            settings.fan_strobe = False
    except:
        settings.outs['Strobes'][0] = not settings.outs['Strobes'][0]
@thread_wraper
def action_strobe2(dt):
    time.sleep(dt)
    try:
        settings.outs['Strobes'][1] = not settings.outs['Strobes'][1]
        if settings.outs['Strobes'][1]:
            print("on strobe2")
            game_server.send_message("r1:y17:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off strobe2")
            game_server.send_message("r1:y17:0;")
            settings.fan_strobe = False
    except:
        settings.outs['Strobes'][1] = not settings.outs['Strobes'][1]
@thread_wraper
def action_strobe3(dt):
    time.sleep(dt)
    try:
        settings.outs['Strobes'][2] = not settings.outs['Strobes'][2]
        if settings.outs['Strobes'][2]:
            print("on strobe3")
            game_server.send_message("r1:y18:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off strobe3")
            game_server.send_message("r1:y18:0;")
            settings.fan_strobe = False
    except:
        settings.outs['Strobes'][2] = not settings.outs['Strobes'][2]
@thread_wraper
def action_fan1(dt):
    try:
        time.sleep(dt)
        settings.outs['Fans'][0] = not settings.outs['Fans'][0]

        if settings.outs['Fans'][0]:
            print("on fan1")
            game_server.send_message("r1:y12:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off fan1")
            game_server.send_message("r1:y12:0;")
            settings.fan_strobe = False
    except:
        settings.outs['Fans'][0] = not settings.outs['Fans'][0]
@thread_wraper
def action_fan2(dt):
    try:
        time.sleep(dt)
        settings.outs['Fans'][1] = not settings.outs['Fans'][1]

        if settings.outs['Fans'][1]:
            print("on fan2")
            game_server.send_message("r1:y13:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off fan2")
            game_server.send_message("r1:y13:0;")
            settings.fan_strobe = False
    except:
        settings.outs['Fans'][1] = not settings.outs['Fans'][1]
@thread_wraper
def action_fan3(dt):
    try:
        time.sleep(dt)
        settings.outs['Fans'][2] = not settings.outs['Fans'][2]

        if settings.outs['Fans'][2]:
            print("on fan3")
            game_server.send_message("r1:y14:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off fan3")
            game_server.send_message("r1:y14:0;")
            settings.fan_strobe = False
    except:
        settings.outs['Fans'][2] = not settings.outs['Fans'][2]
@thread_wraper
def action_fan4(dt):
    try:
        time.sleep(dt)
        settings.outs['Fans'][3] = not settings.outs['Fans'][3]

        if settings.outs['Fans'][3]:
            print("on fan4")
            game_server.send_message("r1:y15:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off fan4")
            game_server.send_message("r1:y15:0;")
            settings.fan_strobe = False
    except:
        settings.outs['Fans'][3] = not settings.outs['Fans'][3]
@thread_wraper
def action_uv1(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[0]:
            settings.outs['UVlamps'][0] = not settings.outs['UVlamps'][0]
        if settings.outs['UVlamps'][0]:
            print("on uv1")
            game_server.send_message("r1:y3:1;")
        elif not settings.staticUV[0]:
            print("off uv1")
            game_server.send_message("r1:y3:0;")
    except:
        pass
@thread_wraper
def action_uv2(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[1]:
            settings.outs['UVlamps'][1] = not settings.outs['UVlamps'][1]
        if settings.outs['UVlamps'][1]:
            print("on uv2")
            game_server.send_message("r1:y4:1;")
        elif not settings.staticUV[1]:
            print("off uv2")
            game_server.send_message("r1:y4:0;")
    except:
        pass
@thread_wraper
def action_uv3(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[2]:
            settings.outs['UVlamps'][2] = not settings.outs['UVlamps'][2]
        if settings.outs['UVlamps'][2]:
            print("on uv3")
            game_server.send_message("r1:y5:1;")
        elif not settings.staticUV[2]:
            print("off uv3")
            game_server.send_message("r1:y5:0;")
    except:
        pass
@thread_wraper
def action_uv4(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[3]:
            settings.outs['UVlamps'][3] = not settings.outs['UVlamps'][3]
        if settings.outs['UVlamps'][3]:
            print("on uv4")
            game_server.send_message("r1:y6:1;")
        elif not settings.staticUV[3]:
            print("off uv4")
            game_server.send_message("r1:y6:0;")
    except:
        pass
@thread_wraper
def action_uv5(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[4]:
            settings.outs['UVlamps'][4] = not settings.outs['UVlamps'][4]
        if settings.outs['UVlamps'][4]:
            print("on uv5")
            game_server.send_message("r1:y7:1;")
        elif not settings.staticUV[4]:
            print("off uv5")
            game_server.send_message("r1:y7:0;")
    except:
        pass
@thread_wraper
def action_uv6(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[5]:
            settings.outs['UVlamps'][5] = not settings.outs['UVlamps'][5]
        if settings.outs['UVlamps'][5]:
            print("on uv6")
            game_server.send_message("r1:y8:1;")
        elif not settings.staticUV[5]:
            print("off uv6")
            game_server.send_message("r1:y8:0;")
    except:
        pass
@thread_wraper
def action_uv7(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[6]:
            settings.outs['UVlamps'][6] = not settings.outs['UVlamps'][6]
        if settings.outs['UVlamps'][6]:
            print("on uv7")
            game_server.send_message("r1:y9:1;")
        elif not settings.staticUV[6]:
            print("off uv7")
            game_server.send_message("r1:y9:0;")
    except:
        pass
@thread_wraper
def action_uv8(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[7]:
            settings.outs['UVlamps'][7] = not settings.outs['UVlamps'][7]
        if settings.outs['UVlamps'][7]:
            print("on uv8")
            game_server.send_message("r1:y10:1;")
        elif not settings.staticUV[7]:
            print("off uv8")
            game_server.send_message("r1:y10:0;")
    except:
        pass
@thread_wraper
def action_uv9(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[8]:
            settings.outs['UVlamps'][8] = not settings.outs['UVlamps'][8]
        if settings.outs['UVlamps'][8]:
            print("on uv9")
            game_server.send_message("r1:y11:1;")
        elif not settings.staticUV[8]:
            print("off uv9")
            game_server.send_message("r1:y11:0;")
    except:
        pass
@thread_wraper
def lamp_activation(dt):
    while True:
        dt -= 0.1
        time.sleep(0.1)
        if not settings.uv_event:
            return
        if dt <= 0:
            break
    if settings.runstop:
        if settings.order % 60 == 1:
            settings.order+=3

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv7(0)
                action_uv4(settings.bonus_time)
                action_uv7(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*3 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*3)

        elif settings.order % 60 == 4:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv3(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 5:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv6(0)
                action_uv6(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 6:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv9(0)
                action_uv9(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*2)

        elif settings.order % 60 == 8:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv5(0)
                action_uv5(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*2)

        elif settings.order % 60 == 10:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv7(0)
                action_uv7(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 11:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv4(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 12:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv2(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 13:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv8(0)
                action_uv1(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 14:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv6(0)
                action_uv6(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 15:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv3(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 16:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv7(0)
                action_uv7(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*2)

        elif settings.order % 60 == 18:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv9(0)
                action_uv9(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 19:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv4(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*2)

        elif settings.order % 60 == 21:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv8(0)
                action_uv2(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 22:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv5(0)
                action_uv5(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 23:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv1(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 24:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv6(0)
                action_uv2(settings.bonus_time)
                action_uv6(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 25:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv3(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 26:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv4(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 27:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv5(0)
                action_uv5(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 28:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv6(0)
                action_uv6(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 29:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv7(0)
                action_uv3(settings.bonus_time)
                action_uv7(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 30:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv8(0)
                action_uv1(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 31:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv9(0)
                action_uv9(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*2)

        elif settings.order % 60 == 33:
            settings.order+=3

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv6(0)
                action_uv2(settings.bonus_time)
                action_uv6(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*3 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*3)

        elif settings.order % 60 == 36:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv4(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 37:
            settings.order+=3

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv3(0)
                action_uv5(0)
                action_uv7(0)
                action_uv9(0)
                action_uv1(settings.bonus_time)
                action_uv3(settings.bonus_time)
                action_uv5(settings.bonus_time)
                action_uv7(settings.bonus_time)
                action_uv9(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*3 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*3)

        elif settings.order % 60 == 40:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv7(0)
                action_uv7(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 41:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv1(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 42:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv5(0)
                action_uv8(0)
                action_uv5(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 43:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv4(0)
                action_uv2(settings.bonus_time)
                action_uv4(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 44:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv9(0)
                action_uv9(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*2)

        elif settings.order % 60 == 46:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv6(0)
                action_uv3(settings.bonus_time)
                action_uv6(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*2)

        elif settings.order % 60 == 48:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv8(0)
                action_uv4(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 50:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv7(0)
                action_uv3(settings.bonus_time)
                action_uv7(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 51:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv5(0)
                action_uv1(settings.bonus_time)
                action_uv5(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*2)

        elif settings.order % 60 == 53:
            settings.order+=2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv9(0)
                action_uv4(settings.bonus_time)
                action_uv9(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*2)

        elif settings.order % 60 == 55:
            settings.order+=3

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv4(0)
                action_uv6(0)
                action_uv8(0)
                action_uv2(settings.bonus_time)
                action_uv4(settings.bonus_time)
                action_uv6(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time*3 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time*3)

        elif settings.order % 60 == 58:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv4(0)
                action_uv1(settings.bonus_time)
                action_uv4(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 59:
            settings.order+=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv6(0)
                action_uv6(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 0:
            settings.order=1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv8(0)
                action_uv2(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m*60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)
@thread_wraper
def shadow_lamp_activation(dt):
    while True:
        dt -= 0.1
        time.sleep(0.1)
        if not settings.shadow_lamp_enent:
            return
        if dt <= 0:
            break
    action_shadow_lamp(0)
    shadow_lamp_activation(settings.timebox['t10'])
@thread_wraper
def strobe_activation(dt):
    while True:
        dt -= 0.1
        time.sleep(0.1)
        if not settings.strobe_event:
            return
        if dt <= 0:
            break
    settings.strobe_event = False
    if settings.runstop:
        if settings.order_strobe == 1:
            settings.order_strobe+=1
            if settings.bonuses['strobes']:
                action_strobe1(0)
                action_strobe1(settings.timebox['t18'])

            if (settings.time_m*60 + settings.time_s) - settings.timebox['t19'] > 5:
                settings.strobe_music_event = True
                settings.strobe_event = True
                strobe_music_play(settings.timebox['t19'] - settings.timebox['t20'])
                strobe_activation(settings.timebox['t19'])

        elif settings.order_strobe == 2:
            settings.order_strobe+=1
            if settings.bonuses['strobes']:
                action_strobe2(0)
                action_strobe2(settings.timebox['t18'])

            if (settings.time_m*60 + settings.time_s) - settings.timebox['t19'] > 5:
                settings.strobe_music_event = True
                settings.strobe_event = True
                strobe_music_play(settings.timebox['t19'] - settings.timebox['t20'])
                strobe_activation(settings.timebox['t19'])

        elif settings.order_strobe == 3:
            settings.order_strobe=1
            if settings.bonuses['strobes']:
                action_strobe3(0)
                action_strobe3(settings.timebox['t18'])

            if (settings.time_m*60 + settings.time_s) - settings.timebox['t19'] > 5:
                settings.strobe_music_event = True
                settings.strobe_event = True
                strobe_music_play(settings.timebox['t19'] - settings.timebox['t20'])
                strobe_activation(settings.timebox['t19'])
@thread_wraper
def timer_run(dt):
    while True:
        if not settings.timer_event:
            return
        if settings.time_s - 1 >= 0:
            settings.time_s -= 1
        elif settings.time_m > 0:
            settings.time_m -= 1
            settings.time_s = 59
        if settings.time_m < 10:
            m1 = f"0{str(settings.time_m)}"
        else:
            m1 = str(settings.time_m)
        if settings.time_s < 10:
            s1 = f"0{str(settings.time_s)}"
        else:
            s1 = str(settings.time_s)
        settings.time = f"{m1}:{s1}"
        settings.time_event = True

        try:
            if settings.time_m == 1 and settings.time_s == 0 and settings.scripts == 1 and settings.timer != "05:00":
                play_music("r1", 16)
            elif settings.time_m == 2 and settings.time_s == 0 and settings.scripts == 1:
                play_music("r1", 17)
            elif settings.time_m == 3 and settings.time_s == 0 and settings.scripts == 1:
                play_music("r1", 18)
            elif settings.time_m == 4 and settings.time_s == 0 and settings.scripts == 1:
                play_music("r1", 19)
            elif settings.time_m == 5 and settings.time_s == 0 and settings.scripts == 1:
                play_music("r1", 20)
        except:
            pass

        if settings.time_m == 0 and settings.time_s == 0 or not settings.runstop:
            settings.order = 1
            settings.order_strobe = 1
            settings.order_music = 1
            stop_events()
            settings.time = settings.timer
            settings.runstop = False
            settings.end_timer_event = True
            play_end_music()

            if settings.outs['RunStopLamp']:
                action_runstop_lamp(0)
            return
        time.sleep(dt)

def off_all():
    off_fans()
    off_strobes()
    off_UV_lamps()
    off_other()
def off_other():
    try:
        game_server.send_message("r1:y1:0;")
        game_server.send_message("r1:y2:0;")
        game_server.send_message("r1:y19:0;")
    except:
        pass
def off_fans():
    try:
        game_server.send_message("r1:y12:0;")
        game_server.send_message("r1:y13:0;")
        game_server.send_message("r1:y14:0;")
        game_server.send_message("r1:y15:0;")
    except:
        pass
def off_strobes():
    try:
        game_server.send_message("r1:y16:0;")
        game_server.send_message("r1:y17:0;")
        game_server.send_message("r1:y18:0;")
    except:
        pass
def off_UV_lamps():
    try:
        game_server.send_message("r1:y3:0;")
        game_server.send_message("r1:y4:0;")
        game_server.send_message("r1:y5:0;")
        game_server.send_message("r1:y6:0;")
        game_server.send_message("r1:y7:0;")
        game_server.send_message("r1:y8:0;")
        game_server.send_message("r1:y9:0;")
        game_server.send_message("r1:y10:0;")
        game_server.send_message("r1:y11:0;")
    except:
        pass
@thread_wraper
def music_play(dt):
    try:
        while True:
            dt -= 0.1
            time.sleep(0.1)
            if not settings.music_play_event:
                return
            if dt <= 0:
                break
        settings.music_play_event = False
        if settings.runstop:
            if settings.scripts == 0:
                if settings.order_music == 1:
                    settings.order_music+=1

                    play_music("r1", 1)
                    settings.music_play_event = True
                    music_play(6)

                elif settings.order_music == 2:
                    settings.order_music+=1

                    tmp = random.randint(1,4)
                    if tmp == 1:
                        play_music("r1", 2)
                    elif tmp == 2:
                        play_music("r1", 3)
                    elif tmp == 3:
                        play_music("r1", 4)
                    elif tmp == 4:
                        play_music("r1", 5)

                    if settings.time_m*60 + settings.time_s > 15*60:
                        settings.order_music-=1
                        settings.music_play_event = True
                        music_play(15*60 - 0.1)
                    else:
                        settings.music_play_event = True
                        music_play(settings.time_m*60 + settings.time_s - 0.1)

                elif settings.order_music == 3:
                    settings.order_music=1

            elif settings.scripts == 1:
                if settings.order_music == 1:
                    settings.order_music+=1
                    play_music("r1", 7)
                    settings.music_play_event = True
                    music_play(11)

                elif settings.order_music == 2:
                    settings.order_music+=1
                    tmp = random.randint(1,4)
                    if tmp == 1:
                        play_music("r1", 8)
                    elif tmp == 2:
                        play_music("r1", 9)
                    elif tmp == 3:
                        play_music("r1", 10)
                    elif tmp == 4:
                        play_music("r1", 11)

                    if settings.time_m*60 + settings.time_s> 15*60:
                        settings.order_music-=1
                        settings.music_play_event = True
                        music_play(15*60 - 0.1)
                    else:
                        settings.music_play_event = True
                        music_play(settings.time_m*60 + settings.time_s - 0.1)

                elif settings.order_music == 3:
                    settings.order_music=1
    except:
        pass
@thread_wraper
def strobe_music_play(dt):
    try:
        while True:
            dt -= 0.1
            time.sleep(0.1)
            if not settings.strobe_music_event:
                return
            if dt <= 0:
                break
        settings.strobe_music_event = False
        if settings.bonuses['strobes']:
            tmp = random.randint(1,3)
            print(tmp)
            if tmp == 1:
                play_music("r1", 13)
            elif tmp == 2:
                play_music("r1", 14)
            elif tmp == 3:
                play_music("r1", 15)
    except:
        pass
def play_end_music():
    try:
        if settings.scripts == 0:
            play_music("r1", 6)

        if settings.scripts == 1:
            play_music("r1", 12)
    except:
        pass

def stop_events():
    settings.start_event = False
    settings.timer_event = False
    settings.music_play_event = False
    settings.uv_event = False
    settings.strobe_event = False
    settings.strobe_music_event = False
    settings.shadow_lamp_enent = False
    settings.shadow_event = False
    if settings.outs['Souls']:
        action_shadow(0)
    if settings.outs['ShadowLamp']:
        action_shadow_lamp(0)
    if settings.outs['RunStopLamp']:
        action_runstop_lamp(0)
    try:
        game_server.connection[0].send("M00;") # TODO stop ALL
    except:
        pass
    if settings.runstop:
        play_end_music()

def play_music(rpi: str, track: str):
    game_server.send_message(f'{rpi}:play:{track};')

def pause_music(rpi: str, track: str):
    game_server.send_message(f'{rpi}:pause:{track};')

def stop_music(rpi: str, track: str):
    game_server.send_message(f'{rpi}:stop:{track};')

def change_volume(rpi: str, volume: int):
    settings.volumes[rpi] = volume
    game_server.send_message(f'{rpi}:volume:{volume};')
