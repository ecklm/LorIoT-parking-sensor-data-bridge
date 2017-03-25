from sensor_model.frametype import *

class SensorMessage:
	"""

	"""
	eui = None
	timestamp = None
	frame_type = None
	battery_ok = None
	slot_occupied = None

	def __init__(self, eui, timestamp, payload):
		super().__init__()
		self.eui = eui
		self.timestamp = timestamp
		self.setPayload(payload)

	def setPayload(self, payload):
		# All frames are 12 bytes long
		# The last 11 bytes depend on the type value of the basic data byte

		# Byte 1: Basic data
		basic_data = int(payload[:2],16) # msb
		self.__parseBasicData(basic_data)

		# Separate last 11 bytes
		rest_of_payload = []
		for i in range(2, 2*12, 2):
			rest_of_payload.append(int(payload[i:i+2], 16))

		if(self.frame_type == FrameType.INFO):
			self.__parseInfoFrame(rest_of_payload)
		elif(self.frame_type == FrameType.KEEP_ALIVE):
			self.__parseKeepAliveFrame(rest_of_payload)
		elif(self.frame_type == FrameType.DAILY_UPDATE):
			self.__parseDailyFrame(rest_of_payload)
		elif(self.frame_type == FrameType.ERROR):
			self.__parseErrorFrame(rest_of_payload)
		elif(self.frame_type == FrameType.START1):
			self.__parseStart1Frame(rest_of_payload)
		elif(self.frame_type == FrameType.START2):
			self.__parseStart2Frame(rest_of_payload)

	def __parseBasicData(self, basic_data_byte):
		type = (basic_data_byte & 0x0F)
		if (type == 0):
			self.frame_type = FrameType.INFO
		elif (type == 1):
			self.frame_type = FrameType.KEEP_ALIVE
		elif (type == 2):
			self.frame_type = FrameType.DAILY_UPDATE
		elif (type == 3):
			self.frame_type = FrameType.ERROR
		elif (type == 4):
			self.frame_type = FrameType.START1
		elif (type == 5):
			self.frame_type = FrameType.START2
		else:
			raise AttributeError

		self.battery_ok = (basic_data_byte & 0b01000000)==0
		self.slot_occupied = (basic_data_byte & 0b10000000)!=0

	# The following parser functions parse the frame of the type of which name it contains
	# rest_of_payload is tha last 11 bytes of the payload in an integer array.
	# Every element is an integer created from that byte => x[i] < 256
	def __parseInfoFrame(self, rest_of_payload):
		pass

	def __parseKeepAliveFrame(self, rest_of_payload):
		pass

	def __parseDailyFrame(self, rest_of_payload):
		pass

	def __parseErrorFrame(self, rest_of_payload):
		pass

	def __parseStart1Frame(self, rest_of_payload):
		pass

	def __parseStart2Frame(self, rest_of_payload):
		pass