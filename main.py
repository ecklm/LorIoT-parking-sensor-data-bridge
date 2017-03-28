import logging

from loriotpoller.loriotpoller import LoriotPoller
from conf import *
from sensor_model import sensormessage
from publisher.awspublisher.AWSPublisher import AWSPublisher
import json

# TODO: argparse

logging.basicConfig(filename="", level=logging.DEBUG, format="%(asctime)s - %(levelname)s: %(message)s")

lpoller = LoriotPoller(loriot_id, loriot_token)
aws_publisher = AWSPublisher("parkingSensor", aws_host, aws_root_CA_path, aws_certificate_path, aws_private_key_path, aws_topic)
aws_publisher.connect()

lpoller.connect()
msg = lpoller.recv()
if(type(msg) == sensormessage.SensorMessage):
	print(vars(msg))
	aws_publisher.publish(json.dumps(vars(msg), cls=sensormessage.FrameTypeJSONEncoder))

lpoller.close()
aws_publisher.disconnect()
