'''
Class for controlling hue lights, using the Qhue API wrapper
'''
try:
	from qhue import Bridge
except:
	print("!!!\n!!!\nYou need to install qhue! see\nhttps://github.com/quentinsf/qhue\n!!!\n!!!")
	quit()

try:
	import color
except:
	print("!!!\n!!!\nYou need the companion color.py library!\n!!!\n!!!")
	quit()

#standard imports
import time
import random

DEBUG = False

defaultIP = "192.168.1.14"
defaultUsername = "GDJxO2fgnZ1Emk-hLGdGAQsAQ2ymbM7p8ICJWmtF"

#map the top level hue api strings to variables


class Hue:

	def __init__(self, bridgeIP, username):
		if bridgeIP is None:
			bridgeIP = defaultIP
		if username is None:
			username = defaultUsername
		self.bridge = Bridge(bridgeIP, username)


	def testing(self, lightNumbersArray):
		for i in range(3):
			for ind in lightNumbersArray:
				self.bridge.lights(ind, 'state', on=True, bri=254, xy=[0.3+(0.25-random.random()/2), 0.3+(0.25-random.random()/2)], transitiontime=30)
				if DEBUG: print("updated lights")
			time.sleep(10)


	def printLightNames(self):
		for (light, data) in self.bridge.lights().items():
			print(light, data['name'])


	def incrementBrightness(self, lightNumbers, amount):
		if amount < -254 or amount > 254:
			raise ValueError("Increment amount must be in [-254, 254] but was %s"%amount)
		#check if we got a single light, or an array of them:
		if isinstance(lightNumbers, list):
			#create a group
			groupNum = self.createGroup(lightNumbers)

			#blink that group
			self.incrementGroupBrightness(groupNum, amount)

			#delete the group
			self.deleteGroup(groupNum)
		else:
			self.bridge.lights(str(lightNumbers), 'state', on=True, bri_inc=amount, transitiontime=2)


	def incrementGroupBrightness(self, groupNum, amount):
		if amount < -245 or amount > 254:
			raise ValueError("Increment amount must be in [-254, 254] but was %s"%amount)
		self.bridge.groups(str(groupNum), 'action', on=True, bri_inc=amount, transitiontime=2)


	def setBrightness(self, lightNumbers, brightness):
		#check if we got a single light, or an array of them:
		if isinstance(lightNumbers, list):
			#create a group
			groupNum = self.createGroup(lightNumbers)

			#blink that group
			self.setGroupBrightness(groupNum, brightness)

			#delete the group
			self.deleteGroup(groupNum)
		else:
			if brightness < 0 or brightness > 254:
				raise ValueError("Brightness must be in [0, 254] but was %s"%brightness)
			if brightness == 0:
				#turn off lights
				self.bridge.lights(str(lightNumbers), 'state', on=False)
			else:
				self.bridge.lights(str(lightNumbers), 'state', on=True, bri=brightness)


	def setGroupBrightness(self, groupNum, brightness):
		if brightness < 0 or brightness > 254:
			raise ValueError("Brightness must be in [0, 254] but was %s"%brightness)
		if brightness == 0:
			#turn off lights
			self.bridge.groups(str(groupNum), 'action', on=False)
		else:
			self.bridge.groups(str(groupNum), 'action', on=True, bri=brightness)


	#set a *single* light to the color provided
	def setState(self, lightNumber, color, on=True):
		if isinstance(lightNumber, list):
			raise ValueError("setState can only handle a single light not a list of them")
		d = color.getDict()
		d['on'] = on
		return self.setStateWithDict(lightNumber, d)


	#set a *singe* light to the parameters pass in in stateDict
	def setStateWithDict(self, lightNumber, stateDict):
		if isinstance(lightNumber, list):
			raise ValueError("setStateWithDict can only handle a single light not a list of them")
		stateDict.pop('mode', None)
		stateDict.pop('colormode', None)
		stateDict.pop('reachable', None)
		stateDict.pop('alert', None)
		if DEBUG: print(self.bridge.lights[str(lightNumber)]())
		if DEBUG: print(stateDict)
		return self.bridge.lights[str(lightNumber)].state(**stateDict)


	#return any currently enabled schedules
	def getEnabledSchedules(self):
		schedules = []
		s = self.bridge.schedules()
		for k in s:
			if s[k]['status'] == 'enabled':
				schedules.append(s[k])
		return schedules


	def getRules(self):
		rules = {}
		for (k, v) in self.bridge.rules().items():
			rules[k] = v
		return rules


	#blink the selected light or lights to help identify them
	def blink(self, lightNumbers, blinks=3, delay=0.5):
		#blink the selected light(s) _blinks_ times, with a delay of _delay_ between each change

		#check if we got a single light, or an array of them:
		if isinstance(lightNumbers, list):
			#create a group
			groupNum = self.createGroup(lightNumbers)

			#blink that group
			self.blinkGroup(groupNum, blinks, delay)

			#delete the group
			self.deleteGroup(groupNum)

		else:
			initialBrightness = self.bridge.lights()[str(lightNumbers)]['state']['bri']
			for i in range(blinks):
				self.bridge.lights(str(lightNumbers), 'state', on=True, bri=254)
				time.sleep(delay)
				self.bridge.lights(str(lightNumbers), 'state', on=True, bri=25)
				time.sleep(delay)
				self.bridge.lights(str(lightNumbers), 'state', bri=initialBrightness)


	#blink an entire group of lights, then reset them to their initial values
	def blinkGroup(self, groupNum, blinks=3, delay=0.5):
		#cache the light states
		lights = self.bridge.lights()
		lightsInGroup = self.bridge.groups()[str(groupNum)]['lights']
		initialState = {}
		for light in lightsInGroup:
			initialState[light] = lights[light]['state']

		for i in range(blinks):
			self.bridge.groups(str(groupNum), 'action', on=True, bri=254)
			time.sleep(delay)
			self.bridge.groups(str(groupNum), 'action', on=True, bri=25)
			time.sleep(delay)

		for (lightNum, state) in initialState.items():
			self.setStateWithDict(lightNum, state)


	#returns (index, name) for each group/room
	def getGroupNames(self):
		names = []
		groups = self.bridge.groups()
		for key in groups:
			names.append((key, groups[key]['name']))
		return names


	#greate a group of lights and return its group number
	def createGroup(self, lightNumbersArray, name=None):
		#make sure lightNumbersArray is all string
		lightNumbersArray = [str(value) for value in lightNumbersArray]
		if name:
			result = self.bridge.groups(lights=lightNumbersArray, name=name, http_method='post')
		else:
			result = self.bridge.groups(lights=lightNumbersArray, http_method='post')
		if 'success' in result[0].keys():
			return int(result[0]['success']['id'])
		else:
			return result


	#delete the specified group
	def deleteGroup(self, groupNum):
		return self.bridge.groups(str(groupNum), http_method='delete')


	#set one or many lights to one or many colors
	def setLights(self, lights, colors):
		if not isinstance(colors, list):
			colors = [colors]
		totalColors = len(colors)
		index=0
		if not isinstance(lights, list):
			lights = [lights]
		for lightNumber in lights:
			self.setState(lightNumber, colors[index])
			index = (index+1)%totalColors

	def setScene(self, lights, scene, offset=0):
		colors = scene.colors[offset:] + scene.colors[:offset] #rotate the scenes colors by the offset
		return self.setLights(lights, colors)


	def stopIConnectHueAnimation(self):
		schedules = self.bridge.schedules()
		for k in schedules:
			if schedules[k]['status'] == 'enabled' and schedules[k]['description'].startswith('XFDani'):
				if DEBUG:
					print(schedules[k])
				self.bridge.schedules[k](status='disabled')




