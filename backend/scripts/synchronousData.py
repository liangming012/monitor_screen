import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from core.config import settings
from crud.crud_project import crud_project
from crud.crud_user import crud_user
from models import *

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
users = crud_user.list(db)
projects = crud_project.list(db)
print(projects)
db.close()
print('同步完成！')
