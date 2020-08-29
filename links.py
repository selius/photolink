import os

class LinkCreator(object):
	def __init__(self, tagsPath, eventsPath, dryRun, logger):
		super(LinkCreator, self).__init__()
		self._tagsPath = tagsPath
		self._eventsPath = eventsPath
		self._dryRun = dryRun
		self._logger = logger
		self._dirsCreated = 0
		self._linksCreated = 0

	def createLinks(self, collection):
		self._dirsCreated = 0
		self._linksCreated = 0

		for tag in collection.tags:
			self._processMediaList(tag, self._getTagPath(tag))

		for event in collection.events:
			self._processMediaList(event, self._getEventPath(event))

	def dirsCreated(self):
		return self._dirsCreated

	def linksCreated(self):
		return self._linksCreated

	def _processMediaList(self, mediaList, path):
		self._ensurePath(path, mediaList)
		for media in mediaList.objects:
			self._createLink(media, path)

	def _createLink(self, media, linkPath):
		fileName = os.path.basename(media.path)
		linkPath = os.path.join(linkPath, fileName)
		pathExists = os.path.exists(linkPath)
		self._logger.logLinkCreation(media, linkPath, pathExists)
		if not pathExists:
			self._linksCreated += 1
			if not self._dryRun:
				os.link(media.path, linkPath)

	def _ensurePath(self, path, mediaList):
		pathExists = os.path.exists(path)
		self._logger.logPathCreation(mediaList, path, pathExists)
		if not pathExists:
			self._dirsCreated += 1
			if not self._dryRun:
				os.makedirs(path)

	def _getTagPath(self, tag):
		tagName = tag.name
		if tagName.startswith("/"):
			return self._tagsPath + tagName
		else:
			return os.path.join(self._tagsPath, tagName)

	def _getEventPath(self, event):
		return os.path.join(self._eventsPath, event.name)
