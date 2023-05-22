from dotenv import dotenv_values
import argparse
import getpass
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Item, Tag, statuses, priorities

parser = argparse.ArgumentParser(description="Your to-do list")
parser.add_argument("-a", "--add", type=str, help="Add an item to the to-do list")
parser.add_argument("-e", "--edit", type=int, help="edit an existing item")
parser.add_argument(
    "-p",
    "--priority",
    choices=priorities,
    help="give your item a priority, default is none",
)
parser.add_argument(
    "-s",
    "--status",
    choices=statuses,
    help="give your item a status, to-do, in-progress, waiting, done",
)
parser.add_argument(
    "-t", "--title", type=str, help="change the title of an item when editing"
)
parser.add_argument("-d", "--done", type=int, help="quickly mark an item done")


config = dotenv_values("config.env")

if config["USER"]:
    db_user = config["USER"]
else:
    db_user = getpass.getuser()

db_name = config["DB_NAME"]

engine = create_engine(
    f"mysql+mysqlconnector://{db_user}@localhost/{db_name}", echo=False
)
engine.connect()
session = Session(bind=engine)

args = parser.parse_args()

spacing = "%4s %40s %10s %10s"

if args.done:
    todo_item = session.query(Item).filter_by(id=args.done).first()
    todo_item.status = 1
    session.add(todo_item)
    session.commit()
    print(f"item {todo_item.id} has been marked complete!")

elif args.add:
    p = "none"
    s = "to-do"
    if args.priority:
        p = args.priority
    if args.status:
        s = args.status
    todo = Item(priority=priorities.index(p), status=statuses.index(s), title=args.add)
    session.add(todo)
    session.commit()

elif args.edit:
    todo_item = session.query(Item).filter_by(id=args.edit).first()
    p = "none"
    s = "to-do"
    if args.priority:
        p = args.priority
        todo_item.priority = priorities.index(p)
    if args.status:
        s = args.status
        todo_item.status = statuses.index(s)
    if args.title:
        todo_item.title = args.title
    session.add(todo_item)
    session.commit()
    print(f"changed item {todo_item.id}")

else:
    items = (
        session.query(Item).order_by(Item.status.desc()).order_by(Item.priority.desc())
    )
    print(spacing % ("Id", "Title", "Priority", "Status"))
    for item in items:
        print(
            spacing
            % (item.id, item.title, priorities[item.priority], statuses[item.status])
        )
