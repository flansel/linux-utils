import subprocess
import argparse
import os
from typing import Tuple, Dict

parser = argparse.ArgumentParser()
parser.add_argument("--script-name", help="Name of the output script (default screen-name)", default=None)
args, unkown = parser.parse_known_args()

def parse_w_line(line: str) -> Tuple[int, str]:
    cols = line.split()
    command = ' '.join(cols[7:])
    window_number = int(cols[2].split('.')[-1])
    return window_number, command

def running_in_screen() -> bool:
    return os.getenv("STY") is not None

def get_window_names() -> Dict[int, str]:
    """
    TODO:
    screen -Q windows is not a reliable way to get tab title informtion as it is affected by window size and
    only displays the first few tabs. So for now window titles are best effort.
    """
    process = subprocess.Popen(['screen', '-Q', 'windows'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data = process.stdout.read()
    res = res.split()
    res = {int(res[i]):res[i + 1] for i in range(0, res, 2)}
    return {}

def get_window_name(window: int) -> str:
     res = subprocess.check_output(['screen', '-p', str(window), '-Q', 'title']).decode("utf-8")
     return res

def get_current_window() -> int:
    res = subprocess.check_output(['screen', '-Q', 'number']).split()[0]
    return int(res)

def get_current_screen_name() -> str:
    return os.getenv("STY")

def save():
    screen_name = get_current_screen_name()
    script_name = args.script_name if args.script_name is not None else screen_name

    res = subprocess.check_output(['w'])
    res = str(res)
    # break up res into lines, remove the first line which is a header
    res = res.split('\\n')[2:-1]
    res = [parse_w_line(r) for r in res]
    #window_names = get_window_names()
    
    # build the bash script
    f = open(script_name, "w")
    f.write("#!/bin/sh\nscreen -dmS {0}\n".format(screen_name))
    for window, command in res:
        if window != 0:
            f.write("screen -S {0} -X screen -t {1}\n".format(screen_name, get_window_name(window)))
        f.write("screen -S {0} -p {1} -X stuff {2}\r\n".format(screen_name, window, command))

    f.close()
    os.chmod(script_name, 0o775)

if __name__ == "__main__":
    if not running_in_screen():
        raise SystemError("screen-saver must be run inside of a GNU-screen.")
    save()
