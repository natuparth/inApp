from typing import Union, Optional, List
from fastapi import Depends,FastAPI, Query, HTTPException, status
from sqlalchemy import create_engine, text
import os
import models
from models import Users, Token, UserInDB, TokenData
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
import jwt
from typing_extensions import Annotated

origins = [
    "http://localhost:5173",
]

SECRET_KEY = "a72746cabf9f0036435168e5461180364dd12b10334f052497628bbe0c605bd1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


password = quote_plus("Abc@123")
app = FastAPI()
user = "postgres"
host = "localhost"
port = 5432
db = "imdb"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DB_URL)

fake_users_db = {
    "johndoe@gmail.com": {
        "username": "johndoe@gmail.com",
        "full_name": "John Doe",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    }
}
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    print(db, 'db')
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_from_db(username: str) -> Union[Users, None]:
    query = text("SELECT username, full_name FROM users WHERE username = :username")
    with engine.connect() as conn:
        result = conn.execute(query, {"username": username}).fetchone()
        if result:
            return Users(**dict(result))
    return None

async def get_current_user_updated(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_from_db(token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    print(form_data, form_data.username, form_data.password)
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/search_movie")
def search_movie(
    title: Optional[str] = Query(None),
    year: Union[int,str, None] = Query(None),
    genre: Optional[str] = Query(None),
    person_name: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    token: str = Depends(oauth2_scheme),
    current_user: dict = Depends(get_current_user),
):
    filters = []
    params = {}

    if title:
        filters.append('t."primaryTitle" ILIKE :title')
        params["title"] = f"%{title}%"

    if year:
        filters.append('t."startYear" = :year')
        params["year"] = str(year)

    if genre:
        filters.append('t."genres" ILIKE :genre')
        params["genre"] = f"%{genre}%"

    if type:
        filters.append('t."titleType" ILIKE :type')
        params["type"] = type

    if person_name:
        filters.append('a."primaryName" ILIKE :person_name')
        params["person_name"] = f"%{person_name}%"

    query_str = f"""
        SELECT 
            t."primaryTitle" AS title,
            t."startYear" AS year_released,
            t."titleType" AS type,
            t."genres" AS genre,
            ARRAY_AGG(DISTINCT a."primaryName") AS people_associated
        FROM inapp.titles t
        LEFT JOIN inapp.actors a
            ON t.nconst = ANY (string_to_array(a."knownForTitles", ','))
        {"WHERE " + " AND ".join(filters) if filters else ""}
        GROUP BY t."primaryTitle", t."startYear", t."titleType", t."genres"
        ORDER BY t."startYear" DESC
        LIMIT 20;
    """

    with engine.connect() as conn:
        result = conn.execute(text(query_str), params).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="No movies found.")

        return [
            {
                "title": row.title,
                "year_of_release": row.year_released,
                "type": row.type,
                "genre": row.genre,
                "cast": row.people_associated or []
            }
            for row in result
        ]

@app.get("/search_actors")
def search_person(
    name: Optional[str] = Query(None),
    profession: Optional[str] = Query(None),
    movie_title: Optional[str] = Query(None),
    token: str = Depends(oauth2_scheme),  # Token required
    current_user: dict = Depends(get_current_user),
):
    filters = []
    params = {}

    if name:
        filters.append('a."primaryName" ILIKE :name')
        params["name"] = f"%{name}%"

    if profession:
        filters.append('a."primaryProfession" ILIKE :profession')
        params["profession"] = f"%{profession}%"

    if movie_title:
        filters.append('t."primaryTitle" ILIKE :movie_title')
        params["movie_title"] = f"%{movie_title}%"

    query = f"""
        SELECT 
            a."primaryName" AS name,
            a."birthYear" AS birth_year,
            a."primaryProfession" AS profession,
            ARRAY_AGG(DISTINCT t."primaryTitle") AS known_for_titles
        FROM inapp.actors a
        LEFT JOIN inapp.titles t
            ON t.nconst = ANY (string_to_array(a."knownForTitles", ','))
        {"WHERE " + " AND ".join(filters) if filters else ""}
        GROUP BY a."primaryName", a."birthYear", a."primaryProfession"
        ORDER BY a."primaryName"
        LIMIT 20;
    """

    with engine.connect() as conn:
        result = conn.execute(text(query), params).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="No matching people found.")

        return [
            {
                "name": row.name,
                "year_of_birth": row.birth_year,
                "profession": row.profession.replace(',', ', '),
                "known_for_titles": str(', '.join(row.known_for_titles))
            }
            for row in result
        ]

    return { results: [] }