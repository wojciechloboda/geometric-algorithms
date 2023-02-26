from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

EPS = 10 ** -12


class Point():
    def __init__(self, x: float, y: float) -> 'Point':
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return (self.x - EPS <= other.x <= self.x + EPS and self.y - EPS <= other.y <= self.y + EPS)

    def __str__(self) -> str:
        return "{}, {}".format(self.x, self.y)

    def __repr__(self) -> str:
        return self.__str__()

    def follows(self, other: 'Point') -> bool:
        return self.x > other.x - EPS and self.y > other.y - EPS

    def precedes(self, other: 'Point') -> bool:
        return self.x < other.x + EPS and self.y < other.y + EPS

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, key: int):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("No coordinate at index {}".format(key))


class Rect():
    def __init__(self, lower_left: Tuple[float, float], upper_right: Tuple[float, float]) -> 'Rect':
        self.lower_left = Point(*lower_left)
        self.upper_right = Point(*upper_right)

        # if not self.lower_left.precedes(self.upper_right):
        #  raise ValueError('Lower-left point must precede the upper-right')

    def __eq__(self, other: 'Rect') -> bool:
        return self.lower_left == other.lower_left and self.upper_right == other.upper_right

    def __str__(self) -> str:
        return "{} - {}".format(self.lower_left, self.upper_right)

    def __repr__(self):
        return self.__str__()

    def intersects(self, other: 'Rect') -> bool:
        return self.lower_left.precedes(other.upper_right) and other.lower_left.precedes(self.upper_right)

    # Type of point is left intentionally ambiguous
    def contains_point(self, point: Point) -> bool:
        return self.lower_left.precedes(point) and self.upper_right.follows(point)

    def contains_rectangle(self, rect: 'Rect') -> bool:
        return self.lower_left.precedes(rect.lower_left) and self.upper_right.follows(rect.upper_right)

    def divide_vertically(self) -> Tuple['Rect', 'Rect']:
        midpoint = (self.lower_left.x + self.upper_right.x) / 2
        left = Rect((self.lower_left.x, self.lower_left.y),
                    (midpoint, self.upper_right.y))
        right = Rect((midpoint, self.lower_left.y),
                     (self.upper_right.x, self.upper_right.y))
        return left, right

    def divide_horizontally(self) -> Tuple['Rect', 'Rect']:
        midpoint = ((self.lower_left.y + self.upper_right.y) / 2)
        up = Rect((self.lower_left.x, midpoint),
                  (self.upper_right.x, self.upper_right.y))
        down = Rect((self.lower_left.x, self.lower_left.y),
                    (self.upper_right.x, midpoint))
        return up, down

    @staticmethod
    def find_bounding_box(points: List['Point']) -> 'Rect':
        low_x = points[0].x
        low_y = points[0].y
        high_x = points[0].x
        high_y = points[0].y

        for point in points:
            if point.x < low_x:
                low_x = point.x
            if point.y < low_y:
                low_y = point.y
            if point.x > high_x:
                high_x = point.x
            if point.y > high_y:
                high_y = point.y
        return Rect((low_x, low_y), (high_x, high_y))

    def get_polyline(self: 'Rect') -> List[Tuple[float, float]]:
        return [tuple(self.lower_left),
                (self.upper_right.x, self.lower_left.y),
                tuple(self.upper_right),
                (self.lower_left.x, self.upper_right.y),
                tuple(self.lower_left)]
