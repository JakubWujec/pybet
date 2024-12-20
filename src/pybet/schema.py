from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.orm import declarative_base, attribute_mapped_collection
from sqlalchemy.sql import func, text
from sqlalchemy.sql.functions import GenericFunction
from typing import List, Dict, Optional
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))
    
    bets: Mapped[List["Bet"]] = relationship(
        "Bet",  
        back_populates="user",  
        cascade="all, delete-orphan"  
    )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_authenticated(self):
        #is_authenticated: a property that is True if the user has valid credentials or False otherwise.
        return True
    def is_active(self):
        # a property that is True if the user's account is active or False otherwise.
        return True
    def is_anonymous(self):
        #is_anonymous: a property that is False for regular users, and True only for a special, anonymous user.
        return False
    def get_id(self):
        #a method that returns a unique identifier for the user as a string.
        return f"{self.id}"

    
class Bet(Base):
    __tablename__ = "bets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False)
    home_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    points: Mapped[int] = mapped_column(Integer, default = 0, server_default="0")

    __table_args__ = (UniqueConstraint("user_id", "match_id", name="uq_user_match"),)
    
    user: Mapped["User"] = relationship(
        User, 
        back_populates="bets"
    )
    match: Mapped["Match"] = relationship(
        "Match", 
        back_populates="bets" 
    )
    

    def calculate_points(self, home_team_score: int, away_team_score: int):
        POINTS_FOR_WINNER = 2
        POINTS_FOR_DRAW = 3
        POINTS_FOR_EXACT_SCORE = 5
        
        match_score_diff = home_team_score - away_team_score
        bet_score_diff = self.home_team_score - self.away_team_score
        
        if self.home_team_score == home_team_score and away_team_score == self.away_team_score:
            return POINTS_FOR_EXACT_SCORE
        if bet_score_diff == 0 and match_score_diff == 0:
            return POINTS_FOR_DRAW
        if match_score_diff * bet_score_diff > 0 or (match_score_diff == 0 and bet_score_diff == 0):
            return POINTS_FOR_WINNER
   
        return 0
        
    

class Match(Base):
    __tablename__ = "matches"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    home_team_id: Mapped[int] = mapped_column(Integer, nullable=False)
    away_team_id: Mapped[int] = mapped_column(Integer, nullable=False)
    home_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    kickoff: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        default=datetime.datetime.now(datetime.timezone.utc),
        nullable=False
    )
    
    bets: Mapped[Dict[int, "Bet"]] = relationship(
        "Bet",  # Target class
        back_populates="match",  
        collection_class=attribute_mapped_collection("user_id"),
        cascade="all, delete-orphan",
    )
    
    def place_bet(self, bet: Bet):
        self.bets[bet.user_id] = bet


    def is_after_kickoff(self) -> bool:
        # not flushed
        if self.kickoff is None:
            return False
        
        return datetime.datetime.now() >= self.kickoff