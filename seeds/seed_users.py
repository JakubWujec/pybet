from pybet import schema
from config import Config, session_scope
    
def seed_admin_user(session):
    user = schema.User(
        username= Config.ADMIN_LOGIN
    )
    user.set_password(Config.ADMIN_PASSWORD)
    user.role = schema.Role.ADMIN
    
    session.add(user)
    session.commit()
    
def seed_test_user(session):
    user = schema.User(
        username="user"
    )
    user.set_password("user")
    
    session.add(user)
    session.commit()
    
if __name__ == "__main__":    
    with session_scope() as session:
        seed_test_user(session)
        seed_admin_user(session)
        
