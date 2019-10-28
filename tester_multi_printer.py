import time
import sys, getopt
from datetime import datetime, timedelta

__version__ = "beta 3"

printerip = ""
publishto = "printer"
authuser = "Xadmin"
authkey = "12345678"
authpriv = "12345678"

flag_send = 1
errordatainterval = 10
datainterval = 10

from snmp2engine import *
lastrunfunc = time.time()
lastrunerr = time.time()

def tester2():
	print("Testing SNMP Version 2")
	errorIndication, errorStatus, errorIndex, varBinds = next(
	getCmd(SnmpEngine(), CommunityData('public'), UdpTransportTarget((printerip,161)), ContextData(),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.5.1.1.17.1'))))
	if errorIndication:
		print("SNMPv2 Test failed")
		return 0, "N/A"
	else:
		print("SNMPv2 Test success")
		for varBind in varBinds:  # SNMP response conten
			oidmsg = str(varBind)
			oidvalue = oidmsg[oidmsg.index("=")+2::]
		if "No Such Instance currently exists at this OID" in oidvalue:
			oidvalue = "N/A"
		print("Got serial number : %s" % oidvalue)
		sernum = oidvalue
		return 1, oidvalue

def tester3():
	global authuser
	global authkey
	global authpriv
	global managerid
	print("Testing SNMP Version 3")
	errorIndication, errorStatus, errorIndex, varBinds = next(
    	getCmd(SnmpEngine(),
           UsmUserData(authuser,authkey, authpriv,usmHMACMD5AuthProtocol,usmAesCfb128Protocol),
           UdpTransportTarget((printerip, 161)),
           ContextData(),
           ObjectType(ObjectIdentity('1.3.6.1.2.1.43.5.1.1.17.1'))))
	if errorIndication:
		print("SNMPv3 Test failed")
		return 0, "N/A"
	else:
		print("SNMPv3 Test success")
		for varBind in varBinds:  # SNMP response conten
			oidmsg = str(varBind)
			oidvalue = oidmsg[oidmsg.index("=")+2::]
		if "No Such Instance currently exists at this OID" in oidvalue:
			oidvalue = "N/A"
		print("Got serial number : %s" % oidvalue)
		return 1, oidvalue

def snmp2main(mgrid, publishto):
	snmp2func(mgrid, publishto)
	snmp2errfunc(mgrid, publishto)
		
def snmp2func(mgrid, topic):
	global datainterval
	global lastrunfunc
	if (flag_send):
		iterator = getCmd(SnmpEngine(), CommunityData('public'), UdpTransportTarget((printerip, 161)), ContextData(),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.5.1.1.17.1')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.33')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.34')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.43')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.103.20.3')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.7')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.104.20.15')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.1')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.1')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.4')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.6')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.4')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.6')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.3')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.3')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.2')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.2')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.9')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.9')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.8')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.8')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.7')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.7')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.5')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.5')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.101.20.4')))

		mainfunc(iterator, mgrid, targettopic = topic)
			
def snmp2errfunc(mgrid, topic):
	iterator = []
	if (flag_send):
		iterator.append(getCmd(SnmpEngine(), CommunityData('public'), UdpTransportTarget((printerip, 161)), ContextData(),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.1')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.2')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.3')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.4')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.5')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.6')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.7')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.8')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.9')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.10')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.11')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.12')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.13')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.14')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.15')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.16')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.17')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.18')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.19')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.20'))))
		iterator.append(getCmd(SnmpEngine(), CommunityData('public'), UdpTransportTarget((printerip, 161)), ContextData(),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.21')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.22')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.23')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.24')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.25')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.26')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.27')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.28')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.29')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.30')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.31')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.32')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.33')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.34')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.35')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.36')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.37')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.38')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.39')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.40')),
		))
		errfunc(iterator, mgrid, targettopic = topic)

def snmp3main(mgrid, publishto):
	snmp3func(mgrid, publishto)
	snmp3errfunc(mgrid, publishto)

