"""Search Algos: MiniMax, AlphaBeta
"""
from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT
import math
import time


# TODO: you can import more modules, if needed


class SearchAlgos:
    def __init__(self, utility, succ, perform_move, undo_move):
        """The constructor for all the search algos.
        You can code these functions as you like to,
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param undo_move: The undo move function
        //:param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.undo_move = undo_move

    def search(self, state, time_limit):
        pass


class MiniMax(SearchAlgos):

    def search(self, state, time_limit):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        start_time = time.time()
        depth = 1
        result = None
        while time.time() - start_time < 0.3 * time_limit: #branch factor is 3, so the last tree will take 2 times time then all previous toghether
            depth += 1
            result = self.search_helper(state, depth, 1)

        passed_time = time.time() - start_time
        remaining_time = time_limit - passed_time
        iteration_start_time = iteration_finish_time = iteration_delta = 0

        for move in self.succ():
            iteration_delta = iteration_finish_time - iteration_start_time
            iteration_start_time = time.time()
            remaining_time -= iteration_delta
            if (2/3)*passed_time < remaining_time: #the time that took to calc last tree
                self.perform_move(state, 1 , move)
                son_result = self.search_helper(state, depth, 1)
                self.undo_move(state, 1, move)
                if son_result[1] > result[1]:
                    result[0] = move
                    result[1] = son_result[1]
            iteration_finish_time = time.time()

        return result[0]

    def search_helper(self, state, depth, maximizing_player):
        if maximizing_player == 0:
            best = [None, -math.inf]
        else:
            best = [None, math.inf]
        if depth == 0:
            score = state.h()
            return [None, score]

        move = score = None
        for move in self.succ():
            self.perform_move(state, maximizing_player, move)
            [move, score] = self.search_helper(state, depth - 1, 1 - maximizing_player)
            self.undo_move(state, maximizing_player, move)

        if maximizing_player == 1:
            if score > best[1]:
                best = [move, score]
        else:
            if score < best[1]:
                best = [move, score]
        return best


class AlphaBeta(SearchAlgos):

    def search(self, state, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        raise NotImplementedError
