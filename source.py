import sqlite3
from contextlib import closing

from models import Tag, Photo, Event, PhotoCollection


class PhotoInfoSource(object):
	def getCollection(self):
		return NotImplementedError


class ShotwellDB(PhotoInfoSource):
	class PhotoID(object):
		TYPE_NAME = "thumb"

		@classmethod
		def sourceIdToNumericId(cls, sourceId):
			"""
			:type sourceId: str
			"""
			if sourceId.startswith(cls.TYPE_NAME):
				return int(sourceId[len(cls.TYPE_NAME):], 16)
			else:
				return sourceId

		@classmethod
		def isSourceId(cls, sourceId):
			return sourceId.startswith(cls.TYPE_NAME)


	class VideoID(object):
		TYPE_NAME = "video"


	def __init__(self, path):
		super(ShotwellDB, self).__init__()
		self._path = path
		self._conn = None

	def getCollection(self):
		self._conn = sqlite3.connect(self._path)
		try:
			self._conn.row_factory = sqlite3.Row

			col = PhotoCollection()
			self._loadTags(col)
			self._loadEvents(col)

			return col
		finally:
			self._conn.close()

	def _loadTags(self, col):
		with closing(self._conn.cursor()) as c:
			for row in c.execute("SELECT name, photo_id_list FROM TagTable"):
				photoIdList = self._parseSourceIdList(row["photo_id_list"])
				col.tags.append(Tag(row["name"], self._listPhotosByIds(photoIdList)))

	def _loadEvents(self, col):
		with closing(self._conn.cursor()) as c:
			for row in c.execute("SELECT id, name FROM EventTable WHERE name IS NOT NULL"):
				col.events.append(Event(row["name"], self._listPhotosByEventId(row["id"])))

	def _listPhotosByIds(self, ids):
		result = []
		if ids:
			with closing(self._conn.cursor()) as c:
				sql = "SELECT id, filename FROM PhotoTable WHERE id IN (%s)" % ",".join("?" * len(ids))
				for row in c.execute(sql, ids):
					result.append(Photo(row["id"], row["filename"]))
		return result

	def _listPhotosByEventId(self, eventId):
		result = []
		with closing(self._conn.cursor()) as c:
			sql = "SELECT id, filename FROM PhotoTable WHERE event_id = ?"
			for row in c.execute(sql, [eventId]):
				result.append(Photo(row["id"], row["filename"]))
		return result

	def _parseSourceIdList(self, sourceIds):
		result = []
		if sourceIds:
			sourceIdList = sourceIds.split(",")
			for sourceId in sourceIdList:
				if self.PhotoID.isSourceId(sourceId):
					result.append(self.PhotoID.sourceIdToNumericId(sourceId))
		return result
