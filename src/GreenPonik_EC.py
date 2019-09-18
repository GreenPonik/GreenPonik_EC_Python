"""
####################################################################
####################################################################
####################################################################
################ GreenPonik Read EC through Python3 ################
####################################################################
####################################################################
####################################################################
Based on DFRobot_EC library
https://github.com/DFRobot/DFRobot_EC/tree/master/RaspberryPi/Python

Need DFRobot_ADS1115 library
https://github.com/DFRobot/DFRobot_ADS1115/tree/master/RaspberryPi/Python
"""

import time
import sys

_kvalue                 = 1.0
_kvalueLow              = 1.0
_kvalueHigh             = 1.0
_cmdReceivedBufferIndex = 0
_voltage                = 0.0
_temperature            = 25.0

class GreenPonik_EC():
	def begin(self):
		global _kvalueLow
		global _kvalueHigh
		try:
			with open('ecdata.txt','r') as f:
				kvalueLowLine  = f.readline()
				kvalueLowLine  = kvalueLowLine.strip('kvalueLow=')
				_kvalueLow     = float(kvalueLowLine)
				kvalueHighLine = f.readline()
				kvalueHighLine = kvalueHighLine.strip('kvalueHigh=')
				_kvalueHigh    = float(kvalueHighLine)
		except :
			reset()
			sys.exit(1)

	def readEC(self,voltage,temperature):
		global _kvalueLow
		global _kvalueHigh
		global _kvalue
		rawEC = 1000*voltage/820.0/200.0
		valueTemp = rawEC * _kvalue
		if(valueTemp > 2.5):
			_kvalue = _kvalueHigh
		elif(valueTemp < 2.0):
			_kvalue = _kvalueLow
		value = rawEC * _kvalue
		value = value / (1.0+0.0185*(temperature-25.0))
		return value

	def KvalueTempCalculation(self,compECsolution,voltage):
		return 820.0*200.0*compECsolution/1000.0/voltage

	def calibration(self,voltage,temperature):
		rawEC = 1000*voltage/820.0/200.0
		if (rawEC>0.9 and rawEC<1.9):#automated 1.413 buffer solution dection
			compECsolution = 1.413*(1.0+0.0185*(temperature-25.0))
			KValueTemp = KvalueTempCalculation(compECsolution,voltage)
			round(KValueTemp,2)
			print(">>>Buffer Solution:1.413us/cm")
			f=open('ecdata.txt','r+')
			flist=f.readlines()
			flist[0]='kvalueLow='+ str(KValueTemp) + '\n'
			f=open('ecdata.txt','w+')
			f.writelines(flist)
			f.close()
			print(">>>EC:1.413us/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
			time.sleep(5.0)
		elif (rawEC > 3 and rawEC <7):#automated 2.76 buffer solution dection
			compECsolution = 2.76*(1.0+0.0185*(temperature-25.0))
			KValueTemp = KvalueTempCalculation(compECsolution,voltage)
			round(KValueTemp,2)
			print(">>>Buffer Solution:2.76ms/cm")
			f=open('ecdata.txt','r+')
			flist=f.readlines()
			flist[0]='kvalueHigh='+ str(KValueTemp) + '\n'
			f=open('ecdata.txt','w+')
			f.writelines(flist)
			f.close()
			print(">>>EC:2.76ms/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
			time.sleep(5.0)
		elif (rawEC>9 and rawEC<16.8):#automated 12.88 buffer solution dection
			compECsolution = 12.88*(1.0+0.0185*(temperature-25.0))
			KValueTemp = KvalueTempCalculation(compECsolution,voltage)
			print(">>>Buffer Solution:12.88ms/cm")
			f=open('ecdata.txt','r+')
			flist=f.readlines()
			flist[1]='kvalueHigh='+ str(KValueTemp) + '\n'
			f=open('ecdata.txt','w+')
			f.writelines(flist)
			f.close()
			print(">>>EC:12.88ms/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds")
			time.sleep(5.0)
		else:
			print(">>>Buffer Solution Error Try Again<<<")
	def reset(self):
		_kvalueLow              = 1.0
		_kvalueHigh             = 1.0
		try:
			f=open('ecdata.txt','r+')
			flist=f.readlines()
			flist[0]='kvalueLow=' + str(_kvalueLow)  + '\n'
			flist[1]='kvalueHigh='+ str(_kvalueHigh) + '\n'
			f=open('ecdata.txt','w+')
			f.writelines(flist)
			f.close()
			print(">>>Reset to default parameters<<<")
		except:
			f=open('ecdata.txt','w')
			flist   ='kvalueLow=' + str(_kvalueLow)  + '\n'
			flist  +='kvalueHigh='+ str(_kvalueHigh) + '\n'
			f.writelines(flist)
			f.close()
			print(">>>Reset to default parameters<<<")