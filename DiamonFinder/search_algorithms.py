#import sys, os

#sys.path.extend([f'{item[0]}' for item in os.walk(".") if os.path.isdir(item[0])])
from problem import Node, PriorityQueue, memoize  # Ignore this error
from collections import deque


def depthFirstSearch(problem):
    """
     Search the deepest nodes in the search tree first.

     Your search algorithm needs to return a list of actions that reaches the
     goal. Make sure to implement a graph search algorithm.

     To get started, you might want to try some of these simple commands to
     understand the search problem that is being passed in:
     """
    print("depthFirstSearch ......... ")
    frontier = [Node(problem.initial)]  # Stack
    explored = set()
    while frontier:
        next_node = frontier.pop()
        if problem.is_goal_state(next_node.state):
            print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print(next_node)
            print(next_node.path())
            print(next_node.solution())
            return next_node
        explored.add(next_node.state)
        for node in next_node.expand(problem):
            if node.state not in explored and node not in frontier:
                frontier.append(node)
        problem.display(next_node.state, frontier)
    return None


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    raise ValueError('Not Defined!')


def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search. """
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    print(frontier)
    frontier.append(node)
    print(frontier)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.is_goal_state(node.state):
            if display:
                if display:
                    print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        to_expand = []
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                to_expand.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
                    to_expand.append(child)
        problem.display(node.state, to_expand)
    return None



def uniformCostSearch(problem):
    """Search the node of least total cost first.
    Note that each Node has its own path_cost
    attribute that you as cost function value."""
    "*** YOUR CODE HERE ***"
    raise ValueError('Not Defined!')
# uniform cost search doesn't use heuristics, but the greedy search and A* use them.
# so we need to define some heuristic function

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def euclideanHeuristic(node, problem):
    return min(map(lambda x: distance_squared(node.state, x), problem.goal))


## distance functions can be used as heuristics
def distance_squared(a, b):
    """The square of the distance between two (x, y) points."""
    xA, yA = a
    xB, yB = b
    return (xA - xB) ** 2 + (yA - yB) ** 2


def manhattan_distance(xy1, xy2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

# add a new heuristic called 'manhattanHeuristic' based on manhattan distance
# *** YOUR CODE HERE ***


def greedyBestFirstSearch(problem, heuristic=nullHeuristic):
    "*** YOUR CODE HERE ***"
    raise ValueError('Not Defined!')


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    raise ValueError('Not Defined!')


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
a_star = aStarSearch
ucs = uniformCostSearch
gs = greedyBestFirstSearch

