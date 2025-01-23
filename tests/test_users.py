from pybet import schema, unit_of_work
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

import pytest 

def test_cannot_create_two_users_with_the_same_username(session: Session):
    user1 = schema.User(username="username")
    user2 = schema.User(username="username")
    
    session.add(user1)
    session.commit()

    with pytest.raises(Exception):
        session.add(user2)
        session.commit()

def test_can_create_two_users_with_different_usernames(session: Session):
    user1 = schema.User(username="username1")
    user2 = schema.User(username="username2")
    
    session.add(user1)
    session.commit()
    
    session.add(user2)
    session.commit()


    result = session.execute(text(
        "SELECT COUNT(*) FROM users"
    )).scalar()
    
    assert result == 2
    
    
    
 
    
 