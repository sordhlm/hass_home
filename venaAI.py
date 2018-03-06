from hassAPI import *
from wxpy import *
import logging
import aiml
import os
import re

class venaAI(object):
    def __init__(self):
        self.hass = hassAPI()
        self._loadAIML()
        cwd = os.getcwd()
    def _loadAIML(self):
        self.vena = aiml.Kernel()
        cwd = os.getcwd()
        aiml_path = cwd+'/lib/Py3kAiml/'
        xml_file = aiml_path + 'std-startup.xml'
        os.chdir(aiml_path)
        self.vena.learn(xml_file)
        self.vena.respond('LOAD AIML B')
        os.chdir(cwd)
    def _ctrlDev(self,cmd):
        self.hass.cmdProc(cmd)
    def _srhInfo(self):
        pass
    def aimlTalk(self,cmd):
        res = self.vena.respond(cmd)
        return res

    def aimlUnderstand(self,cmd):
        if cmd['usr'] == 'dev':
            resp = self.vena.respond('HASS CONTROL')
        resp = self.vena.respond(cmd['cmd'])
        #logging.debug(resp)
        print(resp)
        if 'hass' in resp:
            id = 0
        elif 'srh' in resp:
            id = 1
        else:
            id = 2
        return (id, resp)
    def _devCtrlCmdParse(self,cmd):
        trans = {}
        cl = cmd.split(' ')
        trans['target'] = cl[0]
        trans['act'] = cl[1]
        trans['eid'] = cl[2]
        return trans
    def _isValidCmd(self,cmd):
        return 1
        if len(cmd) != 2:
            return 0
        elif (cmd['usr'] != 'master') or (cmd['usr'] != 'dev'):
            return 0
        elif (cmd['usr'] != 'dev') and ('hass' in cmd['cmd']):
            return 0
        else:
            return 1
    def brain(self,cmd):
        if self._isValidCmd(cmd):
            cmdp = self.aimlUnderstand(cmd)
            if cmdp[0] == 0:
                trans = self._devCtrlCmdParse(cmdp[1])
                self._ctrlDev(trans)
            elif cmdp[0] == 1:
                self._srhInfo(cmdp[1])
            else:
                logging.info(cmdp[1])
        else:
            logging.info('Invalid Usr or Command!')




if __name__ == "__main__":
    api = hassAPI()
    vena = venaAI()
    while True:
        cmd = input('Enter your cmd:')
        print(vena.aimlTalk(cmd))
    #bot = Bot(console_qr=True, cache_path=True)
    #while True:
    #    my_friend = bot.friends().search('幸运的大娜')[0]
    #    @bot.register()
    #    def just_print(msg):
    #打印消息
    #        print(msg)
    #        if 'turn on' in msg.text:
    #            print ('get turn on light cmd')
    #            api.turnOn('light.Living_Room')
    #        elif 'turn off' in msg.text:
    #            print ('get turn off light cmd')
    #            api.turnOff('light.Living_Room')
    #        elif 'shutdown' in msg.text:
    #            print('get shutdown cmd')
    #            exit(1)
