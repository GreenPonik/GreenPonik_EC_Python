## GreenPonik_EC.py Library for Raspberry pi
---------------------------------------------------------
This is the sample code for Gravity: Analog Electrical Conductivity Sensor / Meter Kit V2 (K=1.0), SKU: DFR0300
## Table of Contents

- [## GreenPonik_EC.py Library for Raspberry pi](#greenponikecpy-library-for-raspberry-pi)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Methods](#methods)
- [Examples](#examples)
- [Credits](#credits)
<snippet>
<content>

## Installation

Dependencies:

The [Analog Electrical Conductivity Sensor](https://wiki.dfrobot.com/Gravity__Analog_Electrical_Conductivity_Sensor___Meter_V2__K%3D1__SKU_DFR0300) should work with ADS1115
[DFRobot_ADS1115](https://github.com/DFRobot/DFRobot_ADS1115/tree/master/RaspberryPi/Python)

Call modules:

```Python

from DFRobot_ADS1115 import ADS1115
from GreenPonik_EC import GreenPonik_EC

```

or run example directly

```shell
$> python3 example/EC_Read.py

```
## Methods

```python

"""
@brief Init The Analog EC Sensor
"""
def begin(self);

"""
@brief Convert voltage to EC with temperature compensation
"""
def readEC(self,voltage,temperature);

"""
@brief Calibrate the calibration data
"""
def calibration(self,voltage,temperature);

"""
@brief Reset the calibration data to default value
"""
def reset(self);

```

## Examples
EC read => EC_Read.py
in libs folder

> git clone https://github.com/DFRobot/DFRobot_ADS1115.git
```Python
import sys
sys.path.insert(0,'DFRobot_ADS1115/RaspberryPi/Python/')
sys.path.insert(0,'GreenPonik_EC_Python/src/')


from GreenPonik_EC import GreenPonik_EC
from DFRobot_ADS1115 import ADS1115

ADS1115_REG_CONFIG_PGA_6_144V = 0x00  # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V = 0x02  # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V = 0x04  # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V = 0x06  # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V = 0x08  # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V = 0x0A  # 0.256V range = Gain 16

ads1115 = ADS1115()
ec = GreenPonik_EC()
ec.begin()

def read_ec():
    global ads1115
    global ec
    temperature = 25 # or make your own temperature read method
    # Set the IIC address
    ads1115.setAddr_ADS1115(0x48)
    # Sets the gain and input voltage range.
    ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
    # Get the Digital Value of Analog of selected channel
    adc0 = ads1115.readVoltage(0)
    # Convert voltage to EC with temperature compensation
    EC = ec.readEC(adc0['r'], temperature)
    print("Temperature:%.1f ^C EC:%.3f ms/cm " % (temperature, EC))
    return EC


while True:
	read_ec()

```
EC calibration => EC_Calibration.py

in libs folder

> git clone https://github.com/DFRobot/DFRobot_ADS1115.git
```Python
import sys
sys.path.insert(0,'libs/DFRobot_ADS1115/RaspberryPi/Python/')
sys.path.insert(0,'libs/GreenPonik_EC_Python/src/')

from DFRobot_ADS1115 import ADS1115
from GreenPonik_EC import GreenPonik_EC

ADS1115_REG_CONFIG_PGA_6_144V = 0x00  # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V = 0x02  # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V = 0x04  # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V = 0x06  # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V = 0x08  # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V = 0x0A  # 0.256V range = Gain 16

ads1115 = ADS1115()
ec = GreenPonik_EC()
ec.begin()


def calibration():
    global ads1115
    global ec
    temperature = 25 # or make your own temperature read method
    # Set the IIC address
    ads1115.setAddr_ADS1115(0x48)
    # Sets the gain and input voltage range.
    ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
    # Get the Digital Value of Analog of selected channel
    adc0 = ads1115.readVoltage(0)
    return ec.calibration(adc0['r'], temperature)


calibration()

```

read both pH and EC => PH_EC.py

in libs folder

> git clone https://github.com/GreenPonik/GreenPonik_EC_Python.git

> git clone https://github.com/DFRobot/DFRobot_ADS1115.git

```Python
import sys
sys.path.insert(0,'libs/DFRobot_ADS1115/RaspberryPi/Python/')
sys.path.insert(0,'libs/GreenPonik_EC_Python/src/')
sys.path.insert(0,'libs/GreenPonik_PH_Python/src/')


ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16

from DFRobot_ADS1115 import ADS1115
from GreenPonik_EC import GreenPonik_EC
from GreenPonik_PH import GreenPonik_PH

ads1115 = ADS1115()
ec      = GreenPonik_EC()
ph      = GreenPonik_PH()

ec.begin()
ph.begin()


def read_ph_ec():
	global ads1115
	global ec
	global ph
	temperature = 25 # or make your own temperature read process
	#Set the IIC address
	ads1115.setAddr_ADS1115(0x48)
	#Sets the gain and input voltage range.
	ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)
	#Get the Digital Value of Analog of selected channel
	adc0 = ads1115.readVoltage(0)
	adc1 = ads1115.readVoltage(1)
	#Convert voltage to EC with temperature compensation
	EC = ec.readEC(adc0['r'],temperature)
	PH = ph.readPH(adc1['r'])
	print("Temperature:%.1f ^C EC:%.2f ms/cm PH:%.2f " %(temperature,EC,PH))
	return temperature, EC, PH


while True:
	read_ph_ec()

```

## Credits
Writter by Mickael Lehoux, from [GreenPonik](https://www.greenponik.com), 2019

based on [DFRobot library](https://github.com/DFRobot/DFRobot_EC/tree/master/RaspberryPi/Python)

## support us
[become a patreon](https://www.patreon.com/bePatron?u=32614023)
