#!/usr/bin/python3

import sys
import time
import curses


class Config:
    prefix = "CPU Temperature: "
    color = False


def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        return int(f.read().strip()) / 1000.0


def print_cpu_temp():
    temp = get_cpu_temp()
    end = "\x1B[0m"
    if Config.color:
        if temp >= 80:
            color = "31;1"
        elif temp >= 70:
            color = "33;1"
        elif temp >= 50:
            color = "36;1"
        else:
            color = "32;1"
        print("\r\x1B[K{}\x1B[{}m{}'C".format(Config.prefix, color, temp), end=end)
    else:
        print("\r\x1B[K{}{}'C".format(Config.prefix, temp), end=end)


def main_loop():
    while True:
        print_cpu_temp()
        time.sleep(1)


def parse_args():
    for arg in sys.argv[1:]:
        if arg in {"-C", "--color"}:
            Config.color = True


def main(scr=None):
    try:
        main_loop()
    except (KeyboardInterrupt, SystemExit):
        print()
        return
    finally:
        pass


if __name__ == "__main__":
    parse_args()
    main()
