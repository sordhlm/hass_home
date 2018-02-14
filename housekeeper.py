from hassAPI import *
from venaAI import *
from wxpy import *
from multiprocessing import Process,Queue,Value,Manager
import time
import sys,os
import logging
from lib.dataStructure import *

class housekeeper(object):
    def __init__(self):
        self.msgQ = Queue()
        self.hass = hassAPI()
        self.vena = venaAI()
        self.delta = 1
        self.nte = Value('i',0)

    def sensorRec(self):
        cmdl = {}
        while True:
            time.sleep(5)
            cmdl['usr'] = 'dev'
            cmdl['cmd'] = 'hass door open'
            self.msgQ.put(cmdl)

    def remoteRec(self,fn):
        pass

    def msgRec(self,fn):
        pass

    def debugRec(self,fn):
        sys.stdin = os.fdopen(fn)
        cmdl = {}
        while True:
            time.sleep(self.delta)
            cmd = input('[Debug]Enter your cmd:')
            cmdl['usr'] = 'master'
            cmdl['cmd'] = cmd
            self.msgQ.put(cmdl)

    def cmdProc(self):
        while True:
            #time.sleep(10)
            cmd = self.msgQ.get()
            logging.debug('get cmd:%s'%cmd)
            self.vena.brain(cmd)

if __name__ == "__main__":
    shome = housekeeper()
    logging.basicConfig(level=logging.DEBUG)
    fn = sys.stdin.fileno()
    #while True:
    #    a = sys.stdin.readline()
    #    print(a)
    p1 = Process(target=shome.debugRec, args=(fn,))
    p2 = Process(target=shome.sensorRec, args=())
    p3 = Process(target=shome.cmdProc, args=())

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
