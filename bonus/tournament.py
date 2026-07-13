from bonus.strategy import SittingStrategy
from bonus.models import TournamentResult
import logging

LOG = {'origin': 'Tournament'}

class Tournament:

    def __init__(self, players: list, num_tables: int, players_per_table: int, strategy: SittingStrategy):
        self.players = players
        self.num_tables = num_tables
        self.players_per_table = players_per_table
        self.strategy = strategy

    def run(self):
        num_rounds = len(self.players)
        logging.info(
            f'Tournament starting: {len(self.players)} players, {num_rounds} rounds, '
            f'{self.num_tables} tables of {self.players_per_table} using {self.strategy.__class__.__name__}',
            extra=LOG
        )

        round_history = []
        rounds = self.strategy.generate_schedule(self.players, self.num_tables, self.players_per_table)

        for i, round in enumerate(rounds, start=1):
            winners = round.play()
            round_history.append(winners)
            winner_names = ', '.join(str(w) for w in winners)
            logging.info(f'Round {i}/{num_rounds} complete — winners: {winner_names}', extra=LOG)

        overall_winner = max(self.players, key=lambda p: p.num_wins)

        return TournamentResult(winner=overall_winner, round_history=round_history)