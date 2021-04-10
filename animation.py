from scene import Scene
import threading, sched, time

class Animation:
	def __init__(self, lights, scenes, hue, delay=5, transitiontime=2, lightIndexOffset=0, sceneIndexOffset=0):
		if not isinstance(lights, list):
			lights = [lights]
		self.lights = lights
		if not isinstance(scenes, list):
			scenes = [scenes]
		self.scenes = scenes
		self.hue = hue
		self.delay = delay
		self.transitiontime = transitiontime*10 #hue uses an annoying 100ms per count measurement
		self.lightIndexOffset = lightIndexOffset
		self.sceneIndexOffset = sceneIndexOffset
		self.thread = None
		self.terminate = False

	def animate(self, delay=0, sceneIndex=None):
		#print("starting animate")
		if not sceneIndex:
			sceneIndex = self.sceneIndexOffset
		time.sleep(delay)
		if self.terminate:
			return
		self.hue.setScene(lights=self.lights, scene=self.scenes[sceneIndex % len(self.scenes)], offset=self.lightIndexOffset, transitiontime=self.transitiontime)
		self.thread = threading.Thread(target=self.animate, kwargs={'delay':self.delay, 'sceneIndex': sceneIndex+1})
		#print("ending animate")
		self.thread.start()

	def stopAnimating(self):
		#try to stop the task saved in scheduledTask
		self.terminate = True