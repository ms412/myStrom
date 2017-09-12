
import os
import time
from threading import Thread
import paho.mqtt.client as mqtt




class mqttclient(Thread):
    def __init__(self,config):
        Thread.__init__(self)
        self._host = str(config.get('HOST', 'localhost'))
        self._port = int(config.get('PORT', 1883))
        print(self._host, self._port)
        self._mqttc = mqtt.Client(str(os.getpid()), clean_session=True)

        self._mqttc.on_message = self.on_message
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe

        self.connect()

    def on_connect(self, mqttc, obj, flags, rc):
        print("connect rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        print('message')
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def subscribe(self,topic):
        self._mqttc.subscribe(topic,0)

    def callback(self,topic,data):
        self._mqttc.message_callback_add(topic,data)

    def connect(self):
        self._mqttc.connect(self._host,self._port)

    def publish(self,topic,payload):
        self._mqttc.publish(topic,payload,0)

    def run(self):
       # self._mqttc.connect("192.168.2.50", 1883, 60)
        self.subscribe("/MYSTROM/#")
        print('run')

        rc = 0
        while rc == 0:
            print('x')
            rc = self._mqttc.loop_forever()
        return rc


class printer1(object):
    def output(self,mqttc, obj,msg):
        print('putput1', msg)


class printer2(object):
    def output(self, mqttc, obj, msg):
        print('putput2', msg)


if __name__ == '__main__':

    pp1 = printer1()
    pp2 = printer2()

 #   mqttsub.mqttsubscribe()
    mqttsub = mqttclient({'HOST':'192.168.2.50','PORT':1883})
    #mqttsub.connect()
    #mqttsub.subscribe('/MYSTROM')


#    mqttc = mqttclient()
    mqttsub.callback('/MYSTROM/myStrom1',pp1.output)
    mqttsub.callback('/MYSTROM/myStrom2',pp2.output)
    print('test')
    mqttsub.start()


 #   mqttpub = mqttpublisher({'HOST':'192.168.2.50','PORT':1883})

  #  print('test',rc = mqttsub.run())

    while(True):
        mqttsub.publish('/TEST','1234567')
        time.sleep(10)
  #  mqttpub.publish('/TEST', 'uuuuuuuuuuuuuuuu')
    #time.sleep(2)
   # mqttpub.publish('/TEST', 'uuuuuuuuuuuuuuuu')
    #time.sleep(2)
    #mqttpub.publish('/TEST', 'uuuuuuuuuuuuuuuu')


    #print("rc: "+str(rc))