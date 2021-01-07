from helper_classes import *
import random


def optimize_movements(your_units: Units, movements: [Move]):
    # map all units to their positions
    ids = your_units.get_all_unit_ids()
    pos = {}
    for id in ids:
        pos[id] = your_units.get_unit(id).position()

    i = 0
    moves = []
    while i < len(movements) and len(moves) < len(movements):
        for m in movements:
            if m not in moves:
                dir = m.directions[0]
                moved_pos = get_moved_pos(your_units.get_unit(str(m.unit)).position(), dir)
                occupied = False
                for id in ids:
                    if pos[id] == moved_pos:
                        occupied = True
                        break
                # If spot is free, move there
                if not occupied:
                    moves.append(m)
                    pos[m.unit] = moved_pos
        i += 1
    return moves


def get_moved_pos(pos, dir):
    x, y = pos
    if dir == 'DOWN':
        return (x, y + 1)
    elif dir == 'UP':
        return (x, y - 1)
    elif dir == 'RIGHT':
        return (x + 1, y)
    elif dir == 'LEFT':
        return (x - 1, y)


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
        self.map.set_tile(coord[0], coord[1], 'X')
        self.map.set_tile(pos[0], pos[1], ' ')

    def construct_resource_mapping(self):
        # Construct a resource mapping, where the first is the assigned worker and second
        # is the assigned guard
        self.resource_mapping = {}
        all_resources = self.map.find_all_resources()
        for r in all_resources:
            self.resource_mapping[r] = [None, None]

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
                if (self.resource_mapping[loc])[1] is not None:
                    continue
                # Go towards this resource and guard it
                pos = self.get_melee_resource_pos(unit, loc)
                if pos:
                    (self.resource_mapping[loc])[1] = unit
                    # Mark the new pos as a wall
                    self.mark_moved(unit.position(), unit.direction_to(pos))
                    return unit.move_towards(pos)
        return None

    def get_melee_resource_pos(self, unit: Unit, loc: (int, int)):
        """
        Returns the location near this resource to move to
        If there is only one entrance to this resource, then positions near the entrance
        """
        positions = []
        x, y = loc
        perimeter = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for pos in perimeter:
            # If the position is a wall or resource skip
            if self.map.is_wall(pos[0], pos[1]) or self.map.is_resource(pos[0], pos[1]):
                continue
            positions.append(pos)

        # If there is more than one opening around the resource, return furthest found
        if len(positions) >= 1:
            dist = float('-inf')
            opt = None
            for pos in positions:
                path = self.map.bfs(unit.position(), pos)
                if len(path) - 1 > dist:
                    dist = len(path) - 1
                    opt = path[1]

            return (opt, dist)

        # If only one opening around the resource, return a position around this position
        elif len(positions) == 1:
            return self.get_melee_resource_pos(unit, positions[0])

        # If no valid positions return None
        return None

    def get_all_melee_moves(self, melees: [Unit], enemy_units: Units,
                             resources: int, turns_left: int) -> [Move]:
        moves = []
        crs = {}
        positions = {}
        for unit in melees:
            can_attack = unit.can_attack(enemy_units)
            if can_attack:
                for enemy in can_attack:
                    # If enemy is already being attacked then skip
                    if enemy in self.attacking:
                        continue
                    # Attack this enemy
                    self.attacking[enemy] = unit
                    # Attack with this unit towards the enemy's direction
                    moves.append(unit.attack(enemy[1]))
                    break
                continue

            # ADD STUNNING HERE
            # We want to move towards our destination, add this unit to the people we need to path for
            crs[unit] = self.map.closest_resources_all(unit)
            positions[unit.position()] = unit

        # Need to decide which resource to assign each unit.
        # Assign the resource to the unit closest to it.
        # Based on the Stable Marriage Problem
        unassigned = []
        for unit in crs:
            unassigned.append(unit)
        choice = {}
        # start by picking first choice
        for unit in unassigned:
            choice[unit] = 0

        res = self.map.find_all_resources()
        proposal = {}
        for r in crs:
            loc, dist = crs[r]
            if loc not in proposal:
                proposal[loc] = []

        while unassigned:
            for unit in unassigned:
                # propose to their closest resource
                proposal[crs[unit][choice[unit]][0]].append(unit)

            # let resource pick their best worker
            for res in proposal:
                if not proposal[res]:
                    continue
                # If this resource already picked their best worker
                elif self.resource_mapping[res][0] is not None:
                    continue
                # choose best proposal
                dist = float('inf')
                best = None
                for w in proposal[res]:
                    # if this worker is unassigned
                    if w in unassigned:
                        path = self.map.bfs(w.position(), res)
                        if len(path) - 1 < dist:
                            dist = len(path) - 1
                            best = w
                if best:
                    self.resource_mapping[res][0] = best
                    unassigned.remove(best)

            # increment choice count for unassigned units
            for unit in unassigned:
                choice[unit] += 1

        movements = []
        for res in self.resource_mapping:
            unit = self.resource_mapping[res][0]
            if unit:
                pos = self.get_melee_resource_pos(unit, res)
                path = self.map.bfs(unit.position(), pos)
                movements.append(unit.move_towards(path[1]))

        return moves, movements

    def get_all_worker_moves(self, workers: [Unit], enemy_units: Units,
                             resources: int, turns_left: int) -> [Move]:
        moves = []
        crs = {}
        positions = {}
        for unit in workers:
            # If already mining, then skip
            if 'mining_status' in unit.attr and unit.attr['mining_status'] > 0:
                continue
            # If we can mine, then start mining
            elif unit.can_mine(self.map):
                moves.append(unit.mine())
            # We want to move towards our destination, add this unit to the people we need to path for
            crs[unit] = self.map.closest_resources_all(unit)
            positions[unit.position()] = unit

        # Need to decide which resource to assign each unit.
        # Assign the resource to the unit closest to it.
        # Based on the Stable Marriage Problem
        unassigned = []
        for unit in crs:
            unassigned.append(unit)
        choice = {}
        # start by picking first choice
        for unit in unassigned:
            choice[unit] = 0

        res = self.map.find_all_resources()
        proposal = {}
        for r in res:
            proposal[r] = []

        while unassigned:
            for unit in unassigned:
                # propose to their closest resource
                proposal[crs[unit][choice[unit]][0]].append(unit)

            # let resource pick their best worker
            for res in proposal:
                if not proposal[res]:
                    continue
                # If this resource already picked their best worker
                elif self.resource_mapping[res][0] is not None:
                    continue
                # choose best proposal
                dist = float('inf')
                best = None
                for w in proposal[res]:
                    # if this worker is unassigned
                    if w in unassigned:
                        path = self.map.bfs(w.position(), res)
                        if len(path) - 1 < dist:
                            dist = len(path) - 1
                            best = w
                if best:
                    self.resource_mapping[res][0] = best
                    unassigned.remove(best)

            # increment choice count for unassigned units
            for unit in unassigned:
                choice[unit] += 1

        movements = []
        for res in self.resource_mapping:
            unit = self.resource_mapping[res][0]
            if unit:
                path = self.map.bfs(unit.position(), res)
                movements.append(unit.move_towards(path[1]))

        return moves, movements

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
        movements = []
        # construct a modifiable copy of the grid.
        self.map_copy(game_map)

        # assign current num of resources
        self.resources = resources
        self.construct_resource_mapping()

        self.attacking = {}
        self.stunning = {}

        # get all worker units
        workers = your_units.get_all_unit_of_type('worker')

        # get all melee units
        melees = your_units.get_all_unit_of_type('melee')
        """
        # prioritize movement of melees
        for unit in melees:
            move = self.get_melee_move(unit, enemy_units, resources, turns_left)
            if move:
                moves.append(move)
        """
        # move workers
        # for unit in workers:
        #     move = self.get_worker_move(unit, enemy_units, resources, turns_left)
        #     if move:
        #         moves.append(move)
        melee_moves, melee_movements = self.get_all_melee_moves(melees, enemy_units, resources, turns_left)
        worker_moves, worker_movements = self.get_all_worker_moves(workers, enemy_units, resources, turns_left)
        moves.extend(melee_moves)
        moves.extend(worker_moves)
        movements.extend(melee_movements)
        movements.extend(worker_movements)
        moves.extend(optimize_movements(your_units, movements))
        # self.best_moves(moving)
        return moves


"""
# testing
if __name__ == '__main__':
    size = 7
    grid = [['X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', ' ', 'X', 'R', ' ', ' ', 'X'],
            ['X', ' ', 'X', ' ', ' ', ' ', 'X'],
            ['X', ' ', 'X', ' ', ' ', ' ', 'X'],
            ['X', ' ', 'R', ' ', ' ', 'R', 'X'],
            ['X', 'X', 'X', ' ', ' ', ' ', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X']]
    map = Map(grid)
    attr = {'type': 'worker', 'x': 1, 'y': 1, 'id': '0'}
    # unit = Unit(attr)
    # map.set_tile(1, 1, 'w')
    attr1 = {'type': 'worker', 'x': 1, 'y': 2, 'id': '1'}
    # unit1 = Unit(attr1)
    # map.set_tile(1, 3, 'w')

    units = Units([attr, attr1])
    enemy_units = Units([])
    resources = 0
    turns_left = 1
    gp = GridPlayer()
    while turns_left > 0:
        moves = gp.tick(map, units, enemy_units, resources, turns_left)
        for m in moves:
            print(f"{m.unit} + {m.directions}")
        turns_left -= 1
        print(gp.resource_mapping)
"""
