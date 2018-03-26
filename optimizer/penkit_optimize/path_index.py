import rtree


class PathIndex:
    def __init__(self, path_graph):
        self.idx = rtree.index.Index()
        self.path_graph = path_graph
        for index, coordinate in path_graph.iter_starts_with_index():
            self.idx.add(index, coordinate + coordinate)

    def get_nearest(self, coordinate):
        return next(self.idx.nearest(coordinate))

    def delete(self, index):
        coordinate = self.path_graph.get_coordinates(index)
        self.idx.delete(index, coordinate + coordinate)

    def delete_pair(self, index):
        self.delete(index)
        self.delete(self.path_graph.get_disjoint(index))
