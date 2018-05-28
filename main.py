# !/usr/bin/python
# -*- coding:utf-8 -*-
import subprocess, time, sys

TIME = 3600
CMD = "run.py"


class Auto_Run():
    def __init__(self, sleep_time, cmd):
        self.sleep_time = sleep_time
        self.cmd = cmd
        self.ext = (cmd[-3:]).lower()
        self.p = None
        self.run()

        try:
            while 1:
                time.sleep(sleep_time * 20)
                self.poll = self.p.poll()
                if self.p.poll() is None:
                    print("restarting......")
                    self.p.kill()
                    self.run()

                else:
                    print("starting......")
                    self.run()
        except KeyboardInterrupt as e:
            print("exit???")

    def run(self):
        if self.ext == ".py":
            print('start OK!')
            self.p = subprocess.Popen(['python', '%s' % self.cmd], stdin=sys.stdin, stdout=sys.stdout,
                                      stderr=sys.stderr, shell=False)
        else:
            pass


app = Auto_Run(TIME, CMD)
