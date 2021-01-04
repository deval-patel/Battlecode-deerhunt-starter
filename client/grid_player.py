from helper_classes import *


class GridPlayer:
    map: Map

    def __init__(self):
        self.foo = True
        self.map = NULL

    def get_worker_move(self, game_map: Map, unit: Unit, enemy_units: Units,
                        resources: int, turns_left: int) -> Move:
        pass

    def get_melee_move(self, game_map: Map, unit: Unit, enemy_units: Units,
                       resources: int, turns_left: int) -> Move:
        pass

    def map_copy(self, game_map: Map):
        # Construct a copy of the grid.
        grid = []

        for row in game_map.grid:
            grid.append(row.copy())

        self.map = Map(grid)

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units,
             resources: int, turns_left: int) -> [Move]:
        # empty moves list
        moves = []
        # construct a modifiable copy of the grid.
        self.map_copy(game_map)

        # loop through all of the units and try to make a move for them.
        for unit in your_units:
            if unit.type == 'worker':
                temp = get_worker_move(
                    self.map, unit, enemy_units, resources, turns_left)
                if temp:
                    moves.append(temp)
            else:
                temp = get_melee_move(
                    self.map, unit, enemy_units, resources, turns_left)
                if temp:
                    moves.append(temp)
        return moves
