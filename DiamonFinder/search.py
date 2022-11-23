# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import time

from agents import *
from problem import Problem
from search_algorithms import  *

def get_defined_heuristics():
    heuristics = []
    for key in globals():
        if key.endswith('Heuristic'):
            heuristics.append(key)
    return heuristics


class DiamondExplorerProblem(Problem):
    def __init__(self, environment):
        Problem.__init__(self)
        self.environment = environment
        self.__set_initial()
        self.__set_goal()
        self._expanded = 0

    def __set_initial(self):
        self.initial = self.environment.agent.location

    def __set_goal(self):
        self.goal = self.environment.get_diamond_location()

    def actions(self, state):
        self._expanded += 1
        x, y = state
        if self.environment.is_diamond(x, y):
            return [Action.Grab]
        possible_actions = [Action.LEFT, Action.DOWN, Action.RIGHT, Action.UP]
        x, y = Orientation.U.move_forward(state)
        if self.environment.is_wall(x, y):
            possible_actions.remove(Action.UP)
        x, y = Orientation.D.move_forward(state)
        if self.environment.is_wall(x, y):
            possible_actions.remove(Action.DOWN)
        x, y = Orientation.L.move_forward(state)
        if self.environment.is_wall(x, y):
            possible_actions.remove(Action.LEFT)
        x, y = Orientation.R.move_forward(state)
        if self.environment.is_wall(x, y):
            possible_actions.remove(Action.RIGHT)
        return possible_actions

    def get_successors(self, state, action):
        state2 = Orientation.move(action, state)
        if state2 is state:
            return None
        return state2

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        return 0

    def display(self, state, children_nodes):
        x, y = state
        self.environment.draw_rec(x, y, 'red')
        for n in children_nodes:
            x, y = n.state
            self.environment.draw_rec(x, y, 'blue')
        self.environment.canvas.update()
        time.sleep(self.environment.speed.get() / 1000)


class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs

    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, environment, fn='dfs', prob='DiamondExplorerProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems
        super().__init__(self)

        self.actions = None
        self.environment = environment
        self.total_time = 0.0
        self.nb_expand = 0
        self.total_cost = 0
        self.program = self.planing_program
        self.path_solution = None
        # Get the search function from the name and heuristic
        __my_global = globals()
        if fn not in __my_global.keys():
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = __my_global.get(fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in __my_global.keys():
                my_heuristic = __my_global[heuristic]
            else:
                raise AttributeError(heuristic + ' is not a function.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=my_heuristic)
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type ')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def planing_program(self, percet):
        state = percet
        if not self.actions:
            return self.registerInitialState(state)
        else:
            return self.getAction(state)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: an environment state
        """
        if self.searchFunction is None:
            raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(self.environment)  # Makes a new search problem
        node = self.searchFunction(problem)  # Find a path
        if node:
            self.actions = node.solution()
            self.path_solution = node.path()
            totalCost = problem.cost_of_actions(self.actions)
            run_time = time.time() - starttime
            print('Path found with total cost of %d in %.1f seconds' % (totalCost, run_time))
            if '_expanded' in dir(problem):
                print('Search nodes expanded: %d' % problem._expanded)
            self.total_cost += totalCost
            self.total_time += run_time
            self.nb_expand += problem._expanded
        else:
            print('No solution found!')

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.
        state: a environment state
        """
        if 'actionIndex' not in dir(self):
            self.actionIndex = 0

        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        elif i == len(self.actions):
            return Action.Grab
        else:
            if self.environment.get_diamond_location():
                self.actions = None
                self.actionIndex = 0
                return Action.NoOp
            self.alive = False
            return Action.STOP
