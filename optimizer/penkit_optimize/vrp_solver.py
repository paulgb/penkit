from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from time import time


def vrp_solver(path_graph, initial_solution=None, runtime_seconds=60):
    """Solve a path using or-tools' Vehicle Routing Problem solver.
    Params:
        path_graph        the PathGraph representing the problem
        initial_solution  a solution to start with (list of indices, not
                          including the origin)
        runtime_seconds   how long to search before returning

    Returns: an ordered list of indices in the graph representing a
        solution.
    """
    # Create the VRP routing model. The 1 means we are only looking
    # for a single path.
    routing = pywrapcp.RoutingModel(path_graph.num_nodes(),
                                    1, path_graph.ORIGIN)

    # For every path node, add a disjunction so that we do not also
    # draw its reverse.
    for disjunction in path_graph.iter_disjunctions():
        routing.AddDisjunction(disjunction)

    # Wrap the distance function so that it converts to an integer,
    # as or-tools requires. Values are multiplied by COST_MULTIPLIER
    # prior to conversion to reduce the loss of precision.
    COST_MULTIPLIER = 1e4

    def distance(i, j):
        return int(path_graph.cost(i, j) * COST_MULTIPLIER)
    routing.SetArcCostEvaluatorOfAllVehicles(distance)

    start_time = time()

    def found_solution():
        t = time() - start_time
        cost = routing.CostVar().Max() / COST_MULTIPLIER
        print('\rBest solution at {} seconds has cost {}        '.format(
            int(t), cost), end='')
    routing.AddAtSolutionCallback(found_solution)

    # If we weren't supplied with a solution initially, construct one by taking
    # all of the paths in their original direction, in their original order.
    if not initial_solution:
        initial_solution = [i for i, _ in path_graph.iter_disjunctions()]

    # Compute the cost of the initial solution. This is the number we hope to
    # improve on.
    initial_assignment = routing.ReadAssignmentFromRoutes([initial_solution],
                                                          True)
    # print('Initial distance:',
    #      initial_assignment.ObjectiveValue() / COST_MULTIPLIER)

    # Set the parameters of the search.
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    search_parameters.time_limit_ms = runtime_seconds * 1000
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)

    # Run the optimizer and report the final distance.
    assignment = routing.SolveFromAssignmentWithParameters(initial_assignment,
                                                           search_parameters)
    print()
    #print('Final distance:', assignment.ObjectiveValue() / COST_MULTIPLIER)

    # Iterate over the result to produce a list to return as the solution.
    solution = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        index = assignment.Value(routing.NextVar(index))
        node = routing.IndexToNode(index)
        if node != 0:
            # For compatibility with the greedy solution, exclude the origin.
            solution.append(node)
    return solution
