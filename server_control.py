import os
import subprocess
import yaml


screen_list: dict = {}
with open('~/server_control.yml', 'r') as f:
    config = yaml.safe_load(f)

def run_command(command):
    print(command)
    try:
        return subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError:
        return b''


def get_screen_list():
    raw_list = run_command('screen -ls').decode('utf-8').strip().splitlines()
    output_list = {}
    for i in raw_list:
        if '\t' in i:
            k = i.split('\t')[1]
            j = k.split('.')
            try:
                output_list['.'.join(j[1:])] = j[0]
            except KeyError:
                continue
    return output_list


def start_screen(screen):
    run_command(
        ('kill -9 {}\n'.format(screen_list[screen]) if screen in screen_list else '') +
        'screen -wipe\n' +
        'screen -dmS {}\n'.format(screen) +
        'screen -x -S {} -p 0 -X stuff "{}\\n"'.format(
            screen,
            '\\n'.join(config[screen])
        )
    )


def ask_screen():
    _ = []
    for key in config:
        _.append(key)
    print(', '.join(_))
    while True:
        screen = input('请输入想要开启/重启的Screen\n>>>')
        if screen in config:
            return screen
        else:
            print('不存在名为{}的screen\n'.format(screen))


def main(is_cli=True, arg: list = None):
    global screen_list
    screen_list = get_screen_list()
    if is_cli:
        screen = ask_screen()
        start_screen(screen)
    else:
        for screen in arg:
            start_screen(screen)
