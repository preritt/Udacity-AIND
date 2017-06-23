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
#   print ("Start:", problem.getStartState())
#   print ("Is the start a goal?", problem.isGoalState(problem.getStartState()))
#   print ("Start's successors:", problem.getSuccessors(problem.getStartState()))

#   util.raiseNotDefined()

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  node = problem.getStartState()
  if (problem.isGoalState(node)):
    return [] # no need to make any moves of the start state is goal
  start = (node, 'NoDirection',0)

  frontier_queue = Stack() # queue for frontier
  frontier_queue.push(start) # frontier consists of only the start state

  explored_nodes = set()
  explored_track = {start:None} # keep a track of parent, parent of root node is None

  while not frontier_queue.isEmpty():
    state = frontier_queue.pop() # pop the top element from the queue 
    explored_nodes.add(state)

    if problem.isGoalState(state[0]):
      return get_track(explored_track, state)

    neighbors_state = problem.getSuccessors(state[0])
    for neighbor in neighbors_state: # neighbor will be something like this ((34, 15), 'South', 1)
      if neighbor not in frontier_queue.list  and neighbor not in explored_nodes:
        frontier_queue.push(neighbor)
        explored_track[neighbor] = state


    def get_track(explored_track, state):
      from game import Directions
      track_history = [state]
      track_history_direction = []
      leaf = state
      while (explored_track[leaf]) != start:
        track_history.append(explored_track[leaf])
        leaf = explored_track[leaf]

      for j in range (len(track_history),-1,-1):
        this_step = track_history[j-1]
        this_step = this_step[1]
        track_history_direction.append(this_step)
      return  track_history_direction[:-1]
 

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  node = problem.getStartState()
  if (problem.isGoalState(node)):
    return [] # no need to make any moves of the start state is goal
  start = (node, 'NoDirection',0)

  frontier_queue = Queue() # queue for frontier
  frontier_queue.push(start) # frontier consists of only the start state

  explored_nodes = set()
  explored_track = {start:None} # keep a track of parent, parent of root node is None

  while not frontier_queue.isEmpty():
    state = frontier_queue.pop() # pop the top element from the queue 
    explored_nodes.add(state)

    if problem.isGoalState(state[0]):
      return get_track(explored_track, state)

    neighbors_state = problem.getSuccessors(state[0])
    for neighbor in neighbors_state: # neighbor will be something like this ((34, 15), 'South', 1)
      if neighbor not in frontier_queue.list  and neighbor not in explored_nodes:
        frontier_queue.push(neighbor)
        explored_track[neighbor] = state


    def get_track(explored_track, state):
      from game import Directions
      track_history = [state]
      track_history_direction = []
      leaf = state
      while (explored_track[leaf]) != start:
        track_history.append(explored_track[leaf])
        leaf = explored_track[leaf]

      for j in range (len(track_history),-1,-1):
        this_step = track_history[j-1]
        this_step = this_step[1]
        track_history_direction.append(this_step)
      return  track_history_direction[:-1]


# def uniformCostSearch(problem):
#   "Search the node of least total cost first. "
#   "*** YOUR CODE HERE ***"

#   node = problem.getStartState()
#   if (problem.isGoalState(node)):
#     return [] # no need to make any moves of the start state is goal
#   start = node

#   frontier_queue = PriorityQueueWithFunction(problem.costFn) # queue for frontier
#   frontier_queue.push(start) # frontier consists of only the start state

#   explored_nodes = set()
#   explored_track = {start:None} # keep a track of parent, parent of root node is None
#   # explored_track = {} # keep a track of parent, parent of root node is None

#   while not frontier_queue.isEmpty():
#     state = frontier_queue.pop() # pop the top element from the queue 
#     explored_nodes.add(state)

#     if problem.isGoalState(state):
#       return get_track(explored_track, state)

#     neighbors_state = problem.getSuccessors(state)

#     for neighbor in neighbors_state: # neighbor will be something like this ((34, 15), 'South', 1).
#       if neighbor[0] not in frontier_queue.heap  and neighbor[0] not in explored_nodes:
#         frontier_queue.push(neighbor[0])
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

# def uniformCostSearch(problem):
#   "Search the node of least total cost first. "
#   "*** YOUR CODE HERE ***"

#   node = problem.getStartState()
#   if (problem.isGoalState(node)):
#     return [] # no need to make any moves of the start state is goal
#   start = node
#   item = start
#   priority = 0

#   frontier_queue = PriorityQueue() # queue for frontier
#   # print "="*100
#   # print priority,item
#   # print ":"*100
#   frontier_queue.push(item,priority ) # frontier consists of only the start state
#   priority_track = {}

#   priority_track[start] = 0
#   explored_nodes = set()
#   explored_track = {start:None} # keep a track of parent, parent of root node is None
#   # explored_track = {} # keep a track of parent, parent of root node is None

