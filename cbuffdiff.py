def getNewData(newlist, oldlist):	
	if (len(newlist) > len(oldlist)):
		newlength = len(newlist) - len(oldlist)
		newdata = newlist[(len(newlist) - newlength):]
		#print(newlist[0:len(oldlist)])
		overflownewdata = getNewData(newlist[0:len(oldlist)], oldlist)
		newerdata = newdata+overflownewdata
		return newerdata
	else:
		if oldlist != newlist:
			oldindex = -1
			newpoint = 0
			comboisrunning = 0
			for i in range(len(oldlist)):
				#print("%d %d" % (newlist[i], oldlist[oldpoint]))
				#print(newlist[i] == oldlist[oldpoint])
				if oldlist[i] == newlist[newpoint]:
					newpoint += 1
					if comboisrunning != 1:
						oldindex = i
						comboisrunning = 1
				else:
					comboisrunning = 0
					newpoint = 0
					if oldlist[i] == newlist[newpoint]:
						oldindex = i
						newpoint += 1
						#print("Oldindex update %d" % oldindex)
						#print("%d %d" % (newlist[i], oldlist[oldpoint]))
						#print(newlist[i] == oldlist[oldpoint])
			oldindex = newpoint
			olddata = newlist[0:oldindex]
			newdata = newlist[oldindex:]
			#print (newdata)
			return newdata
		else:
			return []