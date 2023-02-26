import json
from utils.generator import Point
from typing import List, Tuple

class FileHandler():

    @staticmethod
    def save_points_to_file(points : List[Point], name : str):
        jsonString = json.dumps([(p.x, p.y) for p in points])
        with open(name, 'w') as f:
            f.write(jsonString)

    @staticmethod
    def get_saved_points(name : str) -> List[Point]:
        with open(name, 'r') as f:
            jsonContent = f.read()
        points = json.loads(jsonContent)
        points = [Point(p[0], p[1]) for p in points]
        return points