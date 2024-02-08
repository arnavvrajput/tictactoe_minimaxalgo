# Creating different types of players
# 1. Human Player ( Takes input from the console )
# 2. Random Computer Player ( Makes a random move from the available move )
# 3. Smart Computer Player ( Chooses the best possible move to win or make it a tie but never loses )




import math
import random


class Player(): # A big class which comprises of different class of players
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player): # Human player to get the move from the input
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square: # Checking if the move is valid or not
            square = input(self.letter + '\'s turn. Input move (0-9): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


class RandomComputerPlayer(Player): # Random computer player to choose any random move from the available moves
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class SmartComputerPlayer(Player): # Smart computer player which will use predefined Minimax Algorithm Function
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        # First we want to check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # Each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # Each score should minimize
        for possible_move in state.available_moves(): # This loop simulates each and every move possible and until it reaches the final state/winning move
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # Simulate a game after making that move

            # Each simulated move is deleted and the move which made the player win is recorded in sim_score
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best