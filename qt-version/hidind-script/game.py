import random
import threading
import time

import settings
from server import Server

def message_handler(mes: str):
    try:
        rpi, inputName, value = mes.split(':')
        settings.inputs[f"{rpi}:{inputName}"] = bool(int(value))
    except Exception as e:
        print(e)


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
    settings.order = 1
    settings.order_strobe = 1
    settings.order_music = 1
    settings.order_fans = [0, 0, 0, 0]
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
    settings.fans_run_time = [0, 0, 0, 0]
    settings.fan_strobe = False
    settings.staticUV = [False, False, False, False, False, False, False, False, False]
    set_standart_outs()
    settings.game_status = False


def set_standart_outs():
    settings.outs = {
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
        "r2:y38": False,
        "r3:y1": False,
        "r3:y2": False,
        "r3:y38": False,
    }


def check_start():
    if settings.inputs['r1:x1'] == True and not settings.game_status:
        settings.start_run_time = time.time()
        settings.game_status = True

    if settings.game_status and settings.start_button_release:
        if settings.timebox['t1'] < time.time() - settings.start_run_time:
            settings.game_status = False
            settings.start_run_time = -1
            settings.start_button_release = False
            return not settings.runstop

    if settings.inputs['r1:x1'] == False:
        settings.game_status = False
        settings.start_run_time = -1
        settings.start_button_release = True


def check_fans():
    for i in range(4):
        fan_input = i + 2
        if not settings.inputs[f"r1:x{fan_input}"] and time.time() - settings.fans_run_time[i] > settings.timebox['t17']:
            settings.order_fans[i] += 1
            settings.fans_run_time[i] = time.time()

            if settings.order_fans[i] == 3:
                settings.order_fans[i] = 0

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
                shadow_lamp_activation(settings.time_m * 60 + settings.time_s - settings.timebox['t4'])

            elif settings.scripts == 1:
                settings.shadow_lamp_enent = True
                shadow_lamp_activation(settings.time_m * 60 + settings.time_s - settings.timebox['t9'])
    except Exception as e:
        print(e)


@thread_wraper
def action_runstop_lamp(dt):
    try:
        time.sleep(dt)
        settings.outs['r1:y1'] = not settings.outs['r1:y1']
        if settings.outs['r1:y1']:
            game_server.send_message("r1:y1:1;")
        else:
            game_server.send_message("r1:y1:0;")
    except:
        settings.outs['r1:y1'] = not settings.outs['r1:y1']


@thread_wraper
def action_shadow_lamp(dt):
    try:
        time.sleep(dt)
        settings.outs['r1:y2'] = not settings.outs['r1:y2']
        if settings.outs['r1:y2']:
            game_server.send_message("r1:y2:1;")
        else:
            game_server.send_message("r1:y2:0;")
    except:
        settings.outs['r1:y2'] = not settings.outs['r1:y2']


@thread_wraper
def action_shadow(dt):
    try:
        time.sleep(dt)
        settings.outs['r1:y19'] = not settings.outs['r1:y19']
        if settings.outs['r1:y19']:
            game_server.send_message("r1:y19:1;")
        else:
            game_server.send_message("r1:y19:0;")
    except:
        settings.outs['r1:y19'] = not settings.outs['r1:y19']


