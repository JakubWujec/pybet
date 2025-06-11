from pybet import schema


class TestGamestage:
    def test_can_create_gamestage(self):
        gamestage = schema.Gamestage(name="Gameweek 1")

        assert gamestage is not None
        assert isinstance(gamestage, schema.Gamestage)
