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
			output = self.cm.getAttributeScores(text)
			print(output)


chatbot = Chatbot()
chatbot.run()