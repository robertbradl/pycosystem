import itertools
import numpy as np
import random as rnd
import matplotlib.pyplot as plt


def __perlin__(x: np.ndarray, y: np.ndarray, seed: int = 0) -> list:
    """Generates Perlin noise for given x and y coordinates.

    Args:
        x (numpy.ndarray): The x coordinates.
        y (numpy.ndarray): The y coordinates.
        seed (int, optional): The random seed. Defaults to 0.

    Returns:
        list: The generated Perlin noise values.
    """
    np.random.seed(seed)
    p = np.arange(256, dtype=int)  # permutation array
    np.random.shuffle(p)  # shuffle shuffle permutations
    p = np.stack(
        [p, p]
    ).flatten()  # 2d array turned 1d for easy dot product interpolations

    xi, yi = x.astype(int), y.astype(int)  # grid coords
    xf, yf = x - xi, y - yi  # distance vector coords

    u, v = __fade__(xf), __fade__(yf)  # fade function

    # gradient vector coordinates top left, top right, bottom left, bottom right
    n00 = __gradient__(p[p[xi] + yi], xf, yf)
    n01 = __gradient__(p[p[xi] + yi + 1], xf, yf - 1)
    n11 = __gradient__(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    n10 = __gradient__(p[p[xi + 1] + yi], xf - 1, yf)

    # linear interpolation
    x1 = __lerp__(n00, n10, u)
    x2 = __lerp__(n01, n11, u)
    return __lerp__(x1, x2, v)


def __lerp__(a: float, b: float, x: float) -> float:
    """Linear interpolation.

    Args:
        a (float): The start value.
        b (float): The end value.
        x (float): The interpolation factor.

    Returns:
        float: The interpolated value.
    """
    return a + x * (b - a)


def __fade__(t: float) -> float:
    """Calculates the fade value for Perlin noise.

    Args:
        t (float): The input value.

    Returns:
        float: The calculated fade value.
    """
    return 6 * t**5 - 15 * t**4 + 10 * t**3


def __gradient__(h: int, x: float, y: float):
    """Calculates the gradient vectors and the dot product.

    Args:
        h (int): The hash value.
        x (float): The x coordinate.
        y (float): The y coordinate.
    """
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y


def generate_plot() -> list:
    """Generates a plot of Perlin noise.

    Returns:
        list: The generated plot.
    """
    p = np.zeros((50, 50))
    for i in range(4):
        freq = 2**i
        lin = np.linspace(0, freq, 50, endpoint=False)
        x, y = np.meshgrid(lin, lin)
        seed = rnd.randint(0, 999999999)
        p = __perlin__(x, y, seed=seed) / freq + p

    return p


def generate_map() -> list:
    """Generates a map using Perlin noise.

    Returns:
        list: The generated map.
    """
    p = generate_plot()
    randmap = np.zeros((50, 50))
    land_tiles = []
    for y, x in itertools.product(range(50), range(50)):
        if -0.05 < p[y][x] < 0.4:
            randmap[y][x] = 2.0
            land_tiles.append((y, x))
        else:
            randmap[y][x] = 5.0
    b_needed = int(len(land_tiles) * 0.03)
    h_needed = int(len(land_tiles) * 0.04)
    c_needed = int(len(land_tiles) * 0.02)
    o_needed = int(len(land_tiles) * 0.01)
    for _ in range(b_needed):
        coord = rnd.choice(land_tiles)
        land_tiles.remove(coord)
        randmap[coord[0]][coord[1]] = 0.0

    for _ in range(h_needed):
        coord = rnd.choice(land_tiles)
        land_tiles.remove(coord)
        randmap[coord[0]][coord[1]] = 3.0

    for _ in range(c_needed):
        coord = rnd.choice(land_tiles)
        land_tiles.remove(coord)
        randmap[coord[0]][coord[1]] = 1.0

    for _ in range(o_needed):
        coord = rnd.choice(land_tiles)
        land_tiles.remove(coord)
        randmap[coord[0]][coord[1]] = 4.0

    return randmap


def main() -> None:
    """Main function to generate and display a plot of Perlin noise."""
    p = generate_plot()
    plt.imshow(p, origin="upper")
    plt.show()


if __name__ == "__main__":
    main()
