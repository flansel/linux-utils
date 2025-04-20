import subprocess
import argparse
import os

def save():
    res = subprocess.check_output(['w'])
    res = str(res)
    # break up res into lines, remove the first line which is a header
    res = res.split('\\n')[2:-1]
    res = [r.split(' ')[-1] for r in res]
    
    # build the bash script
    f = open("test.sh", "w")
    f.write("#!/bin/sh\n")
    f.write("screen -dmS test\n")
    f.write("screen -S test -p 0 -X stuff " + res[0] + "\r\n")
    for i in range(1, len(res)):
        f.write("screen -S test -X screen " + str(i) + "\n")
        f.write("screen -S test -p " + str(i) + " -X stuff " + str(res[i]) + "\r\n")

    f.close()
    os.chmod("test.sh", 0o775)

if __name__ == "__main__":
    save()
