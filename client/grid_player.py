from helper_classes import *
import random

class GridPlayer:

    def __init__(self):
        self.foo = True

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units, resources: int, turns_left: int) -> [Move]:
        print("ticks")
        allied_workers = your_units.get_all_unit_of_type('worker')
        moves = []
        allied_melee = your_units.get_all_unit_of_type('melee')
        allied = allied_workers + allied_melee
        resources_targeted = [] # list of coordinates
        for i in range(len(allied_workers)):
            if allied_workers[i].can_mine(game_map):
                moves.append(allied_workers[i].mine())
                continue
            closest_resource= game_map.closest_resources(allied_workers[i])
            if closest_resource is None:
                moves.append(self.wander(game_map, allied_workers[i], allied))
            else:
                path_wanted = game_map.bfs(allied_workers[i].position(), closest_resource)
                if path_wanted:
                    moves.append(path_wanted[0])    

        for i in range(len(allied_melee)):    
            attackables = allied_melee[i].can_attack(enemy_units)
            if attackables:
                moves.append(allied_melee[i].attack(attackables[0][1]))
            else:
                moves.append(self.wander(game_map, allied_melee[i], allied))
        return moves

    # def tick(self, game_map: Map, your_units: Units, enemy_units: Units, resources: int, turns_left: int) -> [Move]:
    #     workers = your_units.get_all_unit_of_type('worker')
    #     return [worker.move('RIGHT') for worker in workers]


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
