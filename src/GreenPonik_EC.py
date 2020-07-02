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

_kvalue = 1.0
_kvalueLow = 1.0
_kvalueHigh = 1.0
_voltage = 0.0
_temperature = 25.0


class GreenPonik_EC():
    def begin(self):
        global _kvalueLow
        global _kvalueHigh
        try:
            print(">>>Initialization of ec lib<<<")
            with open('ecdata.txt', 'r') as f:
                kvalueLowLine = f.readline()
                kvalueLowLine = kvalueLowLine.strip('kvalueLow=')
                _kvalueLow = float(kvalueLowLine)
                print("get k value low from txt file: %.3f" % _kvalueLow)
                kvalueHighLine = f.readline()
                kvalueHighLine = kvalueHighLine.strip('kvalueHigh=')
                _kvalueHigh = float(kvalueHighLine)
                print("get k value high from txt file: %.3f" % _kvalueHigh)
        except:
            self.reset()

    def readEC(self, voltage, temperature):
        global _kvalueLow
        global _kvalueHigh
        global _kvalue
        rawEC = 1000*voltage/820.0/200.0
        print(">>>current rawEC is: %.3f" % rawEC)
        valueTemp = rawEC * _kvalue
        if(valueTemp > 2.5):
            _kvalue = _kvalueHigh
        elif(valueTemp < 2.0):
            _kvalue = _kvalueLow
        value = rawEC * _kvalue
        value = value / (1.0+0.0185*(temperature-25.0))
        return value

    def KvalueTempCalculation(self, compECsolution, voltage):
        return 820.0*200.0*compECsolution/1000.0/voltage

    def calibration(self, voltage, temperature):
        rawEC = 1000*voltage/820.0/200.0
        print(">>>current rawEC is: %.3f" % rawEC)
        if (rawEC > 0.8 and rawEC < 2.1):  # automated 1.413 buffer solution dection
            compECsolution = 1.413*(1.0+0.0185*(temperature-25.0))
            KValueTemp = self.KvalueTempCalculation(compECsolution, voltage)
            KValueTemp = round(KValueTemp, 2)
            print(">>>Buffer Solution:1.413us/cm")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[0] = 'kvalueLow=' + str(KValueTemp) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>EC:1.413us/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 1413,
                       'kvalue': KValueTemp,
                       'status_message': status_msg}
            return cal_res
        elif (rawEC > 2 and rawEC < 3.5):  # automated 2.76 buffer solution dection
            compECsolution = 2.76*(1.0+0.0185*(temperature-25.0))
            KValueTemp = self.KvalueTempCalculation(compECsolution, voltage)
            KValueTemp = round(KValueTemp, 2)
            print(">>>Buffer Solution:2.76ms/cm")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[1] = 'kvalueHigh=' + str(KValueTemp) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>EC:2.76ms/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 276,
                       'kvalue': KValueTemp,
                       'status_message': status_msg}
            return cal_res
        elif (rawEC > 9 and rawEC < 16.8):  # automated 12.88 buffer solution dection
            compECsolution = 12.88*(1.0+0.0185*(temperature-25.0))
            KValueTemp = self.KvalueTempCalculation(compECsolution, voltage)
            print(">>>Buffer Solution:12.88ms/cm")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[1] = 'kvalueHigh=' + str(KValueTemp) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
            status_msg = ">>>EC:12.88ms/cm Calibration completed,Please enter Ctrl+C exit calibration in 5 seconds"
            print(status_msg)
            time.sleep(5.0)
            cal_res = {'status': 1288,
                       'kvalue': KValueTemp,
                       'status_message': status_msg}
            return cal_res
        else:
            status_msg = ">>>Buffer Solution Error, EC raw: %.3f, Try Again<<<" % rawEC
            print(status_msg)
            cal_res = {'status': 9999, 'status_message': status_msg}
            return cal_res

    def reset(self):
        global _kvalueLow
        global _kvalueHigh
        _kvalueLow = 1.0
        _kvalueHigh = 1.0
        print(">>>Reset to default parameters<<<")
        try:
            print(">>>Read k from txt files<<<")
            f = open('ecdata.txt', 'r+')
            flist = f.readlines()
            flist[0] = 'kvalueLow=' + str(_kvalueLow) + '\n'
            flist[1] = 'kvalueHigh=' + str(_kvalueHigh) + '\n'
            f = open('ecdata.txt', 'w+')
            f.writelines(flist)
            f.close()
        except:
            print(">>>Cannot read k from txt files<<<")
            print(">>>Let's create them and apply the default values<<<")
            f = open('ecdata.txt', 'w')
            flist = 'kvalueLow=' + str(_kvalueLow) + '\n'
            flist += 'kvalueHigh=' + str(_kvalueHigh) + '\n'
            f.writelines(flist)
            f.close()
