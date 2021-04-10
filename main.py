from controller import Controller
from scene import Scene
from animation import Animation
import color

username = "GDJxO2fgnZ1Emk-hLGdGAQsAQ2ymbM7p8ICJWmtF"
ipAddress = "192.168.1.14"

lightGroups = {
	'hanging lights': ['12','13','14','19','21'],
	'bookshelf': ['16','17'],
	'sphere' : ['31', '32']
	}


scenes = [
	Scene([color.red, color.blue, color.green]),
	Scene([color.red]),
	Scene([color.blue, color.green, color.red, color.yellow, color.purple])
	]

hangingScenes = []
for hue in range(12):
	c = color.Color(0, sat=255, bri=255)
	c.rotateHue(hue*30)
	hangingScenes.append(Scene([c, c, c, c, c.getComplimentary()[1]]))

c = Controller(ipAddress, username, lightGroups, scenes)

animation = Animation(
			lights=lightGroups['hanging lights'],
			scenes=hangingScenes,
			hue = c.hue,
			delay=2
			)
animation.animate()