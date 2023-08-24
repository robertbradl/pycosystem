import csv
import sys
from settings import *
from queue import PriorityQueue


class Astar:

    # calculates the manhatten distance of 2 coordinates
    def __manhatten_distance__(self, p1: tuple, p2: tuple) -> int:
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]

        return abs(x1 - x2) + abs(y1 - y2)

    # returns a list of all valid neighbors of the current coordinate
    def __get_neighbors__(self, p: tuple, end: tuple, map: list) -> list:
        up = (p[0], p[1]-1)
        right = (p[0]+1, p[1])
        down = (p[0], p[1]+1)
        left = (p[0]-1, p[1])

        neighbors = []

        if p[1] != 0:
            if map[up[1]][up[0]] != 5.0 or up == end:
                neighbors.append(up)
        if p[0] != 199:
            if map[right[1]][right[0]] != 5.0 or right == end:
                neighbors.append(right)
        if p[1] != 199:
            if map[down[1]][down[0]] != 5.0 or down == end:
                neighbors.append(down)
        if p[0] != 0:
            if map[left[1]][left[0]] != 5.0 or left == end:
                neighbors.append(left)

        return neighbors

    # constructs and returns the complete path
    def __reconstruct_path__(self, came_from: dict, current: tuple) -> list:
        retlist = []
        endpoint = current
        while current in came_from:
            current = came_from[current]
            retlist.append(current)

        retlist.reverse()
        retlist.pop(0)
        retlist.append(endpoint)

        return retlist

    # the actual a* algorithm
    def find_path(self, grid: list, start: tuple, end: tuple) -> list:
        if start == end:
            return [end]

        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))

        came_from = {}

        score_g = {
            tuple((col_index, row_index)): float("inf") for row_index, row in enumerate(grid) for col_index, col in enumerate(row)
        }
        score_g[start] = 0

        score_f = {
            tuple((col_index, row_index)): float("inf") for row_index, row in enumerate(grid) for col_index, col in enumerate(row)
        }
        score_f[start] = self.__manhatten_distance__(start, end)

        open_set_hash = {start}

        while not open_set.empty():

            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == end:
                return self.__reconstruct_path__(came_from, end)

            for neighbor in self.__get_neighbors__(current, end, grid):
                score_g_temp = score_g[current] + 1

                if score_g_temp < score_g[neighbor]:
                    came_from[neighbor] = current
                    score_g[neighbor] = score_g_temp
                    score_f[neighbor] = score_g_temp + \
                        self.__manhatten_distance__(neighbor, end)

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((score_f[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)

        return []

    # just a template function to ensure that the find_path fucntion is working correctly
    def __template__(self):
        map = []
        with open("World/map.csv") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                map.append(row)

        try:
            p1 = tuple((int(sys.argv[1]), int(sys.argv[2])))
            p2 = tuple((int(sys.argv[3]), int(sys.argv[4])))
        except:
            p1 = (0, 0)
            p2 = (11, 9)

        path = self.find_path(map, p1, p2)

        print(path)


if __name__ == "__main__":
    astar = Astar()
    astar.__template__()
