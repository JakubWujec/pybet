import enum
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    attribute_mapped_collection,
    declarative_base,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from pybet import events

Base = declarative_base()
metadata = Base.metadata


class Role(enum.Enum):
    USER = 1
    ADMIN = 2
    BOT = 3


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    role: Mapped[Role] = mapped_column(
        Enum(Role), nullable=False, default=Role.USER, server_default="USER"
    )

    bets: Mapped[List["Bet"]] = relationship(
        "Bet", back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash or "", password)

    @property
    def is_authenticated(self):
        # is_authenticated: a property that is True if the user has valid credentials or False otherwise.
        return True

    @property
    def is_active(self):
        # a property that is True if the user's account is active or False otherwise.
        return True

    @property
    def is_anonymous(self):
        # is_anonymous: a property that is False for regular users, and True only for a special, anonymous user.
        return False

    def get_id(self):
        # a method that returns a unique identifier for the user as a string.
        return f"{self.id}"

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    def __repr__(self):
        return f"User(username={self.username})"

    def __str__(self):
        return self.username


class Bet(Base):
    __tablename__ = "bets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False)
    home_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    points: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    __table_args__ = (UniqueConstraint("user_id", "match_id", name="uq_user_match"),)

    user: Mapped["User"] = relationship(User, back_populates="bets")
    match: Mapped["Match"] = relationship("Match", back_populates="bets")

    def update_points(self, points: int):
        self.points = points


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    # Relationship to refer matches where this team is home or away
    home_matches: Mapped[List["Match"]] = relationship(
        "Match", back_populates="home_team", foreign_keys="Match.home_team_id"
    )
    away_matches: Mapped[List["Match"]] = relationship(
        "Match", back_populates="away_team", foreign_keys="Match.away_team_id"
    )

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return self.name


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    gamestage_id: Mapped[int] = mapped_column(
        ForeignKey("gamestages.id"), nullable=True
    )
    home_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    kickoff: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    bets: Mapped[Dict[int, "Bet"]] = relationship(
        "Bet",  # Target class
        back_populates="match",
        collection_class=attribute_mapped_collection("user_id"),
        cascade="all, delete-orphan",
    )
    events: List["events.Event"] = []

    home_team: Mapped["Team"] = relationship("Team", foreign_keys=[home_team_id])
    away_team: Mapped["Team"] = relationship("Team", foreign_keys=[away_team_id])
    gamestage: Mapped["Gamestage"] = relationship(
        "Gamestage", foreign_keys=[gamestage_id]
    )

    __table_args__ = (
        CheckConstraint(
            "home_team_id != away_team_id", name="check_home_away_different"
        ),
    )

    def place_bet(self, bet: Bet):
        if bet.user_id in self.bets:
            self.bets[bet.user_id].home_team_score = bet.home_team_score
            self.bets[bet.user_id].away_team_score = bet.away_team_score
        else:
            self.bets[bet.user_id] = bet

    def update_score(self, home_team_score: int, away_team_score: int):
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score

        self.events.append(events.MatchScoreUpdated(self.id))

    def is_after_kickoff(self) -> bool:
        # not flushed
        if self.kickoff is None:
            return False
        kickoff = self.kickoff.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) >= kickoff

    def __str__(self):
        if self.away_team is not None and self.home_team is not None:
            return f"{self.home_team.name} VS {self.away_team.name} (GR:{self.gamestage_id})"
        return f"Match <{self.id}>"


class Gamestage(Base):
    __tablename__ = "gamestages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    matches: Mapped[List["Match"]] = relationship(
        "Match", back_populates="gamestage", foreign_keys="Match.gamestage_id"
    )

    def add_match(self, match: "Match"):
        self.matches.append(match)

    @property
    def deadline(self):
        return min(match.kickoff for match in self.matches)

    def to_dict(self):
        return dict(id=self.id, name=self.name, deadline=self.deadline)

    def __str__(self):
        return f"{self.name} ({self.deadline})"
