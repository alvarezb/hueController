from controller import Controller
import scene
from scene import Scene
from animation import Animation
import color
import time
import os
rpi = (os.uname().nodename == 'raspberrypi')
if rpi:
	from encoder import Encoder
	brightnessEncoder = Encoder(5, 17)
	sceneEncoder = Encoder(18, 23)


username = "GDJxO2fgnZ1Emk-hLGdGAQsAQ2ymbM7p8ICJWmtF"
ipAddress = "192.168.1.14"

lightGroups = {
	'hanging lights': ['21','12','13','14','19'],
	'bookshelf': ['16','17'],
	'sphere' : ['31', '32']
	}


scenes = [
	scene.rgb,
	scene.red,
	scene.tentacles,
	scene.warm,
	scene.pastels
	]

hangingScenes = []
for hue in range(12):
	c = color.Color(0, sat=255)
	c.rotateHue(hue*30)
	hangingScenes.append(Scene([c.getComplimentary()[1], c, c, c, c]))

c = Controller(ipAddress, username, lightGroups, scenes)

complimentaryAnimation = Animation(
	lights=lightGroups['hanging lights'],
	scenes=hangingScenes,
	hue = c.hue,
	delay=2
	)

pastelsAnimation = Animation(
	lights=lightGroups['hanging lights'],
	scenes=[scene.pastels.withoutBrightness().rotated(x) for x in range(5)],
	hue=c.hue,
	delay=2
	)

if rpi:
	for i in range(100):
		print(brightnessEncoder.read())
		print(sceneEncoder.read())
		time.sleep(.1)
