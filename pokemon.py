class Pokemon:
    
    def __init__(self, name, abilities, types, species, description):
        self.name = name
        self.abilities = abilities
        self.types = types
        self.species = species
        self.description = description

    def to_dict(self):
        return {
                "name" : self.name,
                "abilities" : self.abilities,
                "types" : self.types,
                "species" : self.species,
                "description" : self.description
        }
    
    def __str__(self):
        ability_str = "\n".join(f"- {ability}" for ability in self.abilities)
        type_str = "\n".join(f"- {p_type}" for p_type in self.types)
        return f"Pokemon name: {self.name}\n\nAbility:\n{ability_str}\n\nType:\n{type_str}\n\nDescription: \n{self.description}\n"
