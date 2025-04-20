import subprocess
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--script-name", help="Name of the output script (default screen-name)", default=None)
args, unkown = parser.parse_known_args()

def parse_w_line(line: str):
    cols = line.split()
    command = ' '.join(cols[7:])
    window_number = int(cols[2].split('.')[-1])
    return window_number, command

def running_in_screen() -> bool:
    return os.getenv("STY") is not None

def get_window_names():
    res = subprocess.check_output(['screen', '-Q', 'windows'])
    res = res.split()
    res = [res[i] for i in range(res) if i % 2 != 0]
    return res

def get_current_screen_name() -> str:
    if not running_in_screen():
        raise SystemError("Not running inside of a screen.")
    return os.getenv("STY")

def save():
    screen_name = get_current_screen_name()
    script_name = args.script_name if args.script_name is not None else screen_name

    res = subprocess.check_output(['w'])
    res = str(res)
    # break up res into lines, remove the first line which is a header
    res = res.split('\\n')[2:-1]
    res = [parse_w_line(r) for r in res]
    
    # build the bash script
    f = open(script_name, "w")
    f.write("#!/bin/sh\nscreen -dmS {0}\n".format(screen_name))
    for window, command in res:
        if window != 0:
            f.write("screen -S test -X screen {0}\n".format(window))
        f.write("screen -S test -p {0} -X stuff {1}\r\n".format(window, command))

    f.close()
    os.chmod(script_name, 0o775)

if __name__ == "__main__":
    save()
