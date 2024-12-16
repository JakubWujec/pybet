from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.orm import declarative_base
from typing import List

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)

    bets: Mapped[List["Bet"]] = relationship(
        "Bet",  
        back_populates="user",  
        cascade="all, delete-orphan"  
    )
    
class Bet(Base):
    __tablename__ = "bets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False)
    home_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    

    __table_args__ = (UniqueConstraint("user_id", "match_id", name="uq_user_match"),)
    

    user: Mapped["User"] = relationship(
        User, 
        back_populates="bets"
    )
    match: Mapped["Match"] = relationship(
        "Match", 
        back_populates="bets" 
    )
    

class Match(Base):
    __tablename__ = "matches"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    home_team_id: Mapped[int] = mapped_column(Integer, nullable=False)
    away_team_id: Mapped[int] = mapped_column(Integer, nullable=False)
    home_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    away_team_score: Mapped[int] = mapped_column(Integer, nullable=True)
    

    bets: Mapped[List["Bet"]] = relationship(
        Bet,  # Target class
        back_populates="match",  
        cascade="all, delete-orphan",
    )
    
    def place_bet(self, bet: Bet):
        self.bets.append(bet)


