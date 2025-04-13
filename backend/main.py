from typing import Union, Optional, List
from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
import os
import models
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
]



password = quote_plus("Abc@123")
app = FastAPI()
user = "postgres"
host = "localhost"
port = 5432
db = "imdb"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DB_URL)

@app.get("/search_movie")
def search_movie(
    title: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    genre: Optional[str] = Query(None),
    person_name: Optional[str] = Query(None),
    type: Optional[str] = Query(None)
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

@app.get("/search_person")
def search_person(
    name: Optional[str] = Query(None),
    profession: Optional[str] = Query(None),
    movie_title: Optional[str] = Query(None)
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
                "profession": row.profession.split(",") if row.profession else [],
                "known_for_titles": row.known_for_titles or []
            }
            for row in result
        ]







    return { results: [] }