from conf import *
from websocket import create_connection
import json
from sensor_model import sensormessage

connectURL = "wss://eu1.loriot.io/app?id=%s&token=%s" % (loriot_id, loriot_token)

def json2loriotMessage(inbound_message):
	"""

	:param inbound_message: The dict decoded from json.
	:return: A message object with the
	"""
	if(inbound_message["port"] not in watched_ports or inbound_message["cmd"] != "rx"):
		return None
	# else
	m = sensormessage.SensorMessage(inbound_message["EUI"], inbound_message["ts"], inbound_message["data"])
	return m


ws = create_connection(connectURL)
print ("Receiving...")
result =  ws.recv()
obj = json.loads(result,
                 object_hook=json2loriotMessage)

print(json.dumps(obj.__dict__, cls=sensormessage.FrameTypeJSONEncoder))
ws.close()

