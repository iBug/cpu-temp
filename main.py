#!/usr/bin/python3

import sys
import time
import curses


class Config:
    temp_source = "/sys/class/thermal/thermal_zone0/temp"
    freq_source = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"

    temp_prefix = "CPU Temperature: "
    freq_prefix = "CPU Frequency: "
    usage_prefix = "CPU Utilization: "
    color = False
    last_usage = None


def get_cpu_temp():
    with open(Config.temp_source, "r") as f:
        return int(f.read()) / 1000.0


def get_cpu_freq():
    with open(Config.freq_source, "r") as f:
        return int(f.read()) / 1000.0  # This converts KHz to MHz


def get_cpu_usage():
    with open("/proc/stat", "r") as f:
        for line in f:
            if line.startswith("cpu "):
                items = line.split()
                a, b, c = int(items[1]), int(items[3]), int(items[4])
                if Config.last_usage is None:
                    Config.last_usage = a, b, c
                    return 1  # Placeholder
                else:
                    la, lb, lc = Config.last_usage
                    Config.last_usage = a, b, c
                    a -= la
                    b -= lb
                    c -= lc
                    return (a + b) / (a + b + c)


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


def format_cpu_usage():
    usage = get_cpu_usage() * 100
    if Config.color:
        if usage >= 90:
            color = "31;1"
        elif usage >= 75:
            color = "33;1"
        elif usage >= 50:
            color = "36;1"
        else:
            color = "32;1"
        return "\x1B[K{}\x1B[{}m{:.1f}%".format(Config.usage_prefix, color, usage)
    else:
        return "\x1B[K{}{:.1f}%".format(Config.usage_prefix, usage)


def print_cpu_temp():
    print("\r" + format_cpu_temp(), end="\x1B[0m")


def print_cpu_freq():
    print("\r" + format_cpu_freq(), end="\x1B[0m")


def print_cpu_usage():
    print("\r" + format_cpu_usage(), end="\x1B[0m")


def print_all():
    print("\x1B[2F" + format_cpu_temp() + "\x1B[0m\n" + format_cpu_freq() + "\x1B[0m\n" + format_cpu_usage(), end="\x1B[0m")


def main_loop():
    print(end="\n\n")
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
