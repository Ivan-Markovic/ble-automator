#!/usr/bin/env python

__author__ = 'Bart van Vliet'

import bluepy.btle
from bleAutomator2 import *
from Bluenet import *
from ConversionUtils import *
#import matplotlib.pyplot as plt
#import random
#import numpy as np

if __name__ == '__main__':
	try:
		parser = optparse.OptionParser(usage='%prog [-v] [-i <interface>] [-a <ble address>]\n\nExample:\n\t%prog -i hci0 -a CD:E3:4A:47:1C:E4',
									version='0.1')

		parser.add_option('-a', '--address',
				action='store',
				dest="address",
				type="string",
				default=None,
				help='Target address. (Can be found by running "hcitool lescan")'
				)
		parser.add_option('-i', '--interface',
				action='store',
				dest="interface",
				type="string",
				default="hci0",
				help='HCI interface to be used.'
				)
		parser.add_option('-v', '--verbose',
				action='store_true',
				dest="verbose",
				help='Be verbose.'
				)

		options, args = parser.parse_args()

	except Exception, e:
		print e
		print "For help use --help"
		sys.exit(2)

	targets = []
	if (options.address):
		targets = [options.address]

class ScanDelegate(bluepy.btle.DefaultDelegate):
	def __init__(self):
		bluepy.btle.DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev, isNewDev, isNewData):
		if ((len(targets) == 0) or (dev.addr in targets)):
			print "Advertisements from:", dev.addr, "rssi:", dev.rssi
			for (adtype, desc, value) in dev.getScanData():
				print "type:", adtype, "description:", desc
				if (adtype == 22): # ServiceData
					serviceData = Conversion.hex_string_to_uint8_array(value)
					print "Service data:", list(serviceData)

					ind = 0
					uuid = Conversion.uint8_array_to_uint16(serviceData[ind:ind+2])
					ind += 2
					protocolVersion = serviceData[ind]
					ind += 1
					crownstoneId = Conversion.uint8_array_to_uint16(serviceData[ind:ind+2])
					ind += 2
					switchState = serviceData[ind]
					ind += 1
					eventBitmask = serviceData[ind]
					ind += 1
					temperature = Conversion.uint8_to_int8(serviceData[ind])
					ind += 1
					powerUsage = Conversion.uint8_array_to_uint32(serviceData[ind:ind+4])
					ind += 4
					energyUsage = Conversion.uint8_array_to_uint32(serviceData[ind:ind+4])
					ind += 4
					randNr = list(serviceData[ind:ind+3])
					ind += 3

					print "UUID:", uuid # Crownstone uuid = 49153, Guidestone uuid = 49154
					print "crownstoneId:", crownstoneId
					print "switchState:", switchState
					print "eventBitmask:", "{0:08b}".format(eventBitmask)
					print "temperature:", temperature
					print "powerUsage:", powerUsage
					print "energyUsage:", energyUsage
					print "randNr:", randNr

				if (adtype == 8): # Name
					print "Name:", value
			print ""


for i in range(0, len(targets)):
	targets[i] = targets[i].lower()

scanner = bluepy.btle.Scanner(options.interface[3:]).withDelegate(ScanDelegate())
scanner.start()
while True:
	scanner.process(0.5)
scanner.stop()