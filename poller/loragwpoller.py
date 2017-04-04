from poller.poller import Poller
import logging
import paho.mqtt.client
from sensor_model import sensormessage

class LoragwPoller(Poller):
	"""

	"""
	__host__ = None
	__port__ = None
	__username__ = None
	__passwd__ = None
	__listening_topics__ = None
	__watched_ports__ = None

	__connected__ = False

	__mqtt_client__ = None

	def __init__(self, host, port, user, passwd, topics, watched_ports) -> None:
		"""
		Initialises the necessary
		:param user: Username to be used for the authentication
		:param str passwd: Password to be used for the authentication
		:param str|list topics: This may be a single topic name or list of topic names
		"""
		super().__init__()
		self.__host__ = host
		self.__port__ = port
		self.__username__ = user
		self.__passwd__ = passwd
		self.__listening_topics__ = topics
		if(type(self.__listening_topics__) not in (str, list)):
			raise AttributeError("topics should be string or list of strings")
		self.__watched_ports__ = watched_ports

		self.__mqtt_client__ = paho.mqtt.client.Client()
		self.__mqtt_client__.username_pw_set(self.__username__, self.__passwd__)
		self.__mqtt_client__.on_connect = self.__on_connect
		self.__mqtt_client__.on_disconnect = self.__on_disconnect
		self.__mqtt_client__.on_message = self.__on_message
		self.__mqtt_client__.on_subscribe = self.__on_subscribe
		self.__mqtt_client__.on_log = self.__on_log

	def __on_connect(self, client, userdata, flags, rc):
		logging.info("%s: %s" % (client._client_id, "Connected with result code "+str(rc)))
		# Subscribe to topics
		# It is cool because it automatically resubscribes on reconnect
		self.__connected__ = True
		self.__subscribeToTopics()

	def __on_disconnect(self, client, userdata, rc):
		self.__connected__ = False

	def __on_message(self, client, userdata, msg):
		# TODO: parse the message
		print(msg.topic + " " + str(msg.payload))

	def __on_subscribe(self, client, userdata, mid, granted_qos):
		# does not reveal anything interesting for me...
		pass

	def __on_log(self, client, userdata, level, buf):
		logging.debug("%s: %s" % (client._client_id, buf))

	def __subscribeToTopics(self):
		if(type(self.__listening_topics__) is str):
			self.__mqtt_client__.subscribe(self.__listening_topics__)
		else: # Here it only be list now
			for topic in self.__listening_topics__:
				self.__mqtt_client__.subscribe(topic)

	def connect(self) -> int:
		"""
		Connets to the platform with the configured credentials.

		:return: True if the connect attempt succeeded False if it failed
		"""

		ret = self.__mqtt_client__.connect(self.__host__, self.__port__)
		self.__mqtt_client__.loop_forever()
		return ret

	def isConnected(self) -> bool:
		return self.__connected__

	def close(self) -> bool:
		"""
		Closes the initiated connection

		:return: True if the disconnect request was successful. False otherwise.		
		"""
		return self.__mqtt_client__.disconnect()

	def recv(self) -> sensormessage.SensorMessage or None:
		raise NotImplementedError
