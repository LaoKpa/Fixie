
from . import Constants, Parser, Tags, Types

class FIXMessage:
	"""
	Represents a single FIX message, including helpful accessors.
	"""

	def __init__(self, message):
		"""
		Initializes a new instance of FIXMessage with an unparsed message.
		"""
		assert(type(message) is str)

		self._message = message
		self._parsedMessage = Parser.parseMessage(message)

	########## Basic Accessors ##########

	def message(self):
		"""
		Returns the message underlying this object.

		:return: str
		"""
		return self._message

	def parsedMessage(self):
		"""
		Returns the parsed message underlying this message.

		:return: dict
		"""
		return self._parsedMessage

	def get(self, id):
		"""
		Returns the string value of the given tag ID.

		:return: str or None
		"""
		return self._parsedMessage.get(id)

	def getParsed(self, id):
		"""
		Returns the string value of the given tag ID.

		:return: str or None
		"""
		value = self.get(id)

		tag = Mappings.TAG_ID_TO_TAG.get(id)
		if tag is None:
			return value
		else:
			return tag.type().parse(value)

	def __str__(self):
		"""
		Returns the string underlying this message.

		:return: str
		"""
		return self._message

	def __len__(self):
		"""
		Returns the length of the message as a string.

		:return: int
		"""
		return len(self._message)

	########## Methods ##########

	def calculateChecksum(self):
		"""
		Calculates the checksum of this message, excluding the last tag if it is a checksum.

		:return: int
		"""
		#Remove the checksum tag from consideration
		lastTag = self._message.rfind(Constants.SEPARATOR, 0, -2)
		if self._message[lastTag+1:lastTag+4] == '10=':
			end = lastTag + 1
		else:
			end = len(self._message)

		#Calculate the checksum over the part before the checksum
		checksum = sum(ord(ch) for ch in self._message[0:end])
		return checksum % 256

	def updateMessage(self):
		"""
		Updates the message to reflect the dictionary (including the checksum, which is also
		updated in the dictionary).
		"""
		#TODO

	########## Tag Helpers ##########

	def _parsePrice(self, price):
		#TODO: is this correct?
		return float(price)

	def averagePrice(self):
		"""
		Returns the average price of the message as indicated by tag 6.

		:return: int
		"""
		rawValue = self._parsedMessage.get(6)
		return None if rawValue is None else self._parsePrice(rawValue)

	def bodyLength(self):
		"""
		Returns the body length of the message as indicated by tag 9.

		:return: int
		"""
		rawValue = self._parsedMessage.get(9)
		return None if rawValue is None else int(rawValue)

	def checksum(self):
		"""
		Returns the checksum of the message as indicated by tag 10.

		:return: int
		"""
		rawValue = self._parsedMessage.get(10)
		return None if rawValue is None else int(rawValue)

	def currency(self):
		"""
		Returns the currency of the message as indicated by tag 15.

		:return: str
		"""
		return self._parsedMessage.get(15)

	def lastPrice(self):
		"""
		Returns the last price of the message as indicated by tag 31.

		:return: int
		"""
		rawValue = self._parsedMessage.get(31)
		return None if rawValue is None else self._parsePrice(rawValue)

	def sequenceNumber(self):
		"""
		Returns the sequence number of the message as indicated by tag 34.

		:return: int
		"""
		rawValue = self._parsedMessage.get(34)
		return None if rawValue is None else int(rawValue)

	def messageType(self):
		"""
		Returns the type of the message as indicated by tag 35.

		:return: str
		"""
		return self._parsedMessage.get(35)

	def price(self):
		"""
		Returns the price of the message as indicated by tag 44.

		:return: float
		"""
		rawValue = self._parsedMessage.get(44)
		return None if rawValue is None else self._parsePrice(rawValue)

	def senderCompID(self):
		"""
		Returns the SenderCompID of the message as indicated by tag 49.

		:return: str
		"""
		return self._parsedMessage.get(49)

	def symbol(self):
		"""
		Returns the symbol of the message as indicated by tag 55.

		:return: str
		"""
		return self._parsedMessage.get(55)

	def strikePrice(self):
		"""
		Returns the strike price of the message as indicated by tag 202.

		:return: float
		"""
		rawValue = self._parsedMessage.get(202)
		return None if rawValue is None else self._parsePrice(rawValue)

	def securityExchange(self):
		"""
		Returns the security exchange of the message as indicated by tag 207.

		:return: str
		"""
		return self._parsedMessage.get(207)

	#TODO: others
