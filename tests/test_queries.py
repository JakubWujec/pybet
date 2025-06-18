from pybet import message_bus, unit_of_work, commands, schema
from pybet.queries import gamestage_queries, queries
from sqlalchemy.sql import text
import datetime
import pytest


class TestGetActiveGamestageQuery:
    @pytest.fixture(autouse=True)
    def setup(self, in_memory_sqlite_session_factory):
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)

        self.today = datetime.datetime.now()
        self.previous_week = self.today - datetime.timedelta(days=7)
        self.next_week = self.today + datetime.timedelta(days=7)

        teams = [
            schema.Team(name="A"),
            schema.Team(name="B"),
            schema.Team(name="C"),
            schema.Team(name="D"),
        ]
        with self.uow:
            for t in teams:
                self.uow.session.add(t)
            self.uow.session.commit()

        message_bus.handle(
            commands.CreateGamestageCommand("Gamestage 1", 1), uow=self.uow
        )
        message_bus.handle(
            commands.CreateGamestageCommand("Gamestage 2", 2), uow=self.uow
        )

        ## ROUND 1 PREVIOUS WEEK
        message_bus.handle(
            commands.CreateMatchCommand(
                home_team_id=1,
                away_team_id=2,
                gamestage_id=1,
                kickoff=self.previous_week,
            ),
            self.uow,
        )
        message_bus.handle(
            commands.CreateMatchCommand(
                home_team_id=3,
                away_team_id=4,
                gamestage_id=1,
                kickoff=self.previous_week,
            ),
            self.uow,
        )

        ## ROUND 2 NEXT WEEK
        message_bus.handle(
            commands.CreateMatchCommand(
                home_team_id=1, away_team_id=3, gamestage_id=2, kickoff=self.next_week
            ),
            self.uow,
        )
        message_bus.handle(
            commands.CreateMatchCommand(
                home_team_id=2, away_team_id=4, gamestage_id=2, kickoff=self.next_week
            ),
            self.uow,
        )

    def test_returns_returns_none_before_any_matches(self):
        before_any_match_started = self.previous_week - datetime.timedelta(days=7)
        result = gamestage_queries.get_gamestage_id_by_date(
            date=before_any_match_started, uow=self.uow
        )
        assert result is None

    def test_returns_one_when_between_rounds(self):
        result = gamestage_queries.get_gamestage_id_by_date(self.today, self.uow)
        assert result == 1

    def test_returns_two_after_all_matches(self):
        after_all_matches = self.next_week + datetime.timedelta(days=7)
        result = gamestage_queries.get_gamestage_id_by_date(after_all_matches, self.uow)
        assert result == 2


class TestStandingsQuery:
    @pytest.fixture(autouse=True)
    def setup(self, in_memory_sqlite_session_factory):
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)

        self.today = datetime.datetime.now()
        self.gamestage_id = 1

        teams = [
            schema.Team(name="A"),
            schema.Team(name="B"),
        ]
        users = [schema.User(username="User1"), schema.User(username="User2")]

        with self.uow:
            for t in teams:
                self.uow.session.add(t)
            for user in users:
                self.uow.session.add(user)
            self.uow.session.commit()

        message_bus.handle(
            commands.CreateGamestageCommand(
                f"Gamestage {self.gamestage_id}", id=self.gamestage_id
            ),
            uow=self.uow,
        )

        message_bus.handle(
            commands.CreateMatchCommand(
                home_team_id=1,
                away_team_id=2,
                gamestage_id=self.gamestage_id,
                kickoff=self.today,
            ),
            self.uow,
        )

        # user1 got 3 points, user2 got 5 points
        # query instead of command to to avoid checking dates
        with self.uow:
            self.uow.session.execute(
                text(
                    """INSERT INTO bets (user_id, match_id, home_team_score, away_team_score, points)
                VALUES (1, 1, 1, 0, 3), (2, 1, 2, 0, 5);
                """
                )
            )
            self.uow.session.commit()

        queryDTO = queries.standings_query(
            gamestage_id=self.gamestage_id, page=1, per_page=20, uow=self.uow
        )

        self.standingsDTO, self.count = queryDTO.standings, queryDTO.count

    def test_count_is_equal_to_number_of_betters(self):
        assert self.count == 2
        assert len(self.standingsDTO) == 2

    def test_standings_are_ordered(self):
        assert self.standingsDTO[0].position == 1
        assert self.standingsDTO[1].position == 2

    def test_first_user_has_more_point_than_second(self):
        assert self.standingsDTO[0].points > self.standingsDTO[1].points


class TestGamestageQueries:
    @pytest.fixture(autouse=True)
    def setup(self, in_memory_sqlite_session_factory):
        self.uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)
        self.today = datetime.datetime.now()

        for i in range(1, 4):
            message_bus.handle(
                commands.CreateGamestageCommand(name=f"Gamestage {i}", id=i),
                uow=self.uow,
            )

    def test_get_available_gamestage_ids_query(self):
        gamestage_ids = gamestage_queries.get_available_gamestage_ids(uow=self.uow)

        assert gamestage_ids == [1, 2, 3]
