import time
import sys, getopt
__version__ = "beta 3"

printerip = "10.21.201.221"
publishto = "printer"
authuser = "Xadmin"
authkey = "12345678"
authpriv = "12345678"

errordatainterval = 15
datainterval = 25

from snmp2engine import *
lastrunfunc = time.time()
lastrunerr = time.time()
#print("Getting from %s" % printerip)

def writeheader():
	print("================================")
	print("SNMP Tester")
	print(__version__)
	print("Engine version: %s" % getversion()) 
	print("================================")
	print("Printer IP   : %s" % printerip)
	print("Target Topic : %s" % publishto)
		


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
	while(1):
		snmp2func(mgrid, publishto)
		snmp2errfunc(mgrid,publishto)
		
def snmp2func(mgrid, topic):
	global datainterval
	global lastrunfunc
	elapsed = time.time()
	if (elapsed - lastrunfunc > datainterval):
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

		lastrunfunc = elapsed
		mainfunc(iterator, mgrid, targettopic = topic)
			
def snmp2errfunc(mgrid, topic):
	global errordatainterval
	global lastrunerr
	elapsed = time.time()
	iterator = []
	if (elapsed - lastrunerr > errordatainterval):
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
		lastrunerr = elapsed
		errfunc(iterator, mgrid, targettopic = topic)

def snmp3main(mgrid, publishto):
	while(1):
		snmp3func(mgrid, publishto)
		snmp3errfunc(mgrid, publishto)

def snmp3func(mgrid, topic):
	global datainterval
	global authuser
	global authkey
	global authpriv
	global managerid
	global lastrunfunc
	elapsed = time.time()
	if (elapsed - lastrunfunc > datainterval):
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

		lastrunfunc = elapsed
		mainfunc(iterator,mgrid, targettopic = topic)

def snmp3errfunc(mgrid, topic):
	global errordatainterval
	global authuser
	global authkey
	global authpriv
	global managerid
	global lastrunerr
	elapsed = time.time()
	iterator = []
	if (elapsed - lastrunerr > errordatainterval):
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
		lastrunerr = elapsed
		#next(iterator)
		errfunc(iterator, mgrid, targettopic = topic)
		
def usagemileage2(printerip):
	global mileageinterval
	global lastrunmileage
	elapsed = time.time()
	if (elapsed - lastrunmileage > mileageinterval):
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
		lastrunmileage = elapsed
	else:
		return False
		
	
try:
	opts, args = getopt.getopt(sys.argv[1:],"ha:t:u:k:p",["address=","topic=","authuser=","authkey=","authpriv="])
except getopt.GetoptError:
	print ('Usage : snmptester.py -a <printerip> -t <targettopic> -u <authuser> -k <authkey> -p <privatekey>')
	sys.exit(2)
	
for opt, arg in opts:
	if opt == '-h':
		print ('Usage : snmptester.py -a <printerip> -t <targettopic> -u <authuser> -k <authkey> -p <privatekey>')
		sys.exit()
	elif opt in ("-a", "--address"):
		printerip = arg
	elif opt in ("-t", "--topic"):
		publishto = arg
	elif opt in ("-u", "--authuser"):
		authuser = arg
	elif opt in ("-k", "--authkey"):
		authkey = arg
	elif opt in ("-p", "--authpriv"):
		authpriv = arg

writeheader()

while 1:
	print("Probing SNMP Version")
	t3res, t3ser = tester3()
	t2res, t2ser = tester2()
	
	if t3res:
		mgrid = t3ser
		print("Using SNMP version 3")
		snmp3main(mgrid, publishto)
	elif t2res:
		mgrid = t2ser
		print("Using SNMP version 2")
		snmp2main(mgrid, publishto)
	else:
		print("SNMP get information failed")
