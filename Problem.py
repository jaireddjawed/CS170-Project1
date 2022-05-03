from queue import PriorityQueue, Queue
from time import time
from copy import deepcopy
from Node import Node

class Problem(object):
  def __init__(self, initialState):
    self.initalState = initialState
    self.goalState = [
      ['1', '2', '3'],
      ['4', '5', '6'],
      ['7', '8', '0']
    ]
    self.startTime = time()

  def uniformCostSearch(self):
    self.graphSearch()

  def misplacedTileHeuristic(self):
    pass

  def graphSearch(self):
    # queue to visit the nodes in order
    frontier = PriorityQueue()

    # add the first node into the frontier
    firstNode = Node(self.initalState)
    frontier.put(firstNode)

    # keeps track of the nodes that have already been visited
    visited = set()

    # set that keeps track of the nodes that are currently within the frontier
    inFrontier = set()

    # current max frontier size is 1 because of the firstNode
    maxFrontierSize = 1

    while True:
      # the search has failed if the frontier is empty
      if frontier.qsize() == 0:
        print('Failure!\n')
        break

      currentNode = frontier.get()

      # print the current node
      print('The best state to expand with a g(n) = {} and h(n) = 0 is ... '.format(currentNode.getGn()))
      currentNode.print()

      # check if the currentNode is a goal state
      if currentNode.getGrid() == self.goalState:
        endTime = time()
        timeToRun = endTime - self.startTime

        print('Goal!')
        print('The maximum number of nodes at any one time: ' + str(maxFrontierSize) + '.')
        print('Depth of the goal node: {}.'.format(currentNode.getGn()))
        print('Time to finish: {} second(s).'.format(timeToRun))
        break

      # mark the current node as visited
      visited.add(currentNode)

      # remove the node from the frontier
      inFrontier.discard(currentNode)

      neighbors = self.expandNodes(currentNode)

      # go through all of the neighbors and add them to the frontier if they haven't yet been visited
      for neighbor in neighbors:

        # add the node to the frontier if we haven't visited it yet and it isn't already in the frontier
        if not neighbor in visited and not neighbor in inFrontier:
          neighbor.setFn(currentNode.getGn())
          frontier.put(neighbor)
          inFrontier.add(neighbor)

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
      tempNode.setGn(currentNode.getGn() + 1)
      neighbors.append(tempNode)

    # check if a neighbor below the currentNode exists
    if (i+1) < len(grid):
      temp = deepcopy(grid)
      temp[i][j], temp[i+1][j] = temp[i+1][j], temp[i][j]
      tempNode = Node(temp)
      tempNode.setGn(currentNode.getGn() + 1)
      neighbors.append(tempNode)

    # to the left
    if (j-1) >= 0:
      temp = deepcopy(grid)
      temp[i][j], temp[i][j-1] = temp[i][j-1], temp[i][j]
      tempNode = Node(temp)
      tempNode.setGn(currentNode.getGn() + 1)
      neighbors.append(tempNode)

    # to the right
    if (j+1) < len(grid[0]):
      temp = deepcopy(grid)
      temp[i][j], temp[i][j+1] = temp[i][j+1], temp[i][j]
      tempNode = Node(temp)
      tempNode.setGn(currentNode.getGn() + 1)
      neighbors.append(tempNode)

    return neighbors
