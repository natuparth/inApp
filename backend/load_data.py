import psycopg2
import os

# --- CONFIGURATION ---
DB_CONFIG = {
    "dbname": "imdb",
    "user": "postgres",
    "password": "Abc@123",
    "host": "localhost",
    "port": "5432",
    "options": "-c search_path=inapp"
}




def clean_line(line):
    # This function will handle cleaning up the string and escaping quotes properly.
    return line.replace('"', '""').strip()

def load_tsv_to_postgres(file_path, table_name, db_config):
    conn = None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Open the TSV file
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read and clean the file line by line
            lines = f.readlines()
            cleaned_lines = [clean_line(line) for line in lines]
            print("First 5 lines of file:")
            print(lines[:5])
           

            # Now perform the COPY operation
            with open(file_path, 'r', encoding='utf-8') as f:
                # Skip header row if needed (PostgreSQL COPY can use HEADER too)
                cur.copy_expert(
                    f"""
                    COPY {table_name} FROM STDIN WITH (
                        FORMAT CSV,
                        DELIMITER E'\t',
                        HEADER,
                        QUOTE '"',
                        ESCAPE '"'
                    );
                    """,
                    f
                )

        conn.commit()
        print(f"Data loaded successfully into '{table_name}' from '{file_path}'")

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

ACTORS_FILE_PATH = "data/name.basics.tsv"
TITLES_FILE_PATH = "data/title.basics.tsv"
# --- EXECUTE ---
if __name__ == "__main__":
    if not os.path.isfile(ACTORS_FILE_PATH):
        print(f"Actors File not found: {ACTORS_FILE_PATH}")
    elif not os.path.isfile(TITLES_FILE_PATH):
        print(f"Actors File not found: {TITLES_FILE_PATH}")
    else:
        load_tsv_to_postgres(ACTORS_FILE_PATH, 'inapp.actors', DB_CONFIG)
        load_tsv_to_postgres(TITLES_FILE_PATH, 'inapp.titles', DB_CONFIG)
