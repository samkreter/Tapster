class Instructions:
	_instruction_list = []

	''' e.g. [ 
			[1, 2]
			[2]
			[2]
			 ] '''

	def __init__(self, recipe):

		#set up instruction structure
		instructions_len = max([ingredient.shots for ingredient in recipe])
		for i in range(0, instructions_len):
			_instruction_list.append([])

		#populate instructions
		for ingredient in recipe:

			bottle = deviceconfig.getbottle(ingredient.name)

			for i in range(0, ingredient.shots):
				_instruction_list[i].append(bottle)

	def execute():
		for step in self._instruction_list:
			for ingredient in step:
				#implement some kind of async thing here later
				cabinet.get(ingredient)


#/tap

def main():

	while(True):
		r = requests.get('')

