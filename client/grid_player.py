from helper_classes import *
import random

class GridPlayer:

    def __init__(self):
        self.foo = True
        self.move_memory = None

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units, resources: int, turns_left: int) -> [Move]:
        
        