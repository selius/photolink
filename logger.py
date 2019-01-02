class Logger(object):
	def logTag(self, tag, path, pathExists):
		raise NotImplementedError

	def logEvent(self, event, path, pathExists):
		raise NotImplementedError


class SilentLogger(Logger):
	def logTag(self, tag, path, pathExists):
		pass

	def logEvent(self, event, path, pathExists):
		pass


class VerboseLogger(Logger):
	def logTag(self, tag, path, pathExists):
		print "Tag: %s, directory: %s - %s..." % (tag.name, path, "exists, skipping" if pathExists else "creating")

	def logEvent(self, event, path, pathExists):
		print "Event: %s, directory: %s - %s..." % (event.name, path, "exists, skipping" if pathExists else "creating")
