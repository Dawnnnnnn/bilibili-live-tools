from colorama import init
from termcolor import *
import time


init()

class Printer():
    instance = None

    def __new__(cls, thoroughly_log=None, *args, **kw):
        if not cls.instance:
            cls.instance = super(Printer, cls).__new__(cls)
            cls.instance.thoroughly_log = True if thoroughly_log == "1" else False
        return cls.instance

    def current_time(self):
        tmp = str(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        return "[" + tmp + "]"

    def printer(self, string, info, color, printable=True):
        ctm = self.current_time()
        tmp = "[" + str(info) + "]"
        if printable:
            msg = ("{:<22}{:<10}{:<20}".format(str(ctm), str(tmp), str(string)))
            print(colored(msg, color), flush=True)
            if self.thoroughly_log or info in ["Error", "Warning"]:
                with open(f"log_{time.strftime('%Y%m')}.txt", "a+", encoding="utf-8") as f:
                    f.write(msg+"\n")
        else:
            pass
