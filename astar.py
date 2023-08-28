import csv
import sys
from settings import *
from queue import PriorityQueue


def __manhatten_distance__(p1: tuple, p2: tuple) -> int:
    """Calculates the manhatten distance between two points.

    Args:
        p1 (tuple): Point 1
        p2 (tuple): Point 2

    Returns:
        int: calculated manhatten distance
    """
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    return abs(x1 - x2) + abs(y1 - y2)

def __get_neighbors__(p: tuple, end: tuple, map: list) -> list:
    """Returns all adjacent tiles from a point which can be moved on. For this the function checks the map array if the entry to the corresponding tile is a valid move destination. (i.e. not water)

    Args:
        p (tuple): point to check for neighboring tiles from
        end (tuple): end point of the A* algorithm
        map (list): the stored map

    Returns:
        list: contains all valid neighboring tiles
    """
    up = (p[0], p[1] - 1)
    right = (p[0] + 1, p[1])
    down = (p[0], p[1] + 1)
    left = (p[0] - 1, p[1])

    neighbors = []

    if p[1] != 0 and (map[up[1]][up[0]] != 5.0 or up == end):
        neighbors.append(up)
    if p[0] != 199 and (map[right[1]][right[0]] != 5.0 or right == end):
        neighbors.append(right)
    if p[1] != 199 and (map[down[1]][down[0]] != 5.0 or down == end):
        neighbors.append(down)
    if p[0] != 0 and (map[left[1]][left[0]] != 5.0 or left == end):
        neighbors.append(left)

    return neighbors

def __reconstruct_path__(came_from: dict, current: tuple) -> list:
    """Retraces the steps of the A* algorithm and constructs the path taken to the end point.

    Args:
        came_from (dict): dictionary containing tiles and the position from which they got accessed/moved on
        current (tuple): the current position

    Returns:
        list: the reconstructed path
    """
    retlist = []
    endpoint = current
    while current in came_from:
        current = came_from[current]
        retlist.append(current)

    retlist.reverse()
    retlist.pop(0)
    retlist.append(endpoint)

    return retlist

def find_path(grid: list, start: tuple, end: tuple) -> list:
    """A* algorithm to find a path in a 2D grid

    Args:
        grid (list): the map
        start (tuple): start point
        end (tuple): end point

    Returns:
        list: path containing the path, if none was found an empty one is returned
    """
    if start == end:
        return [end]

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}

    score_g = {
        (col_index, row_index): float("inf")
        for row_index, row in enumerate(grid)
        for col_index, x in enumerate(row)
    }
    score_g[start] = 0

    score_f = {
        (col_index, row_index): float("inf")
        for row_index, row in enumerate(grid)
        for col_index, x in enumerate(row)
    }
    score_f[start] = __manhatten_distance__(start, end)

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            return __reconstruct_path__(came_from, end)

        for neighbor in __get_neighbors__(current, end, grid):
            score_g_temp = score_g[current] + 1

            if score_g_temp < score_g[neighbor]:
                came_from[neighbor] = current
                score_g[neighbor] = score_g_temp
                score_f[neighbor] = score_g_temp + __manhatten_distance__(
                    neighbor, end
                )

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((score_f[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return []

def __test__():
    """Test function to test the algorithm directly from the file."""
    map_array = []
    with open("World/map.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        map_array.extend(iter(reader))
    try:
        p1 = (int(sys.argv[1]), int(sys.argv[2]))
        p2 = (int(sys.argv[3]), int(sys.argv[4]))
    except Exception:
        p1 = (0, 0)
        p2 = (11, 9)

    path = find_path(map_array, p1, p2)

    print(path)


if __name__ == "__main__":
    __test__()
