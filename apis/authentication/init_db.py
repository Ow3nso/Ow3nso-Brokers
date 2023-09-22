from database import Base, engine
from apis.authentication.models import User

Base.metadata.create_all(bind=engine)