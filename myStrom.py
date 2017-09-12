#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


__app__ = "owntracks Gateway"
__VERSION__ = "0.4"
__DATE__ = "04.09.2017"
__author__ = "Markus Schiesser"
__contact__ = "M.Schiesser@gmail.com"
__copyright__ = "Copyright (C) 2017 Markus Schiesser"
__license__ = 'GPL v3'

import time
import os
import glob
import json
import cherrypy
from configobj import ConfigObj
from library.mqttclient import mqttclient
from library.httpd import httpd



class myStrom2mqtt(object):

    def __init__(self,configfile):
        self._configfile = configfile

#        self._storage = nesteddict()
      #  self._storage['STATUS']='INIT'

        self._mqttc = None

        self._logCfg = None
        self._owntracksCfg = None
        self._httpdCfg = None
        self._mqttCfg = None

        self._cardFileManager = None
        self._cmdFileManager = None
        self._cardUpdate = True

    def readConfigFile(self):
        _cfg = ConfigObj(self._configfile)
        print('zzz',_cfg)

        self._logCfg = _cfg.get('LOGING')
        self._mqttCfg = _cfg.get('MQTT')
        self._httpdCfg = _cfg.get('HTTPD')
        self._owntracksCfg = _cfg.get('OWNTRACKS')
        return True

    def startHttpd(self):
        _httpdCfg = {}
        _httpdCfg['server.socket_host'] = str(self._httpdCfg.get('SOCKET','0.0.0.0'))
        _httpdCfg['server.socket_port'] = int(self._httpdCfg.get('PORT', 9888))

        cherrypy.config.update(_httpdCfg)

        USERS = {"admin": "2Sec4You", "test": "test", "test": "mobil"}

        conf = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
               # 'tools.sessions.on': True,
                'tools.response_headers.on': True,
                'tools.response_headers.headers': [('Content-Type', 'application/json')],
                'tools.encode.on': True,
                'tools.encode.encoding': 'utf-8'
             #   'tools.auth_basic.on': True,
              #  'tools.auth_basic.realm': 'localhost'
               # 'tools.auth_basic.checkpassword': validate_password
            }

        }

        _gw = httpd()
        _gw.register_callback(self.httpCallback)
        print('config', cherrypy.config)
        cherrypy.tree.mount(_gw,'/',conf)
        cherrypy.engine.start()
        return True

    def httpCallback(self):
        pass

    def startMqtt(self):
        self._mqttc = mqttclient(self._mqttCfg)


        self._mqttc.register_callback('owntracks/+/+',self.mqttCallback)
      #  self._mqttc.register_callback('owntracks/+/+/card', self._updateCard)
       # self._mqttc.register_callback('owntracks/#', self._updatePossition)
    #    self._mqttc.callback(self.msgBroker)
        self._mqttc.connect()
        self._mqttc.run()

        self._mqttc.subscribe('+/+')
        return True

    def run(self):
        self.readConfigFile()
        self.startHttpd()



if __name__ == '__main__':

    myMqtt = myStrom2mqtt('myStrom2mqtt.cfg')
    myMqtt.run()