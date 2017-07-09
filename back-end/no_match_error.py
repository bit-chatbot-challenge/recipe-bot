"""
Custom exception for error related to finding no match for a search
"""
class NoMatchError(Exception):
	def __init__(self, search_term, **search_criteria):
		self.search_term = search_term
		self.search_criteria = search_criteria

	def message(self):
		base_message = 'No matching recipes found for ' + self.search_term
		if self.search_criteria:
			return base_message + ' with the following search criteria: ' + str(self.search_criteria)
		else:
			return base_message