from models import Base, Item, Tag
from connect import engine

print("Creating tables")
Base.metadata.create_all(bind=engine)
