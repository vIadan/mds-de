from abc import ABC, abstractmethod
from bonus.models import Table, Round
import random

class SittingStrategy(ABC):
    
    @abstractmethod
    def generate_schedule(self, players: list, num_tables: int, players_per_table: int):
        pass

class RandomSittingStrategy(SittingStrategy):

    def generate_schedule(self, players, num_tables, players_per_table):
        num_rounds = len(players)
        rounds = []

        for _ in range(num_rounds):
            random.shuffle(players)
            tables = []
            
            for start in range(0, num_tables*players_per_table, players_per_table):
                player_group = players[start:start+players_per_table]
                tables.append(Table(player_group))
                
            rounds.append(Round(tables))
        
        return rounds
    
class SocialGolferStrategy(SittingStrategy):

    def generate_schedule(self, players, num_tables, players_per_table):
        pair_count = {}
        rounds = []
        num_rounds = len(players)

        for _ in range(num_rounds):
            available = players.copy()
            random.shuffle(available)
            tables = []

            for _ in range(num_tables):
                if len(available) < players_per_table:
                    break

                table_players, available = self._select_table(available, pair_count, players_per_table)

                # update pair counts for all new pairs at this table
                for i in range(len(table_players)):
                    for j in range(i + 1, len(table_players)):
                        pair = (min(table_players[i].id, table_players[j].id),
                                max(table_players[i].id, table_players[j].id))
                        pair_count[pair] = pair_count.get(pair, 0) + 1

                tables.append(Table(table_players))

            rounds.append(Round(tables))

        return rounds

    def _select_table(self, available_players, pair_count, players_per_table):
        # seed the table with the first available player
        table = [available_players[0]]
        remaining = available_players[1:]

        while len(table) < players_per_table and remaining:
            best_player = None
            best_score = float('inf')

            for candidate in remaining:
                # calculate how many times this candidate has already sat with everyone at the table
                score = 0
                for seated in table:
                    pair = (min(candidate.id, seated.id), max(candidate.id, seated.id))
                    score += pair_count.get(pair, 0)

                # pick the candidate with the lowest score - fewest repeated pairings
                if score < best_score:
                    best_score = score
                    best_player = candidate

            table.append(best_player)
            remaining.remove(best_player)

        return table, remaining