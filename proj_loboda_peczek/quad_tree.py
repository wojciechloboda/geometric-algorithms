from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from utils.drawing import LinesCollection, PointsCollection, Scene
from utils.geometry import Point, Rect


class QuadTree():
    CAPACITY = 1  # Arbitrary constant to indicate how many elements can be stored in this quad tree node

    def __init__(self, bounding_box: Rect) -> 'QuadTree':
        self.bounding_box = bounding_box
        self.points: List[Point] = []

        self.upper_right: QuadTree = None
        self.upper_left: QuadTree = None
        self.lower_right: QuadTree = None
        self.lower_left: QuadTree = None

    def _visualize_tree(self, color: str) -> LinesCollection:
        def get_bounds(tree: QuadTree) -> List[Rect]:
            if tree.upper_right == None:
                return [tree.bounding_box.get_polyline()]
            return get_bounds(tree.lower_left) + get_bounds(tree.lower_right) + get_bounds(tree.upper_left) + get_bounds(tree.upper_right)
        return LinesCollection(lines=get_bounds(self), color=color)

    @staticmethod
    def visualize_build(points: List[Point]) -> List[Scene]:
        tree = QuadTree(Rect.find_bounding_box(points))
        scenes: List[Scene] = []
        for i, point in enumerate(points):
            lines_visualization: LinesCollection = tree._visualize_tree(
                "blue")
            tree._visualize_insert(
                points, i, scenes, lines_visualization)
        return scenes

    def _visualize_insert(self, points: List[Point], i: int, scenes: List[Scene], lines_vis: LinesCollection):
        previous = points[:i]
        future = points[i+1:] if i < len(points) else []
        point = points[i]

        lower_left = self.bounding_box.lower_left
        upper_right = self.bounding_box.upper_right

        if not self.bounding_box.contains_point(point):
            return False

        scenes.append(Scene(
            points=[
                PointsCollection([tuple(p) for p in previous], color="green"),
                PointsCollection([tuple(point)], color="red"),
                PointsCollection([tuple(p) for p in future], color="orange"),
            ],
            lines=[
                lines_vis,
            ],
            rects=[
                self.bounding_box
            ]
        ))

        if len(self.points) < QuadTree.CAPACITY and self.upper_right == None:
            self.points.append(point)
            return True
        if self.upper_right == None:
            self._subdivide()

        if self.upper_right._visualize_insert(points, i, scenes, lines_vis):
            return True
        if self.upper_left._visualize_insert(points, i, scenes, lines_vis):
            return True
        if self.lower_right._visualize_insert(points, i, scenes, lines_vis):
            return True
        if self.lower_left._visualize_insert(points, i, scenes, lines_vis):
            return True

        raise RuntimeError("Failed when inserting {}".format(point))

    def insert(self, point: Point):
        if not self.bounding_box.contains_point(point):
            return False
        if len(self.points) < QuadTree.CAPACITY and self.upper_right == None:
            self.points.append(point)
            return True
        if self.upper_right == None:
            self._subdivide()

        if self.upper_right.insert(point):
            return True
        if self.upper_left.insert(point):
            return True
        if self.lower_right.insert(point):
            return True
        if self.lower_left.insert(point):
            return True

        raise RuntimeError("Failed when inserting {}".format(point))

    @staticmethod
    def visualize_querry(points: List[Point], rect: Rect) -> List[Scene]:
        tree = QuadTree(Rect.find_bounding_box(points))
        for p in points:
            tree.insert(p)
        scenes: List[Scene] = []
        solution: List[Point] = []
        tree._visualize_querry(rect, scenes, solution, points,
                               tree._visualize_tree("blue"))
        return scenes

    def _visualize_querry(self, rect: Rect, scenes: List[Scene], solution: List[Point], all_points: List[Point], line_vis: LinesCollection) -> List[Point]:

        if not rect.intersects(self.bounding_box):
            scenes.append(Scene(
                points=[
                    PointsCollection(points=[tuple(p)
                                     for p in all_points], color='blue'),
                    PointsCollection(points=[tuple(p)
                                             for p in solution], color='red'),
                ],
                lines=[
                    line_vis,
                    LinesCollection(lines=[[
                        tuple(self.bounding_box.lower_left),
                        tuple(self.bounding_box.upper_right)]],
                        color='red')],
                rects=[rect, self.bounding_box]
            ))
            return []

        result: List[Point] = list(
            filter(lambda point: rect.contains_point(point), self.points))

        solution += result

        if self.upper_right == None:
            scenes.append(Scene(
                points=[
                    PointsCollection(points=[tuple(p)
                                     for p in all_points], color='blue'),
                    PointsCollection(points=[tuple(p)
                                     for p in solution], color='red')
                ],
                lines=[
                    line_vis,
                    LinesCollection(
                        lines=[self.bounding_box.get_polyline()], color='red')
                ],
                rects=[rect]
            ))
            return result

        scenes.append(Scene(
            points=[
                PointsCollection(points=[tuple(p)
                                         for p in all_points], color='blue'),
                PointsCollection(points=[tuple(p)
                                         for p in solution], color='red')
            ],
            lines=[
                line_vis,
                LinesCollection(
                    lines=[self.bounding_box.get_polyline()], color='red')
            ],
            rects=[rect]
        ))

        result.extend(self.upper_right._visualize_querry(
            rect, scenes, solution, all_points, line_vis))
        result.extend(self.upper_left._visualize_querry(
            rect, scenes, solution, all_points, line_vis))
        result.extend(self.lower_right._visualize_querry(
            rect, scenes, solution, all_points, line_vis))
        result.extend(self.lower_left._visualize_querry(
            rect, scenes, solution, all_points, line_vis))
        return result

    def querry_range(self, rect: Rect) -> List[Point]:
        if not rect.intersects(self.bounding_box):
            return []

        result: List[Point] = list(
            filter(lambda point: rect.contains_point(point), self.points))
        if self.upper_right == None:
            return result

        result.extend(self.upper_right.querry_range(rect))
        result.extend(self.upper_left.querry_range(rect))
        result.extend(self.lower_right.querry_range(rect))
        result.extend(self.lower_left.querry_range(rect))
        return result

    def _subdivide(self):
        left, right = self.bounding_box.divide_vertically()
        up_left, down_left = left.divide_horizontally()
        up_right, down_right = right.divide_horizontally()

        self.upper_right = QuadTree(up_right)
        self.upper_left = QuadTree(up_left)
        self.lower_right = QuadTree(down_right)
        self.lower_left = QuadTree(down_left)
