from colorama import init
from termcolor import *
import time


init()

class Printer():

    def current_time(self):
        tmp = str(
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        return "[" + tmp + "]"

    def printer(self, string, info, color,printable=True):
        ctm = self.current_time()
        tmp = "[" + str(info) + "]"
        if printable:
            msg = ("{:<22}{:<15}{:<20}".format(str(ctm), str(tmp), str(string)))
            print(colored(msg, color), flush=True)
            with open("log.txt","a+",encoding="utf-8")as f:
                f.write(msg+"\n")
        else:
            pass
