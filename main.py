from Problem import Problem

class Startup(object):
  def main(self):
    print('Welcome to jjawe001\'s 8 puzzle solver.\n')

    puzzleChoice = input('Type "1" to use a default puzzle or "2" to enter your own puzzle: ')
    eightPuzzleMatrix = []

    while True:
      if puzzleChoice == "1":
        # default matrix
        eightPuzzleMatrix.append(["1", "2", "3"])
        eightPuzzleMatrix.append(["4", "8", "0"])
        eightPuzzleMatrix.append(["7", "6", "5"])

        break
      elif puzzleChoice == "2":
        print('Enter your puzzle, use a "0" to represent the blank.')

        for i in range(3):
          try:
            row = input('Enter row ' + str(i+1) + ', use spaces between numbers: ')
            eightPuzzleMatrix.append(row.split(' '))
          except:
            print('There was an error in your matrix formatting. Please restart the program and try again.')

        break
      else:
        puzzleChoice = input('That choice was not valid. Please type "1" to use a default puzzle or "2" to enter your own puzzle: ')

    print('\n')
    print('1) Uniform Cost Search')
    print('2) A* with the Misplaced Tile Heuristic')
    print('3) A* with the Eucledian Distance Heuristic')
    print('\n')

    algoChoice = input('Select your choice of algorithm by entering the number associated: ')

    while True:
      if algoChoice == "1":
        Problem(eightPuzzleMatrix).uniformCostSearch()
        break
      elif algoChoice == "2":
        break
      elif algoChoice == "3":
        break
      else:
        algoChoice = input('Your input was not valid. Select your choice of algorithm by entering the number associated: ')

        print('1) Uniform Cost Search')
        print('2) A* with the Misplaced Tile Heuristic')
        print('3) A* with the Eucledian Distance Heuristic')

if __name__ == '__main__':
  Startup().main()
