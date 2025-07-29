import threading
import time
import random

import settings
from server import Server
s = Server()
threading.Thread(target=s.serverFunction, daemon=True).start()

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
                s.connection[0].send("MG1;".encode('utf-8'))
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
            s.connection[0].send("RS1;".encode('utf-8'))
        else:
            print("off RunStopLamp")
            s.connection[0].send("RS0;".encode('utf-8'))
    except:
        settings.outs['RunStopLamp'] = not settings.outs['RunStopLamp']
@thread_wraper
def action_shadow_lamp(dt):
    try:
        time.sleep(dt)
        settings.outs['ShadowLamp'] = not settings.outs['ShadowLamp']
        if settings.outs['ShadowLamp']:
            print("on ShadowLamp")
            s.connection[0].send("SL1;".encode('utf-8'))
        else:
            print("off ShadowLamp")
            s.connection[0].send("SL0;".encode('utf-8'))
    except:
        settings.outs['ShadowLamp'] = not settings.outs['ShadowLamp']
@thread_wraper
def action_shadow(dt):
    try:
        time.sleep(dt)
        settings.outs['Souls'] = not settings.outs['Souls']
        if settings.outs['Souls']:
            print("on shadow")
            s.connection[0].send("SH1;".encode('utf-8'))
        else:
            print("off shadow")
            s.connection[0].send("SH0;".encode('utf-8'))
    except:
        settings.outs['Souls'] = not settings.outs['Souls']
@thread_wraper
def action_strobe1(dt):
    time.sleep(dt)
    try:
        settings.outs['Strobes'][0] = not settings.outs['Strobes'][0]
        if settings.outs['Strobes'][0]:
            print("on strobe1")
            s.connection[0].send("S11;".encode('utf-8'))
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off strobe1")
            s.connection[0].send("S10;".encode('utf-8'))
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
            s.connection[0].send("S21;".encode('utf-8'))
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off strobe2")
            s.connection[0].send("S20;".encode('utf-8'))
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
            s.connection[0].send("S31;".encode('utf-8'))
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off strobe3")
            s.connection[0].send("S30;".encode('utf-8'))
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
            s.connection[0].send("F11;".encode('utf-8'))
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off fan1")
            s.connection[0].send("F10;".encode('utf-8'))
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
            s.connection[0].send("F21;".encode('utf-8'))
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off fan2")
            s.connection[0].send("F20;".encode('utf-8'))
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
            s.connection[0].send("F31;".encode('utf-8'))
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off fan3")
            s.connection[0].send("F30;".encode('utf-8'))
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
            s.connection[0].send("F41;".encode('utf-8'))
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            print("off fan4")
            s.connection[0].send("F40;".encode('utf-8'))
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
            s.connection[0].send("U11;".encode('utf-8'))
        elif not settings.staticUV[0]:
            print("off uv1")
            s.connection[0].send("U10;".encode('utf-8'))
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
            s.connection[0].send("U21;".encode('utf-8'))
        elif not settings.staticUV[1]:
            print("off uv2")
            s.connection[0].send("U20;".encode('utf-8'))
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
            s.connection[0].send("U31;".encode('utf-8'))
        elif not settings.staticUV[2]:
            print("off uv3")
            s.connection[0].send("U30;".encode('utf-8'))
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
            s.connection[0].send("U41;".encode('utf-8'))
        elif not settings.staticUV[3]:
            print("off uv4")
            s.connection[0].send("U40;".encode('utf-8'))
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
            s.connection[0].send("U51;".encode('utf-8'))
        elif not settings.staticUV[4]:
            print("off uv5")
            s.connection[0].send("U50;".encode('utf-8'))
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
            s.connection[0].send("U61;".encode('utf-8'))
        elif not settings.staticUV[5]:
            print("off uv6")
            s.connection[0].send("U60;".encode('utf-8'))
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
            s.connection[0].send("U71;".encode('utf-8'))
        elif not settings.staticUV[6]:
            print("off uv7")
            s.connection[0].send("U70;".encode('utf-8'))
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
            s.connection[0].send("U81;".encode('utf-8'))
        elif not settings.staticUV[7]:
            print("off uv8")
            s.connection[0].send("U80;".encode('utf-8'))
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
            s.connection[0].send("U91;".encode('utf-8'))
        elif not settings.staticUV[8]:
            print("off uv9")
            s.connection[0].send("U90;".encode('utf-8'))
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
                s.connection[0].send('MH1;'.encode('utf-8'))
            elif settings.time_m == 2 and settings.time_s == 0 and settings.scripts == 1:
                s.connection[0].send('MI1;'.encode('utf-8'))
            elif settings.time_m == 3 and settings.time_s == 0 and settings.scripts == 1:
                s.connection[0].send('MJ1;'.encode('utf-8'))
            elif settings.time_m == 4 and settings.time_s == 0 and settings.scripts == 1:
                s.connection[0].send('MK1;'.encode('utf-8'))
            elif settings.time_m == 5 and settings.time_s == 0 and settings.scripts == 1:
                s.connection[0].send('ML1;'.encode('utf-8'))
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
        s.connection[0].send("SH0;".encode('utf-8'))
        s.connection[0].send("RS0;".encode('utf-8'))
        s.connection[0].send("SL0;".encode('utf-8'))
    except:
        pass
def off_fans():
    try:
        s.connection[0].send("F10;".encode('utf-8'))
        s.connection[0].send("F20;".encode('utf-8'))
        s.connection[0].send("F30;".encode('utf-8'))
        s.connection[0].send("F40;".encode('utf-8'))
    except:
        pass
def off_strobes():
    try:
        s.connection[0].send("S10;".encode('utf-8'))
        s.connection[0].send("S20;".encode('utf-8'))
        s.connection[0].send("S30;".encode('utf-8'))
    except:
        pass
def off_UV_lamps():
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

                    s.connection[0].send("M11;".encode('utf-8'))
                    settings.music_play_event = True
                    music_play(6)

                elif settings.order_music == 2:
                    settings.order_music+=1

                    tmp = random.randint(1,4)
                    if tmp == 1:
                        s.connection[0].send("M21;".encode('utf-8'))
                    elif tmp == 2:
                        s.connection[0].send("M31;".encode('utf-8'))
                    elif tmp == 3:
                        s.connection[0].send("M41;".encode('utf-8'))
                    elif tmp == 4:
                        s.connection[0].send("M51;".encode('utf-8'))

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
                    s.connection[0].send("M71;".encode('utf-8'))
                    settings.music_play_event = True
                    music_play(11)

                elif settings.order_music == 2:
                    settings.order_music+=1
                    tmp = random.randint(1,4)
                    if tmp == 1:
                        s.connection[0].send("M81;".encode('utf-8'))
                    elif tmp == 2:
                        s.connection[0].send("M91;".encode('utf-8'))
                    elif tmp == 3:
                        s.connection[0].send("MA1;".encode('utf-8'))
                    elif tmp == 4:
                        s.connection[0].send("MB1;".encode('utf-8'))

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
                s.connection[0].send("MD1;".encode('utf-8'))
            elif tmp == 2:
                s.connection[0].send("ME1;".encode('utf-8'))
            elif tmp == 3:
                s.connection[0].send("MF1;".encode('utf-8'))
    except:
        pass
def play_end_music():
    try:
        if settings.scripts == 0:
            s.connection[0].send("M61;".encode('utf-8'))

        if settings.scripts == 1:
            s.connection[0].send("MC1;".encode('utf-8'))
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
        s.connection[0].send("M00;".encode('utf-8'))
    except:
        pass
    if settings.runstop:
        play_end_music()
