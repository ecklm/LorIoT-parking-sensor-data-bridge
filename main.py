import logging

from loriotpoller.loriotpoller import LoriotPoller
from loriotpoller.conf import *

# TODO: argparse

logging.basicConfig(filename="", level=logging.DEBUG, format="%(asctime)s - %(levelname)s: %(message)s")

lpoller = LoriotPoller(loriot_id, loriot_token)
lpoller.connect()
print(vars(lpoller.recv()))
lpoller.close()
