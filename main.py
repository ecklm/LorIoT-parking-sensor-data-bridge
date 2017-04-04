import logging

from poller.loragwpoller import LoragwPoller
from conf import *
from sensor_model import sensormessage
from publisher.awspublisher.AWSPublisher import AWSPublisher
import json

# TODO: argparse

log_level = logging.DEBUG
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
aws_publisher = AWSPublisher("parkingSensor", aws_host, aws_root_CA_path, aws_certificate_path, aws_private_key_path, aws_topic)
aws_publisher.connect()

lpoller.connect()
msg = lpoller.recv()
if(type(msg) == sensormessage.SensorMessage):
	logging.debug(vars(msg))
	aws_publisher.publish(json.dumps(vars(msg), cls=sensormessage.FrameTypeJSONEncoder))

lpoller.close()
aws_publisher.disconnect()
