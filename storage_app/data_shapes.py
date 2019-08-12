import json


class Player:
    __slots__ = ['first_name', 'second_name', 'age', 'plays_for', 'player_number', 'photo_destination']

    def __init__(self, first_name, second_name=None):
        self.first_name = first_name
        self.second_name = second_name
        self.age = None
        self.plays_for = None
        self.player_number = None
        self.photo_destination = None

    def get_json_representation(self):
        return {'first_name': self.first_name,
                'second_name': self.second_name,
                'age': self.age,
                'plays_for': self.plays_for,
                'player_number': self.player_number,
                'photo_destination': self.photo_destination}


class Team:
    __slots__ = ['name_olimp', 'name_localized', 'name_apl', 'logo_destination']

    def __init__(self, olimp_name):
        self.name_olimp = olimp_name
        self.name_localized = None
        self.name_apl = None
        self.logo_destination = None

    def get_json_representation(self):
        return {'name_olimp': self.name_olimp,
                'name_localized': self.name_localized,
                'name_apl': self.name_apl,
                'logo_destination': self.logo_destination}
