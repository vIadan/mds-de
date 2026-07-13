from .models import Player
from .strategy import SocialGolferStrategy
from .tournament import Tournament
import logging
from app.logging_config import ColorFormatter

handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter('[%(asctime)s] (%(origin)s) - %(message)s'))
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    players = [Player(id=i) for i in range(12)]
    strategy = SocialGolferStrategy()
    tournament = Tournament(players=players, num_tables=3, players_per_table=4, strategy=strategy)
    result = tournament.run()
    logging.info(f'Tournament finished. {result}', extra={'origin': 'Tournament'})
