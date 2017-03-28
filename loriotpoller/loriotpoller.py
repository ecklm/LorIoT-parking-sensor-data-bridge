from conf import *
import logging
from websocket import create_connection
import json
from sensor_model import sensormessage

connectURL = "wss://eu1.loriot.io/app?id=%s&token=%s" % (loriot_id, loriot_token)

def json2loriotMessage(inbound_message):
	"""

	:param inbound_message: The dict decoded from json.
	:return: A message object with the
	"""
	try:
		if(inbound_message["cmd"] != "rx" or inbound_message["port"] not in watched_ports):
			return None
	except KeyError as ex:
		logging.log(logging.DEBUG, "Unsuccessful LorIoT message parsing: " + inbound_message.__dict__)
		return inbound_message
	# else
	m = sensormessage.SensorMessage(inbound_message["EUI"], inbound_message["ts"], inbound_message["data"])
	return m

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
	while True:
		ws = create_connection(connectURL)
		print ("Receiving...")
		result =  ws.recv()
		print (result)
		obj = json.loads(result,
		                 object_hook=json2loriotMessage)
		if(obj != None):
			print(json.dumps(obj.__dict__, cls=sensormessage.FrameTypeJSONEncoder))
		ws.close()


