import os

from logger import Logger, SilentLogger, VerboseLogger
from source import ShotwellDB


class LinkCreator(object):
	def __init__(self, tagsPath, eventsPath, dryRun, logger):
		"""
		:type logger: Logger
		"""
		super(LinkCreator, self).__init__()
		self._tagsPath = tagsPath
		self._eventsPath = eventsPath
		self._dryRun = dryRun
		self._logger = logger

	def createLinks(self, collection):
		for tag in collection.tags:
			self._processPhotoList(tag, self._getTagPath(tag))

		for event in collection.events:
			self._processPhotoList(event, self._getEventPath(event))

	def _processPhotoList(self, photoList, path):
		self._ensurePath(path, photoList)
		for photo in photoList.photos:
			self._createLink(photo, path)

	def _createLink(self, photo, linkPath):
		fileName = os.path.basename(photo.path)
		linkPath = os.path.join(linkPath, fileName)
		self._logger.logLinkCreation(photo, linkPath)
		if not self._dryRun:
			os.link(photo.path, linkPath)

	def _ensurePath(self, path, photoList):
		pathExists = os.path.exists(path)
		self._logger.logPathCreation(photoList, path, pathExists)
		if not self._dryRun and not pathExists:
			os.makedirs(path)

	def _getTagPath(self, tag):
		tagName = tag.name
		if tagName.startswith("/"):
			return self._tagsPath + tagName
		else:
			return os.path.join(self._tagsPath, tagName)

	def _getEventPath(self, event):
		return os.path.join(self._eventsPath, event.name)


def main():
	# TODO: arguments
	DB_PATH = "~/.local/share/shotwell/data/photo.db"
	BASE_PATH = "~/images/photos"
	DRY_RUN = False
	VERBOSE = True

	TAGS_DIR = "_tags"
	EVENTS_DIR = "_events"

	dbPath = os.path.expanduser(DB_PATH)
	tagsPath = os.path.expanduser(os.path.join(BASE_PATH, TAGS_DIR))
	eventsPath = os.path.expanduser(os.path.join(BASE_PATH, EVENTS_DIR))

	if VERBOSE:
		logger = VerboseLogger()
	else:
		logger = SilentLogger()
	creator = LinkCreator(tagsPath, eventsPath, DRY_RUN, logger)
	source = ShotwellDB(dbPath)

	creator.createLinks(source.getCollection())


if __name__ == '__main__':
	main()
