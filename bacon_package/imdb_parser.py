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

actors_data_path = Path(__file__).parent / "imdb_data" / "name.basics.tsv"
movies_data_path = Path(__file__).parent / "imdb_data" / "title.basics.tsv"
principals_data_path = Path(__file__).parent / "imdb_data" / "title.principals.tsv"

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
    for i in range(1, 21):
        add_actor(i, f"a{i}", conn)

    for i in range(1, 6):
        add_movie(i, f"m{i}", conn)

    relations = {
        1: [1, 2, 3, 4, 5],
        2: [5, 6, 7, 8],
        3: [8, 9, 10, 11],
        4: [11, 12, 13, 14, 15],
        5: [15, 16, 17, 18, 19, 20],
    }
    for movie_id, actors in relations.items():
        for actor_id in actors:
            add_movie_to_actor(movie_id, actor_id, conn)
