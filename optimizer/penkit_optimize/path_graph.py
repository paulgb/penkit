from penkit_optimize.route_util import dist


class PathGraph:
    # The origin is always at index 0.
    ORIGIN = 0

    def __init__(self, paths, origin=0. + 0j):
        """Constructs a PathGraph from the output of svgpathtools.svg2paths."""
        self.paths = paths
        # For any node i, endpoints[i] will be a pair containing that node's
        # start and end coordinates, respectively. For i==0 this represents
        # the origin.
        self.endpoints = [(origin, origin)]

        for path in paths:
            # For each path in the original list of paths,
            # create nodes for the path as well as its reverse.
            self.endpoints.append((path.start, path.end))
            self.endpoints.append((path.end, path.start))

    def get_path(self, i):
        """Returns the path corresponding to the node i."""
        index = (i - 1) // 2
        reverse = (i - 1) % 2
        path = self.paths[index]
        if reverse:
            return path.reversed()
        else:
            return path

    def cost(self, i, j):
        """Returns the distance between the end of path i
        and the start of path j."""
        return dist(self.endpoints[i][1], self.endpoints[j][0])

    def get_coordinates(self, i, end=False):
        """Returns the starting coordinates of node i as a pair,
        or the end coordinates iff end is True."""
        if end:
            endpoint = self.endpoints[i][1]
        else:
            endpoint = self.endpoints[i][0]
        return (endpoint.real, endpoint.imag)

    def iter_starts_with_index(self):
        """Returns a generator over (index, start coordinate) pairs,
        excluding the origin."""
        for i in range(1, len(self.endpoints)):
            yield i, self.get_coordinates(i)

    def get_disjoint(self, i):
        """For the node i, returns the index of the node associated with
        its path's opposite direction."""
        return ((i - 1) ^ 1) + 1

    def iter_disjunctions(self):
        """Returns a generator over 2-element lists of indexes which must
        be mutually exclusive in a solution (i.e. pairs of nodes which represent
        the same path in opposite directions.)"""
        for i in range(1, len(self.endpoints), 2):
            yield [i, self.get_disjoint(i)]

    def num_nodes(self):
        """Returns the number of nodes in the graph (including the origin.)"""
        return len(self.endpoints)
