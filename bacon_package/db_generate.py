from pathlib import Path
import sqlite3
from typing import List, Optional


def initialize_connection() -> sqlite3.Connection:
    return sqlite3.connect(Path(__file__).parents[1] / "bacon.db", check_same_thread=False)


def enable_foreign_keys(conn: sqlite3.Connection) -> str:
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        conn.commit()
        return "Success"
    except Exception as e:
        print(f"An error occurred during enable_foreign_keys: {e}")
        return "Failure"


def create_actor_table(conn: sqlite3.Connection) -> str:
    try:
        cur = conn.cursor()
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS actors ("
            "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
            "Name varchar(255) NOT NULL"
            ")"
        )
        cur.execute(create_table_query)
        conn.commit()
        return "Success"

    except Exception as e:
        print(f"An error occurred while creating actor table: {e}")
        return "Failure"


def create_movies_table(conn: sqlite3.Connection) -> str:
    try:
        cur = conn.cursor()
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS movies ("
            "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
            "Name varchar(255) NOT NULL"
            ")"
        )
        cur.execute(create_table_query)
        conn.commit()
        return "Success"

    except Exception as e:
        print(f"An error occurred while creating movies table: {e}")
        return "Failure"


def create_actors_movies_table(conn: sqlite3.Connection) -> str:
    try:
        cur = conn.cursor()
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS actors_movies ("
            "MovieID INTEGER NOT NULL,"
            "ActorID INTEGER NOT NULL,"
            "FOREIGN KEY(MovieID) REFERENCES movies(ID)"
            "FOREIGN KEY(ActorID) REFERENCES actors(ID)"
            "PRIMARY KEY (MovieID, ActorID)"
            ");"
        )
        cur.execute(create_table_query)
        conn.commit()
        return "Success"

    except Exception as e:
        print(f"An error occurred while creating actors_movies table: {e}")
        return "Failure"


def create_tables(conn: sqlite3.Connection) -> None:
    enable_foreign_keys(conn)
    create_actor_table(conn)
    create_movies_table(conn)
    create_actors_movies_table(conn)


