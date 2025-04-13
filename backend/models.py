from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel
from typing import Union
url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Abc@123",
    host="localhost",
    database="imdb",
    port=5432
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'inapp'}
    username = Column(String, primary_key=True)
    full_name = Column(String, nullable=True)


class UserInDB(Users):
    hashed_password = Column(String)


class Actors(Base):
    __tablename__ = "actors"
    __table_args__ = {'schema': 'inapp'}
    nconst = Column(String, primary_key=True)
    primaryName = Column(String)
    birthYear = Column(String, nullable=True)
    deathYear = Column(String, nullable=True)
    primaryProfession = Column(String)
    knownForTitles = Column(String)

class Titles(Base):
    __tablename__ = "titles"
    __table_args__ = {'schema': 'inapp'}
    nconst = Column(String, primary_key=True)
    titleType = Column(String)
    primaryTitle = Column(String)
    originalTitle = Column(String)
    isAdult = Column(Integer)
    startYear = Column(String, nullable=True)
    endYear = Column(String, nullable=True)
    runtimeMinutes = Column(String, nullable=True)
    genres = Column(String)


Base.metadata.create_all(engine)