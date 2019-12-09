import requests
import json
import operator

class ContentModerator():
	def __init__(self):
		key_file = open('../GoogleKey.txt')
		self.api_key = key_file.readline()
		self.requestedAttributes = ['SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'THREAT', 'SEXUALLY_EXPLICIT', 'FLIRTATION']
		self.rollingWindow = [""] * 20
		self.moderate = True

	def clear(self):
		self.rollingWindow = [""] * 20

	def off(self):
		self.moderate = False

	def on(self):
		self.moderate = True

	def current(self):
		test_string = " ".join(self.rollingWindow[-20:])
		attributes = self._getAttributeScores(" ".join(self.rollingWindow[-20:]))
		return attributes

	def makeDecision(self, text):
		self.rollingWindow.append(text)
		test_string = " ".join(self.rollingWindow[-20:])
		print(test_string)
		if self.moderate:
			attributes = self._getAttributeScores(" ".join(self.rollingWindow[-20:]))
			action = self._suggestedActions(attributes)
			categories = self._suggestedCategories(attributes)
			output = "Suggested Action: " + action + '\n' + "Suggested Categories: " + ', '.join(categories)
			return output
		else:
			return ""

	def _suggestedActions(self, attributeScores):
		if attributeScores['THREAT'] > 0.95:
			return 'Display "Threatening message detected". Suggest report and block, suggest to call the police'
		elif attributeScores['IDENTITY_ATTACK'] > 0.90:
			return 'Display "Hateful language detected". Suggest report and block'
		elif attributeScores['SEVERE_TOXICITY'] > 0.90:
			return 'Display "Toxic message detected". Suggest report and block.'
		else:
			return 'No action suggested'

	def _suggestedCategories(self, attributeScores):
		categories = set()
		if attributeScores['THREAT'] > 0.95:
			categories.add('Threat')
		if attributeScores['SEVERE_TOXICITY'] > 0.90:
			categories.add('Harassment')
			categories.add('Bullying')
		if attributeScores['IDENTITY_ATTACK'] > 0.90:
			categories.add('Hate Speech')
		if attributeScores['SEXUALLY_EXPLICIT'] > 0.95:
			categories.add('Nudity')
		return list(categories)

	def _getAttributeScores(self, text):
		response = self._makeRequest(text)
		attributeScores = {key: value['summaryScore']['value'] for (key, value) in response['attributeScores'].items()}
		return attributeScores

	def _makeRequest(self, text):
	    api_key = self.api_key
	    url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
	        '?key=' + api_key)
	    data_dict = {
	        'comment': {'text': text},
	        'languages': ['en'],
	        'requestedAttributes': {key: {} for key in self.requestedAttributes}
	    }
	    response = requests.post(url=url, data=json.dumps(data_dict)) 
	    response_dict = json.loads(response.content) 
	    return response_dict