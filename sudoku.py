import os
import sys
import time
import threading
from operator import is_not
from functools import partial
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Number(threading.Thread):
    def __init__(self, x, y, board, val=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = f"{x},{y}"
        self.x = x
        self.y = y
        self.val = val
        self.board = board
        self.all_allowed_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        if self.val == 0:
            self.possible_values = self.all_allowed_values
        else:
            self.possible_values = [None]*9
            self.possible_values[val-1] = val

    def get_number(self):
        return self.val

    def get_possible_values(self):
        return self.possible_values

    def get_not_possible_values(self):
        ret = []
        for i in range(0, 9):
            ret.append(None if self.possible_values[i] is not None else i+1)
        return ret

    def run(self):
        if self.val != 0:
            return
        while True:
            if self.val != 0:
                logger.info(f"{self.x} {self.y} = {self.val}")
                return
            
            not_possible_row_vals = []
            for i in range(0, len(self.board[0])):
                if i == self.y:
                    continue 
                num = self.board[self.x][i]
                not_possible_row_vals.append(num.get_not_possible_values())
                if num.get_number() != 0:
                    self.possible_values[num.get_number()-1] = None

            not_possible_row_vals = set.intersection(*[set(x) for x in not_possible_row_vals])

            not_possible_col_vals = []
            for i in range(0, len(self.board[0])):
                if i == self.x:
                    continue
                num = self.board[i][self.y]
                not_possible_col_vals.append(num.get_not_possible_values())
                if num.get_number() != 0:
                    self.possible_values[num.get_number()-1] = None

            not_possible_col_vals = set.intersection(*[set(x) for x in not_possible_col_vals])

            starting_row = int(self.x/3)*3
            ending_row = starting_row+3

            starting_col = int(self.y/3)*3
            ending_col = starting_col+3

            not_possible_box_vals = []
            for i in range(starting_row, ending_row):
                for j in range(starting_col, ending_col):
                    if i == self.x and j == self.y:
                        continue
                    num = self.board[i][j]
                    not_possible_box_vals.append(num.get_not_possible_values())
                    if num.get_number() != 0:
                        self.possible_values[num.get_number()-1] = None

            not_possible_box_vals = set.intersection(*[set(x) for x in not_possible_box_vals])

            all_not_possible_vals = [list(not_possible_row_vals)+list(not_possible_col_vals)+list(not_possible_box_vals)]
            not_possible = set.intersection(*[set(x) for x in all_not_possible_vals])
            not_possible = list(filter(partial(is_not, None), list(not_possible)))
            if len(not_possible) == 1:
                logger.info(f"{self.x} :  {self.y} : {not_possible}")
                self.val = not_possible[0]
                continue

            possible_vals = list(filter(partial(is_not, None), self.possible_values))
            if len(possible_vals) == 1:
                self.val = possible_vals[0]

class Sudoku:
    def __init__(self, rows, cols, vals):
        self.vals = []
        self.rows = rows
        self.cols = cols

        for i in range(0, rows):
            self.vals.append([None]*cols)

        for i in range(0, rows):
            for j in range(0, cols):
                self.vals[i][j] = Number(i, j, self.vals, vals[i][j])

    def start(self):
        #self.vals[1][3].start()
        #return
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                self.vals[i][j].start()

        #for i in range(0, self.rows):
        #    for j in range(0, self.cols):
        #        self.vals[i][j].join()


    def is_done(self):
        done=True

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if self.vals[i][j].get_number() == 0:
                    done=False

        return done
    
    def get(self, x, y):
        return self.vals[x][y].get_number()

def Solve():
    sudoku = Sudoku(9, 9, 
        [
            [9, 5, 7, 6, 1, 3, 2, 8, 4],
            [4, 8, 3, 2, 5, 7, 1, 9, 6],
            [6, 1, 2, 8, 4, 9, 5, 3, 7],
            [1, 7, 8, 3, 6, 4, 9, 5, 2],
            [5, 2, 4, 9, 0, 1, 3, 6, 8],
            [3, 6, 9, 5, 2, 8, 7, 4, 1],
            [8, 4, 5, 7, 9, 2, 6, 1, 3],
            [2, 9, 1, 4, 3, 6, 8, 7, 5],
            [7, 3, 6, 1, 8, 5, 4, 2, 9],
        ])

    sudoku = Sudoku(9, 9, 
        [
            [0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 8, 0, 0, 0, 7, 0, 9, 0],
            [6, 0, 2, 0, 0, 0, 5, 0, 0],
            [0, 7, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 9, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 4, 0],
            [0, 0, 5, 0, 0, 0, 6, 0, 3],
            [0, 9, 0, 4, 0, 0, 0, 7, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
        ])

    sudoku = Sudoku(9, 9, 
        [
            [0, 0, 0, 0, 0, 0, 2, 0, 0],
            [0, 8, 0, 0, 0, 7, 0, 9, 0],
            [6, 0, 2, 0, 0, 0, 5, 0, 0],
            [0, 7, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 9, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 4, 0],
            [0, 0, 5, 0, 0, 0, 6, 0, 3],
            [0, 9, 0, 4, 0, 0, 0, 7, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
        ])

    sudoku = Sudoku(9, 9, 
        [
            [0, 7, 0, 5, 8, 3, 0, 2, 0],
            [0, 5, 9, 2, 0, 0, 3, 0, 0],
            [3, 4, 0, 0, 0, 6, 5, 0, 7],
            [7, 9, 5, 0, 0, 0, 6, 3, 2],
            [0, 0, 3, 6, 9, 7, 1, 0, 0],
            [6, 8, 0, 0, 0, 2, 7, 0, 0],
            [9, 1, 4, 8, 3, 5, 0, 7, 6],
            [0, 3, 0, 7, 0, 1, 4, 9, 5],
            [5, 6, 7, 4, 2, 9, 0, 1, 3],
        ])

def solve(input):
    sudoku = Sudoku(9, 9, input)

    sudoku.start()

    heighest = 0

    while True:
        completed = 0
        time.sleep(1)

        for i in range(0, 9):
            for j in range(0, 9):
                num = sudoku.get(i, j)
                if num != 0:
                    completed += 1

        if heighest < completed:
            print("\n")
            heighest = completed
            for i in range(0, 9):
                for j in range(0, 9):
                    num = sudoku.get(i, j)
                    print(f"{num} ", end="")
                print("")

        if sudoku.is_done() is True:
            print("Done")
            break

def solve_from_file():
    with open("Dataset", 'r') as fp:
        lines = fp.readlines()

        for line in lines:
            data = line.split(",")[0]
            input = [[0 for _ in range(9)] for _ in range(9)]
            for i in range(0, 9):
                for j in range(0, 9):
                    input[i][j] = int(data[i*9+j])
            solve(input)

solve_from_file()

print("Done")