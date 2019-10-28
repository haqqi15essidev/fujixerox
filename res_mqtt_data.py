
import paho.mqtt.client as mqtt
import time
import json
import pytz
from datetime import datetime

broker="52.163.52.95"
port = 1883

mqtt.Client.connected_flag=False

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True 
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

def on_publish(client, userdata, result):            
    print("data published \n")
    pass

def transport_data(broker, port, data):
    insert_type = {"oid":"data_type","value":"data"}
    data.append(insert_type)
    client = mqtt.Client("client_data")             
    client.on_connect=on_connect               
    client.loop_start()
    print("Connecting to broker ",broker)
    client.connect(broker,port)      
    while not client.connected_flag: 
        print("In wait loop")
        time.sleep(1)
    print("publising data")
    client.on_publish = on_publish                         
    client.connect(broker, port)                                
    ret= client.publish("/printer/log/data",json.dumps(data))
    client.loop_stop()     
    client.disconnect()

def transport_error(sernum, broker, port, data):
    currenttime = str(datetime.now(pytz.timezone('Asia/Jakarta'))).split('.')[0]
    data.insert(0, currenttime)
    data.insert(1, sernum)
    client = mqtt.Client("client_error")             
    client.on_connect=on_connect               
    client.loop_start()
    print("Connecting to broker ",broker)
    client.connect(broker,port)      
    while not client.connected_flag: 
        print("In wait loop")
        time.sleep(1)
    print("publising data")
    client.on_publish = on_publish                         
    client.connect(broker, port)                                
    ret= client.publish("/printer/log/error",json.dumps(data))
    data = []
    client.loop_stop()     
    client.disconnect()



