import math
from itertools import combinations
from typing import Tuple

import pytmx

from project.utils import Dimensions, Point


class Triangle:
    def __init__(self, obj: pytmx.TiledObject):
        self.origin = Point(obj.x, obj.y)
        self.size = Dimensions(obj.width, obj.height)
        self.points = tuple(Point(*p) for p in obj.points)
        self.hypotenuse = self._get_hypotenuse()
        self.slope = self._get_slope(self.hypotenuse)

    @property
    def x(self) -> float:
        return self.origin.x

    @property
    def y(self) -> float:
        return self.origin.y

    @property
    def width(self) -> int:
        return self.size.width

    @property
    def height(self) -> int:
        return self.size.height

    def slope_intercept(self, x: float) -> float:
        """For a given x, calculates the y position on the slope."""
        b = self.origin.y if self.slope < 0 else self.origin.y - self.size.height  # y-intercept
        return self.slope * x + b  # y = mx + b

    def _get_hypotenuse(self) -> Tuple[Point, Point]:
        combs = combinations(self.points, 2)
        points = max(combs, key=self._calc_distance)  # Finds the longest side
        return tuple(sorted(points, key=lambda p: p[0]))  # Sort by x

    @staticmethod
    def _get_slope(line: Tuple[Point, Point]) -> float:
        a, b = line
        return (b.y - a.y) / (b.x - a.x)  # (y2 - y1) / (x2 - x2)

    @staticmethod
    def _calc_distance(points: Tuple[Point, Point]) -> float:
        """Calculates the distance between two points."""
        a, b = points
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
