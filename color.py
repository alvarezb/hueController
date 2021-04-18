import numpy as np

class Color:

	def __init__(self, hue, sat, bri=None):
		if sat<0 or sat>255:
			raise ValueError("Saturation parameter is out of range: %s"%sat)
		if bri != None and (bri<0 or bri>255):
			raise ValueError("Brightness parameter is out of range: %s"%bri)

		self._hue = np.uint16(hue)
		self._sat = np.uint8(sat)
		if bri is None:
			self._bri = None
		else:
			self._bri = np.uint8(bri)

	@property
	def hue(self):
		return int(self._hue)
	@hue.setter 
	def hue(self, hue):
		self._hue = np.uint16(hue)

	@property
	def sat(self):
		return int(self._sat if self._sat < 255 else 254)
	@sat.setter
	def sat(self, sat):
		if sat<0 or sat>255:
			raise ValueError("Saturation parameter is out of range: %s"%sat)
		self._sat = np.uint8(sat)

	@property
	def bri(self):
		if self._bri is None:
			return None
		else:
			return int(self._bri if self._bri < 255 else 254)
	@bri.setter 
	def bri(self, bri):
		if bri<0 or bri>255:
			raise ValueError("Brightness parameter is out of range: %s"%bri)
		self._bri = np.uint8(bri)

	def __str__(self):
		return "<Color object: hue=%s, sat=%s, bri=%s>"%(self.hue, self.sat, self.bri)
	def __repr__(self):
		return self.__str__()

	def getDict(self, mode="HSB"):
		if mode == "HSB":
			if self.bri is None:
				return {'hue': self.hue, 'sat': self.sat}
			else:
				return {'bri': self.bri, 'hue': self.hue, 'sat': self.sat}
		elif mode == "XY":
			raise ValueError("XY is not yet implemented")
		else:
			raise ValueError("unsupported dict mode")

	def _getRotatedHue(self, degrees):
		return self._hue + (65536.0*float(degrees)/360.0)

	def withoutBrightness(self):
		#return a new color object that does not have the brightness value set
		return Color(self.hue, self.sat)

	def rotateHue(self, degrees):
		self.hue = self._getRotatedHue(degrees=degrees)

	def getRotatedColor(self, degrees):
		return Color(hue=self._getRotatedHue(degrees), sat=self.sat, bri=self.bri)

	def getComplimentary(self):
		return (self, self.getRotatedColor(180))

	def getTriadic(self):
		return (self, self.getRotatedColor(120), self.getRotatedColor(240))

	def getTetradic(self):
		return (self, self.getRotatedColor(90), self.getRotatedColor(180), self.getRotatedColor(270))

	def getSplitComplimentary(self):
		return (self, self.getRotatedColor(150), self.getRotatedColor(210))


#static colors
red = Color(hue=0, sat=255, bri=255)

orange = red.getRotatedColor(30)
yellow = orange.getRotatedColor(30)
lime = yellow.getRotatedColor(30)

green = Color(hue=25500, sat=255, bri=255)

ocean = green.getRotatedColor(30)
cyan = ocean.getRotatedColor(30)
sky = cyan.getRotatedColor(30)

blue = Color(hue=46920, sat=255, bri=255)

purple = blue.getRotatedColor(30)
magenta = purple.getRotatedColor(30)
crimson = magenta.getRotatedColor(30)

white = Color(hue=0, sat=0, bri = 255)