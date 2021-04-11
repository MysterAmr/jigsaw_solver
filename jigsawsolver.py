import random #importing the random module
import sys #importing the sys modeult
import numpy as np #importing the numpy module to use for matrix operations
import matplotlib.pyplot as plt #importing the matplotlib module to use for plotting
sys.setrecursionlimit(2000) #set limit for maximum recursion calls


class PuzzlePiece: #Class which will generate puzzle piece
  def __init__(self, connected_pieces = [], secret_id = ()): #The constructor for the class
    self.connected_pieces = connected_pieces #list of puzzle pieces which are connected
    self.secret_id = secret_id #An x y coordinate id

  def connect_to(self, other): #This method connect two pieces to one another
    other.connected_pieces.append(self)
    self.connected_pieces.append(other)

  def __str__(self): #This returns the secret id
    return self.secret_id

class Puzzle: #Class which creates the entire puzle
  def __init__(self): #constructor for the puzzle class
    self.pieces = [] #List of puzzle pieces
    puzzle_grid = [[PuzzlePiece([], (i,j)) for j in range(10)] for i in range(10)] #A grid of all of the puzzle pieces. PuzzlePiece is called to randomly generate a piece

    for i in range(10):
      for j in range(10):
        if i != 9: #if this piece is not at the right edge
          puzzle_grid[i][j].connect_to(puzzle_grid[i+1][j]) #it will connect the i,j piece to the i+1,j piece
        if i != 0: #if this piece is not at the left edge
          puzzle_grid[i][j].connect_to(puzzle_grid[i-1][j]) #it will connect the i,j piece to the ii1,j piece
        if j != 9: #if this piece is not at the bottom edge
          puzzle_grid[i][j].connect_to(puzzle_grid[i][j+1]) #it will connect the i,j piece to the i,j+1 piece
        if j != 0: #if this piece is not at the top edge
          puzzle_grid[i][j].connect_to(puzzle_grid[i][j-1]) #it will connect the i,j piece to the i,j-1 piece
        
    for i in range(10):
      for j in range(10):
        self.pieces.append(puzzle_grid[i][j]) #append each piece from the puzzle grid to the pieces list

  def random_piece(self, exclude): #This method will choose a random piece from the pieces list
    R = random.choice(self.pieces) #call choice function to randomly choose element
    while R in exclude: #if R is in exclude
      R = random.choice(self.pieces) #choose another piece
    return R #return random piece

  def p_solve(self, num, exclude = [], success = []): #this method will actually solve the puzzle
    P = self.random_piece(exclude) #choose a random piece
    num += 1 #everytime a random piece is picked, add 1 to num
    for i in success: #iterate through the solve puzzle pieces
      if P in i.connected_pieces: #if P is connected to some piece in success
        if P not in success: #if P was not yet solved
          success.append(P) #append P to the success list
          exclude.append(P) #append P to be excluded
    
    if len(success) < 100: #if the entire puzzle has not yet been solved (i.e., all 100 pieces were solved)
      return self.p_solve(num, exclude, success) #recursively call the p_solve method
    else: #if the entire puzzle has been solved
      print("%d random pieces were picked up!" % num) #print the number of times a random piece was chosen
      return success #return the list of solved pieces

  def p_solve_table(self): #This is a method to display the completed puzzle
    L = self.p_solve(1, [], [self.random_piece([])]) #Assign the completed puzzle to L
    arr = np.empty([10,10]) #Create an empty array
    fig, ax = plt.subplots() #Create a figure and axis
    ax.set_axis_off()
    xCoordinate = [i.secret_id[0] for i in L] #assign x coordinates of the secret id of each piece to xCoordinate
    yCoordinate = [i.secret_id[1] for i in L] #assign y coordinates of the secret id of each piece to yCoordinate
    for i in range(100):
      arr[xCoordinate[i]][yCoordinate[i]] = i+1 #fill up the matrix with the labels of pieces in the order they were solved
    table = ax.table(cellText = arr.astype(int), loc='center') #create the table and center it
    ax.set_title("Jigsaw Puzzle") #Title the table
    plt.savefig("Puzzle.png") #Save the table
    plt.show() #Display the table
