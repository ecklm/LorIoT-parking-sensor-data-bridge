import logging

from loriotpoller.loriotpoller import LoriotPoller
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

lpoller = LoriotPoller(loriot_id, loriot_token, loriot_watched_ports)
aws_publisher = AWSPublisher("parkingSensor", aws_host, aws_root_CA_path, aws_certificate_path, aws_private_key_path, aws_topic)
aws_publisher.connect()

lpoller.connect()
msg = lpoller.recv()
if(type(msg) == sensormessage.SensorMessage):
	print(vars(msg))
	aws_publisher.publish(json.dumps(vars(msg), cls=sensormessage.FrameTypeJSONEncoder))

lpoller.close()
aws_publisher.disconnect()
