import requests
import json


class Drink:

    def __init__(self, drink_data):
        self.name = drink_data['drink_name']
        self.ingredients = []

        for ingredient_data in drink_data['ingredients']:
            self.ingredients.append(Ingredient(ingredient_data))


class Ingredient:

    def __init__(self, ingredient_data):
        self.name = ingredient_data['name']
        self.proportion = ingredient_data['ratio']
        self.location = CabinetConfig.get_location(self.name)


#consider finding a better solution for this
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

        return None

class CabinetHelper:

    BASE_URL = 'http://localhost:8000'
    cabinet_id = None #format for now: {"cabinet_id": 24}
    
    def register():
        r = requests.get(CabinetHelper.BASE_URL + '/registerCabinet')
        CabinetHelper.cabinet_id = r.text

    def get_order():
        r = requests.get(CabinetHelper.BASE_URL + '/tap', params=CabinetHelper.cabinet_id)
        data = json.loads(r.text)
        return Drink(data['drink'])

    def get_settings():
        r = requests.get(CabinetHelper.BASE_URL + '/tap', params=CabinetHelper.cabinet_id)
        data = json.loads(r.text)
        return data['settings']
        