def snmp3func(mgrid, topic):
	global datainterval
	global authuser
	global authkey
	global authpriv
	global managerid
	if (flag_send):
		iterator = getCmd(SnmpEngine(), 
			UsmUserData(authuser,authkey, authpriv,usmHMACMD5AuthProtocol,usmAesCfb128Protocol), 
			CommunityData('public'), UdpTransportTarget((printerip, 161)), 
			ContextData(),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.5.1.1.17.1')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.33')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.34')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.43')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.103.20.3')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.7')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.104.20.15')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.1')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.1')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.4')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.6')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.4')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.6')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.3')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.3')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.2')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.2')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.9')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.9')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.8')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.8')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.7')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.7')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8.1.5')),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9.1.5')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.13.2.1.6.101.20.4')))

		mainfunc(iterator,mgrid, targettopic = topic)

def snmp3errfunc(mgrid, topic):
	global errordatainterval
	global authuser
	global authkey
	global authpriv
	global managerid
	iterator = []
	if (flag_send):
		iterator.append(getCmd(SnmpEngine(), UsmUserData(authuser,authkey, authpriv,usmHMACMD5AuthProtocol,usmAesCfb128Protocol), CommunityData('public'), UdpTransportTarget((printerip, 161)), ContextData(),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.1')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.2')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.3')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.4')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.5')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.6')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.7')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.8')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.9')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.10')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.11')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.12')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.13')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.14')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.15')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.16')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.17')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.18')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.19')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.20'))))
		iterator.append(getCmd(SnmpEngine(), UsmUserData(authuser,authkey, authpriv,usmHMACMD5AuthProtocol,usmAesCfb128Protocol), CommunityData('public'), UdpTransportTarget((printerip, 161)), ContextData(),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.21')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.22')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.23')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.24')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.25')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.26')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.27')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.28')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.29')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.30')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.31')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.32')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.33')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.34')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.35')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.36')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.37')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.38')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.39')),
		ObjectType(ObjectIdentity('1.3.6.1.4.1.253.8.53.8.2.1.4.40')),
		))

		errfunc(iterator, mgrid, targettopic = topic)
		
def usagemileage2(printerip):
	if (flag_send):
		iterator = getCmd(SnmpEngine(), CommunityData('public'), UdpTransportTarget((printerip, 161)), ContextData(),
		ObjectType(ObjectIdentity('1.3.6.1.2.1.43.5.1.1.17.1')))
		#mainfunc(iterator, mgrid, targettopic = topic)
		errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
		if errorIndication:
			return False
		else:
			if errorStatus:  # SNMP agent errors
				print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
				return False
			else:
				print(varBinds[0])
				currentdata = str(varBinds[0])
				currentuse = int(currentdata[currentdata.index('=')+2::])
				if (currentuse - lastuse > 10):
					return True
					lastuse = currentuse
				else:
					return False
	else:
		return False
		
printer_bind = ["10.21.201.221", "10.21.201.225", "10.21.201.226", "10.21.201.227", "10.21.201.228", "10.21.201.229", "10.21.201.230", "10.21.201.72", "10.21.202.225", "10.21.203.226", "10.21.203.231", "10.21.203.236", "10.21.203.237", "10.21.203.239", "10.21.205.226", "10.21.205.228", "10.21.205.229", "10.21.206.225", "10.21.206.227", "10.21.206.230", "10.21.207.226", "10.21.208.225", "10.21.208.227", "10.21.208.229", "10.21.208.230"]
time_to_transport = datetime.now()

while True:
	while datetime.now() >= time_to_transport:
		print(printer_bind)
		for i in range(25):
			printerip = printer_bind[i]
			print(printerip)
			t3res, t3ser = tester3()
			t2res, t2ser = tester2()
			if t2res:
				mgrid = t2ser
				snmp2main(mgrid, publishto)
				print("using SNMP V2")
			elif t3res:
				mgrid = t3ser
				snmp3main(mgrid, publishto)
				print("using SNMP V3")
			else:
				print("failed to get SNMP version")
			print("=================")
			print("to next printer")

			if i >= 24:
				time_to_transport = datetime.now() + timedelta(hours = 12)
				print(time_to_transport)
			else:
				print("iteration on %s" %i)
