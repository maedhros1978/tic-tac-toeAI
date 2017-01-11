# Simple Tic-Tac-Toe AI. 
# - A 0 is be a 'O' and a 1 is an 'X'
# - A board is a length 9 list of 0s and 1s or 'e' for empty

from __future__ import division
from __future__ import print_function

class EndGame(Exception):
    """Exception raised when game ends"""
    pass

import random

def main():
    """Simple AI playing tic-tac-toe. You start! Just select where to put
    your cross on the ASCII board, by entering numbers from 1 to 9, and the
    program will respond. Its strategy is simple, but winning is not always
    easy."""
    def play_next_move(board):
        """Main AI decision making. Strategy: it looks for places where it can win,
        and play if one is found. If none are found it looks for places where the
        opponent can win, and stop them. If none are found it looks for places where
        it can win at its next move. If none are found it just plays randomly."""
        possibilities = get_empty_positions(board)
        for trial in possibilities:
            if evaluate_board(place_one(board, trial, 0)) == -1:
                return place_one(board, trial, 0)
        for trial in possibilities:
            if evaluate_board(place_one(board, trial, 1)) == 1:
                return place_one(board, trial, 0)
        for trial in possibilities:
            bd = place_one(board, trial, 0)
            new_possibilities = get_empty_positions(bd)
            for new_trial in new_possibilities:
                bd2 = place_one(bd, new_trial, 1)
                new_possibilities2 = get_empty_positions(bd2)
                for new_trial2 in new_possibilities2:
                    if evaluate_board(place_one(bd2, new_trial2, 0)) == -1:
                        return place_one(board, trial, 0)
        choice = random.sample(possibilities, 1)[0]
        return place_one(board, choice, 0)
    
    def get_empty_positions(board):
        """1-based position of empty places on board."""
        return [i+1 for i, x in enumerate(board) if x == 'e']
    
    def evaluate_board(board):
        """Given a board, return who is winning:
        - -1 for O
        -  1 for X
        -  0 in case of even game"""
        # Definition of winning sets
        rows = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
        columns = ((0, 3, 6), (1, 4, 7), (2, 5, 8))
        diagonals = ((0, 4, 8), (2, 4, 6))
        winning_conditions = (rows, columns, diagonals)
        
        value = 0
        for wc in winning_conditions:
            for triple in wc:
                if board[triple[0]] == board[triple[1]] and board[triple[1]] == board[triple[2]]\
                and board[triple[0]] != 'e':
                    value = -1 if board[triple[0]] == 0 else 1
        return value
    
    def print_board(board):
        """ASCII board printing"""
        dictionary = {
              0: 'O',
              1: 'X',
            'e': ' '
        }
        print(
""" -----------
| {} | {} | {} |
|---|---|---|
| {} | {} | {} |
|---|---|---|
| {} | {} | {} |
 -----------""".format(*(
                dictionary[i] for i in board)))
    
    def place_one(board, place, sign):
        if place == 1:
            return [sign] + board[1:]
        elif place == 9:
            return board[:8] + [sign]
        elif place in [2, 3, 4, 5, 6, 7, 8]:
            return board[:place-1] + [sign] + board[place:]
    
    def check_victory(board):
        """Check if one of the player has won."""
        standing = evaluate_board(board)
        if standing == 1:
            print_board(board)
            print('You won!')
            raise(EndGame)
        elif standing == -1:
            print_board(board)
            print('You loose!')
            raise(EndGame)
        elif 'e' not in board:
            print_board(board)
            print('Even game')
            raise(EndGame)
    
    game_board = 9 * ['e'] # Empty board
    answer = ''
    while answer != 'q':
        print_board(game_board)
        while answer not in ['q'] + map(str, get_empty_positions(game_board)):
            answer = raw_input("1-9 for choosing a spot, q for quit: ")
        if answer != 'q':
            answer = int(answer)
            game_board = place_one(game_board, answer, 1)
            try:
                check_victory(game_board)
            except(EndGame):
                return
            game_board = play_next_move(game_board)
            try:
                check_victory(game_board)
            except(EndGame):
                return
    return

if __name__ == '__main__':
    main()