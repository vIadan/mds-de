import random

class Player:

    def __init__(self, id):
        self.id = id
        self.num_wins = 0

    def record_win(self):
        self.num_wins += 1

    def __repr__(self):
        return f'Player_{self.id} with {self.num_wins} wins'

class Table:

    def __init__(self, players: list):
        self.players = players
    
    def play(self):
        winning_player = random.choice(self.players)
        winning_player.record_win()

        return winning_player
    
class Round:

    def __init__(self, tables: list):
        self.tables = tables

    def play(self):
        winners = []

        for table in self.tables:
            winner = table.play()
            winners.append(winner)

        return winners
    
class TournamentResult:

    def __init__(self, winner: Player, round_history: list):
        self.winner = winner
        self.round_history = round_history

    def __repr__(self):
        return f'Tournament result -> winner: {self.winner}, rounds={len(self.round_history)}'