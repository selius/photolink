import os

class LinkCreator(object):
	def __init__(self, tagsPath, eventsPath, dryRun, logger):
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
