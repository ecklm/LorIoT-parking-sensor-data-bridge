import logging
import websocket._exceptions, websocket
import json
from sensor_model import sensormessage
from loriotpoller.conf import * # TODO: make clear the origin of watched ports

def json2loriotMessage(inbound_message):
	"""

	:param dict inbound_message: The dict decoded from json.
	:return: A message object with the required fields.
		If the inbound JS object is not like what we need, it only returns the original python object
	"""
	try:
		if(inbound_message["cmd"] != "rx" or inbound_message["port"] not in watched_ports):
			return None
	except KeyError as ex:
		logging.debug("Unsuccessful LorIoT message parsing: " + inbound_message)
		return inbound_message
	# else
	m = sensormessage.SensorMessage(inbound_message["EUI"], inbound_message["ts"], inbound_message["data"])
	return m

class LoriotPoller:
	"""
	
	"""
	__connectURL__ = None
	__ws__ = None

	def __init__(self, appid, token) -> None:
		super().__init__()
		self.__connectURL__ = "wss://eu1.loriot.io/app?id=%s&token=%s" % (appid, token)

	def connect(self):
		try:
			self.__ws__ = websocket.create_connection(self.__connectURL__)
			logging.info("Websocket connected to " + self.__connectURL__)
		except websocket._exceptions.WebSocketException as ex:
			# TODO: Correctly handle the correct exception
			pass

	def close(self):
		self.__ws__.close()
		logging.info("Websocket connection closed to " + self.__connectURL__)

	def isConnected(self):
		if(type(self.__ws__) is websocket.WebSocket):
			return self.__ws__.connected
		else:
			return False

	def recv(self):
		"""
		
		:return: 
		"""
		if(self.isConnected() == False):
			raise ConnectionError("You are not connected to the server")
		logging.debug("Receiving...")
		result = self.__ws__.recv()
		logging.debug("Received: " + result)
		result = json.loads(result, object_hook=json2loriotMessage)
		if(type(result) is sensormessage.SensorMessage):
			return result
		else:
			return None