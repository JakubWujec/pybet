from src.pybet import model
from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey, event, ForeignKeyConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship, registry, mapper
from sqlalchemy.ext.instrumentation import InstrumentationManager


mapper_registry = registry()
metadata = mapper_registry.metadata

users = Table(
    "users",
    mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50)),
)

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
    Column('user_id', ForeignKey('users.id')),
    Column('match_id', ForeignKey('matches.id')),
    Column('home_team_score', Integer, nullable=False),
    Column('away_team_score', Integer, nullable=False),
    UniqueConstraint('user_id', 'match_id', name='uq_user_match')
)


def start_mappers():
    users_mapper = mapper_registry.map_imperatively(
        model.User,
        users,
    )
    
    match_mapper = mapper_registry.map_imperatively(
        model.Match,
        matches,
       
    )
    
    bets_mapper = mapper_registry.map_imperatively(
        model.Bet,
        bets,
    )
    
    bets_mapper.add_properties({
        "user": relationship(
            users_mapper,  # Target class
            back_populates="bets"  # Back-populated attribute on User
        ),
        "match": relationship(
            match_mapper,  # Target class
            back_populates="bets"  # Back-populated attribute on Match
        )
    })
    
    match_mapper.add_properties({
        "bets": relationship(bets_mapper, back_populates="match", cascade="all, delete-orphan")
    })
    
    users_mapper.add_properties({
        "bets": relationship(
            bets_mapper,  # Target class
            back_populates="user",  # Back-populated attribute on Bet
            cascade="all, delete-orphan",  # Automatically manage related objects
        )
    })
    
    
        
