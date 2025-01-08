from src.pybet import queries
from src.pybet import message_bus, unit_of_work, commands, schema
import datetime 
import pytest

class TestMyBetsQuery:
    @pytest.fixture(autouse=True)
    def setup(self, in_memory_sqlite_session_factory):
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)
        self.user_id = 1
        self.gameround_id = 1
        self.tommorow = datetime.datetime.now() + datetime.timedelta(days=1)

        teams = [
            schema.Team(name="A"),
            schema.Team(name="B"),
            schema.Team(name="C"),
            schema.Team(name="D")
        ]
        with self.uow:
            for t in teams:
                self.uow.session.add(t)
            self.uow.session.commit()

        message_bus.handle(commands.CreateMatchCommand(home_team_id=1, away_team_id=2, gameround_id=self.gameround_id, kickoff=self.tommorow), self.uow)
        message_bus.handle(commands.CreateMatchCommand(home_team_id=3, away_team_id=4, gameround_id=self.gameround_id, kickoff=self.tommorow), self.uow)
        message_bus.handle(commands.MakeBetCommand(self.user_id, 1, 2, 3), self.uow)
        
        self.result = queries.mybets(self.user_id, self.gameround_id, self.uow)

    @property
    def matches(self):
        return self.result["matches"]

    @property
    def first_match(self):
        return next((row for row in self.matches if row["home_team_id"] == 1), None)
    
    @property 
    def second_match(self):
        return next((row for row in self.matches if row["home_team_id"] == 3), None)
    
    def test_both_team_are_fetched(self):
        assert self.first_match is not None
        assert self.second_match is not None
        
    def test_mybets_view_returns_correct_number_of_matches(self):
        assert len(self.matches) == 2

    def test_first_match_have_a_bet(self):
        assert self.first_match["bet"] is not None

    def test_mybets_view_contains_second_match(self):
        assert self.second_match is not None
        
    def test_second_match_doesnt_have_a_bet(self):
        assert self.second_match["bet"] is None
        
    def test_returns_kickoff_as_datetime(self):
        assert isinstance(self.first_match["kickoff"], datetime.datetime)

    def test_bet(self):
        bet = self.first_match["bet"]
        bet is not None
        bet["home_team_score"] == 2
        bet["away_team_score"] == 3
        
    def test_other_user_doesnt_have_any_bets(self):
        other_user_id = 2
        result = queries.mybets(other_user_id, self.gameround_id, self.uow)
        matches = result["matches"]
        
        first_match = next((row for row in matches if row["home_team_id"] == 1), None)
        second_match = next((row for row in matches if row["home_team_id"] == 3), None)
        
        assert first_match["bet"] is None
        assert second_match["bet"] is None
