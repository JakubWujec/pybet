from pybet import queries
from pybet import message_bus, unit_of_work, commands, schema
from sqlalchemy.sql import text
import datetime 
import pytest

class TestMyBetsQuery:
    @pytest.fixture(autouse=True)
    def setup(self, in_memory_sqlite_session_factory):
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)
        self.user_id = 1
        self.gameround = 1
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

        message_bus.handle(commands.CreateMatchCommand(home_team_id=1, away_team_id=2, gameround=self.gameround, kickoff=self.tommorow), self.uow)
        message_bus.handle(commands.CreateMatchCommand(home_team_id=3, away_team_id=4, gameround=self.gameround, kickoff=self.tommorow), self.uow)
        message_bus.handle(commands.MakeBetCommand(self.user_id, 1, 2, 3), self.uow)
        
        self.result = queries.mybets(self.user_id, self.gameround, self.uow)

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
        result = queries.mybets(other_user_id, self.gameround, self.uow)
        matches = result["matches"]
        
        first_match = next((row for row in matches if row["home_team_id"] == 1), None)
        second_match = next((row for row in matches if row["home_team_id"] == 3), None)
        
        assert first_match["bet"] is None
        assert second_match["bet"] is None


class TestGetActiveGameRoundQuery:
    @pytest.fixture(autouse=True)
    def setup(self, in_memory_sqlite_session_factory):
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)

        self.today =datetime.datetime.now()
        self.previous_week = self.today - datetime.timedelta(days = 7)
        self.next_week = self.today + datetime.timedelta(days = 7)
        
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
        
        ## ROUND 1 PREVIOUS WEEK 
        message_bus.handle(commands.CreateMatchCommand(home_team_id=1, away_team_id=2, gameround=1, kickoff=self.previous_week), self.uow)
        message_bus.handle(commands.CreateMatchCommand(home_team_id=3, away_team_id=4, gameround=1, kickoff=self.previous_week), self.uow)
        
        ## ROUND 2 NEXT WEEK 
        message_bus.handle(commands.CreateMatchCommand(home_team_id=1, away_team_id=3, gameround=2, kickoff=self.next_week), self.uow)
        message_bus.handle(commands.CreateMatchCommand(home_team_id=2, away_team_id=4, gameround=2, kickoff=self.next_week), self.uow)
                                                       
    
    def test_returns_returns_none_before_any_matches(self):
        before_any_match_started = self.previous_week - datetime.timedelta(days = 7)
        result = queries.get_active_gameround_by_date(before_any_match_started, self.uow)
        assert result is None
    
    def test_returns_one_when_between_rounds(self):
        result = queries.get_active_gameround_by_date(self.today, self.uow)
        assert result == 1
    
    def test_returns_two_after_all_matches(self):
        after_all_matches = self.next_week + datetime.timedelta(days = 7)
        result = queries.get_active_gameround_by_date(after_all_matches, self.uow)
        assert result == 2
        
            
class TestStandingsQuery:
    @pytest.fixture(autouse=True)
    def setup(self, in_memory_sqlite_session_factory):
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)

        self.today = datetime.datetime.now()
        self.gameround = 1
        
        teams = [
            schema.Team(name="A"),
            schema.Team(name="B"),
        ]
        users = [
            schema.User(username="User1"),
            schema.User(username="User2")
        ]
        
        with self.uow:
            for t in teams:
                self.uow.session.add(t)
            for user in users:
                self.uow.session.add(user)
            self.uow.session.commit()
        
        message_bus.handle(commands.CreateMatchCommand(home_team_id=1, away_team_id=2, gameround=self.gameround, kickoff=self.today), self.uow)
        
        # user1 got 3 points, user2 got 5 points
        # query instead of command to to avoid checking dates
        with self.uow:
            self.uow.session.execute(text(
                '''INSERT INTO bets (user_id, match_id, home_team_score, away_team_score, points)
                VALUES (1, 1, 1, 0, 3), (2, 1, 2, 0, 5);
                '''   
            ))
            self.uow.session.commit()

        d = queries.standings_query(
            round=self.gameround,
            page=1,
            per_page=20,
            uow=self.uow
        )

        self.standings, self.count = d['standings'], d['count']
        
    def test_count_is_equal_to_number_of_betters(self):
        assert self.count == 2
        assert len(self.standings) == 2
        
    def test_standings_are_ordered(self):
        assert self.standings[0]['position'] == 1
        assert self.standings[1]['position'] == 2
        
    def test_first_user_has_more_point_than_second(self):
        assert self.standings[0]['points'] > self.standings[1]['points']
        
class TestGameroundQueries:
    @pytest.fixture(autouse=True)
    def setup(self, in_memory_sqlite_session_factory):
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)
        self.today = datetime.datetime.now()
        
        message_bus.handle(commands.CreateMatchCommand(home_team_id=1, away_team_id=2, gameround=1, kickoff=self.today - datetime.timedelta(days=7)), self.uow)
        message_bus.handle(commands.CreateMatchCommand(home_team_id=1, away_team_id=2, gameround=2, kickoff=self.today + datetime.timedelta(days=7)), self.uow)
        message_bus.handle(commands.CreateMatchCommand(home_team_id=1, away_team_id=2, gameround=3, kickoff=self.today + datetime.timedelta(days=14)), self.uow)
        message_bus.handle(commands.CreateMatchCommand(home_team_id=1, away_team_id=2, gameround=3, kickoff=self.today + datetime.timedelta(days=14)), self.uow)

    def test_get_available_gamerounds_query(self):
        gamerounds = queries.get_available_gamerounds(uow=self.uow)
        
        assert gamerounds == [1,2,3]
        
    def test_get_next_gameround_query(self):
        gameround = queries.get_next_gameround(uow=self.uow)
        
        assert gameround == 2