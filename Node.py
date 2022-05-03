class Node(object):
  def __init__(self, grid):
    self.grid = grid

    # get the zero index within the grid
    # it's set to -1 in the case where there are no 0s within the grid
    self.zero_i = -1
    self.zero_j = -1

    for i in range(len(self.grid)):
      for j in range(len(self.grid[i])):
        if self.grid[i][j] == '0':
          self.zero_i = i
          self.zero_j = j

    # set fn and gn to 0 by default
    self.fn = 0
    self.gn = 0
    self.hn = 0

  def __repr__(self):
      return 'Node <{}>'.format(self.grid)

  def __lt__(self, comparedNode):
    return self.fn < comparedNode.fn

  def getGrid(self):
    return self.grid

  def getZeroIndex(self):
    return (self.zero_i, self.zero_j)

  def print(self):
    for i in range(len(self.grid)):
      row = ' '.join(self.grid[i]).replace('0', '*')
      print(row)

    print('\n')

  def setFn(self, fn):
    self.fn = fn

  def getFn(self):
    return self.fn

  def setGn(self, gn):
    self.gn = gn

  def getGn(self):
    return self.gn

  def setHn(self, hn):
    self.hn = hn

  def getHn(self):
    return self.hn
