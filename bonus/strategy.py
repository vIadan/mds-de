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