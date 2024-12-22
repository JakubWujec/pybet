from src.pybet import message_bus, unit_of_work, commands, views
import datetime 
import pytest

class TestMyBetsView:
    @pytest.fixture(autouse=True)
    def setup(self, in_memory_sqlite_session_factory):
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)
        self.user_id = 1
        self.tommorow = datetime.datetime.now() + datetime.timedelta(days=1)

        message_bus.handle(commands.CreateMatchCommand(1, 2, self.tommorow), self.uow)
        message_bus.handle(commands.CreateMatchCommand(3, 4, self.tommorow), self.uow)
        message_bus.handle(commands.MakeBetCommand(self.user_id, 1, 2, 3), self.uow)
        
        
        self.result = views.mybets(self.user_id, self.uow)
        self.first_match = next((row for row in self.result if row["home_team_id"] == 1), None)
        self.second_match = next((row for row in self.result if row["home_team_id"] == 3), None)


    def test_mybets_view_returns_correct_number_of_matches(self):
        assert len(self.result) == 2

    def test_first_match_have_a_bet(self):
        assert self.first_match["bet"] is not None

    def test_mybets_view_contains_second_match(self):
        assert self.second_match is not None
        
    def test_second_match_doesnt_have_a_bet(self):
        assert self.second_match["bet"] is None

    def test_bet(self):
        bet = self.first_match["bet"]
        bet is not None
        bet["home_team_score"] == 2
        bet["away_team_score"] == 3
        