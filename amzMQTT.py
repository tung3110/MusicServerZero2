import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
class ConectMQTT:
    def __init__(self, broker,user,pwd,port,on_connect,on_message):
        self.broker = broker
        self.user = user
        self.pwd = pwd
        self.port = port
        self.on_connect = on_connect
        self.on_message = on_message
        print("Ket noi MQTT online {}, {},{},{})".format(broker,user,pwd,port))
    def publish_mqtt(self,topic,sensor_data):
        print(sensor_data)
        mqttc = mqtt.Client("python_pub")
        mqttc.username_pw_set(username=self.user, password=self.pwd)
        mqttc.connect(self.broker, self.port)
        Pub_RadioTech = topic
        mqttc.publish(Pub_RadioTech, sensor_data)
    def ConectMQTT(self):
        try:
                #global MQTT_Timeout
                #MQTT_Timeout = 30
                print("conect MQTT  1 ",self.broker)
                client = mqtt.Client()
#client = mqtt.Client(client_id= "" ,clean_session=True, userdata=None, protoco$
                client.on_connect = self.on_connect
                client.on_message = self.on_message
                client.tls_set()  # <--- even without arguments
                client.username_pw_set(username=self.user, password=self.pwd)
                print("step 2")
                client.connect(self.broker, self.port)
                print("step 3")
                client.loop_start()
                print("end")
        except:
                MQTT_Flag = 0
                print("Khong the ket noi MQTT online") 