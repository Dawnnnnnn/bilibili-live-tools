# !/usr/bin/python
# -*- coding:utf-8 -*-
import subprocess, time, sys

TIME = 3600
CMD = "run.py"


class Auto_Run():
    def __init__(self, sleep_time, cmd):
        if sys.version_info < (3, 6):
            print("only support python 3.6 and later version")
            sys.exit(1111)
        self.sleep_time = sleep_time
        self.cmd = cmd
        self.ext = (cmd[-3:]).lower()
        self.p = None
        self.run()

        try:
            while 1:
                time.sleep(sleep_time * 20)
                if self.p.poll() is None:
                    print("restarting......")
                    self.p.kill()
                    self.run()

                else:
                    print("starting......")
                    self.run()
        except KeyboardInterrupt as e:
            self.p.kill()
            print("exit???")

    def run(self):
        if self.ext == ".py":
            print('start OK!')
            # use now running python version, think multiple python installed and now use python3.6 to run
            python_path = sys.executable
            print("use the absolute path of python to run", python_path)
            self.p = subprocess.Popen([python_path, '%s' % self.cmd], stdin=sys.stdin, stdout=sys.stdout,
                                      stderr=sys.stderr, shell=False)
        else:
            pass


app = Auto_Run(TIME, CMD)
