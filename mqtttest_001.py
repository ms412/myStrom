import paho.mqtt.client as mqtt

class printer1(object):

    def output(self,mqttc, obj,msg):
        print('putput1', msg)


class printer2(object):
    def output(self, mqttc, obj, msg):
        print('putput2', msg)


class MyMQTTClass(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, rc):
        print("connect rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        print('message')
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

   # def on_log(self, mqttc, obj, level, string):
    #    print(string)

    def subs(self,channel,obj):
        self.message_callback_add(channel,obj)

    def run(self):
        self.connect("192.168.2.50", 1883, 60)
        self.subscribe("/MYSTROM/#", 0)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc


# If you want to use a specific client id, use
# mqttc = MyMQTTClass("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
pp1 = printer1()
pp2 = printer2()
mqttc = MyMQTTClass()
mqttc.subs('/MYSTROM/myStrom1',pp1.output)
mqttc.subs('/MYSTROM/myStrom2',pp2.output)

rc = mqttc.run()

print("rc: "+str(rc))