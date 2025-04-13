from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# 🔧 Replace with your DB URL (PostgreSQL example)
password = quote_plus("Abc@123")
user='postgres'
user = "postgres"
host = "localhost"
port = 5432
db = "imdb"

DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

# Create engine
engine = create_engine(DB_URL)
# Dummy users to insert
dummy_users = [
    {
        "username": "user1@inapp.com",
        "full_name": "Dummy User 1"
    },
     {
        "username": "user2@inapp.com",
        "full_name": "Dummy User 2"
    },
     {
        "username": "user3@inapp.com",
        "full_name": "Dummy User 3"
    },
]

def load_users():
    insert_query = text("""
        INSERT INTO inapp.users (username, full_name)
        VALUES (:username, :full_name)
        ON CONFLICT (username) DO NOTHING;
    """)

    with engine.connect() as conn:
        for user in dummy_users:
            conn.execute(insert_query, user)
        conn.commit()
        print("Users loaded successfully.")

if __name__ == "__main__":
    load_users()