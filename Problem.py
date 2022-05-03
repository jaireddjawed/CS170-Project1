from queue import PriorityQueue
from time import time
from copy import deepcopy
from Node import Node

class Problem(object):
  def __init__(self, initialState):
    # the initial puzzle that the user chooses
    self.initalState = initialState

    # the puzzle we want to reach from the user's chosen puzzle
    self.goalState = [
      ['1', '2', '3'],
      ['4', '5', '6'],
      ['7', '8', '0']
    ]

    '''
    possible goal states for reference (depends on the test cases used)

    [
      ['1', '2', '3'],
      ['4', '5', '6'],
      ['7', '8', '0']
    ]

    [
      ['0', '1', '2'],
      ['3', '4', '5'],
      ['6', '7', '8']
    ]
    '''

    # start time of the algorithm
    self.startTime = time()

    # will hold all of the nodes that we've already visited
    self.visited = set()

    # will hold all of the nodes that are currently in the frontier already
    self.alreadyInFrontier = set()

    # only one of these can be true at any given time
    # determines what type of search we are using
    self.uniform = False
    self.misplaced = False
    self.euclidean = False

  def setGoalState(self, goalState):
    self.goalState = goalState

  def uniformCostSearch(self):
    # set the search algorithm to ucs and start the search algorithm
    self.uniform = True
    self.graphSearch()

  def misplacedSearch(self):
    # set the search algorithm to A* with misplaced heuristic and start the search algorithm
    self.misplaced = True
    self.graphSearch()

  def euclideanSearch(self):
    # set the search algorithm to euclidean and start the search algorithm
    self.euclidean = True
    self.graphSearch()

  def graphSearch(self):
    # queue to visit the nodes in order
    frontier = PriorityQueue()

    # add the first node into the frontier
    firstNode = Node(self.initalState)
    frontier.put(firstNode)

    # we already have one node in the frontier and we've already expanded one node
    maxFrontierSize = 1
    numNodesExpanded = 1

    while True:
      # there's a failure if the frontier is ever empty
      if frontier.qsize() == 0:
        print('Failure!\n')
        break

      currentNode = frontier.get()

      # print the current node
      print('The best state to expand with a g(n) = {} and h(n) = {} is ... '.format(currentNode.getGn(), currentNode.getHn()))
      currentNode.print()

      # when we reach a puzzle that matches the goal state, we terminate the loop and print out
      # the statistics that were required to reach the goal state
      if currentNode.getGrid() == self.goalState:
        endTime = time()
        timeToRun = endTime - self.startTime

        print('Goal!')
        print('Number of nodes expanded: {}.'.format(numNodesExpanded))
        print('The maximum number of nodes in the queue at any one time: {}.'.format(maxFrontierSize))
        print('Depth of the goal node: {}.'.format(currentNode.getGn()))
        print('Time to finish: {} second(s).'.format(timeToRun))
        break

      # remove the node from the frontier set
      self.alreadyInFrontier.discard(currentNode)

      neighbors = self.expandNodes(currentNode)

      # go through all of the neighbors and add them to the frontier if they haven't yet been visited
      for neighbor in neighbors:
        if self.uniform:
          # add the node to the frontier if we haven't visited it yet and it isn't already in the frontier
          if not neighbor in self.alreadyInFrontier:
            neighbor.setFn(currentNode.getGn())
            frontier.put(neighbor)
            self.alreadyInFrontier.add(neighbor)
            numNodesExpanded += 1

        if self.misplaced:
          if not neighbor in self.alreadyInFrontier:
            misplacedCount = 0

            # count the number of nodes that are in the incorrect place
            # we will use it to set the heuristic

            for i in range(len(neighbor.getGrid())):
              for j in range(len(neighbor.getGrid()[0])):
                if neighbor.getGrid()[i][j] != self.goalState[i][j]:
                  misplacedCount += 1

            # h(n) is the number of misplaced nodes
            neighbor.setHn(misplacedCount)
            # f(n) = g(n) + h(n)
            neighbor.setFn(currentNode.getGn() + currentNode.getHn())

            frontier.put(neighbor)
            self.alreadyInFrontier.add(neighbor)
            numNodesExpanded += 1

        if self.euclidean:
          if not neighbor in self.alreadyInFrontier:
            euclideanDistance = 0

            row, col = 0, 0
            goalRow, goalCol = 0, 0

            # total number of numbers within grid (used to make it easy to convert it to a puzzle of a different length)
            totalNumsInGrid = 9

            # we go through the numbers within the grid and find how far each number is from where it is supposed to be in the goal state
            num = 0
            while num < totalNumsInGrid:
              for i in range(len(neighbor.getGrid())):
                  for j in range(len(neighbor.getGrid()[i])):
                      if int(neighbor.getGrid()[i][j]) == num:
                        row = i
                        col = j

                      if int(self.goalState[i][j]) == num:
                          goalRow = i
                          goalCol = j

              # add up how far the number is on the row and column lengths
              euclideanDistance += abs(goalRow-row) + abs(goalCol-col)
              num += 1

            # h(n) is the euclidean distance
            neighbor.setHn(euclideanDistance)
            # f(n) = g(n) + h(n)
            neighbor.setFn(currentNode.getGn() + currentNode.getHn())

            frontier.put(neighbor)
            self.alreadyInFrontier.add(neighbor)
            numNodesExpanded += 1

      # if the frontier is larger than the max size we've seen so far, we replace the old size
      if frontier.qsize() > maxFrontierSize:
          maxFrontierSize = frontier.qsize()

  def expandNodes(self, currentNode):
    neighbors = []

    i, j = currentNode.getZeroIndex()
    grid = currentNode.getGrid()

    # check if a neighbor is above the currentNode
    if (i-1) >= 0:
      # we can't use a shallow copy because it will modify the original grid and ruin it for the other neighbors
      temp = deepcopy(grid)

      # swap the * grid cell with the number that exists above it
      temp[i][j], temp[i-1][j] = temp[i-1][j], temp[i][j]
      tempNode = Node(temp)

      # do not add the node to the neighbors list if we've already checked it
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
