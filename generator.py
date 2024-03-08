import itertools
import numpy as np
import random as rnd
import matplotlib.pyplot as plt


def __perlin__(x, y, seed=0) -> float:

    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()

    xi, yi = x.astype(int), y.astype(int)
    xf, yf = x - xi, y - yi

    u, v = __fade__(xf), __fade__(yf)

    n00 = __gradient__(p[p[xi] + yi], xf, yf)
    n01 = __gradient__(p[p[xi] + yi + 1], xf, yf - 1)
    n11 = __gradient__(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    n10 = __gradient__(p[p[xi + 1] + yi], xf - 1, yf)

    x1 = __lerp__(n00, n10, u)
    x2 = __lerp__(n01, n11, u)
    return __lerp__(x1, x2, v)


def __lerp__(a, b, x) -> float:
    """linear interpolation"""
    return a + x * (b - a)


def __fade__(t) -> float:
    """6t^5 - 15t^4 + 10t^3"""
    return 6 * t**5 - 15 * t**4 + 10 * t**3


def __gradient__(h, x, y):
    """grad converts h to the right gradient vector and return the dot product with (x,y)"""
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y


def generate_plot() -> list:
    p = np.zeros((50, 50))
    for i in range(4):
        freq = 2**i
        lin = np.linspace(0, freq, 50, endpoint=False)
        x, y = np.meshgrid(lin, lin)
        seed = rnd.randint(0, 999999999)
        p = __perlin__(x, y, seed=seed) / freq + p

    return p


def generate_map() -> list:
    p = generate_plot()
    randmap = np.zeros((50, 50))
    for y, x in itertools.product(range(50), range(50)):
        randmap[x][y] = 2.0 if -0.05 < p[x][y] < 0.4 else 5.0

    return randmap


def main() -> None:
    p = generate_plot()
    plt.imshow(p, origin="upper")
    plt.show()


if __name__ == "__main__":
    main()
