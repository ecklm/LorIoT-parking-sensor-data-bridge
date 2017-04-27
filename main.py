import logging
import time
import argparse

from poller.loragwpoller import LoragwPoller
from conf import *
from sensor_model import sensormessage
from publisher.awspublisher.AWSPublisher import AWSPublisher
from publisher.sensorhubpublisher.SensorHubPublisher import SensorHUBPublisher
import json

parser = argparse.ArgumentParser(
		description="Polls given sensor sources, and uploads the data to the given IoT platforms")
parser.add_argument("-d", "--debug", action="store_true",
                    help="Prints debug messages.")
parser.add_argument("-f", "--log-file", action="store",
                    help="Log file to witch log messages should be writen")

args = parser.parse_args()
if(args.debug == True):
	log_level = logging.DEBUG
else:
	log_level = logging.INFO

if(args.log_file != None):
	log_file = args.log_file
else:
	log_file = ""

log_format = "%(levelname)s: %(message)s"

if(log_level == logging.DEBUG):
	log_format = "%(name)s - "+ log_format
if(len(log_file) == 0): # Messages goes to STDERR
	log_format = "%(asctime)s - " + log_format

logging.basicConfig(filename=log_file, level=log_level, format=log_format)


try:
	from setproctitle import setproctitle
	proc_name = "loriot-data-bridge"
	setproctitle(proc_name)
	logging.debug("Process name is set to " + "loriot-data-bridge")
except (ModuleNotFoundError, ImportError):
	logging.error("setproctitle module is not installed")
	pass

lpoller = LoragwPoller(loragw_host, loragw_port, loragw_user, loragw_passwd, loragw_topics, loragw_watched_ports)
lpoller.connect()

aws_publisher = AWSPublisher("parkingSensor", aws_host, aws_root_CA_path, aws_certificate_path, aws_private_key_path, aws_topic)
aws_publisher.connect()
sensorhub_publisher = SensorHUBPublisher(sensorhub_host, sensorhub_port, sensorhub_user, sensorhub_passwd, sensorhub_topic)
sensorhub_publisher.connect()

stop = False
while stop == False:
	try:
		msg = lpoller.recv()
		if(type(msg) == sensormessage.SensorMessage):
			logging.debug("Received and parsed data: " + str(vars(msg)))
			msg = json.dumps(vars(msg), cls=sensormessage.FrameTypeJSONEncoder)
			aws_publisher.publish(msg)
			sensorhub_publisher.publish(msg)
		else:
			time.sleep(5)
	except KeyboardInterrupt:
		stop = True

sensorhub_publisher.disconnect()
aws_publisher.disconnect()

lpoller.close()
