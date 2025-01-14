import random
from src.pybet import schema
from src import config

def seed_bot_users(session, count = 10):
    for i in range(count):
        user = schema.User(
            username=f"botuser_{random.randint(100_000, 999_999)}"
        )
        user.set_password("user")
        user.role = schema.Role.BOT
        
        session.add(user)
        
    session.commit()
    
if __name__ == "__main__":    
    with config.session_scope() as session:
        seed_bot_users(session)