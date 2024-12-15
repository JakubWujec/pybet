from src.pybet import model
from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey, event, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship, registry
from sqlalchemy.ext.instrumentation import InstrumentationManager


mapper_registry = registry()
metadata = mapper_registry.metadata

matches = Table(
    "matches",
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('home_team_id', Integer, nullable=False),
    Column('away_team_id', Integer, nullable=False),
    Column('home_team_score', Integer, nullable=True),
    Column('away_team_score', Integer, nullable=True),
)

bets = Table(
    "bets",
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('match_id', ForeignKey('matches.id')),
    Column('home_team_score', Integer, nullable=False),
    Column('away_team_score', Integer, nullable=False)
)


def start_mappers():
    matches_mapper = mapper_registry.map_imperatively(model.Match, matches)
    bets_mapper = mapper_registry.map_imperatively(model.Bet, bets)
    
  
    
