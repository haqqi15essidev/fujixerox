import json
import datetime
import pytz
from cbuffdiff import *
from pysnmp.hlapi import *
import paho.mqtt.client as mqtt
from res_mqtt_data import *

__engineversion__ = "devbuild 2"
dataPackageContainer = []
errorPackageContainer = []
errorcompare = []
olddata = []


def getversion():
	return __engineversion__

def mainfunc(iterator, managerid, targettopic = "printer/log/data"):
	errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
	print("Grabbing data from printer")
	if errorIndication:  # SNMP engine errors
		print(errorIndication)
		currenttime = str(datetime.now(pytz.timezone('Asia/Jakarta'))).split('.')[0]
		noreplypackage = {}
		norep = {}
		norep[currenttime] = {"0":"No Reply"}
		noreplypackage[managerid] = norep
		transport_data(broker, port, noreplypackage)
	else:
		if errorStatus:  # SNMP agent errors
			print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
		else:
			global dataPackageContainer
			currenttime = str(datetime.now(pytz.timezone('Asia/Jakarta'))).split('.')[0]
			print("Data acquired at %s managerID : %s" % (currenttime, managerid))
			idheader = {"managerid" : managerid}
			completelist = []
			completelist = getDataSet(varBinds)
			dataPackageContainer = completelist
			print(dataPackageContainer)
			try:
				print("Attempting to send to %s" % broker)
				transport_data(broker, port, dataPackageContainer)
				dataPackageContainer = []
				print("Data successfully sent")
			except:
				print("in except")
				print("Failed to send data")
				print("Data in memory : %d" % len(dataPackageContainer))

def errfunc(iterators, managerid, targettopic = "printer/log/error"):
	global olddata
	varBinds = []
	for iterator in iterators:
		iteratordata = next(iterator)
		errorIndication = iteratordata[0]
		errorStatus = iteratordata[1]
		errorIndex = iteratordata[2]
		varBinds.extend(iteratordata[3])
	print("Grabbing errors from printer")
	if errorIndication:  # SNMP engine errors
		print(errorIndication)
		currenttime = str(datetime.now(pytz.timezone('Asia/Jakarta'))).split('.')[0]
		noreplypackage = {}
		norep = {}
		norep[currenttime] = {"0":"No Reply"}
		noreplypackage[managerid] = norep
		transport_error(broker, port, noreplypackage)
	else:
		if errorStatus:  # SNMP agent errors
			print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
		else:
			global errorPackageContainer
			global errorcompare
			currenttime = str(datetime.now(pytz.timezone('Asia/Jakarta'))).split('.')[0]
			print("Data acquired at %s managerID : %s" % (currenttime, managerid))
			idheader = {"managerid" : managerid}
			completelist = []
			newvallist = []
			
			completelist = getDataSet(varBinds, timestamp=0)
			newvallist = getValueOnly(completelist)
			errorlist = getNewData(newvallist, olddata);

			if (len(errorlist) > 0):
				print("New data available")
				errorPackageContainer= errorlist
			else:
				print("No data available")
				olddata = newvallist.copy()
			
			print("EPC in loop --> %s" % errorPackageContainer)
			# print("error compare in loop --> %s" % errorcompare)
			# print("=====================================================================")
			# difference = list(set(errorPackageContainer) - set(errorcompare))
			# print("different both --> %s" % difference)
			# try:
			# 	print("try to sending MQTT error payload....")
			# 	transport_error(managerid, broker, port, errrorPackageContainer)
			# 	print("DONE....")
			# except:
			# 	print("sending MQTT error payload is failed...")

			if len(errorcompare) == 0:
				print("first time to sending")
				transport_error(managerid, broker, port, errorPackageContainer)
				errorcompare = errorPackageContainer
			else:
				# print("errorcompare is not empty")
				try:
					if len(difference) > 0 :
						print("new error available")
						errorcompare = errorPackageContainer
						transport_error(managerid, broker, port, errorPackageContainer)
						errorPackageContainer = []
						print("Data successfully sent")
					else:
						print("no error occured")
						errorcompare = errorPackageContainer
				except:
					print("failed to transport error")
				

def getDataSet(varBinds, timestamp=1):
	dumpdict = []
	
	if(timestamp):
		currenttime = str(datetime.now(pytz.timezone('Asia/Jakarta'))).split('.')[0]
		timestampoid = {'oid':"timestamp", 'value':currenttime}
		dumpdict.append(timestampoid)
	
	for varBind in varBinds:  # SNMP response content
		oidmsg = str(varBind)
		oidvalue = oidmsg[oidmsg.index("=")+2::]
		oiddesc = oidmsg[oidmsg.index("::")+2:oidmsg.index("=")]
		if "No Such Instance currently exists at this OID" in oidvalue:
			oidvalue = "N/A"
		keyvalpair = {'oid':oiddesc, 'value':oidvalue}
		dumpdict.append(keyvalpair)
	return dumpdict
	
def getValueOnly(datas):
	retlist = []
	for a in datas:
		retlist.append(a['value'])
	return retlist	
	
def getErrorList(varBinds, olderrorlist):
	newerrorlist = []
	for varBind in varBinds:  # SNMP response content
		oidmsg = str(varBind)
		oidvalue = oidmsg[oidmsg.index("=")+2::]
		oiddesc = oidmsg[oidmsg.index("::")+2:oidmsg.index("=")]
		if "No Such Instance currently exists at this OID" in oidvalue:
			oidvalue = "N/A"
		keyvalpair = {'oid':oiddesc, 'value':oidvalue}
		newerrorlist.append(keyvalpair)
		
		
	currenttime = str(datetime.now(pytz.timezone('Asia/Jakarta'))).split('.')[0]
	dumpdict = []
	
	timestampoid = {'oid':"timestamp", 'value':currenttime}
	dumpdict.append(timestampoid)
	

	return dumpdict