import color

class Scene:

	def __init__(self, colors, name=None, transitionMilliSeconds=500):
		self.name = name
		if isinstance(colors, list):
			self.colors = colors
		else:
			self.colors = [colors]
		self.transition = transitionMilliSeconds / 100 # Hue uses a weird "100ms per count" timing scheme

	def __len__(self):
		return len(self.colors)

tentecles = Scene([color.Color(hue=4096, sat=255, bri=255), color.Color(hue=37323, sat=217, bri=176)])
red = Scene([color.red])
christmas = Scene([color.red, color.green, color.white])

