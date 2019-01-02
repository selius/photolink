import sqlite3
import os
from contextlib import closing


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


class PhotoTag(object):
	def __init__(self, name, photoIdList):
		"""
		:type photoIdList: str
		"""
		super(PhotoTag, self).__init__()
		self._name = name
		self._photos = []
		if photoIdList:
			photoIds = photoIdList.split(",")
			for photoId in photoIds:
				if PhotoID.isSourceId(photoId):
					self._photos.append(PhotoID.sourceIdToNumericId(photoId))

	@property
	def name(self):
		return self._name

	@property
	def photos(self):
		return self._photos


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


class Event(object):
	def __init__(self, id, name):
		super(Event, self).__init__()
		self._id = id
		self._name = name

	@property
	def id(self):
		return self._id

	@property
	def name(self):
		return self._name


class ShotwellDB(object):
	def __init__(self, path):
		super(ShotwellDB, self).__init__()

		self._conn = sqlite3.connect(path)
		self._conn.row_factory = sqlite3.Row

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._conn.close()

	def listTags(self):
		result = []
		with closing(self._conn.cursor()) as c:
			for row in c.execute("SELECT name, photo_id_list FROM TagTable"):
				result.append(PhotoTag(row["name"], row["photo_id_list"]))
		return result

	def listEvents(self):
		result = []
		with closing(self._conn.cursor()) as c:
			for row in c.execute("SELECT id, name FROM EventTable WHERE name IS NOT NULL"):
				result.append(Event(row["id"], row["name"]))
		return result

	def listPhotosByTag(self, tag):
		"""
		:type tag: PhotoTag
		"""
		result = []
		ids = tag.photos
		if ids:
			with closing(self._conn.cursor()) as c:
				sql = "SELECT id, filename FROM PhotoTable WHERE id IN (%s)" % ",".join("?" * len(ids))
				for row in c.execute(sql, ids):
					result.append(Photo(row["id"], row["filename"]))
		return result

	def listPhotosByEvnet(self, event):
		result = []
		with closing(self._conn.cursor()) as c:
			sql = "SELECT id, filename FROM PhotoTable WHERE event_id = ?"
			for row in c.execute(sql, [event.id]):
				result.append(Photo(row["id"], row["filename"]))
		return result


def linkPhotos(photos, basePath, dryRun):
	for photo in photos:
		fileName = os.path.basename(photo.path)
		linkPath = os.path.join(basePath, fileName)
		print "Photo: %s - %s, link: %s" % (photo.id, photo.path, linkPath)
		if not dryRun:
			os.link(photo.path, linkPath)


def main():
	DB_PATH = "~/.local/share/shotwell/data/photo.db"
	TAGS_PATH = "~/images/photos/_tags"
	EVENTS_PATH = "~/images/photos/_events"
	DRY_RUN = False

	tagsPath = os.path.expanduser(TAGS_PATH)
	eventsPath = os.path.expanduser(EVENTS_PATH)

	with ShotwellDB(os.path.expanduser(DB_PATH)) as db:
		tags = db.listTags()

		for tag in tags:
			tagName = tag.name
			if tagName.startswith("/"):
				tagPath = tagsPath + tagName
			else:
				tagPath = os.path.join(tagsPath, tagName)

			tagPathExists = os.path.exists(tagPath)
			print "Tag: %s, directory: %s - %s..." % (
				tagName, tagPath, "exists, skipping" if tagPathExists else "creating")
			if not DRY_RUN:
				if not tagPathExists:
					os.makedirs(tagPath)

			photos = db.listPhotosByTag(tag)
			linkPhotos(photos, tagPath, DRY_RUN)

		events = db.listEvents()

		for event in events:
			eventPath = os.path.join(eventsPath, event.name)
			eventPathExists = os.path.exists(eventPath)
			print "Event: %s, directory: %s - %s..." % (
				event.name, eventPath, "exists, skipping" if eventPathExists else "creating")
			if not DRY_RUN:
				if not eventPathExists:
					os.makedirs(eventPath)

			photos = db.listPhotosByEvnet(event)
			linkPhotos(photos, eventPath, DRY_RUN)


if __name__ == '__main__':
	main()
