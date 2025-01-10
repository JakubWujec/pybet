from src.pybet import schema
from src import config
    
def seed_admin_user(session):
    user = schema.User(
        username= config.Config.ADMIN_LOGIN
    )
    user.set_password(config.Config.ADMIN_PASSWORD)
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
    with config.session_scope() as session:
        seed_test_user(session)
        seed_admin_user(session)
        
