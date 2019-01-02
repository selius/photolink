class Logger(object):
	def logPathCreation(self, photoList, path, pathExists):
		raise NotImplementedError

	def logLinkCreation(self, photo, path):
		raise NotImplementedError


class SilentLogger(Logger):
	def logPathCreation(self, photoList, path, pathExists):
		pass

	def logLinkCreation(self, photo, path):
		pass


class VerboseLogger(Logger):
	def logPathCreation(self, photoList, path, pathExists):
		print "%s: %s, directory: %s - %s..." % (
			photoList.typeName(), photoList.name, path, "exists, skipping" if pathExists else "creating")

	def logLinkCreation(self, photo, path):
		print "Photo: %s: %s -> %s" % (photo.id, photo.path, path)
