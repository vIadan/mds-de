from bonus.models import Table, Player, Round
from bonus.strategy import RandomSittingStrategy
from bonus.tournament import Tournament

def test_table_play():
    players = [Player(id=i) for i in range(4)]
    table = Table(players)
    winner = table.play()

    assert winner in players
    assert winner.num_wins == 1

def test_round_play():
    players = [Player(id=i) for i in range(12)]
    table1 = players[0:4]
    table2 = players[4:8]
    table3 = players[8:12]
    tables = [Table(table1), Table(table2), Table(table3)]

    round = Round(tables)
    winners = round.play()

    assert len(winners) == 3

def test_tournament_winner_has_most_wins():
    players = [Player(id=i) for i in range(12)]
    strategy = RandomSittingStrategy()
    tournament = Tournament(players=players, num_tables=3, players_per_table=4, strategy=strategy)
    result = tournament.run()

    for player in players:
        if player.id == result.winner.id:
            continue

        assert result.winner.num_wins >= player.num_wins