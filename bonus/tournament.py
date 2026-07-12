from bonus.strategy import SittingStrategy
from bonus.models import TournamentResult

class Tournament:

    def __init__(self, players: list, num_tables: int, players_per_table: int, strategy: SittingStrategy):
        self.players = players
        self.num_tables = num_tables
        self.players_per_table = players_per_table
        self.strategy = strategy

    def run(self):
        round_history = []
        rounds = self.strategy.generate_schedule(self.players, self.num_tables, self.players_per_table)

        for round in rounds:
            winners = round.play()
            round_history.append(winners)

        overall_winner = max(self.players, key=lambda p: p.num_wins)

        return TournamentResult(winner=overall_winner, round_history=round_history)