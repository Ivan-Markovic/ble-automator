#!/usr/bin/env python

__author__ = 'Bart van Vliet'

from bleAutomator2 import *
import ConfigUtils
#import matplotlib.pyplot as plt
from Bluenet import *
import datetime

if __name__ == '__main__':
	try:
		parser = optparse.OptionParser(usage="%prog [-vm] [-i <interface>] [-a <address>] [-f <output file>] \n\nExample:\n\t%prog -i hci0 -a 01:23:45:67:89:AB",
									version="0.1")

		parser.add_option('-i', '--interface',
				action="store",
				dest="interface",
				type="string",
				default="hci0",
				help="Interface to be used."
				)
		parser.add_option('-v', '--verbose',
				action="store_true",
				dest="verbose",
				help="Be verbose."
				)
		parser.add_option('-m', '--mesh',
				action="store_true",
				dest="mesh",
				help="Read via mesh characteristic."
				)
		parser.add_option('-a', '--address',
				action="store",
				dest="address",
				type="string",
				default=None,
				help="Target bluetooth address."
				)
		parser.add_option('-f', '--file',
				action='store',
				dest="data_file",
				type="string",
				default="data.txt",
				help='File to store the data'
				)

		options, args = parser.parse_args()

	except Exception, e:
		print e
		print "For help use --help"
		sys.exit(2)

	if (not options.address):
		parser.print_help()
		exit(2)

	ble = BleAutomator(options.interface, options.verbose)

	# Connect to peer device.
	if (not ble.connect(options.address)):
		exit(1)

	# Subscribe for notifications
	handle = ble.getHandle(CHAR_POWER_SAMPLES) + 2
	if (options.mesh):
		handle = ble.getHandle(CHAR_MESH_VALUE) + 1
	if (not ble.writeCharacteristicHandle(handle, Conversion.uint16_to_uint8_array(1))):
		exit(1)
	# print "subscribed for notifications"

	while True:
		notification = ble.waitForNotification(1000.0)
		if (notification):
			data = list(notification["data"])
			line = datetime.datetime.now().strftime("%I:%M:%S %f") + " "
			for val in data:
				line += str(val) + " "
			print line
			# f = open(options.data_file, 'a')
			# f.write(datetime.datetime.now().strftime("%I:%M:%S %f"))
			# f.write(" ")
			# f.write(data)
			# f.write("\n")
		# 	curve = Bluenet.getPowerCurveFromNotification(notification["data"])
		# 	if (options.verbose):
		# 		print curve
		# 	for val in curve:
		# 		f.write("%i\n" % (val))
		#  	f.close()
			# print "Notification on handle", notification["handle"]
			# print list(notification["data"])


	# ble.disconnect()

	# plt.plot(curve["currentTimestamps"], curve["currentSamples"])
	# plt.plot(curve["voltageTimestamps"], curve["voltageSamples"])
	# plt.show()

	exit(0)