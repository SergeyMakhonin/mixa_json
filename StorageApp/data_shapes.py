import json


class Player:
    __slots__ = ['first_name', 'second_name', 'age', 'plays_for', 'player_number', 'photo_path']

    def __init__(self, first_name, second_name=None):
        self.first_name = first_name
        self.second_name = second_name
        self.age = None
        self.plays_for = None
        self.player_number = None
        self.photo_path = None

    def get_json_representation(self):
        return json.dumps(
            {'first_name': self.first_name,
             'second_name': self.second_name,
             'age': self.age,
             'plays_for': self.plays_for,
             'player_number': self.player_number,
             'photo_path': self.photo_path})


class Team:
    __slots__ = ['name_olimp', 'name_localized', 'name_epl', 'name_short', 'name_short_localized', 'logo_path',
                 'logo_path_alias']

    def __init__(self, olimp_name):
        self.name_olimp = olimp_name
        self.name_localized = None
        self.name_epl = None
        self.name_short = None
        self.name_short_localized = None
        self.logo_path = None
        self.logo_path_alias = None

    def get_json_representation(self):
        return json.dumps(
            {'name_olimp': self.name_olimp,
             'name_localized': self.name_localized,
             'name_epl': self.name_epl,
             'name_short': self.name_short,
             'name_short_localized': self.name_localized,
             'logo_path': self.logo_path,
             'logo_path_alias': self.logo_path_alias})
