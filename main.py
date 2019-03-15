#!/usr/bin/python3

import sys
import time
import curses


class Config:
    temp_source = "/sys/class/thermal/thermal_zone0/temp"
    freq_source = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"

    temp_prefix = "CPU Temperature: "
    freq_prefix = "CPU Frequency: "
    color = False


def get_cpu_temp():
    with open(Config.temp_source, "r") as f:
        return int(f.read()) / 1000.0


def get_cpu_freq():
    with open(Config.freq_source, "r") as f:
        return int(f.read()) / 1000.0  # This converts KHz to MHz


def format_cpu_temp():
    temp = get_cpu_temp()
    if Config.color:
        if temp >= 80:
            color = "31;1"
        elif temp >= 70:
            color = "33;1"
        elif temp >= 50:
            color = "36;1"
        else:
            color = "32;1"
        return "\x1B[K{}\x1B[{}m{}'C".format(Config.temp_prefix, color, temp)
    else:
        return "\x1B[K{}{}'C".format(Config.temp_prefix, temp)


def format_cpu_freq():
    freq = get_cpu_freq()
    if freq >= 1000:
        freq_s = "{:.2f} GHz".format(freq / 1000)
    else:
        freq_s = "{:g} MHz".format(freq)
    if Config.color:
        if freq >= 1200:
            color = "31;1"
        elif freq >= 1000:
            color = "33;1"
        elif freq >= 800:
            color = "36;1"
        else:
            color = "32;1"
        return "\x1B[K{}\x1B[{}m{}".format(Config.freq_prefix, color, freq_s)
    else:
        return "\x1B[K{}{}".format(Config.freq_prefix, freq_s)


def print_cpu_temp():
    print("\r" + format_cpu_temp(), end="\x1B[0m")


def print_cpu_freq():
    print("\r" + format_cpu_freq(), end="\x1B[0m")


def print_all():
    print("\x1B[F" + format_cpu_temp() + "\x1B[0m\n" + format_cpu_freq(), end="\x1B[0m")


def main_loop():
    while True:
        print_all()
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
