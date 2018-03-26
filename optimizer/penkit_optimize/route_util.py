from collections import Counter
import svgpathtools


def check_valid_solution(solution, graph):
    """Check that the solution is valid: every path is visited exactly once."""
    expected = Counter(
        i for (i, _) in graph.iter_starts_with_index()
        if i < graph.get_disjoint(i)
    )
    actual = Counter(
        min(i, graph.get_disjoint(i))
        for i in solution
    )

    difference = Counter(expected)
    difference.subtract(actual)
    difference = {k: v for k, v in difference.items() if v != 0}
    if difference:
        print('Solution is not valid!'
              'Difference in node counts (expected - actual): {}'.format(difference))
        return False
    return True


def get_route_from_solution(solution, graph):
    """Converts a solution (a list of node indices) into a list
    of paths suitable for rendering."""

    # As a guard against comparing invalid "solutions",
    # ensure that this solution is valid.
    assert check_valid_solution(solution, graph)

    return [graph.get_path(i) for i in solution]


def join_close_paths(paths, threshold):
    new_paths = []
    current_path = []

    for path in paths:
        start = path[0].start
        end = path[-1].end

        if current_path:
            last_point = current_path[-1].end
            start_point = path[0].start
            if dist(last_point, start_point) < threshold:
                current_path.append(svgpathtools.Line(last_point, start_point))
                current_path.extend(path)
                continue
            else:
                new_paths.append(svgpathtools.Path(*current_path))
        current_path = list(path)

    if current_path:
        new_paths.append(svgpathtools.Path(*current_path))
    return new_paths


def dist(p1, p2):
    return abs(p1 - p2)


def cost_of_route(path, origin=0. + 0j):
    # Cost from the origin to the start of the first path
    cost = dist(origin, path[0].start)
    # Cost between the end of each path and the start of the next
    cost += sum(
        dist(path[i].end, path[i + 1].start) for i in range(len(path) - 1)
    )
    # Cost to return back to the origin
    cost += dist(path[-1].end, origin)
    return cost
