from content_moderator import ContentModerator
import code

class Chatbot():
	def __init__(self):
		self.cm = ContentModerator()

	def run(self):
		while(True):
			text = input("> ")
			if text == 'exit':
				print("Stay moderate!")
				return
			if text == 'clear':
				self.cm.clear()
				continue
			if text == 'moderate_off':
				self.cm.off()
				continue
			if text == 'moderate_on':
				self.cm.on()
				continue
			if text == 'current':
				print(self.cm.current())
				continue
			output = self.cm.makeDecision(text)
			print(output)


chatbot = Chatbot()
chatbot.run()