from hue import Hue
import color
from scene import Scene
from animation import Animation


class Controller:

	def __init__(self, bridgeIP, bridgeUsername, lightGroups, scenes):
		self.hue = Hue(bridgeIP, bridgeUsername)
		self.lightGroups = lightGroups
		self.scenes = scenes

		self.selectedKey = [*lightGroups][0] #select a first group
		self.sceneIndex = 0


	def setBrightness(self, brightness):
		return self.hue.setBrightness(self.lightGroups[self.selectedKey], brightness)


	def incrementBrightness(self, amount=30):
		return self.hue.incrementBrightness(self.lightGroups[self.selectedKey], amount)


	def decrementBrightness(self, amount=-30):
		return self.hue.incrementBrightness(self.lightGroups[self.selectedKey], amount)


	#select a group and return its name
	def selectGroup(self, groupName, blink=True):
		if groupName in self.lightGroups.keys():
			self.selectedKey = groupName
		else:
			raise ValueError("Selected key is not a valid group name")
		if blink:
			self.blinkGroup()
		return self.selectedKey


	def incrementGroup(self, amount=1, blink=True):
		groups = [*self.lightGroups] #creates an array of the dictionary keys. *magic*
		currentIndex = groups.index(self.selectedKey)
		newIndex = (currentIndex + amount) % len(groups)
		return self.selectGroup(groups[newIndex], blink=blink)


	def decrementGroup(self, amount=1, blink=True):
		return self.incrementGroup(amount=-1*amount, blink=blink)


	def incrementScene(self, amount=1):
		self.sceneIndex = (self.sceneIndex + amount) % len(self.scenes)
		return self.hue.setScene(self.lightGroups[self.selectedKey], self.scenes[self.sceneIndex])


	def decrementScene(self, amount=1):
		return self.incrementScene(amount= -1*amount)


	def blinkGroup(self, blinks=1, delay=0.5):
		return self.hue.blink(self.lightGroups[self.selectedKey], blinks=blinks, delay=delay)


	def turnGroupOff(self):
		return self.setBrightness(0)

	def turnAllOff(self):
		for (name, lightNumbers) in self.lightGroups.items():
			self.hue.setBrightness(lightNumbers, 0)

	#only call this on a raspberry pi, otherwise it wont work
	def monitorEncoders(self, brightnessAddress, sceneAddress, groupAddress):
		#initialize everything
		import qwiic_twist
		brightnessEncoder = qwiic_twist.QwiicTwist(address=brightnessAddress)
		brightnessEncoder.begin()
		sceneEncoder = qwiic_twist.QwiicTwist(address=sceneAddress)
		sceneEncoder.begin()
		groupEncoder = qwiic_twist.QwiicTwist(address=groupAddress)
		groupEncoder.begin()

		brightnessEncoder.set_color(230,255,255) #white-ish
		sceneEncoder.set_color(0,0,255) #blue
		groupEncoder.set_color(0,0,0) #no colors

		brightnessPrior = brightnessEncoder.count
		scenePrior = sceneEncoder.count
		groupPrior = groupEncoder.count
		while True:
			if brightnessPrior - brightnessEncoder.count >= 2:
				self.decrementBrightness()
				brightnessPrior = brightnessEncoder.count
				print("decrementBrightness")
			elif brightnessPrior - brightnessEncoder.count <= -2:
				self.incrementBrightness()
				brightnessPrior = brightnessEncoder.count
				print("incrementBrightness")

			if scenePrior - sceneEncoder.count >= 4:
				#self.decrementScene()
				scenePrior = sceneEncoder.count 
				print("decrementScene", scenePrior, sceneEncoder.count)
			elif scenePrior - sceneEncoder.count <= -4:
				#self.incrementScene()
				scenePrior = sceneEncoder.count
				print("incrementScene", scenePrior, sceneEncoder.count)

			if groupPrior - groupEncoder.count >= 6:
				self.decrementGroup()
				groupPrior = groupEncoder.count 
				print("decrementGroup")
			elif groupPrior - groupEncoder.count <= -6:
				self.incrementGroup()
				groupPrior = groupEncoder.count
				print("incrementGroup")





