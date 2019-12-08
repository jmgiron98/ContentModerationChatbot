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
			return attributes
		else:
			return ""

	def _getAttributeScores(self, text):
		response = self._makeRequest(text)
		attributeScores = {key: value['summaryScore']['value'] for (key, value) in response['attributeScores'].items()}
		return sorted(attributeScores.items(), key=operator.itemgetter(1))

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