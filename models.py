class Media(object):
	def __init__(self, id, path):
		super(Media, self).__init__()
		self._id = id
		self._path = path

	@property
	def id(self):
		return self._id

	@property
	def path(self):
		return self._path

	@classmethod
	def typeName(cls):
		return NotImplementedError


class Photo(Media):
	@classmethod
	def typeName(cls):
		return "Photo"


class Video(Media):
	@classmethod
	def typeName(cls):
		return "Video"


class MediaList(object):
	def __init__(self, name, objects):
		super(MediaList, self).__init__()
		self._name = name
		self._objects = objects

	@property
	def name(self):
		return self._name

	@property
	def objects(self):
		return self._objects

	@classmethod
	def typeName(cls):
		return NotImplementedError


class Tag(MediaList):
	@classmethod
	def typeName(cls):
		return "Tag"


class Event(MediaList):
	@classmethod
	def typeName(cls):
		return "Event"


class MediaCollection(object):
	def __init__(self):
		super(MediaCollection, self).__init__()
		self._tags = []
		self._events = []

	@property
	def tags(self):
		return self._tags

	@property
	def events(self):
		return self._events
