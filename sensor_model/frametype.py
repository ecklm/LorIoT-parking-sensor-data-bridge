from enum import Enum
from json import JSONEncoder

class FrameType(Enum):
	INFO = "INFO"
	KEEP_ALIVE = "KEEP_ALIVE"
	DAILY_UPDATE = "DAILY_UPDATE"
	ERROR = "ERROR"
	START1 = "START1"
	START2 = "START2"

	def value(self):
		return str(self).split(".")[1]

class FrameTypeJSONEncoder(JSONEncoder):
	def default(self, obj):
		if type(obj) is FrameType:
			return obj.value()
		else:
			return JSONEncoder.default(self, obj)