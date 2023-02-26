from typing import List, Tuple

from utils.drawing import LinesCollection, Plot, PointsCollection, Scene
from utils.geometry import Point, Rect


class Visualizer():
    @staticmethod
    def visualize_points(points: List[Point]):
        plot = Plot(scenes=[
            Scene(points=[PointsCollection(points=[tuple(p) for p in points])])
        ])
        plot.draw()

    @staticmethod
    def visualize_build(points: List[Point], tree):
        scenes: List[Scene] = tree.visualize_build(points)
        plot = Plot(scenes=scenes)
        plot.draw()

    @staticmethod
    def visualize_result(points: List[Point], rect: Rect, tree):
        scenes = tree.visualize_querry(points, rect)
        plot = Plot(scenes=scenes)
        plot.draw()
