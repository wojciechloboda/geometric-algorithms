from utils.geometry import EPS as eps
from utils.drawing import PointsCollection
from utils.drawing import LinesCollection
from utils.drawing import Scene
from utils.geometry import Rect, Point
from typing import List, Tuple

class KDtree:
    class Region:
        def __init__(self, lower_left, upper_right):
            self.lower_left = lower_left
            self.upper_right = upper_right

    class Node:
        def __init__(self, point_idx):
            self.point_idx = point_idx
            self.left = None
            self.right = None
            self.region = None
            self.subtree_nodes = []

    def __init__(self, P:List[Point]):
        P=[tuple(p) for p in P]
        self.P = P
        self.points_indices = [i for i in range(len(P))]
        x_sorted = sorted(self.points_indices, key = lambda x : P[x][0])
        y_sorted = sorted(self.points_indices, key = lambda x : P[x][1])
        self.head = self._build_tree(x_sorted, y_sorted, 0)

    @staticmethod
    def _median(T):
        idx = ((len(T) - 1) // 2)
        return T[idx]

    @staticmethod
    def _find_region_lower_left(P, p_ind):
        x = min([P[i][0] for i in p_ind])
        y = min([P[i][1] for i in p_ind])
        return (x, y)

    @staticmethod
    def _find_region_upper_right(P, p_ind):
        x = max([P[i][0] for i in p_ind])
        y = max([P[i][1] for i in p_ind])
        return(x, y)

    def _build_tree(self, x_sorted, y_sorted, depth):
        if len(x_sorted) == 0:
            return None
        if len(x_sorted) == 1:
            new_node =  self.Node(x_sorted[0])
            new_node.subtree_nodes = [x for x in x_sorted]
            new_node.region = self.Region(self.P[x_sorted[0]], self.P[x_sorted[0]])
            return new_node

        dim = depth % 2
        if dim == 0:
            mid_idx = KDtree._median(x_sorted)
        else:
            mid_idx = KDtree._median(y_sorted)
        
        x1_sorted = [p for p in x_sorted if self.P[p][dim] < self.P[mid_idx][dim] + eps]
        x2_sorted = [p for p in x_sorted if self.P[p][dim] > self.P[mid_idx][dim]]
        y1_sorted = [p for p in y_sorted if self.P[p][dim] < self.P[mid_idx][dim] + eps]
        y2_sorted = [p for p in y_sorted if self.P[p][dim] > self.P[mid_idx][dim]]
        
        new_node = self.Node(mid_idx)
        new_node.subtree_nodes = [x for x in x_sorted]
        region = self.Region(KDtree._find_region_lower_left(self.P, x_sorted), KDtree._find_region_upper_right(self.P, x_sorted))
        new_node.region = region

        new_node.left = self._build_tree(x1_sorted, y1_sorted, depth + 1)
        new_node.right = self._build_tree(x2_sorted, y2_sorted, depth + 1)
        return new_node

    @staticmethod
    def visualize_build(points : List[Point]) -> List[Scene]:
        P=[tuple(p) for p in points]
        points_indices = [i for i in range(len(P))]
        x_sorted = sorted(points_indices, key = lambda x : P[x][0])
        y_sorted = sorted(points_indices, key = lambda x : P[x][1])

        min_x = min([P[i][0] for i in range(len(P))])
        min_y = min([P[i][1] for i in range(len(P))])
        max_x = max([P[i][0] for i in range(len(P))])
        max_y = max([P[i][1] for i in range(len(P))])
        bounds_lines = []
        scenes = []
        def _build_tree_vis(x_sorted, y_sorted, depth, bounds):
            if len(x_sorted) == 0:
                scenes.append(
                Scene(points = \
                                [PointsCollection(P)],
                        lines = \
                            [LinesCollection([l for l in bounds_lines])],
                        rects = [Rect(bounds[0], bounds[2])])
            )
                return None
            if len(x_sorted) == 1:
                return KDtree.Node(x_sorted[0])
            
            dim = depth % 2

            bounds_a = [b for b in bounds]
            bounds_b = [b for b in bounds]
            new_line = []
            
            if dim == 0:
                mid_idx = KDtree._median(x_sorted)
                bounds_a[1] = (P[mid_idx][0], bounds[1][1])
                bounds_a[2] = (P[mid_idx][0], bounds[2][1])
                bounds_b[0] = (P[mid_idx][0], bounds[1][1])
                bounds_b[3] = (P[mid_idx][0], bounds[2][1])
                new_line = [bounds_a[1], bounds_a[2]]
            else:
                mid_idx = KDtree._median(y_sorted)
                bounds_b[0] = (bounds[0][0], P[mid_idx][1])
                bounds_b[1] = (bounds[1][0], P[mid_idx][1])
                bounds_a[2] = (bounds[2][0], P[mid_idx][1])
                bounds_b[3] = (bounds[3][0], P[mid_idx][1])
                new_line = [bounds_b[0], bounds_b[1]]

            bounds_lines.append(new_line)
            
            x1_sorted = [p for p in x_sorted if P[p][dim] < P[mid_idx][dim] + eps]
            x2_sorted = [p for p in x_sorted if P[p][dim] > P[mid_idx][dim]]
            y1_sorted = [p for p in y_sorted if P[p][dim] < P[mid_idx][dim] + eps]
            y2_sorted = [p for p in y_sorted if P[p][dim] > P[mid_idx][dim]]
            
            new_node = KDtree.Node(mid_idx)
            new_node.lower_left = KDtree._find_region_lower_left(P, x_sorted)
            new_node.upper_right = KDtree._find_region_upper_right(P, x_sorted)

            scenes.append(
                Scene(points = \
                                [PointsCollection(P)] + \
                                [PointsCollection([P[mid_idx]], color = 'red')],
                        lines = \
                            [LinesCollection([l for l in bounds_lines])],
                        rects = [Rect(bounds[0], bounds[2])])
            )

            new_node.left = _build_tree_vis(x1_sorted, y1_sorted, depth + 1, bounds_a)
            new_node.right = _build_tree_vis(x2_sorted, y2_sorted, depth + 1, bounds_b)
            return new_node

        bounds = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
        bounds_lines = [[bounds[0], bounds[1]], [bounds[1], bounds[2]], [bounds[2], bounds[3]], [bounds[3], bounds[0]]]
        head = _build_tree_vis(x_sorted, y_sorted, 0, bounds)
        return scenes

    def _intersect(self, p1, p2):
        r1 = Rect(p1.lower_left, p1.upper_right)
        r2 = Rect(p2.lower_left, p2.upper_right)
        return r1.intersects(r2)
            
    def _contains(self, p1, p2):
        r1 = Rect(p1.lower_left, p1.upper_right)
        r2 = Rect(p2.lower_left, p2.upper_right)
        return r1.contains_rectangle(r2)

    def querry_range(self, rect: Rect) -> List[Point]:
        x1 = rect.lower_left.x
        x2 = rect.upper_right.x
        y1 = rect.lower_left.y
        y2 = rect.upper_right.y

        def _query(r, head):
            if head.left == None and head.right == None:
                return []
            
            res = []
            if head.left != None:
                if self._contains(r, head.left.region):
                    res += head.left.subtree_nodes
                elif self._intersect(r, head.left.region):
                    res += _query(r, head.left)
            if head.right != None:
                if self._contains(r, head.right.region):
                    res += head.right.subtree_nodes
                elif self._intersect(r, head.right.region):
                    res += _query(r, head.right)
            return res

        r_lower_left = (min(x1, x2), min(y1, y2))
        r_upper_right = (max(x1, x2), max(y1, y2))
        r = self.Region(r_lower_left, r_upper_right)
        res = _query(r, self.head)

        return [Point(self.P[idx][0], self.P[idx][1]) for idx in res]

    def _get_bound_lines(self, head):
        p1 = head.region.lower_left
        p2 = (head.region.upper_right[0], head.region.lower_left[1])
        p3 = head.region.upper_right
        p4 = (head.region.lower_left[0], head.region.upper_right[1])

        return [[p1, p2], [p2, p3], [p3, p4], [p4, p1]]

    def _vis_querry(self, rect: Rect):
        x1 = rect.lower_left.x
        x2 = rect.upper_right.x
        y1 = rect.lower_left.y
        y2 = rect.upper_right.y
        scenes = []
        scenes.append(Scene(points = [PointsCollection(self.P)], rects=[rect]))
        self.inside = []

        def _query(r, head):
            if head.left == None and head.right == None:
                return []

            scenes.append(Scene(
                        points = [PointsCollection(self.P), PointsCollection([p for p in self.inside], color = 'red')],
                        lines = [LinesCollection(self._get_bound_lines(head))], 
                        rects=[rect]))
            
            res = []
            if head.left != None:
                if self._contains(r, head.left.region):
                    res += head.left.subtree_nodes
                    self.inside += [self.P[idx] for idx in head.left.subtree_nodes]
                    scenes.append(Scene(
                        points = [PointsCollection(self.P), PointsCollection([p for p in self.inside], color = 'red')],
                        lines = [LinesCollection(self._get_bound_lines(head.left))], 
                        rects=[rect]))

                elif self._intersect(r, head.left.region):
                    res += _query(r, head.left)
            if head.right != None:
                if self._contains(r, head.right.region):
                    res += head.right.subtree_nodes
                    self.inside += [self.P[idx] for idx in head.right.subtree_nodes]
                    scenes.append(Scene(
                        points = [PointsCollection(self.P), PointsCollection([p for p in self.inside], color = 'red')], 
                        lines = [LinesCollection(self._get_bound_lines(head.right))],
                        rects=[rect]))
                elif self._intersect(r, head.right.region):
                    res += _query(r, head.right)
            return res

        r_lower_left = (min(x1, x2), min(y1, y2))
        r_upper_right = (max(x1, x2), max(y1, y2))
        r = self.Region(r_lower_left, r_upper_right)
        res = _query(r, self.head)
        scenes.append(Scene(
                        points = [PointsCollection(self.P), PointsCollection([p for p in self.inside], color = 'red')], 
                        rects=[rect]))
        return scenes

    
    @staticmethod
    def visualize_querry(points: List[Point], rect: Rect) -> List[Scene]:
        tree = KDtree(points)
        scenes = tree._vis_querry(rect)
        return scenes



