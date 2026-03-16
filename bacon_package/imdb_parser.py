from pathlib import Path
import csv
import sqlite3
from bacon_package.db_generate import (
    add_actor,
    add_movie,
    add_movie_to_actor,
    initialize_connection,
    get_colleagues_of_actor,
)

actors_data_path = str(Path(__file__).parent / "imdb_data" / "name.basics.tsv")
movies_data_path = str(Path(__file__).parent / "imdb_data" / "title.basics.tsv")
principals_data_path = str(Path(__file__).parent / "imdb_data" / "title.principals.tsv")

conn = initialize_connection()


def extract_actors(path: str) -> None:
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            add_actor(int(row["nconst"][2:]), row["primaryName"], conn)


def extract_movies(path: str) -> None:
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            add_movie(int(row["tconst"][2:]), row["primaryTitle"], conn)


def extract_principals(path: str) -> None:
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for i, row in enumerate(reader):
            if row["category"] == "actor":
                add_movie_to_actor(int(row["tconst"][2:]), int(row["nconst"][2:]), conn)


if __name__ == "__main__":
    extract_actors(actors_data_path)
    extract_movies(movies_data_path)
    extract_principals(principals_data_path)
