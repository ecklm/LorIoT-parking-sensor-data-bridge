import logging
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from publisher.publisher import Publisher


class AWSPublisher(Publisher):
	"""
	
	"""
	__client_id__ = None
	__host__ = None
	__root_CA_path__ = None
	__cert_path__ = None
	__priv_key_path__ = None
	__publish_topic__ = None

	__mqtt_client__ = None

	def __init__(self, cliend_id, host, root_ca, cert, priv_key, topic) -> None:
		"""
		
		:param str cliend_id:
		:param str host: 
		:param str root_ca: 
		:param str cert: 
		:param str priv_key: 
		:param str topic: 
		"""
		super().__init__()
		self.__client_id__ = cliend_id
		self.__host__ = host
		self.__root_CA_path__ = root_ca
		self.__cert_path__ = cert
		self.__priv_key_path__ = priv_key
		self.__publish_topic__ = topic

	def connect(self) -> bool:
		"""
		Connets to the platform with the configured credentials.
		
		:return: True if the connect attempt succeeded False if it failed
		"""
		self.__mqtt_client__ = AWSIoTMQTTClient(self.__client_id__)
		self.__mqtt_client__.configureEndpoint(self.__host__, 8883)
		self.__mqtt_client__.configureCredentials(self.__root_CA_path__, self.__priv_key_path__, self.__cert_path__)

		# AWSIoTMQTTClient connection configuration
		self.__mqtt_client__.configureAutoReconnectBackoffTime(1, 32, 20)
		self.__mqtt_client__.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		self.__mqtt_client__.configureDrainingFrequency(2)  # Draining: 2 Hz
		self.__mqtt_client__.configureConnectDisconnectTimeout(10)  # 10 sec
		self.__mqtt_client__.configureMQTTOperationTimeout(5)  # 5 sec

		# Connect and subscribe to AWS IoT
		return self.__mqtt_client__.connect()

	def disconnect(self) -> bool:
		"""
		Closes the initiated connection
		
		:return: True if the disconnect request was successful. False otherwise.		
		"""
		return self.__mqtt_client__.disconnect()

	def publish(self, message) -> bool:
		"""
		Publis a message to the MQTT topic set in the constructor
		
		:param str message: JSON payload to publish
		:return bool: Whether the publish request have been successful
		"""
		logging.debug("Message is being requested to publish: " + message)
		return self.__mqtt_client__.publish(self.__publish_topic__, message, 1)
