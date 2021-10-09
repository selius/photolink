class Logger(object):
	def logPaths(self, tagsPath, eventsPath):
		raise NotImplementedError

	def logPathCreation(self, mediaList, path, pathExists):
		raise NotImplementedError

	def logLinkCreation(self, media, path, pathExists):
		raise NotImplementedError

	def logResults(self, dirsCreated, linksCreated):
		raise NotImplementedError


class SilentLogger(Logger):
	def logPaths(self, tagsPath, eventsPath):
		pass

	def logPathCreation(self, mediaList, path, pathExists):
		pass

	def logLinkCreation(self, media, path, pathExists):
		pass

	def logResults(self, dirsCreated, linksCreated):
		pass


class VerboseLogger(Logger):
	def logPaths(self, tagsPath, eventsPath):
		print("Tags directory: %s" % tagsPath)
		print("Events directory: %s" % eventsPath)

	def logPathCreation(self, mediaList, path, pathExists):
		print("%s: %s, directory: %s - %s..." % (
			mediaList.typeName(), mediaList.name, path, "exists, skipping" if pathExists else "creating"))

	def logLinkCreation(self, media, path, pathExists):
		print("%s: %s: %s -> %s%s" % (media.typeName(), media.id, media.path, path, " (exists)" if pathExists else ""))

	def logResults(self, dirsCreated, linksCreated):
		print("Directories created: %d" % dirsCreated)
		print("Links created: %d" % linksCreated)
