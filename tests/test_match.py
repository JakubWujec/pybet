from pybet import schema, unit_of_work
import pytest
from sqlalchemy import exc


def test_can_create_match():
    match = schema.Match(
        home_team_id=1,
        away_team_id=2,
    )

    assert match is not None
    assert isinstance(match, schema.Match)


def test_match_cannot_be_created_two_exact_teams(in_memory_sqlite_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)
    team_id = 1

    match = schema.Match(home_team_id=team_id, away_team_id=team_id)

    with pytest.raises(exc.IntegrityError, match="check_home_away_different"):
        with uow:
            uow.matches.add(match)
            uow.commit()

            m = uow.matches.list()[0]
            print(vars(m))


@pytest.mark.skip()
def test_match_cannot_be_created_with_nonexistent_teams(
    in_memory_sqlite_session_factory,
):
    uow = unit_of_work.SqlAlchemyUnitOfWork(in_memory_sqlite_session_factory)

    # Attempt to create a match with nonexistent team IDs
    nonexistent_team_id_1 = 1000
    nonexistent_team_id_2 = 2000

    match = schema.Match(
        home_team_id=nonexistent_team_id_1,
        away_team_id=nonexistent_team_id_2,
    )

    with uow:
        uow.matches.add(match)
        uow.commit()

    with pytest.raises(Exception, match="FOREIGN KEY constraint failed"):
        with uow:
            uow.matches.add(match)
            uow.commit()

            m = uow.matches.list()[0]
            print(vars(m))
