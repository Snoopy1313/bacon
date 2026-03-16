import json
from pathlib import Path
import sqlite3
from typing import List
import pika
from bacon_package.db_generate import (
    get_movie_id,
    add_movie,
    get_actor_id,
    add_actor,
    add_movie_to_actor,
    get_highest_actor_id,
    get_highest_movie_id,
    get_actors,
    get_actors_movies,
    get_movies
)


def db_connection() -> sqlite3.Connection:
    return sqlite3.connect(Path.cwd() / "bacon.db", check_same_thread=False)


if __name__ == "__main__":
    db_conn = db_connection()
    credentials = pika.PlainCredentials('admin', 'admin')
    rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=credentials))
    channel = rabbit_connection.channel()
    channel.queue_declare(queue="new_movies")

    message = {"Name": "Xmen", "Actors": ["Mark", "Ely"]}

    channel.basic_publish(exchange="", routing_key="new_movies", body=json.dumps(message))

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"data: {data}")
        movie_name: str = data["Name"]
        movie_actors: List[str] = data["Actors"]
        base_movie_id = get_highest_movie_id(db_conn)
        base_actor_id = get_highest_actor_id(db_conn)


        movie_id = get_movie_id(movie_name, db_conn)
        movie_id =  movie_id[0] if movie_id else base_movie_id + 1
        add_movie(movie_id, movie_name, db_conn)

        for index, actor in enumerate(movie_actors):
            actor_id = get_actor_id(actor, db_conn)
            actor_id = actor_id[0] if actor_id else base_actor_id + index + 1
            add_actor(actor_id, actor, db_conn)
            add_movie_to_actor(movie_id, actor_id, db_conn)

        print(get_actors(db_conn))
        print(get_movies(db_conn))
        print(get_actors_movies(db_conn))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="new_movies", on_message_callback=callback)

    channel.start_consuming()
