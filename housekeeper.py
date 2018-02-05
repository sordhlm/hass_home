from hassAPI import *
from venaAI import *
from wxpy import *
from multiprocessing import Process,Queue
import queue
import time
import sys,os
import logging

class housekeeper(object):
    def __init__(self):
        self.msgQ = Queue()
        self.hass = hassAPI()
        self.vena = venaAI()
        self.delta = 1
    def _checkDev(self):
        pass

    def msgProc(self,fn):
        sys.stdin = os.fdopen(fn)
        cmdl = {}
        while True:
            time.sleep(self.delta)
            cmd = input('Enter your cmd:')
            cmdl['usr'] = 'master'
            cmdl['cmd'] = cmd
            self.msgQ.put(cmdl)

    def cmdProc(self):
        while True:
            #time.sleep(1)
            cmd = self.msgQ.get()
            #print('get cmd:%s'%cmd)
            self.vena.brain(cmd)

if __name__ == "__main__":
    shome = housekeeper()
    logging.basicConfig(level=logging.DEBUG)
    fn = sys.stdin.fileno()
    #while True:
    #    a = sys.stdin.readline()
    #    print(a)
    p1 = Process(target=shome.msgProc, args=(fn,))
    p2 = Process(target=shome.cmdProc, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()
