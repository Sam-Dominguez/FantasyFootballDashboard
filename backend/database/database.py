from decouple import config
from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, create_engine
from backend.models.models import *

sqlite_file_name = config('DB_FILENAME')
sqlite_url = f"sqlite:///{sqlite_file_name}"

class Database():
    _instance = None

    engine : Engine = None

    def __new__(self):
        if self._instance is None:
            print('Creating database object')
            self._instance = super(Database, self).__new__(self)
            
            self.engine = create_engine(sqlite_url, echo=True)
            SQLModel.metadata.create_all(self.engine)

        return self._instance
    
    def save(self, record):
        session = Session(self.engine)

        session.add(record)

        session.commit()
    