#   while not frontier_queue.isEmpty():
#     # print frontier_queue.heap
#     # print "<>"*50
#     state = frontier_queue.pop() # pop the top element from the queue 
#     explored_nodes.add(state)
#     # print state
#     # print "<>"*50

#     if problem.isGoalState(state):
#       return get_track(explored_track, state)

#     neighbors_state = problem.getSuccessors(state)

#     for neighbor in neighbors_state: # neighbor will be something like this ((34, 15), 'South', 1).
#       if neighbor[0] not in frontier_queue.heap  and neighbor[0] not in explored_nodes:
#         item = neighbor[0]
#         priority_step = neighbor[2] 
#         priority_path = priority_track[state]
#         print (priority_step, priority_path, neighbor)
#         priority_track[neighbor[0]] = priority_step + priority_path
#         # print item, neighbor
#         # print "="*50
#         # priority = problem.getCostOfActions(item) 
#         # print "="*50
#         # print priority
#         # print "="*50
#         frontier_queue.push(item, priority_track[neighbor[0]] )
#         if state == start:
#           explored_track[neighbor] = start
#         else:
#           explored_track[neighbor] = state


#     def get_track(explored_track, state):

#       # print explored_track

#       print explored_track
#       from game import Directions
#       track_history = []
#       final_move = [j for j in explored_track.keys() if j[0] == state]

#       move = final_move
#       while explored_track[move[0]] != start:
#         move = [j for j in explored_track.keys() if j[0] == state]
#         track_history.append(move[0][1])
#         state = explored_track[move[0]]
#       return track_history[::-1]

# def nullHeuristic(state, problem=None):
#   """
#   A heuristic function estimates the cost from the current state to the nearest
#   goal in the provided SearchProblem.  This heuristic is trivial.
#   """
#   return 0
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"

  node = problem.getStartState()
  if (problem.isGoalState(node)):
    return [] # no need to make any moves of the start state is goal
  start = node
  item = start
  priority = 0

  frontier_queue = PriorityQueue() # queue for frontier
  frontier_queue.push(item,priority ) # frontier consists of only the start state
  priority_track = {}

  priority_track[start] = 0
  explored_nodes = set()
  explored_track = {start:None} # keep a track of parent, parent of root node is None

  while not frontier_queue.isEmpty():
    state = frontier_queue.pop() # pop the top element from the queue 
    explored_nodes.add(state)

    if problem.isGoalState(state):
      return get_track(explored_track, state)

    neighbors_state = problem.getSuccessors(state)

    for neighbor in neighbors_state: # neighbor will be something like this ((34, 15), 'South', 1).
      if neighbor[0] not in frontier_queue.heap  and neighbor[0] not in explored_nodes:
        item = neighbor[0]
        priority_step = neighbor[2] 
        priority_path = priority_track[state]

        priority_track[neighbor[0]] = priority_step + priority_path
        frontier_queue.push(item, priority_track[neighbor[0]] )
        if state == start:
          explored_track[neighbor] = start
        else:
          explored_track[neighbor] = state


    def get_track(explored_track, state):

      # print explored_track

      print explored_track
      from game import Directions
      track_history = []
      final_move = [j for j in explored_track.keys() if j[0] == state]

      move = final_move
      while explored_track[move[0]] != start:
        move = [j for j in explored_track.keys() if j[0] == state]
        track_history.append(move[0][1])
        state = explored_track[move[0]]
      return track_history[::-1]

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0
def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  node = problem.getStartState()
  if (problem.isGoalState(node)):
    return [] # no need to make any moves of the start state is goal
  start = node

 
  heuristic_costFn = lambda x: heuristic(x,problem) + problem.costFn(x) + problem.getCostOfActions(x)



  frontier_queue = PriorityQueueWithFunction(heuristic_costFn) # queue for frontier
  frontier_queue.push(start) # frontier consists of only the start state

  explored_nodes = set()
  explored_track = {start:None} # keep a track of parent, parent of root node is None
  # explored_track = {} # keep a track of parent, parent of root node is None

  while not frontier_queue.isEmpty():
    state = frontier_queue.pop() # pop the top element from the queue 
    explored_nodes.add(state)

    if problem.isGoalState(state):
      return get_track(explored_track, state)

    neighbors_state = problem.getSuccessors(state)



    for neighbor in neighbors_state: # neighbor will be something like this ((34, 15), 'South', 1).
      if neighbor[0] not in frontier_queue.heap  and neighbor[0] not in explored_nodes:
        frontier_queue.push(neighbor[0])
        if state == start:
          explored_track[neighbor] = start
        else:
          explored_track[neighbor] = state


    def get_track(explored_track, state):

      from game import Directions
      track_history = []
      final_move = [j for j in explored_track.keys() if j[0] == state]

      move = final_move
      while explored_track[move[0]] != start:
        move = [j for j in explored_track.keys() if j[0] == state]
        track_history.append(move[0][1])
        state = explored_track[move[0]]
      return track_history[::-1]
  # util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
