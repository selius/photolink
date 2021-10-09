import sqlite3
from contextlib import closing

from models import Tag, Photo, Video, Event, MediaCollection


class MediaCollectionSource(object):
	def getCollection(self):
		return NotImplementedError


class ShotwellDB(MediaCollectionSource):
	class SourceID(object):
		@classmethod
		def sourceIdToNumericId(cls, sourceId: str):
			if sourceId.startswith(cls.getTypeName()):
				return int(sourceId[len(cls.getTypeName()):], 16)
			else:
				return sourceId

		@classmethod
		def isSourceId(cls, sourceId):
			return sourceId.startswith(cls.getTypeName())

		@classmethod
		def getTypeName(cls):
			raise NotImplementedError


	class PhotoID(SourceID):
		@classmethod
		def getTypeName(cls):
			return "thumb"


	class VideoID(SourceID):
		@classmethod
		def getTypeName(cls):
			return "video-"


	class SourceTypeInfo(object):
		def __init__(self, table, mediaCls, idCls):
			#super(ShotwellDB.SourceTypeInfo, self).__init__()
			self.table = table
			self.mediaCls = mediaCls
			self.idCls = idCls


	SOURCE_TYPES = [
		SourceTypeInfo("PhotoTable", Photo, PhotoID),
		SourceTypeInfo("VideoTable", Video, VideoID)
	]


	def __init__(self, path):
		super(ShotwellDB, self).__init__()
		self._path = path
		self._conn = None

	def getCollection(self):
		self._conn = sqlite3.connect(self._path)
		try:
			self._conn.row_factory = sqlite3.Row

			col = MediaCollection()
			self._loadTags(col)
			self._loadEvents(col)

			return col
		finally:
			self._conn.close()

	def _loadTags(self, col: MediaCollection):
		with closing(self._conn.cursor()) as c:
			for row in c.execute("SELECT name, photo_id_list FROM TagTable"):
				sourceIdList = self._parseSourceIdList(row["photo_id_list"])
				col.tags.append(Tag(row["name"], self._listMediaByIds(sourceIdList)))

	def _loadEvents(self, col: MediaCollection):
		with closing(self._conn.cursor()) as c:
			for row in c.execute("SELECT id, name FROM EventTable WHERE COALESCE(name, '') <> ''"):
				col.events.append(Event(row["name"], self._listMediaByEventId(row["id"])))

	def _listMediaByIds(self, ids):
		result = []
		for srcType in self.SOURCE_TYPES:
			typeIds = ids[srcType.idCls]
			if typeIds:
				with closing(self._conn.cursor()) as c:
					sql = "SELECT id, filename FROM %s WHERE id IN (%s)" % (srcType.table, ",".join("?" * len(typeIds)))
					for row in c.execute(sql, typeIds):
						result.append(srcType.mediaCls(row["id"], row["filename"]))
		return result

	def _listMediaByEventId(self, eventId):
		result = []
		for srcType in self.SOURCE_TYPES:
			with closing(self._conn.cursor()) as c:
				sql = "SELECT id, filename FROM %s WHERE event_id = ?" % srcType.table
				for row in c.execute(sql, [eventId]):
					result.append(srcType.mediaCls(row["id"], row["filename"]))
		return result

	def _parseSourceIdList(self, sourceIds):
		result = {}
		for srcType in self.SOURCE_TYPES:
			result[srcType.idCls] = []

		if sourceIds:
			sourceIdList = sourceIds.split(",")
			for sourceId in sourceIdList:
				for idCls in result:
					if idCls.isSourceId(sourceId):
						result[idCls].append(idCls.sourceIdToNumericId(sourceId))
		return result
