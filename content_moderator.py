import requests
import json
import operator

class ContentModerator():
	def __init__(self):
		key_file = open('../GoogleKey.txt')
		self.api_key = key_file.readline()
		self.requestedAttributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT', 'FLIRTATION']

	def getAttributeScores(self, text):
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