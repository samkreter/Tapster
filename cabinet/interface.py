import requests
import json


class CabinetConfig:

    def get_location(ingredient):
        """
        Get the location of the container for ingredient

        Args:
            ingredient (str): the ingredient to retrieve the location of

        Returns:
            location (int): int representing location. -1 indicates failure
        """

        locfile = "liquor_locations.txt"
        f = open(locfile, "r")

        #iterate over lines in the location file to look up location
        for line in f.readlines():
            entry = line.split(':')

            if entry[0].lower() == ingredient.lower():
                return  int(entry[1])

        return -1




class Instructions:

    def __init__(self, recipe):
        """
        Generate a instance of instructions for the Cabinet to prepare a drink.
        Instructions are a list of steps, each step is a list of all locations
        to pour a shot from.
        e.g. [[1, 2], [2], [2]]

        Args:
            recipe: list in format [{'ratio': INT, 'name': STR}, ...]

        """

        #set up instruction structure
        self._steps = []
        num_steps = max([ingredient['ratio'] for ingredient in recipe])

        for i in range(num_steps):
            self._steps.append([])

        #populate instructions
        for ingredient in recipe:

            location = CabinetConfig.get_location(ingredient['name'])
            #add error check here if get_location returns -1

            for i in range(0, ingredient['ratio']):
                self._steps[i].append(location)

    def execute(self):
        """
        Execute the instructions to prepare a drink
        """

        stepcounter = 0
        for step in self._steps:
            stepcounter += 1
            print("Step %s" % stepcounter)
            for location in step:
                print("SHOT FROM LOCATION %s" % location)


if __name__ == "__main__":

    base_url = 'http://localhost:8000'

    #get id

    r = requests.get(base_url + '/registerCabinet')
    cabinet_id = r.text

    #listen for commands
    while(True):
        r = requests.get(base_url + '/tap', params=cabinet_id)
        data = json.loads(r.text)
        settings = data['settings']
        drink_recipe = data['drink']['ingredients']

        instructions = Instructions(drink_recipe)
        instructions.execute()

