import logging
import websocket._exceptions, websocket
import json
from sensor_model import sensormessage

class LoriotPoller:
	"""
	
	"""
	__connectURL__ = None
	__ws__ = None
	__watched_ports__ = None

	def __init__(self, appid, token, watched_ports) -> None:
		"""
		Initializes a connector to LorIoT websocket service.

		:param str appid: AppID field of the URL
		:param str token: Token field of the URL
		:param list watched_ports: List of the LorIoT port numbers to watch
		"""
		super().__init__()
		self.__connectURL__ = "wss://eu1.loriot.io/app?id=%s&token=%s" % (appid, token)
		self.__watched_ports__ = watched_ports

	def connect(self):
		try:
			self.__ws__ = websocket.create_connection(self.__connectURL__)
			logging.info("Websocket connected to " + self.__connectURL__)
		except websocket._exceptions.WebSocketException as ex:
			# TODO: Correctly handle the correct exception
			logging.error(ex)

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
		result = json.loads(result, object_hook=self.__json2loriotMessage)
		if(type(result) is sensormessage.SensorMessage):
			return result
		else:
			return None

	def __json2loriotMessage(self, inbound_message) -> sensormessage.SensorMessage or dict:
		"""

		:param dict inbound_message: The dict decoded from json.
		:return: A message object with the required fields.
			If the inbound JS object is not like what we need, it only returns the original python object
		"""
		try:
			if (inbound_message["cmd"] != "rx" or inbound_message["port"] not in self.__watched_ports__):
				return None
		except KeyError as ex:
			logging.debug("Unsuccessful LorIoT message parsing: " + inbound_message)
			return inbound_message
		# else
		m = sensormessage.SensorMessage(inbound_message["EUI"], inbound_message["ts"], inbound_message["data"])
		return m
