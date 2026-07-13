from bonus.models import Table, Player, Round
from bonus.strategy import RandomSittingStrategy, SocialGolferStrategy
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

def test_social_golfer_minimizes_repeated_pairings():
    players_social = [Player(id=i) for i in range(12)]
    players_random = [Player(id=i) for i in range(12)]

    social_rounds = SocialGolferStrategy().generate_schedule(players_social, num_tables=3, players_per_table=4)
    random_rounds = RandomSittingStrategy().generate_schedule(players_random, num_tables=3, players_per_table=4)

    def max_pair_count(rounds):
        pair_count = {}
        for round in rounds:
            for table in round.tables:
                for i in range(len(table.players)):
                    for j in range(i + 1, len(table.players)):
                        # use sorted tuple so (a,b) and (b,a) map to the same key
                        pair = (min(table.players[i].id, table.players[j].id), max(table.players[i].id, table.players[j].id))
                        pair_count[pair] = pair_count.get(pair, 0) + 1
        return max(pair_count.values())

    # social golfer strategy should produce fewer repeated pairings than random
    assert max_pair_count(social_rounds) < max_pair_count(random_rounds)