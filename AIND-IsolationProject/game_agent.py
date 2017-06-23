"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
from random import randint

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")



    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    score_player = 0
    score_opponent = 0

    def quality_legal_moves(game, legal_move_play):
        y_legal_move, x_legal_move = legal_move_play
        w, h = game.width / 2., game.height / 2.
        dist_from_center_x,dist_from_center_y = abs(x_legal_move - h), abs(y_legal_move - w)
        if (dist_from_center_x <= h-1 and dist_from_center_y <= w-1):
            score_for_this_legal_move = 4.
        elif (dist_from_center_x > h-1 and dist_from_center_y <= w-1) or (dist_from_center_x <= h-1 and dist_from_center_y > w-1):
            score_for_this_legal_move = 3.
        elif (dist_from_center_x > h-1 and dist_from_center_y > w-1):
            score_for_this_legal_move = 2.
        else:
            score_for_this_legal_move = 1.
        return score_for_this_legal_move


    for own in own_moves:
        score_player += quality_legal_moves(game, own)
    for opp in opp_moves:
        score_opponent += quality_legal_moves(game, opp)

    nett_score = score_player*float(len(own_moves)) - 1.3*score_opponent*float(len(opp_moves))



    return nett_score
    # raise NotImplementedError


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.

    y, x = game.get_player_location(player)
    score_center = float((h - y)**2 + (w - x)**2)

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    diff_open_moves = float(own_moves - opp_moves)

    score_open_moves = float(len(game.get_legal_moves(player)))

    linear_score_combination = 0.6*score_center + 0.3*diff_open_moves + 0.1*score_open_moves

    return linear_score_combination
    # raise NotImplementedError


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_location = game.get_player_location(player) #(x,y)
    opposition_player = game.get_opponent(player)
    opposition_location = game.get_player_location(opposition_player) #(x,y)
    diff_location_x = opposition_location[0] - player_location[0] 
    diff_location_y = opposition_location[1] - player_location[1] 
    score_loc_difference = abs(diff_location_x) + abs(diff_location_y)

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    score_center = float((h - y)**2 + (w - x)**2)

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    diff_open_moves = float(own_moves - opp_moves)

 

    linear_score_combination = 0.4*score_center + 0.2*diff_open_moves  + 0.4*score_loc_difference

    return linear_score_combination


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        def MINIMAX_DECISION(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            legal_moves = game.get_legal_moves()
            # print(legal_moves)
            if (depth == 0 or not game.get_legal_moves()): 
                return game.get_player_location(self)
            else:
                # _, best_move = max(self.min_value(game.forecast_move(m), depth-1), for m in legal_moves)
                best_move = max(legal_moves, key = lambda m: min_value(game.forecast_move(m), depth-1))

                return best_move

        def max_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if (depth == 0 or not game.get_legal_moves()):
                return self.score(game, self)
            else:
                v = float("-inf")
                legal_moves = game.get_legal_moves()
                # print(legal_moves)
                for mov in legal_moves:
                    v = max(v, min_value(game.forecast_move(mov), depth-1))
                return v

        def min_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if (depth == 0 or not game.get_legal_moves()):
                return self.score(game, self)
            else:
                v = float("inf")
                legal_moves = game.get_legal_moves()
                # print(legal_moves)
                for mov in legal_moves:
                    v = min(v, max_value(game.forecast_move(mov), depth-1))
                return v

        return  MINIMAX_DECISION(game, depth)

                
        # for each legal move  apply the min_value(state, depth-1) function, this will give the utility for each of the possible
        # moves and pick the move that corresponds to maximum value amongst these
                



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        # raise NotImplementedError

        if (game.get_legal_moves()):
            legal_moves = game.get_legal_moves()
            best_move = legal_moves[randint(0, len(legal_moves) - 1)]
            previous_best_move = best_move
        # else:
        # best_move = (-1, -1)
        # previous_best_move = best_move

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            for deep in range(1,100000000):
                best_move = self.alphabeta(game,deep)
                previous_best_move = best_move
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()


        except SearchTimeout:
            # pass  # Handle any actions required after timeout as needed
            best_move = previous_best_move

        # Return the best move from the last completed search iteration
        return best_move



    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        # raise NotImplementedError



        def ALPHA_BETA_SEARCH(game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            best_move = (-1,-1)
            if (game.get_legal_moves()):
                legal_moves = game.get_legal_moves()
                best_move = legal_moves[randint(0, len(legal_moves) - 1)]

            if (depth == 0 or not game.get_legal_moves()): 
                return game.get_player_location(self)
            else:

                best_score = float("-inf")

                for mov in legal_moves:
                    v = min_value(game.forecast_move(mov), depth-1, alpha, beta) # heuristic at depth = 1
                    if v>best_score:
                        best_move = mov
                        best_score = v

                    alpha = max(alpha, v) # update alpha 


            return best_move


        def max_value(game, depth, alpha, beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if (depth == 0 or not game.get_legal_moves()):
                return self.score(game, self)
            else:
                v = float("-inf")
                legal_moves = game.get_legal_moves()
                for mov in legal_moves:
                    v = max(v, min_value(game.forecast_move(mov), depth-1, alpha, beta))
                    if v >= beta:
                        return v 
                    else:
                        alpha = max(alpha, v)
                return v

        def min_value(game, depth, alpha , beta):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            if (depth == 0 or not game.get_legal_moves()):
                return self.score(game, self)
            else:
                v = float("inf")
                legal_moves = game.get_legal_moves()
                for mov in legal_moves:
                    v = min(v, max_value(game.forecast_move(mov), depth-1, alpha, beta))
                    if v <= alpha:
                        return v 
                    else:
                        beta = min(beta, v)
                return v

        return  ALPHA_BETA_SEARCH(game, depth, alpha, beta)
