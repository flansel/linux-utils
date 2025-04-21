import subprocess
import argparse
import os
import utmp
from typing import Tuple, Dict

parser = argparse.ArgumentParser()
parser.add_argument("--script-name", help="Name of the output script (default screen-name)", default=None)
args, unkown = parser.parse_known_args()

def running_in_screen() -> bool:
    return os.getenv("STY") is not None

def get_window_name(window: int) -> str:
     res = subprocess.check_output(['screen', '-p', str(window), '-Q', 'title']).decode("utf-8")
     return res

def get_current_window() -> int:
    res = subprocess.check_output(['screen', '-Q', 'number']).split()[0]
    return int(res)

def get_current_screen_name() -> str:
    return os.getenv("STY")

def get_pid_cwd(pid: int) -> str:
    return ""

def save():
    screen_name = "".join(get_current_screen_name().split('.')[1:])
    script_name = args.script_name if args.script_name is not None else screen_name + ".sh"

    with open('/var/run/utmp', 'rb') as f:
        buf = f.read()
        for entry in utmp.read(buf):
            print(entry)

    res = []
    if len(res) <= 0:
        raise SystemError("screen-saver must be run inside of a GNU-screen")

    # build the bash script
    f = open(script_name, "w")
    f.write("#!/bin/sh\nscreen -dmS {0} -t {1}\n".format(screen_name, get_window_name(res[0][0])))
    for idx, (window, command) in enumerate(res):
        if idx != 0:
            f.write("screen -S {0} -X screen -t {1}\n".format(screen_name, get_window_name(window)))
        f.write("screen -S {0} -p {1} -X stuff {2}\r\n".format(screen_name, window, command))

    f.close()
    os.chmod(script_name, 0o775)

if __name__ == "__main__":
    if not running_in_screen():
        raise SystemError("screen-saver must be run inside of a GNU-screen.")
    save()
