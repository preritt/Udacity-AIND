# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from util import Stack, Queue, PriorityQueue, PriorityQueueWithFunction
from util import manhattanDistance

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

# # Method 1

# def depthFirstSearch(problem):
#   """
#   Search the deepest nodes in the search tree first
#   [2nd Edition: p 75, 3rd Edition: p 87]
  
#   Your search algorithm needs to return a list of actions that reaches
#   the goal.  Make sure to implement a graph search algorithm 
#   [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
#   To get started, you might want to try some of these simple commands to
#   understand the search problem that is being passed in:
  
#   print "Start:", problem.getStartState()
#   print "Is the start a goal?", problem.isGoalState(problem.getStartState())
#   print "Start's successors:", problem.getSuccessors(problem.getStartState())
#   """
#   "*** YOUR CODE HERE ***"
#   node = problem.getStartState()
#   if (problem.isGoalState(node)):
#     return [] # no need to make any moves of the start state is goal
#   start = node
#   item = start
#   priority = 0

#   frontier_queue = Stack() # queue for frontier
#   frontier_queue.push(item) # frontier consists of only the start state
#   priority_track = {}

#   priority_track[start] = 0
#   explored_nodes = set()
#   explored_track = {start:None} # keep a track of parent, parent of root node is None

#   while not frontier_queue.isEmpty():
#     state = frontier_queue.pop() # pop the top element from the queue 
#     explored_nodes.add(state)

#     if problem.isGoalState(state):
#       return get_track(explored_track, state)

#     neighbors_state = problem.getSuccessors(state)

#     for neighbor in neighbors_state: # neighbor will be something like this ((34, 15), 'South', 1).
#       if neighbor[0] not in frontier_queue.list  and neighbor[0] not in explored_nodes:
#         item = neighbor[0]
#         frontier_queue.push(item)
#         if state == start:
#           explored_track[neighbor] = start
#         else:
#           explored_track[neighbor] = state


#     def get_track(explored_track, state):

#       from game import Directions
#       track_history = []
#       final_move = [j for j in explored_track.keys() if j[0] == state]

#       move = final_move
#       while explored_track[move[0]] != start:
#         move = [j for j in explored_track.keys() if j[0] == state]
#         track_history.append(move[0][1])
#         state = explored_track[move[0]]
#       return track_history[::-1]
# # Method 1 ENDS

def depthFirstSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"

  start_state = problem.getStartState()
  frontier = Stack() # queue for frontier
  explored = set()
  frontier.push((start_state, [])) 
  # [] -> path required to reach here
  # 0 step cost to reach here
  # heuristic(start_state, problem) estimated heurisic distance to reach goal

  while not frontier.isEmpty():
    location, path_to_reach_here = frontier.pop()
    explored.add(location)
    if problem.isGoalState(location):
      return path_to_reach_here
    for neighbor in problem.getSuccessors(location):
      neighbor_location, neighbor_action, neighbor_step_cost = neighbor
      frontier_list = [element[0] for element in frontier.list] # get a list of all elements in frontier s.union(t)
      frontier_union_explored =  list(set(frontier_list).union(explored))
      if neighbor_location not in frontier_union_explored:
        path_till_neighbor = path_to_reach_here + [neighbor_action]
        # print neighbor_location, path_till_neighbor
        frontier.push((neighbor_location, path_till_neighbor))

## Method 1
# def breadthFirstSearch(problem):
#   """
#   Search the shallowest nodes in the search tree first.
#   [2nd Edition: p 73, 3rd Edition: p 82]
#   """
#   "*** YOUR CODE HERE ***"
#   node = problem.getStartState()
#   if (problem.isGoalState(node)):
#     return [] # no need to make any moves of the start state is goal
#   start = node
#   item = start
#   priority = 0

#   frontier_queue = Queue() # queue for frontier
#   frontier_queue.push(item) # frontier consists of only the start state
#   priority_track = {}
#   # print start
#   # print "="*50

#   priority_track[start] = 0
#   explored_nodes = set()
#   explored_track = {start:None} # keep a track of parent, parent of root node is None

#   while not frontier_queue.isEmpty():
#     state = frontier_queue.pop() # pop the top element from the queue 
#     explored_nodes.add(state)

#     if problem.isGoalState(state):
#       return get_track(explored_track, state)

#     neighbors_state = problem.getSuccessors(state)
#     # print neighbors_state
#     # print "*"*50
#     for neighbor in neighbors_state: # neighbor will be something like this ((34, 15), 'South', 1).
#       if neighbor[0] not in frontier_queue.list  and neighbor[0] not in explored_nodes:
#         item = neighbor[0]
#         frontier_queue.push(item)
#         if state == start:
#           explored_track[neighbor] = start
#         else:
#           explored_track[neighbor] = state


#     def get_track(explored_track, state):

#       from game import Directions
#       track_history = []
#       final_move = [j for j in explored_track.keys() if j[0] == state]

#       move = final_move
#       while explored_track[move[0]] != start:
#         move = [j for j in explored_track.keys() if j[0] == state]
#         track_history.append(move[0][1])
#         state = explored_track[move[0]]
#       return track_history[::-1]


## Method 1 Ends

def breadthFirstSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"

  start_state = problem.getStartState()
  frontier = Queue() # queue for frontier
  explored = set()
  frontier.push((start_state, [])) 
  # [] -> path required to reach here
  # 0 step cost to reach here
  # heuristic(start_state, problem) estimated heurisic distance to reach goal

  while not frontier.isEmpty():
    location, path_to_reach_here = frontier.pop()
    explored.add(location)
    if problem.isGoalState(location):
      return path_to_reach_here
    for neighbor in problem.getSuccessors(location):
      neighbor_location, neighbor_action, neighbor_step_cost = neighbor
      frontier_list = [element[0] for element in frontier.list] # get a list of all elements in frontier s.union(t)
      frontier_union_explored =  list(set(frontier_list).union(explored))
      if neighbor_location not in frontier_union_explored:
        path_till_neighbor = path_to_reach_here + [neighbor_action]
        # print neighbor_location, path_till_neighbor
        frontier.push((neighbor_location, path_till_neighbor))


def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"

  start_state = problem.getStartState()
  frontier = PriorityQueue() # queue for frontier
  explored = set()
  frontier.push((start_state, [], 0), 0) 
  # [] -> path required to reach here
  # 0 step cost to reach here
  # heuristic(start_state, problem) estimated heurisic distance to reach goal

  while not frontier.isEmpty():
    location, path_to_reach_here, cost_to_reach_here = frontier.pop()
    explored.add(location)
    if problem.isGoalState(location):
      return path_to_reach_here
    for neighbor in problem.getSuccessors(location):
      neighbor_location, neighbor_action, neighbor_step_cost = neighbor
      frontier_list = [element[0] for element in frontier.heap] # get a list of all elements in frontier s.union(t)
      # frontier_union_explored = list(set(frontier_list) + explored)
      frontier_union_explored =  list(set(frontier_list).union(explored))
      if neighbor_location not in frontier_union_explored:
        neighbor_total_cost_heuristic = cost_to_reach_here + neighbor_step_cost  # fn
        path_till_neighbor = path_to_reach_here + [neighbor_action]
        cost_to_reach_to_neighbor = cost_to_reach_here + neighbor_step_cost
        frontier.push((neighbor_location, path_till_neighbor, cost_to_reach_to_neighbor), neighbor_total_cost_heuristic)
      elif neighbor_location in frontier_list:
        print "Take care"



def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"

  start_state = problem.getStartState()
  frontier = PriorityQueue() # queue for frontier
  explored = set()
  frontier.push((start_state, [], 0), heuristic(start_state, problem)) 
  # [] -> path required to reach here
  # 0 step cost to reach here
  # heuristic(start_state, problem) estimated heurisic distance to reach goal

  while not frontier.isEmpty():
    location, path_to_reach_here, cost_to_reach_here = frontier.pop()
    # explored.add(location)
    if problem.isGoalState(location):
      return path_to_reach_here
    # print location, list(explored)
    # if location not in explored:
      # print "location not in (explored)"
    explored.add(location)
    for neighbor in problem.getSuccessors(location):
      neighbor_location, neighbor_action, neighbor_step_cost = neighbor
      frontier_list = [element[0] for element in frontier.heap] # get a list of all elements in frontier s.union(t)
      # frontier_union_explored = list(set(frontier_list) + explored)
      frontier_union_explored =  list(set(frontier_list).union(explored))
      if neighbor_location not in frontier_union_explored:
        neighbor_total_cost_heuristic = cost_to_reach_here + neighbor_step_cost + heuristic(neighbor_location, problem) # fn
        path_till_neighbor = path_to_reach_here + [neighbor_action]
        cost_to_reach_to_neighbor = cost_to_reach_here + neighbor_step_cost
        frontier.push((neighbor_location, path_till_neighbor, cost_to_reach_to_neighbor), neighbor_total_cost_heuristic)
      elif neighbor_location in frontier_list:
        print "Take care"







## MEthod 2
# def aStarSearch(problem, heuristic=nullHeuristic):
#   "Search the node that has the lowest combined cost and heuristic first."
#   "*** YOUR CODE HERE ***"
#   node = problem.getStartState()
#   if (problem.isGoalState(node)):
#     return [] # no need to make any moves of the start state is goal
#   start = node
#   item = start
#   priority = 0 + heuristic(start, problem)

#   frontier_queue = PriorityQueue() # queue for frontier
#   frontier_queue.push(item,priority ) # frontier consists of only the start state
#   priority_track = {}

#   priority_track[start] = priority
#   explored_nodes = set()
#   explored_track = {start:None} # keep a track of parent, parent of root node is None

#   while not frontier_queue.isEmpty():
#     state = frontier_queue.pop() # pop the top element from the queue 
#     explored_nodes.add(state)

#     if problem.isGoalState(state):
#       return get_track(explored_track, state)

#     neighbors_state = problem.getSuccessors(state)

#     for neighbor in neighbors_state: # neighbor will be something like this ((34, 15), 'South', 1).
#       if neighbor[0] not in frontier_queue.heap  and neighbor[0] not in explored_nodes:
#         item = neighbor[0]
#         priority_step = neighbor[2] 
#         priority_path = priority_track[state]

#         priority_track[neighbor[0]] = priority_step + priority_path + heuristic(neighbor[0], problem)
#         frontier_queue.push(item, priority_track[neighbor[0]] )
#         explored_track[neighbor] = start
#         if state == start:
#           explored_track[neighbor] = start
#         else:
#           explored_track[neighbor] = state


#     def get_track(explored_track, state):

#       # print explored_track
#       from game import Directions
#       track_history = []
#       final_move = [j for j in explored_track.keys() if j[0] == state]

#       move = final_move
#       while explored_track[move[0]] != start:
#         move = [j for j in explored_track.keys() if j[0] == state]
#         track_history.append(move[0][1])
#         state = explored_track[move[0]]
#       return track_history[::-1]

## Method 2 ENDS

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
