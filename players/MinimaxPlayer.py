"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
from copy import deepcopy
from utils import get_directions
import math
import SearchAlgos


# TODO: you can import more modules, if needed
class MinMaxState:
    def __init__(self, board, penalty_score):
        self.fruit_turn_timer = math.ceil(2*min(len(self.current_board), len(self.current_board[0])))
        self.penalty_score = penalty_score
        self.current_board = board
        self.available_fruits = {}
        self.removed_fruits = {}
        self.scores = [0, 0]
        self.turns_played = 0
        self.locations = [None, None]
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i, j] == 0:
                    continue
                if board[i, j] == 1:
                    self.locations[0] = (i, j)
                if board[i, j] == 2:
                    self.locations[1] = (i, j)
                if board[i, j] > 2:
                    self.available_fruits[(i, j)] = board[i, j]
        assert (self.locations[0] is not None and self.locations[1] is not None)


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.penalty_score = penalty_score
        self.currentStateInPlay = None
        self.currentState = None
        self.searchAlgo = SearchAlgos.MiniMax(heuristic, succ, preformMove, undoMove)

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
        move = self.searchAlgo.search(self.currentState, time_limit)
        preformMove(self.currentStateInPlay, 1, move)
        return move


    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        if self.currentStateInPlay.current_board[pos[0], pos[1]] > 2:
            fruit_value = self.currentStateInPlay.current_board[pos[0], pos[1]]
            self.currentStateInPlay.scores[1] += fruit_value
            self.currentStateInPlay.removed_fruits[pos] = fruit_value
            del self.currentStateInPlay.available_fruits[pos]
        self.currentStateInPlay.current_board[pos[0], pos[1]] = 2
        self.currentStateInPlay.current_board[
            self.currentStateInPlay.locations[1][0], self.currentStateInPlay.locations[1][1]] = -1
        self.currentStateInPlay.locations[1] = pos
        self.currentStateInPlay.turns_played += 1
        self.currentState = deepcopy(self.currentStateInPlay)


    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        pass

    ########## helper functions in class ##########

    ########## helper functions for MiniMax algorithm ##########


def succ(state, player):  # (Up/Down , Right/Left)
    assert (type(state) == MinMaxState)
    moves = []
    p_loc = state.locations[1 - player]
    dir = get_directions()
    for dir in get_directions():
        newloc = (p_loc[0] + dir[0], p_loc[1] + dir[1])
        if 0 <= newloc[0] < len(state.current_board):
            if 0 <= newloc[1] < len(state.board[0]):
                if state.current_board[newloc[0], newloc[1]] == 0 or state.current_board[newloc[0], newloc[1]] > 2:
                    moves.append(newloc)
    return moves


def heuristic(state, depth):
    pass


def preformMove(state, player, move):
    assert (type(state) == MinMaxState)
    oldloc = state.locations[1-player]
    newloc = (oldloc[0] + move[0], oldloc[1] + move[1])
    assert(state.current_board[newloc[0], newloc[1]] == 0 or state.current_board[newloc[0], newloc[1]] > 2)
    if state.current_board[newloc[0], newloc[1]] > 0 and state.turns_counter <= state.fruit_turn_timer:
        state.scores[1-player] += state.current_board[newloc[0], newloc[1]]
        state.removed_fruits[newloc] = state.available_Fruits[newloc]
        del state.available_Fruits[newloc]
    state.current_board[newloc[0], newloc[1]] = 2 - player
    state.current_board[oldloc[0], oldloc[1]] = -1
    state.locations[1-player] = newloc
    state.turns_played += 1



def undoMove(state, player, move):
    currloc = state.locations[1-player]
    prevloc = (currloc[0] - move[0], currloc[1] - move[1])
    state.turns_played -= 1
    if currloc in state.removed_fruits:
        state.available_fruits[currloc] = state.removed_fruits[currloc]
        del state.removed_fruits[currloc]
        if state.turns_counter <= state.fruit_turn_timer:
            state.scores[1-player] -= state.available_fruits[currloc]
        state.current_board[currloc[0], currloc[1]] = state.available_fruits[currloc]
    else:
        state.current_board[currloc[0], currloc[1]] = 0
    state.current_board[prevloc[0], prevloc[1]] = 2 - player
    state.locations[1 - player] = prevloc







