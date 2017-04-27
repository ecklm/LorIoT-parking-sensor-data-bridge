import logging
import paho.mqtt.client

from publisher.publisher import Publisher

class SensorHUBPublisher(Publisher):
	__host__ = None
	__port__ = None
	__username__ = None
	__passwd__ = None
	__publishing_topic__ = None

	__connected__ = False

	__mqtt_client__ = None

	def __init__(self, host, port, user, passwd, topic) -> None:
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
		self.__publishing_topic__ = topic

		self.__mqtt_client__ = paho.mqtt.client.Client()
		self.__mqtt_client__.username_pw_set(self.__username__, self.__passwd__)
		self.__mqtt_client__.on_connect = self.__on_connect
		self.__mqtt_client__.on_disconnect = self.__on_disconnect
		self.__mqtt_client__.on_log = self.__on_log

	def __on_connect(self, client, userdata, flags, rc):
		logging.info("%s: %s" % (client._client_id, "Connected with result code "+str(rc)))
		self.__connected__ = True

	def __on_log(self, client, userdata, level, buf):
		logging.debug("%s: %s" % (client._client_id, buf))

	def __on_disconnect(self, client, userdata, rc):
		if(rc != paho.mqtt.client.MQTT_ERR_SUCCESS):
			logging.error("Client has disconnected abnormally. Return code: " + str(rc))
		self.__connected__ = False

	def publish(self, message) -> bool:
		logging.info("Message is being requested to publish: " + message)
		ret = self.__mqtt_client__.publish(self.__publishing_topic__, message)
		ret.wait_for_publish()
		if(ret.is_published() == False):
			logging.error("Message has not been published successfully: " + message)
		return ret.is_published()

	def disconnect(self) -> bool:
		self.__mqtt_client__.loop_stop()
		return self.__mqtt_client__.disconnect()

	def connect(self) -> bool:
		ret = self.__mqtt_client__.connect(self.__host__, self.__port__)
		self.__mqtt_client__.loop_start()
		return ret
