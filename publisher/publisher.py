
class Publisher:

	def connect(self) -> bool:
		"""
		Connets to the platform with the configured credentials.

		:return: True if the connect attempt succeeded False if it failed
		"""
		pass

	def disconnect(self) -> bool:
		"""
		Closes the initiated connection

		:return: True if the disconnect request was successful. False otherwise.		
		"""
		pass

	def publish(self, message) -> bool:
		"""
		Publis a message to the MQTT topic set in the constructor

		:param str message: JSON payload to publish
		:return bool: Whether the publish request have been successful
		"""
		pass
