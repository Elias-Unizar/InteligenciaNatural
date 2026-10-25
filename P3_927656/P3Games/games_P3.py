"""Games or Adversarial Search (Chapter 5)"""

from collections import namedtuple

import numpy as np

GameState = namedtuple('GameState', 'to_move, utility, board, moves')
StochasticGameState = namedtuple('StochasticGameState', 'to_move, utility, board, moves, chance')


# ______________________________________________________________________________
# MinMax Search


def minmax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


global nodosVisitados
def minimax_cutoff_search(state, game, max_depth=4, f_eval=None):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""
    global nodosVisitados
    player = game.to_move(state)
    actual_depth = 0
    nodosVisitados = 0
    def max_value(state, actual_depth):
        global nodosVisitados
        nodosVisitados += 1
        actual_depth += 1
        if game.terminal_test(state):
            return game.utility(state, player)
        if actual_depth >= max_depth:
            return 0 if f_eval == None else f_eval(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), actual_depth))
        return v

    def min_value(state, actual_depth):
        global nodosVisitados
        nodosVisitados += 1
        actual_depth += 1
        if game.terminal_test(state):
            return game.utility(state, player)
        if actual_depth >= max_depth:
            return 0 if f_eval == None else f_eval(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), actual_depth))
        return v
    # Body of minmax_decision:
    mejorAccion = max(game.actions(state), key=lambda a: min_value(game.result(state, a), actual_depth))
    best_Value = 0
    if f_eval != None: best_Value = game.result(state, mejorAccion)
    return mejorAccion, best_Value, nodosVisitados


# ______________________________________________________________________________


def alpha_beta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

global podas_realizadas
def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)
    global nodosVisitados
    global podas_realizadas
    nodosVisitados = 0
    podas_realizadas = 0
    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        global nodosVisitados
        global podas_realizadas
        nodosVisitados += 1
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                podas_realizadas += 1
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        global nodosVisitados
        global podas_realizadas
        nodosVisitados += 1
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                podas_realizadas += 1
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth >= d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action, best_score, nodosVisitados, podas_realizadas

# ______________________________________________________________________________
# Some Sample Games


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state) #Algoritmo que realiza la accion para el jugador n
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        """Place the current player's mark at move and return the new state;
        an illegal move leaves the state unchanged."""
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        """Print the board as a grid, with empty squares shown as dots."""
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k


class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def actions(self, state):
        """Return legal moves: bottom-row squares or squares directly above an occupied one."""
        return [(x, y) for (x, y) in state.moves
                if x == self.h or (x + 1 , y ) in state.board]

    def compute_utility(self, board, move, player):
            """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
            if (self.k_in_row(board, move, player, (0, 1)) or
                    self.k_in_row(board, move, player, (1, 0)) or
                    self.k_in_row(board, move, player, (1, -1)) or
                    self.k_in_row(board, move, player, (1, 1))):
                return +10 if player == 'X' else -10
            else:
                return 0
    def eval_conecta4_basica(self, state, player):
        if self.terminal_test(state):
            return self.utility(state, player)
        poderTerritorial = 0
        for (x, y), ficha in state.board.items():   # x = fila, y = columna (1..6)
            valor = y if y < 4 else 7 - y
            poderTerritorial += valor if ficha == player else -valor
        return poderTerritorial
    
    def display(self, state):
        """Dibuja el tablero: filas con '|', 'X', 'O' y '.', y debajo los números de columna 1-6."""
        print("=" * (4 * self.v + 1))
        for x in range(1, self.h + 1):
            print("| " + " | ".join(state.board.get((x, y), '.') for y in range(1, self.v + 1)) + " |")
        print("=" * (4 * self.v + 1))
        print("  " + "   ".join(str(y) for y in range(1, self.v + 1)))

