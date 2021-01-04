<<<<<<< HEAD
class GridPlayer:

    def __init__(self):
        self.foo = True

    def tick(self, game_map, your_units, enemy_units, resources, turns_left):
        out_lst = []
        for unit in your_units:
            print(unit.location)
        return []
=======
from move import Move
# from pprint import pprint
from helper_classes import Map, Units

WORKER_TYPE = 'worker'
MELEE_TYPE = 'melee'

class GridPlayer:
    def __init__(self) -> None:
        self.safe_turns = 0

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units,
             resources: int, turns_left: int) -> [Move]:

        return []
>>>>>>> d9fb2f1384b0a2af92680723e360214b85c5781f
