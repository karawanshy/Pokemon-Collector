from pokemon import Pokemon
import requests
import random
import json

class PokemonCollector:

    def __init__(self):
        self.existing_pokemon_data = self.load_data_from_file()
        self.fetch_pokemon()
        
    def load_data_from_file(self):
        """
        Loads exsisting pokemon data from DB - pokemon.json file
        """

        try:
            with open("pokemon.json", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        
    def get_pokemon(self, name):
        """
        Searchs the DB for a pokemon with the given name.
        
        Returns: Pokemon object if found and None if not.
        """

        if self.existing_pokemon_data:
            Pokemon_data =  self.existing_pokemon_data.get(name, None)
        
            if Pokemon_data:
                return Pokemon(name, Pokemon_data['abilities'], Pokemon_data['types'], Pokemon_data['species'], Pokemon_data['description'])
        
        return None
    
    def add_to_file(self, pokemon:Pokemon):
        """
        Gets a pokemon object as a parameter, add it to the exsisting pokemon data, and then stores the new data in the DB.
        """

        self.existing_pokemon_data[f'{pokemon.name}'] = pokemon.to_dict()
        
        with open("pokemon.json", "w") as file:
            json.dump(self.existing_pokemon_data, file, indent=4)
    
    def create_pokemon(self, name):
        """
        Fetches Pokemon data from the PokeAPI based on the given name.
        Retrieves information such as abilities, types, species, and description.
        
        Parameters:
        - name (str): The name of the Pokemon to fetch information for.
        
        Returns:
        - Pokemon: A Pokemon object containing the acquired information.
        """
        
        info = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}').json()

        abilities = [ability['ability']['name'] for ability in info['abilities']]

        types = [p_type['type']['name'] for p_type in info['types']]

        species_url = info['species']['url']
        species = requests.get(species_url).json()['genera'][7]['genus']

        descriptions = requests.get(species_url).json()['flavor_text_entries']
        description = next((desc['flavor_text'] for desc in descriptions if desc['language']['name'] == 'en'), '')

        return Pokemon(name, abilities, types, species, description)

    def fetch_pokemon(self):
        """
        Fetches a random Pokemon from the PokeAPI.
        If the Pokemon data is not found in DB, fetches the data from the API, adds it to DB, and returns the Pokemon object.
        If the Pokemon data is found in DB, returns the Pokemon object directly.

        Returns:
        - Pokemon: A Pokemon object containing the fetched Pokemon's information.
        """

        response = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=200')
        pokemon_list = response.json()['results']
        pokemon_name = random.choice(pokemon_list)['name']

        pokemon = self.get_pokemon(pokemon_name)
   
        if not pokemon:
            pokemon = self.create_pokemon(pokemon_name)
            self.add_to_file(pokemon)
        
        # prints fetched pokemon information to user
        print(pokemon.__str__())