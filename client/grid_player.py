from helper_classes import *
import random

class GridPlayer:

    def __init__(self):
        self.foo = True
        self.move_memory = None

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units, resources: int, turns_left: int) -> [Move]:
        resources_loc = game_map.find_all_resources()
        moves = []
        melee = your_units.get_all_unit_of_type("melee")
        worker = your_units.get_all_unit_of_type("worker")
        dic = {}
        for i in worker:
            closest = game_map.closest_resources(i)
            path = game_map.bfs(i.position(), closest)
            
            moves.append(i.move_towards(path[1]))

            if i.can_mine:
                moves.append(i.mine())
        return moves