@thread_wraper
def action_strobe1(dt):
    time.sleep(dt)
    try:
        settings.outs['r1:y16'] = not settings.outs['r1:y16']
        if settings.outs['r1:y16']:
            game_server.send_message("r1:y16:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            game_server.send_message("r1:y16:0;")
            settings.fan_strobe = False
    except:
        settings.outs['r1:y16'] = not settings.outs['r1:y16']


@thread_wraper
def action_strobe2(dt):
    time.sleep(dt)
    try:
        settings.outs['r1:y17'] = not settings.outs['r1:y17']
        if settings.outs['r1:y17']:
            game_server.send_message("r1:y17:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            game_server.send_message("r1:y17:0;")
            settings.fan_strobe = False
    except:
        settings.outs['r1:y17'] = not settings.outs['r1:y17']


@thread_wraper
def action_strobe3(dt):
    time.sleep(dt)
    try:
        settings.outs['r1:y18'] = not settings.outs['r1:y18']
        if settings.outs['r1:y18']:
            game_server.send_message("r1:y18:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            game_server.send_message("r1:y18:0;")
            settings.fan_strobe = False
    except:
        settings.outs['r1:y18'] = not settings.outs['r1:y18']


@thread_wraper
def action_fan1(dt):
    try:
        time.sleep(dt)
        settings.outs['r1:y12'] = not settings.outs['r1:y12']

        if settings.outs['r1:y12']:
            game_server.send_message("r1:y12:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            game_server.send_message("r1:y12:0;")
            settings.fan_strobe = False
    except:
        settings.outs['r1:y12'] = not settings.outs['r1:y12']


@thread_wraper
def action_fan2(dt):
    try:
        time.sleep(dt)
        settings.outs['r1:y13'] = not settings.outs['r1:y13']

        if settings.outs['r1:y13']:
            game_server.send_message("r1:y13:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            game_server.send_message("r1:y13:0;")
            settings.fan_strobe = False
    except:
        settings.outs['r1:y13'] = not settings.outs['r1:y13']


@thread_wraper
def action_fan3(dt):
    try:
        time.sleep(dt)
        settings.outs['r1:y14'] = not settings.outs['r1:y14']

        if settings.outs['r1:y14']:
            game_server.send_message("r1:y14:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            game_server.send_message("r1:y14:0;")
            settings.fan_strobe = False
    except:
        settings.outs['r1:y14'] = not settings.outs['r1:y14']


@thread_wraper
def action_fan4(dt):
    try:
        time.sleep(dt)
        settings.outs['r1:y15'] = not settings.outs['r1:y15']

        if settings.outs['r1:y15']:
            game_server.send_message("r1:y15:1;")
            settings.fan_strobe = True
            if not settings.bonuses['settings']:
                off_UV_lamps()
        else:
            game_server.send_message("r1:y15:0;")
            settings.fan_strobe = False
    except:
        settings.outs['r1:y15'] = not settings.outs['r1:y15']


@thread_wraper
def action_uv1(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[0]:
            settings.outs['r1:y3'] = not settings.outs['r1:y3']
        if settings.outs['r1:y3']:
            game_server.send_message("r1:y3:1;")
        elif not settings.staticUV[0]:
            game_server.send_message("r1:y3:0;")
    except:
        pass


@thread_wraper
def action_uv2(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[1]:
            settings.outs['r1:y4'] = not settings.outs['r1:y4']
        if settings.outs['r1:y4']:
            game_server.send_message("r1:y4:1;")
        elif not settings.staticUV[1]:
            game_server.send_message("r1:y4:0;")
    except:
        pass


@thread_wraper
def action_uv3(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[2]:
            settings.outs['r1:y5'] = not settings.outs['r1:y5']
        if settings.outs['r1:y5']:
            game_server.send_message("r1:y5:1;")
        elif not settings.staticUV[2]:
            game_server.send_message("r1:y5:0;")
    except:
        pass


@thread_wraper
def action_uv4(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[3]:
            settings.outs['r1:y6'] = not settings.outs['r1:y6']
        if settings.outs['r1:y6']:
            game_server.send_message("r1:y6:1;")
        elif not settings.staticUV[3]:
            game_server.send_message("r1:y6:0;")
    except:
        pass


@thread_wraper
def action_uv5(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[4]:
            settings.outs['r1:y7'] = not settings.outs['r1:y7']
        if settings.outs['r1:y7']:
            game_server.send_message("r1:y7:1;")
        elif not settings.staticUV[4]:
            game_server.send_message("r1:y7:0;")
    except:
        pass


@thread_wraper
def action_uv6(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[5]:
            settings.outs['r1:y8'] = not settings.outs['r1:y8']
        if settings.outs['r1:y8']:
            game_server.send_message("r1:y8:1;")
        elif not settings.staticUV[5]:
            game_server.send_message("r1:y8:0;")
    except:
        pass


@thread_wraper
def action_uv7(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[6]:
            settings.outs['r1:y9'] = not settings.outs['r1:y9']
        if settings.outs['r1:y9']:
            game_server.send_message("r1:y9:1;")
        elif not settings.staticUV[6]:
            game_server.send_message("r1:y9:0;")
    except:
        pass


@thread_wraper
def action_uv8(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[7]:
            settings.outs['r1:y10'] = not settings.outs['r1:y10']
        if settings.outs['r1:y10']:
            game_server.send_message("r1:y10:1;")
        elif not settings.staticUV[7]:
            game_server.send_message("r1:y10:0;")
    except:
        pass


@thread_wraper
def action_uv9(dt):
    time.sleep(dt)
    try:
        if not settings.staticUV[8]:
            settings.outs['r1:y11'] = not settings.outs['r1:y11']
        if settings.outs['r1:y11']:
            game_server.send_message("r1:y11:1;")
        elif not settings.staticUV[8]:
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
            settings.order += 3

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv7(0)
                action_uv4(settings.bonus_time)
                action_uv7(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 3 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 3)

        elif settings.order % 60 == 4:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv3(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 5:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv6(0)
                action_uv6(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 6:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv9(0)
                action_uv9(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 2)

        elif settings.order % 60 == 8:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv5(0)
                action_uv5(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 2)

        elif settings.order % 60 == 10:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv7(0)
                action_uv7(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 11:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv4(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 12:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv2(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 13:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv8(0)
                action_uv1(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 14:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv6(0)
                action_uv6(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 15:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv3(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 16:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv7(0)
                action_uv7(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 2)

        elif settings.order % 60 == 18:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv9(0)
                action_uv9(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 19:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv4(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 2)

        elif settings.order % 60 == 21:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv8(0)
                action_uv2(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 22:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv5(0)
                action_uv5(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 23:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv1(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 24:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv6(0)
                action_uv2(settings.bonus_time)
                action_uv6(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 25:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv3(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 26:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv4(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 27:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv5(0)
                action_uv5(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 28:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv6(0)
                action_uv6(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 29:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv7(0)
                action_uv3(settings.bonus_time)
                action_uv7(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 30:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv8(0)
                action_uv1(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 31:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv9(0)
                action_uv9(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 2)

        elif settings.order % 60 == 33:
            settings.order += 3

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv6(0)
                action_uv2(settings.bonus_time)
                action_uv6(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 3 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 3)

        elif settings.order % 60 == 36:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv4(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 37:
            settings.order += 3

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

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 3 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 3)

        elif settings.order % 60 == 40:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv7(0)
                action_uv7(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 41:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv1(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 42:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv5(0)
                action_uv8(0)
                action_uv5(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 43:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv4(0)
                action_uv2(settings.bonus_time)
                action_uv4(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 44:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv9(0)
                action_uv9(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 2)

        elif settings.order % 60 == 46:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv6(0)
                action_uv3(settings.bonus_time)
                action_uv6(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 2)

        elif settings.order % 60 == 48:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv8(0)
                action_uv4(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 50:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv3(0)
                action_uv7(0)
                action_uv3(settings.bonus_time)
                action_uv7(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 51:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv5(0)
                action_uv1(settings.bonus_time)
                action_uv5(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 2)

        elif settings.order % 60 == 53:
            settings.order += 2

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv4(0)
                action_uv9(0)
                action_uv4(settings.bonus_time)
                action_uv9(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 2 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 2)

        elif settings.order % 60 == 55:
            settings.order += 3

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv4(0)
                action_uv6(0)
                action_uv8(0)
                action_uv2(settings.bonus_time)
                action_uv4(settings.bonus_time)
                action_uv6(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time * 3 > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time * 3)

        elif settings.order % 60 == 58:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv1(0)
                action_uv4(0)
                action_uv1(settings.bonus_time)
                action_uv4(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 59:
            settings.order += 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv6(0)
                action_uv6(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
                settings.uv_event = True
                lamp_activation(settings.UV_activation_time)

        elif settings.order % 60 == 0:
            settings.order = 1

            if settings.bonuses["UVlamps"] and not settings.fan_strobe:
                action_uv2(0)
                action_uv8(0)
                action_uv2(settings.bonus_time)
                action_uv8(settings.bonus_time)

            if (settings.time_m * 60 + settings.time_s) - settings.UV_activation_time > settings.UV_activation_time:
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
            settings.order_strobe += 1
            if settings.bonuses['strobes']:
                action_strobe1(0)
                action_strobe1(settings.timebox['t18'])

            if (settings.time_m * 60 + settings.time_s) - settings.timebox['t19'] > 5:
                settings.strobe_music_event = True
                settings.strobe_event = True
                strobe_music_play(settings.timebox['t19'] - settings.timebox['t20'])
                strobe_activation(settings.timebox['t19'])

        elif settings.order_strobe == 2:
            settings.order_strobe += 1
            if settings.bonuses['strobes']:
                action_strobe2(0)
                action_strobe2(settings.timebox['t18'])

            if (settings.time_m * 60 + settings.time_s) - settings.timebox['t19'] > 5:
                settings.strobe_music_event = True
                settings.strobe_event = True
                strobe_music_play(settings.timebox['t19'] - settings.timebox['t20'])
                strobe_activation(settings.timebox['t19'])

        elif settings.order_strobe == 3:
            settings.order_strobe = 1
            if settings.bonuses['strobes']:
                action_strobe3(0)
                action_strobe3(settings.timebox['t18'])

            if (settings.time_m * 60 + settings.time_s) - settings.timebox['t19'] > 5:
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

            if settings.outs['r1:y1']:
                action_runstop_lamp(0)
            return
        time.sleep(dt)


def off_all():
    off_fans()
    off_strobes()
    off_UV_lamps()
    off_other()
    off_r2()
    off_r3()


def off_r2():
    try:
        game_server.send_message("r2:y1:0;")
        game_server.send_message("r2:y16:0;")
        game_server.send_message("r2:y17:0;")
        game_server.send_message("r2:y38:0;")

        game_server.send_message("r2:y2:0;")
        game_server.send_message("r2:y3:0;")
        game_server.send_message("r2:y4:0;")
        game_server.send_message("r2:y5:0;")
        game_server.send_message("r2:y6:0;")
        game_server.send_message("r2:y7:0;")
        game_server.send_message("r2:y8:0;")
        game_server.send_message("r2:y9:0;")
        game_server.send_message("r2:y10:0;")
        game_server.send_message("r2:y11:0;")
        game_server.send_message("r2:y12:0;")
        game_server.send_message("r2:y13:0;")
        game_server.send_message("r2:y14:0;")
        game_server.send_message("r2:y18:0;")
    except:
        pass


def off_r3():
    try:
        game_server.send_message("r3:y1:0;")
        game_server.send_message("r3:y2:0;")
        game_server.send_message("r3:y38:0;")
    except:
        pass


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
                    settings.order_music += 1

                    play_music("r1", 1)
                    settings.music_play_event = True
                    music_play(6)

                elif settings.order_music == 2:
                    settings.order_music += 1

                    tmp = random.randint(1, 4)
                    if tmp == 1:
                        play_music("r1", 2)
                    elif tmp == 2:
                        play_music("r1", 3)
                    elif tmp == 3:
                        play_music("r1", 4)
                    elif tmp == 4:
                        play_music("r1", 5)

                    if settings.time_m * 60 + settings.time_s > 15 * 60:
                        settings.order_music -= 1
                        settings.music_play_event = True
                        music_play(15 * 60 - 0.1)
                    else:
                        settings.music_play_event = True
                        music_play(settings.time_m * 60 + settings.time_s - 0.1)

                elif settings.order_music == 3:
                    settings.order_music = 1

            elif settings.scripts == 1:
                if settings.order_music == 1:
                    settings.order_music += 1
                    play_music("r1", 7)
                    settings.music_play_event = True
                    music_play(11)

                elif settings.order_music == 2:
                    settings.order_music += 1
                    tmp = random.randint(1, 4)
                    if tmp == 1:
                        play_music("r1", 8)
                    elif tmp == 2:
                        play_music("r1", 9)
                    elif tmp == 3:
                        play_music("r1", 10)
                    elif tmp == 4:
                        play_music("r1", 11)

                    if settings.time_m * 60 + settings.time_s > 15 * 60:
                        settings.order_music -= 1
                        settings.music_play_event = True
                        music_play(15 * 60 - 0.1)
                    else:
                        settings.music_play_event = True
                        music_play(settings.time_m * 60 + settings.time_s - 0.1)

                elif settings.order_music == 3:
                    settings.order_music = 1
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
            tmp = random.randint(1, 3)
            print(tmp)
            if tmp == 1:
                play_music("r1", 13) #TODO эти треки зарезервированы под связь установлена
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
    if settings.outs['r1:y19']:
        action_shadow(0)
    if settings.outs['r1:y2']:
        action_shadow_lamp(0)
    if settings.outs['r1:y1']:
        action_runstop_lamp(0)
    try:
        stop_music('r1', -1)
        stop_music('r2', -1)
        stop_music('r3', -1)
    except:
        pass
    if settings.runstop:
        play_end_music()


def play_music(rpi: str, track: int):
    game_server.send_message(f'{rpi}:play:{track};')


def pause_music(rpi: str, track: int):
    game_server.send_message(f'{rpi}:pause:{track};')


def stop_music(rpi: str, track: int):
    game_server.send_message(f'{rpi}:stop:{track};')


def change_volume(rpi: str, volume: int):
    settings.volumes[rpi] = volume
    game_server.send_message(f'{rpi}:volume:{volume};')

def reset_out(out_name : str, status: int):
    settings.outs[out_name] = bool(status)
    game_server.send_message(f'{out_name}:{int(status)};')

@thread_wraper
def reset_light_outs(out1_name : str, out1_status: int, out2_name : str, out2_status: int):
    if (settings.outs[out1_name] and settings.outs[out2_name]) and not (out1_status or out2_status): # если из мрг в on
        settings.outs[out2_name] = bool(out2_status)
        game_server.send_message(f'{out2_name}:{int(out2_status)};')
        time.sleep(settings.timebox['t41'])
        settings.outs[out1_name] = bool(out1_status)
        game_server.send_message(f'{out1_name}:{int(out1_status)};')
    elif not (settings.outs[out1_name] or settings.outs[out2_name]) and (out1_status and out2_status): # если из on в мрг
        settings.outs[out1_name] = bool(out1_status)
        game_server.send_message(f'{out1_name}:{int(out1_status)};')
        time.sleep(settings.timebox['t41'])
        settings.outs[out2_name] = bool(out2_status)
        game_server.send_message(f'{out2_name}:{int(out2_status)};')
    else:
        settings.outs[out1_name] = bool(out1_status)
        game_server.send_message(f'{out1_name}:{int(out1_status)};')
        settings.outs[out2_name] = bool(out2_status)
        game_server.send_message(f'{out2_name}:{int(out2_status)};')
