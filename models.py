class Photo(object):
	def __init__(self, id, path):
		super(Photo, self).__init__()
		self._id = id
		self._path = path

	@property
	def id(self):
		return self._id

	@property
	def path(self):
		return self._path


class PhotoList(object):
	def __init__(self, name, photos):
		super(PhotoList, self).__init__()
		self._name = name
		self._photos = photos

	@property
	def name(self):
		return self._name

	@property
	def photos(self):
		return self._photos

	@classmethod
	def typeName(cls):
		return NotImplementedError


class Tag(PhotoList):
	@classmethod
	def typeName(cls):
		return "Tag"


class Event(PhotoList):
	@classmethod
	def typeName(cls):
		return "Event"


class PhotoCollection(object):
	def __init__(self):
		super(PhotoCollection, self).__init__()
		self._tags = []
		self._events = []

	@property
	def tags(self):
		return self._tags

	@property
	def events(self):
		return self._events
