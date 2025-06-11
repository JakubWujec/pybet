from pybet import schema


class TestGamestage:
    def test_can_create_gamestage(self):
        gamestage = schema.Gamestage(name="Gameweek 1")

        assert gamestage is not None
        assert isinstance(gamestage, schema.Gamestage)

    def test_can_add_match(self):
        gamestage = schema.Gamestage(name="Gameweek 1")
        match = schema.Match(home_team_id=1, away_team_id=2, gameround=1)
        gamestage.add_match(match)

        assert len(gamestage.matches) == 1
        assert gamestage.matches[0] == match
