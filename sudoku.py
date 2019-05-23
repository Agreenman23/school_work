#Alex Greenman
#873392313

#This script contains a class "Puzzle". Puzzle represents a 6x6 Sudoku puzzle
#and has a single attribute 'board', which is a list of lists of integers.
#Within the class there are methods that perform validity checks on the board's
#contents, create a string representation of the board, return a set of possible
#options for a given square on the board, and solve the puzzle. There is also
#a main function that loads a puzzle from a text file and solves that puzzle.


import copy

class Puzzle:
    '''This class represents a 6x6 Sudoku puzzle

    Attributes:
        board: a list of lists containing integers
    '''
    def __init__(self, board):
        #set board attribute with deep copy of board
        self.board=copy.deepcopy(board)
        #conduct validity checks
        if type(board) != list:
            raise ValueError('board must be a list')
        if any(type(elements) != list for elements in board) == True:
            raise ValueError('board contains elements of type other than list')
        if any(len(elements) !=6 for elements in board) == True:
            raise ValueError('board contains a list with length != 6')
        #check that board only contains integers between 0 and 6
        for elements in board:
            if all(0<=x<=6 for x in elements) != True:
                raise ValueError('board contains a number that is not between 0 and 6')

    def __str__(self):
        empty_string = ''
        for elements in self.board:
            #convert 0s on left half of puzzle to underscores, add to string
            #convert non-zero ints on left half to strings, add to string
            for numbers in elements[:3]:
                if numbers == 0:
                    empty_string += '_'
                else:
                    empty_string += str(numbers)
                empty_string+= ' '
            #convert 0s on right half of puzzle to underscores, add to string
            #convert non-zero ints on right half to strings, add to string
            for numbers in elements[3:]:
                if numbers == 0:
                    empty_string += '_'
                else:
                    empty_string += str(numbers)
                empty_string+= ' '
            #add newlines to string so it displays like a board
            empty_string+='\n'
        return empty_string

    def options(self,row, col):
        '''This method return the set of the possible options for
        a given square'''
        board_2x3 = set()
        #create lists to be used later that contain the coordinates for each
        #square in each 2x3 subsection of the puzzle
        upper_left_coordinates = [self.board[0][0], self.board[0][1], self.board[0][2],
        self.board[1][0], self.board[1][1], self.board[1][2]]
        middle_left_coordinates = [self.board[2][0], self.board[2][1], self.board[2][2],
        self.board[3][0], self.board[3][1], self.board[3][2]]
        lower_left_coordinates = [self.board[4][0], self.board[4][1], self.board[4][2],
        self.board[5][0], self.board[5][1], self.board[5][2]]
        upper_right_coordinates = [self.board[0][3], self.board[0][4], self.board[0][5],
        self.board[1][3], self.board[1][4], self.board[1][5]]
        middle_right_coordinates = [self.board[2][3], self.board[2][4], self.board[2][5],
        self.board[3][3], self.board[3][4], self.board[3][5]]
        lower_right_coordinates = [self.board[4][3], self.board[4][4], self.board[4][5],
        self.board[5][3], self.board[5][4], self.board[5][5]]
        #update set to contain each value in upper left 2x3 box of the puzzle
        if 0 <= row <= 1 and 0 <= col <= 2:
            board_2x3.update(upper_left_coordinates)
        #update set to contain each value in middle left 2x3 box of the puzzle
        elif 2 <= row <= 3 and 0 <= col <= 2:
            board_2x3.update(middle_left_coordinates)
        #update set to contain each value in lower left 2x3 box of the puzzle
        elif 4 <= row <= 5 and 0 <= col <= 2:
            board_2x3.update(lower_left_coordinates)
        #update set to contain each value in upper right 2x3 box of the puzzle
        elif 0 <= row <= 1 and 3 <= col <= 5:
            board_2x3.update(upper_right_coordinates)
        #update set to contain each value in middle right 2x3 box of the puzzle
        elif 2 <= row <= 3 and 3 <= col <= 5:
            board_2x3.update(middle_right_coordinates)
        #update set to contain each value in lower right 2x3 box of the puzzle
        elif 4 <= row <= 5 and 3 <= col <= 5:
            board_2x3.update(lower_right_coordinates)
        else:
            print('invalid row/col')
        #create empty sets to store each value in the given row and column
        col_in_question = set()
        row_in_question = set()
        all_possible_values={1,2,3,4,5,6}
        i=0
        #update sets to contain each value in the given row and column
        while i < 6:
            row_in_question.add(self.board[row][i])
            col_in_question.add(self.board[i][col])
            i+=1
        #subtract sets containg row, col, and 2x3 square values to produce
        #set of possible options for a given square
        outcome_set = all_possible_values-board_2x3-col_in_question-row_in_question
        return outcome_set


    def solve(self):
        '''This method recursively solves the puzzle, returns True if a
        solution was found, and False if no solution exists'''
        #display the puzzle
        print(self)
        #search for blank space
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == 0:
                    #blank space detected, calculate all
                    #possible values that could go in given square
                    options = self.options(row, col)
                    #if no possible solutions, return False to indicate an issue
                    if len(options) == 0:
                        return False
                    #fill in blanks w/values, recursively solve rest of puzzle
                    for option in options:
                        new_board = Puzzle(self.board)
                        new_board.board[row][col] = option
                        #if puzzle solved, return True, indicate solution found
                        if new_board.solve():
                            return True
                    #ran out of options, return False, keep trying values
                    return False
        #no zeroes left, puzzle is solved
        return True


if __name__ == '__main__':
    #read in unsolved puzzle txt file, convert to list of lists of integers
    with open('puzzle2.txt', "r") as file:
        myboard = file.read()
        new_board = myboard.split()

    new_board = list(map(int,new_board))
    new_board = [new_board[x:x+6] for x in range(0, len(new_board), 6)]

    #pass in the board to the Puzzle class, solve
    board_well = Puzzle(new_board)
    board_well.solve()
