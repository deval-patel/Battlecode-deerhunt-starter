from helper_classes import *


class GridPlayer:
    map: Map
    attacking: dict
    stunning: dict
    resources: int
    resource_mapping: dict

    def __init__(self):
        self.foo = True
        self.map = None
        self.attacking = {}
        self.stunning = {}
        self.resources = 0
        self.resource_mapping = {}


    def mark_moved(self, pos, direction):
        # Mark the new pos as a wall
        coord = coordinate_from_direction(pos[0], pos[1], direction)
        # x, y = pos
        # if direction == 'LEFT':
        #     coord = (x - 1, y)
        # if direction == 'RIGHT':
        #     coord = (x + 1, y)
        # if direction == 'UP':
        #     coord = (x, y - 1)
        # if direction == 'DOWN':
        #     coord = (x, y + 1)
        self.map.set_tile(coord[0], coord[1], 'x')


    def get_melee_move(self, unit: Unit, enemy_units: Units,
                       resources: int, turns_left: int) -> Move:
        # If we can attack an enemy, do this
        can_attack = unit.can_attack(enemy_units)
        can_stun = unit.can_stun(enemy_units)
        if can_attack:
            for enemy in can_attack:
                # If enemy is already being attacked then skip
                if enemy in self.attacking:
                    continue
                # Attack this enemy
                self.attacking[enemy] = unit
                # Mark the new pos as a wall
                self.mark_moved(unit.position(), enemy[1])
                # Attack with this unit towards the enemy's direction
                return unit.attack(enemy[1])

        # If we can stun an enemy do this
        # do this later

        # Move towards a resource unit
        cr = self.map.closest_resources_all(unit)
        # If there is a closest resource
        if cr:
            for (loc, dist) in cr:
                # Check the guard field to see if there is already a guard
                if self.resource_mapping[loc][1]:
                    continue
                # Go towards this resource and guard it
                pos = self.get_melee_resource_pos(unit, loc)
                if pos:
                    self.resource_mapping[loc][1] = unit
                    # Mark the new pos as a wall
                    self.mark_moved(pos, unit.direction_to(pos))
                    return unit.move_towards(pos)
        return None


    def get_melee_resource_pos(self, unit: Unit, loc: (int, int)):
        """
        Returns the location near this resource to move to
        If there is only one entrance to this resource, then positions near the entrance
        """
        positions = []
        x, y = loc
        perimeter = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for pos in perimeter:
            # If the position is a wall or resource skip
            if self.map.is_wall(pos[0], pos[1]) or self.map.is_resource(pos[0], pos[1]):
                continue
            positions.append(pos)

        # If there is more than one opening around the resource, return first found
        if len(positions) > 1:
            return positions[0]

        # If only one opening around the resource, return a position around this position
        elif len(positions) == 1:
            self.get_melee_resource_pos(unit, positions[0])

        # If no valid positions return None
        return None


    def construct_resource_mapping(self):
        # Construct a resource mapping, where the first is the assigned worker and second
        # is the assigned guard
        all_resources = self.map.find_all_resources()
        for r in all_resources:
            self.resource_mapping[r] = [None, None]


    def get_worker_move(self, unit: Unit, enemy_units: Units,
                        resources: int, turns_left: int) -> Move:
        # If we can mine, mine
        if unit.can_mine(self.map):
            return unit.mine()

        # If already mining, return none
        elif unit.attr['mining_status'] > 0:
            return None

        # Go towards an unoccupied resource
        cr = self.map.closest_resources_all(unit)
        # If there is a closest resource
        if cr:
            for (loc, dist) in cr:
                # Check the worker field to see if there is already a worker
                if self.resource_mapping[loc][0]:
                    continue
                # Go towards this resource to mine it
                path = self.map.bfs(unit.position(), loc)
                if path and len(path) > 1:
                    self.resource_mapping[loc][0] = unit
                    self.mark_moved(path[1], unit.direction_to(path[1]))
                    return unit.move_towards(path[1])
        return None


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

        # assign current num of resources
        self.resources = resources
        self.construct_resource_mapping()

        # get all worker units
        workers = your_units.get_all_unit_of_type('worker')

        # get all melee units
        melees = your_units.get_all_unit_of_type('melee')

        # prioritize movement of melees
        for unit in melees:
            move = self.get_melee_move(unit, enemy_units, resources, turns_left)
            if move:
                moves.append(move)

        # move workers
        for unit in workers:
            move = self.get_worker_move(unit, enemy_units, resources, turns_left)
            if move:
                moves.append(move)
        print(moves)
        return moves
