"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
from copy import deepcopy


# TODO: you can import more modules, if needed
class MinMaxState:
    def __init__(self, board, penalty_score):
        self.fruit_turn_timer = min(len(self.current_board), len(self.current_board[0]))
        self.penalty_score = penalty_score
        self.current_board = board
        self.available_fruits = {}
        self.removed_fruits = {}
        self.score_1 = self.score_2 = 0
        self.loc_1 = self.loc_2 = None
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i, j] == 0:
                    continue
                if board[i, j] == 1:
                    self.loc_1 = (i, j)
                if board[i, j] == 2:
                    self.loc_2 = (i, j)
                if board[i, j] > 2:
                    self.available_fruits[(i, j)] = board[i, j]
        assert (self.loc_1 is not None and self.loc_2 is not None)



class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.penalty_score = penalty_score
        self.currentStateInPlay = None
        self.currentState = None
        self.turn_counter = 0
        #TODO: ADD MINIMAX

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.currentStateInPlay = MinMaxState(board, self.penalty_score)
        self.currentState = deepcopy(self.currentStateInPlay)

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        # TODO: erase the following line and implement this function.
        raise NotImplementedError

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        if self.currentStateInPlay.current_board[pos[0], pos[1]] > 2:
            fruit_value = self.currentStateInPlay.current_board[pos[0], pos[1]]
            self.currentStateInPlay.score_2 += fruit_value
            self.currentStateInPlay.removed_fruits[pos] = fruit_value
            del self.currentStateInPlay.available_fruits[pos]
        self.currentStateInPlay.current_board[pos[0], pos[1]] = 2
        self.currentStateInPlay.current_board[self.currentStateInPlay.loc_2[0], self.currentStateInPlay.loc_2[1]] = -1
        self.currentStateInPlay.loc_2 = pos
        self.currentState = deepcopy(self.currentStateInPlay)

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # TODO: erase the following line and implement this function. In case you choose not to use it, use 'pass' instead of the following line.

    ########## helper functions in class ##########




    ########## helper functions for MiniMax algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm
