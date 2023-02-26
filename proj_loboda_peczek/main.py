import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from utils.generator import Generator as gen
from quad_tree import QuadTree
from utils.geometry import Point, Rect
from utils.visualizer import Visualizer
from KDtree import KDtree

from utils.files import FileHandler


def main():
    points = gen.normal_distribution(Rect((0.0, 0.0), (1.0, 1.0)), 5)
    #points = gen.on_rectangle(Rect((0.0, 0.0), (1.0, 1.0)), 100)
    #points = gen.rectangle_outliers(Rect((-1.0, -1.0), (1.0, 1.0)), 100)
    #points = gen.generate_grid(Rect((0.0, 0.0), (1.0, 1.0)), 100)
    #points = gen.generate_cross(Rect((0.0, 0.0), (1.0, 1.0)), 100)
    #points = gen.generate_circle(Point(0.0, 0.0), 100, 100)

    #Visualizer.visualize_build(points, QuadTree)
    Visualizer.visualize_result(points, Rect(
        (0.25, 0.25), (0.75, 0.75)), QuadTree)


    #FileHandler.save_points_to_file(points, "test.json")
    #points = FileHandler.get_saved_points("test.json")
if __name__ == "__main__":
    main()
