
import os
import time
import paho.mqtt.client as mqtt

class mqttpublisher(object):
    def __init__(self,config):

        self._host = config.get('HOST')
        self._port = config.get('PORT')

        self._client = mqtt.Client()
        self._client.connect(self._host,self._port)
       # self._client.connect('192.168.2.50',1883,60)

    def __del__(self):
        self._client.disconnect()

    def publish(self,topic,data):
        self.publish(topic,data)


class mqttsubscribe(object):
    def __init__(self,config):
        self._host = config.get('HOST', 'localhost')
        self._port = config.get('PORT', 1883)
        print(self._host, self._port)
        self._mqttc = mqtt.Client(str(os.getpid()), clean_session=True)

        self._mqttc.on_message = self.on_message
        self._mqttc.on_connect = self.on_connect
        self._mqttc.on_publish = self.on_publish
        self._mqttc.on_subscribe = self.on_subscribe

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

    def run(self):
        self._mqttc.connect("192.168.2.50", 1883, 60)
        self.subscribe("/MYSTROM/#")
        print('run')

        rc = 0
        while rc == 0:
            rc = self._mqttc.loop()
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
    mqttsub = mqttsubscribe({'HOST':'192.168.2.50','PORT':1883})
    #mqttsub.connect()
    #mqttsub.subscribe('/MYSTROM')


#    mqttc = mqttclient()
    mqttsub.callback('/MYSTROM/myStrom1',pp1.output)
    mqttsub.callback('/MYSTROM/myStrom2',pp2.output)
    print('test')
    mqttsub.run()


 #   mqttpub = mqttpublisher({'HOST':'192.168.2.50','PORT':1883})

    print('test',rc = mqttsub.run())

  #  mqttpub.publish('/TEST', 'uuuuuuuuuuuuuuuu')
    time.sleep(2)
   # mqttpub.publish('/TEST', 'uuuuuuuuuuuuuuuu')
    time.sleep(2)
    #mqttpub.publish('/TEST', 'uuuuuuuuuuuuuuuu')


    print("rc: "+str(rc))