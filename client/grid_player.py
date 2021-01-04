from helper_classes import *
import random

class GridPlayer:

    def __init__(self):
        self.foo = True
        self.move_memory = None

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units, resources: int, turns_left: int) -> [Move]:
        print("ticks")
        allied = []
        ids = your_units.get_all_unit_ids()
        for i in ids:
            allied.append(your_units.get_unit(i))
        moves = [None for i in range(len(allied))]
        foes = enemy_units.units
        if self.move_memory == None:
            self.move_memory = [[] for i in range(len(allied))]
        resources_targeted = [] # list of coordinates
        for i in range(len(allied)):
            if allied[i].type == "worker":
                if allied[i].can_mine(game_map):
                    moves[i] = allied[i].mine()
                    self.move_memory[i] = []
                    continue
                closest_resource= game_map.closest_resources(allied[i])
                if closest_resource is None:
                    moves[i] = self.wander(game_map, allied[i], allied)
                else:
                    if self.move_memory[i]==[]:
                        self.move_memory[i].extend(game_map.bfs(allied[i].position(), closest_resource))
                    moves[i] = self.move_memory[i][0]
            else:
                attackables = allied[i].can_attack(enemy_units)
                if attackables:
                    moves[i] = allied[i].attack(attackables[0][1])
                else:
                    moves[i] = self.wander(game_map, allied[i], allied)
        return moves


    def wander(self, game_map:Map, unit:Unit, allied) -> Move:
        choices = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        print("\n---------------------\nWandering\n-----------------------\n")
        chosen_position = coordinate_from_direction(unit.position()[0], unit.position()[1],choices[random.randint(0,3)])
        while(game_map.is_wall(chosen_position[0], chosen_position[1]) or self.is_occupied(game_map, chosen_position, allied)):
            chosen_position = coordinate_from_direction(unit.position()[0], unit.position()[1],choices[random.randint(0,3)])
        return unit.move(unit.direction_to(chosen_position))


    def is_occupied(self, game_map, coordinates, allied):
        for unit in allied:
            if coordinates == unit.position():
                return True
        return False
        