def add_actor(id: int, name: str, conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()
        data = (id, name)
        cur.execute("INSERT INTO actors(ID, Name) VALUES(?, ?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred during add_actor: {e}")


def add_movie(id: int, name: str, conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()
        data = (id, name)
        cur.execute("INSERT INTO movies(ID, Name) VALUES(?, ?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred during add_movie: {e}")


def add_movie_to_actor(movie_id: int, actor_id: int, conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()
        data = (movie_id, actor_id)
        cur.execute("INSERT INTO actors_movies(MovieID, ActorID) VALUES(?, ?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred during add_movie_to_actor: {e}")


def actor_exists(actor_id: int, conn: sqlite3.Connection) -> Optional[bool]:
    try:
        cur = conn.cursor()
        data = (actor_id,)
        cur.execute("SELECT ID FROM actors WHERE ID = ?", data)
        actor = cur.fetchone()
        return bool(actor)
    except Exception as e:
        print(f"An error occurred during actor_exists: {e}")


def movie_exists(movie_id: int, conn: sqlite3.Connection) -> Optional[bool]:
    try:
        cur = conn.cursor()
        data = (movie_id,)
        cur.execute("SELECT ID FROM movies WHERE ID = ?", data)
        movie = cur.fetchone()
        return bool(movie)
    except Exception as e:
        print(f"An error occurred during movie_exists: {e}")


def get_actors(conn: sqlite3.Connection) -> List:
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM actors")
        actors = cur.fetchall()
        return actors
    except Exception as e:
        print(f"An error occurred during get_actors: {e}")
        return []


def get_movies(conn: sqlite3.Connection) -> List:
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM movies")
        movies = cur.fetchall()
        return movies
    except Exception as e:
        print(f"An error occurred during get_movies: {e}")
        return []


def get_actors_movies(conn: sqlite3.Connection) -> List:
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM actors_movies")
        actors_movies = cur.fetchall()
        return actors_movies
    except Exception as e:
        print(f"An error occurred during get_actors_movies: {e}")
        return []


def get_movie_id(movie_name: str, conn: sqlite3.Connection) -> List[int]:
    try:
        cur = conn.cursor()
        cur.execute("SELECT ID FROM movies WHERE Name = ?", (movie_name,))
        movies_id = cur.fetchall()
        return [movie_tuple[0] for movie_tuple in movies_id]
    except Exception as e:
        print(f"An error occurred during get_movie_id: {e}")
        return [-1]


def get_movie_name(movie_id: int, conn: sqlite3.Connection) -> str:
    try:
        cur = conn.cursor()
        cur.execute("SELECT Name FROM movies WHERE ID = ?", (movie_id,))
        movie_name = cur.fetchone()
        return movie_name[0]
    except Exception as e:
        print(f"An error occurred during get_movie_name: {e}")
        return ""


def get_movie_actors(movie_id: int, conn: sqlite3.Connection) -> List[int]:
    try:
        cur = conn.cursor()
        cur.execute("SELECT ActorID FROM actors_movies WHERE MovieID = ? ", (movie_id,))
        actors_id = cur.fetchall()
        return [actor_tuple[0] for actor_tuple in actors_id]
    except Exception as e:
        print(f"An error occurred during get_movie_actors: {e}")
        return [-1]


def get_actor_id(name: str, conn: sqlite3.Connection) -> List[int]:
    try:
        cur = conn.cursor()
        cur.execute("SELECT ID FROM actors WHERE Name = ?", (name,))
        actors_id = cur.fetchall()
        return [actor_tuple[0] for actor_tuple in actors_id]
    except Exception as e:
        print(f"An error occurred during get_actor_id: {e}")
        return [-1]


def get_actor_name(actor_id: int, conn: sqlite3.Connection) -> str:
    try:
        cur = conn.cursor()
        cur.execute("SELECT Name FROM actors WHERE ID = ?", (actor_id,))
        actor_name = cur.fetchone()
        return actor_name[0]
    except Exception as e:
        print(f"An error occurred during get_actor_name: {e}")
        return ""


def get_actor_movies(actor_id: int, conn: sqlite3.Connection) -> List[int]:
    try:
        cur = conn.cursor()
        cur.execute("SELECT MovieID FROM actors_movies WHERE ActorID = ? ", (actor_id,))
        movies_id = cur.fetchall()
        return [movie_tuple[0] for movie_tuple in movies_id]
    except Exception as e:
        print(f"An error occurred during get_actor_movies: {e}")
        return [-1]


def get_colleagues_of_actor(actor_id: int, conn: sqlite3.Connection) -> List[int]:
    try:
        cur = conn.cursor()
        select_colleagues_query = (
            "SELECT DISTINCT am2.ActorID "
            "FROM actors_movies am1, actors_movies am2 "
            "WHERE am1.ActorID = ? AND am1.MovieID = am2.MovieID AND am2.ActorID <> ?"
        )
        cur.execute(select_colleagues_query, (actor_id, actor_id))
        actors_id = cur.fetchall()
        return [actor_tuple[0] for actor_tuple in actors_id]
    except Exception as e:
        print(f"An error occurred during get_colleagues_of_actor: {e}")
        return [-1]


if __name__ == "__main__":
    conn = initialize_connection()
    create_tables(conn)
    for i in range(1, 26):
        add_actor(i, f"a{i}", conn)

    for i in range(1, 7):
        add_movie(i, f"m{i}", conn)

    relations = {
        1: [1, 2, 3, 4, 5],
        2: [5, 6, 7, 8],
        3: [8, 9, 10, 11],
        4: [11, 12, 13, 14, 15],
        5: [15, 16, 17, 18, 19, 20],
        6: [21, 22, 23, 24, 25],
    }
    for movie_id, actors in relations.items():
        for actor_id in actors:
            add_movie_to_actor(movie_id, actor_id, conn)
