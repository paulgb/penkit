from penkit_optimize.path_index import PathIndex


def greedy_walk(path_graph):
    path_index = PathIndex(path_graph)
    location = path_graph.get_coordinates(path_graph.ORIGIN)
    while True:
        try:
            next_point = path_index.get_nearest(location)
        except StopIteration:
            break
        location = path_graph.get_coordinates(next_point, True)
        path_index.delete_pair(next_point)
        yield next_point
