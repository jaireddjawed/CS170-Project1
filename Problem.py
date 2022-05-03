from queue import PriorityQueue
from time import time
from copy import deepcopy
from Node import Node

class Problem(object):
  def __init__(self, initialState):
    self.initalState = initialState
    self.goalState = [
      ['0', '1', '2'],
      ['3', '4', '5'],
      ['6', '7', '8']
    ]

    # start time of the algorithm
    self.startTime = time()

    # will hold all of the nodes that we've already visited
    self.visited = set()

    # will hold all of the nodes that are currently in the frontier already
    self.alreadyInFrontier = set()

    self.uniform = False
    self.misplaced = False
    self.euclidean = False

  def setGoalState(self, goalState):
    self.goalState = goalState

  def uniformCostSearch(self):
    self.uniform = True
    self.graphSearch()

  def misplacedSearch(self):
    self.misplaced = True
    self.graphSearch()

  def euclideanSearch(self):
    self.euclidean = True
    self.graphSearch()

  def graphSearch(self):
    # queue to visit the nodes in order
    frontier = PriorityQueue()

    # add the first node into the frontier
    firstNode = Node(self.initalState)
    frontier.put(firstNode)

    maxFrontierSize = 1
    numNodesExpanded = 1

    while True:
      if frontier.qsize() == 0:
        print('Failure!\n')
        break

      currentNode = frontier.get()

      # print the current node
      print('The best state to expand with a g(n) = {} and h(n) = {} is ... '.format(currentNode.getGn(), currentNode.getHn()))
      currentNode.print()

      if currentNode.getGrid() == self.goalState:
        endTime = time()
        timeToRun = endTime - self.startTime

        print('Goal!')
        print('Number of nodes expanded: {}.'.format(numNodesExpanded))
        print('The maximum number of nodes in the queue at any one time: ' + str(maxFrontierSize) + '.')
        print('Depth of the goal node: {}.'.format(currentNode.getGn()))
        print('Time to finish: {} second(s).'.format(timeToRun))
        break

      # remove the node from the frontier set
      self.alreadyInFrontier.discard(currentNode)

      neighbors = self.expandNodes(currentNode)

      # go through all of the neighbors and add them to the frontier if they haven't yet been visited
      for neighbor in neighbors:

        # add the node to the frontier if we haven't visited it yet and it isn't already in the frontier
        if not neighbor in self.alreadyInFrontier:
          neighbor.setFn(currentNode.getGn())
          frontier.put(neighbor)
          self.alreadyInFrontier.add(neighbor)
          numNodesExpanded += 1

      if frontier.qsize() > maxFrontierSize:
          maxFrontierSize = frontier.qsize()

  def expandNodes(self, currentNode):
    neighbors = []

    i, j = currentNode.getZeroIndex()
    grid = currentNode.getGrid()

    # check if a neighbor is above the currentNode
    if (i-1) >= 0:
      temp = deepcopy(grid)
      temp[i][j], temp[i-1][j] = temp[i-1][j], temp[i][j]
      tempNode = Node(temp)

      if not tempNode in self.visited:
        self.visited.add(tempNode)
        tempNode.setGn(currentNode.getGn() + 1)
        neighbors.append(tempNode)

    # check if a neighbor below the currentNode exists
    if (i+1) < len(grid):
      temp = deepcopy(grid)
      temp[i][j], temp[i+1][j] = temp[i+1][j], temp[i][j]
      tempNode = Node(temp)

      if not tempNode in self.visited:
        self.visited.add(tempNode)
        tempNode.setGn(currentNode.getGn() + 1)
        neighbors.append(tempNode)

    # to the left
    if (j-1) >= 0:
      temp = deepcopy(grid)
      temp[i][j], temp[i][j-1] = temp[i][j-1], temp[i][j]
      tempNode = Node(temp)

      if not tempNode in self.visited:
        self.visited.add(tempNode)
        tempNode.setGn(currentNode.getGn() + 1)
        neighbors.append(tempNode)

    # to the right
    if (j+1) < len(grid[0]):
      temp = deepcopy(grid)
      temp[i][j], temp[i][j+1] = temp[i][j+1], temp[i][j]
      tempNode = Node(temp)

      if not tempNode in self.visited:
        self.visited.add(tempNode)
        tempNode.setGn(currentNode.getGn() + 1)
        neighbors.append(tempNode)

    return neighbors
