from pathlib import Path
import sqlite3
from typing import List


def create_actor_table(conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS actors ("
            "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
            "FirstName varchar(255) NOT NULL,"
            "LastName varchar(255) NOT NULL,"
            "UNIQUE (FirstName, LastName)"
            ");"
        )
        cur.execute(create_table_query)
        conn.commit()
        return "Success"

    except Exception as e:
        print(f"An error occurred while creating actor table: {e}")
        return "Failure"


def create_movies_table(conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS movies ("
            "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
            "Name varchar(255) NOT NULL,"
            "UNIQUE (Name)"
            ");"
        )
        cur.execute(create_table_query)
        conn.commit()
        return "Success"

    except Exception as e:
        print(f"An error occurred while creating movies table: {e}")
        return "Failure"


def create_actors_movies_table(conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()
        create_table_query = (
            "CREATE TABLE IF NOT EXISTS actors_movies ("
            "MovieID INTEGER NOT NULL,"
            "ActorID INTEGER NOT NULL,"
            "FOREIGN KEY(MovieID) REFERENCES movies(ID)"
            "FOREIGN KEY(ActorID) REFERENCES actors(ID)"
            ");"
        )
        cur.execute(create_table_query)
        conn.commit()
        return "Success"

    except Exception as e:
        print(f"An error occurred while creating actors_movies table: {e}")
        return "Failure"


def create_tables(conn: sqlite3.Connection) -> None:
    create_actor_table(conn)
    create_movies_table(conn)
    create_actors_movies_table(conn)


def add_actor(first_name: str, last_name: str, conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()
        data = (first_name, last_name)
        cur.execute("INSERT INTO actors(FirstName, LastName) VALUES(?, ?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred during add_actor: {e}")


def add_movie(name: str, conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()
        data = (name,)
        cur.execute("INSERT INTO movies(Name) VALUES(?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred during add_movie: {e}")


def add_movie_to_actor(movie_id: str, actor_id: str, conn: sqlite3.Connection) -> None:
    try:
        cur = conn.cursor()
        data = (movie_id, actor_id)
        cur.execute("INSERT INTO actors_movies(MovieID, ActorID) VALUES(?, ?)", data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred during add_movie_to_actor: {e}")


def get_actors(conn: sqlite3.Connection) -> List:
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM actors")
        actor = cur.fetchall()
        return actor
    except Exception as e:
        print(f"An error occurred during get_actors: {e}")
        return []


def get_movies(conn: sqlite3.Connection) -> List:
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM movies")
        actor = cur.fetchall()
        return actor
    except Exception as e:
        print(f"An error occurred during get_movies: {e}")
        return []
    
def get_actors_movies(conn: sqlite3.Connection) -> List:
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM actors_movies")
        actor = cur.fetchall()
        return actor
    except Exception as e:
        print(f"An error occurred during get_movies: {e}")
        return []


if __name__ == "__main__":
    conn = sqlite3.connect(Path(__file__).parents[1] / "bacon.db", check_same_thread=False)
    create_tables(conn)
    add_actor("Marik", "Urman", conn)
    add_movie("Ironn", conn)
    add_movie_to_actor(1, 1, conn)
    print(get_actors(conn))
    print(get_movies(conn))
    print(get_actors_movies(conn))
