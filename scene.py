import color

class Scene:

	def __init__(self, colors, name=None, transitionMilliSeconds=500):
		self.name = name
		if isinstance(colors, list):
			self.colors = colors
		else:
			self.colors = [colors]
		self.transition = transitionMilliSeconds / 100 # Hue uses a weird "100ms per count" timing scheme

	def rotated(self, amount):
		return Scene(colors=self.colors[amount:]+self.colors[:amount], name=self.name, transitionMilliSeconds=self.transition*10)

	def withoutBrightness(self):
		return Scene(colors=[color.withoutBrightness() for color in self.colors], name=self.name, transitionMilliSeconds=self.transition*10)

	def __len__(self):
		return len(self.colors)

	def __print__(self):
		return "<Scene with name %s>"%self.name

	def __repr__(self):
		return "<Scene with name %s>"%self.name

tentacles = Scene(name="Tentacles", colors=[color.Color(hue=4096, sat=255, bri=255), color.Color(hue=37323, sat=217, bri=176)])
red = Scene(name="Red", colors=[color.red])
christmas = Scene(name="Christmas", colors=[color.red, color.green, color.white])
rgb = Scene(name="RGB", colors=[color.red, color.blue, color.green])
pastels = Scene(name="Pastels", colors=[
	color.Color(hue=28950, sat=64, bri=255),
	color.Color(hue=41140, sat=100, bri=255),
	color.Color(hue=52610, sat=75, bri=255),
	color.Color(hue=4551,  sat=100, bri=255),
	color.Color(hue=11650, sat=50, bri=255),
	])
warm = Scene(name="Warm", colors=[color.warmWhite])