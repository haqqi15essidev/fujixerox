#SNMPENGINE in python

Gets SNMP data and then publish it via MQTT.

The script will automatically detects which snmp version (v2 or v3) to use by probing the oid. If neither version works, it will keep probing until the process is killed.


##Dependencies

This project requires these libraries, which can be obtained through pip

* paho-mqtt
* pysnmp
* pytz

##Usage

Run snmptester.py from terminal or cmd

###snmptester.py -a <printerip> -t <targettopic> -u <authuser> -k <authkey> -p <privatekey>'

-a : printer's IP Address
-t : mqtt topic to publish to
-u : SNMP3 authentication username
-k : SNMP3 authentication key
-p : SNMP3 authentication private key

###Configuration file

MQTT host and port settings are configured from the configs.py file. Please edit the file accordingly.

##Changelog

###beta 3
* Added error log acquisition