from requests import get
from requests import post
import logging, json, time, datetime
import re


class hassIF(object):

    def __init__(self, ip='192.168.1.108', passwd='Pian#0919'):
        self.url = 'http://%s:8123/api/' % ip
        self.head = {'x-ha-access': '%s' % passwd,'content-type': 'application/json'}

    def _getRes(self, url):
        return json.loads(get(url, headers=self.head).text)

    def _postRes(self, url, data):
        return json.loads(post(url, data=json.dumps(data), headers=self.head).text)
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

class hass_weather(hassIF):
    def __init__(self):
        super(hass_weather,self).__init__()
        self.__initstat()
    def __initstat(self):
        self.weather = {}
        serv = self.getStatus()
        for i in serv:
            if 'sensor.weather' in i['entity_id']:
                self.weather[i['entity_id']] = i['state']
    def weatherDisplay(self):
        for i in self.weather.keys():
            print ('eid: %s, stat: %s'%(i,self.weather[i]))
    def weatherChk(self):
        ret = ''
        logging.debug('temperature: %d'%int(self.weather['sensor.weather_temperature']))
        if int(self.weather['sensor.weather_temperature']) < 0:
            ret = 'hass temperature very cold'
        elif int(self.weather['sensor.weather_temperature']) < 10:
            ret = 'hass temperature bit cold'
        elif int(self.weather['sensor.weather_temperature']) < 30:
            ret = 'hass temperature good'
        elif int(self.weather['sensor.weather_temperature']) < 35:
            ret = 'hass temperature bit hot'
        else:
            ret = 'hass temperature very hot'
        return ret



class hass_sensor(hassIF):
    def __init__(self,id = '',stat = 0):
        super(hass_sensor,self).__init__()
        self.id = id
        self.stat = stat
        self._initstat()
    def _initstat(self):
        self.getSer()
    def getSer(self):
        serv = self.getStatus()
        #logging.debug(serv)
        dev_name = self.id
        for i in serv:
            if dev_name in i['entity_id']:
                self.stat = 1 if 'on' in i['state'] else 0
                logging.debug('%s state update: %d'%(self.id,self.stat))
                #logging.debug(i)
    def chkStat(self):
        old_stat = self.stat
        self.getSer()
        if ((old_stat & 1) ^ (self.stat & 1)) == 0:
            return 0
        elif (old_stat == 1 and self.stat == 0): #door is closing
            return 1
        else:  # door is opening
            return 2


class hass_light(hassIF):
    def __init__(self,id, stat=0, att = None):
        super(hass_light,self).__init__()
        self.id = id
        self.stat = stat
        if att != None:
            self.att = att
        self._initAttr()
    def _initAttr(self):
        if 'red' not in self.att.keys():
            self.att['red'] = 100
        if 'green' not in self.att.keys():
            self.att['green'] = 100
        if 'blue' not in self.att.keys():
            self.att['blue'] = 100
        if 'bright' not in self.att.keys():
            self.att['bright'] = 200
    def updateAttr(self,cmd):
        logging.debug('%s update attributions'%(self.id))
        m = re.search('(\w+)([+-]\d+)',cmd)
        name = m.group(1)
        act = m.group(2)
        logging.debug('old %s: %d'%(name,self.att[name]))
        self.att[name] = eval('%s%s'%(self.att[name],act))
        if self.att[name] < 0:
            self.att[name] = 0
        elif self.att[name] > 255:
            self.att[name] = 255
        logging.debug('new %s: %d' % (name, self.att[name]))
    def turnOn(self):
        url = self.url + 'services/light/turn_on'
        data = {'entity_id': '%s' % self.id,'rgb_color': [self.att['red'], self.att['green'], self.att['blue']],
                'brightness': self.att['bright']}
        return self._postRes(url, data)

    def turnOff(self):
        url = self.url + 'services/light/turn_off'
        data = {'entity_id': '%s' % self.id}
        return self._postRes(url, data)
    def turnRed(self,attr)
        att = {}
        att['red'] = 255
        att['green'] = 0
        att['blue'] = 0
        att['bright'] = 200
        pass
    def getLightSer(self):
        serv = self._getServ()
        for i in serv:
            if i['domain'] == 'light':
                return i

class hassAPI(object):
    def __init__(self):
        self.hif = hassIF()
        self.light = {}
        self.sensor = {}
        self._initHass()
    def _initLight(self,stat):
        att = {}
        att['red'] = 255
        att['green'] = 0
        att['blue'] = 0
        att['bright'] = 200
        for i in stat:
            if 'light.' in i['entity_id']:
                eid = i['entity_id']
                stat = 1 if 'on' in i['state'] else 0
                self.light[eid] = hass_light(eid,stat,att)
                logging.debug('Create light: %s'%eid)
    def _initSensor(self,stat):
        for i in stat:
            if 'binary_sensor.' in i['entity_id']:
                eid = i['entity_id']
                stat = 1 if 'on' in i['state'] else 0
                self.sensor[eid] = hass_sensor(eid,stat)
                logging.debug('Create Sensor: %s'%eid)
    def _initHass(self):
        stat = self.hif.getStatus()
        self._initLight(stat)
        self._initSensor(stat)
    def cmdProc(self, cmd):
        if 'hass_light' in cmd['target']:
            self.lightCtrl(cmd)
    def lightCtrl(self,cmd):
        att = {}
        att['red'] = 255
        att['green'] = 0
        att['blue'] = 0
        att['bright'] = 200
        logging.debug(cmd)
        eid = 'light.' + cmd['eid']
        act = cmd['act']
        if eid not in self.light.keys():
            logging.debug('new light init')
            self.light[eid] = hass_light(eid,0,att)
        logging.debug('length is %d'%len(cmd))
        if len(cmd) > 3:
            self.light[eid].updateAttr(cmd[3])
        getattr(self.light[eid],act)()

    def time_chk(self):
        t_morn = datetime.time(7,0,0)
        t_up = datetime.time(7,30,0)
        t_night = datetime.time(19,0,0)
        t_now = datetime.datetime.time(datetime.datetime.now())
        if (t_now > t_morn) and (t_now < t_up):
            return 'morning'
        elif (t_now > t_night):
            return 'night'

    def getDevStat(self):
        #cmdl = 'hass livingroom door open'
        #print(self.sensor)
        cmd = 0
        for i in self.sensor.keys():
            ret = self.sensor[i].chkStat()
            logging.debug('%s sensor check: %d'%(i,ret))
            t = time_chk()
            if ('motion_sensor') in i and (ret == 2) and ('night' in t):
                return 'hass livingroom1bed people appear'
            elif ('morning' in t):
                return 'hass livingroom1desk weather bad'

        return cmd






if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    wea = hass_weather()
    stat = wea.getStatus()
    for i in stat:
        print(i)
    wea.weatherDisplay()
    ret = wea.weatherChk()
    print(ret)
