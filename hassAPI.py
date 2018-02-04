from requests import get
from requests import post
import logging, json, time

class hassAPI(object):

    def __init__(self, ip='192.168.1.108', passwd='Pian#0919'):
        self.url = 'http://%s:8123/api/' % ip
        self.head = {'x-ha-access': '%s' % passwd,'content-type': 'application/json'
           }

    def _getRes(self, url):
        return json.loads(get(url, headers=self.head).text)

    def _postRes(self, url, data):
        return json.loads(post(url, data=json.dumps(data), headers=self.head).text)

    def turnOn(self, id, red=255, green=100, blue=100, bright=200):
        url = self.url + 'services/light/turn_on'
        data = {'entity_id': '%s' % id,'rgb_color': [red, green, blue],'brightness': bright}
        return self._postRes(url, data)

    def turnOff(self, id):
        url = self.url + 'services/light/turn_off'
        data = {'entity_id': '%s' % id}
        return self._postRes(url, data)

    def getLive(self):
        return self._getRes(self.url)

    def getconfig(self):
        url = self.url + 'config'
        return self._getRes(url)

    def getStatus(self):
        url = self.url + 'states'
        return self._getRes(url)

    def _getServ(self):
        url = self.url + 'services'
        return self._getRes(url)

    def getDiscoveryInfo(self):
        url = self.url + 'discovery_info'
        return self._getRes(url)

    def getEvents(self):
        url = self.url + 'events'
        return self._getRes(url)

    def getEntitystatus(self, entity_id):
        url = self.url + 'states/' + entity_id
        return self._getRes(url)

    def getError(self):
        url = self.url + 'error_log'
        return self._getRes(url)

    def getLightSer(self):
        serv = self._getServ()
        for i in serv:
            if i['domain'] == 'light':
                return i

    def cmdProc(self, cmd):
        eid = cmd[0]
        act = cmd[1]
        if 'turn on' in act:
            logging.debug('get turn on light cmd')
            self.turnOn(eid)
        elif 'turn off' in act:
            logging.debug('get turn off light cmd')
            self.turnOff(eid)

    def getDevStat(self):
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    api = hassAPI()
    cmd = ['light.Living_Room', 'turn on']
    for i in range(0, 20):
        time.sleep(1)
        api.turnOn('light.Living_Room', 255, 255, i * 10)