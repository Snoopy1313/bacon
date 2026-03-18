import json
import time
from typing import List
import pika
import requests

SERVER_LINK = "http://backend_server:5000"



if __name__ == "__main__":
    credentials = pika.PlainCredentials("admin", "admin")
    while True:
        try:
            print("Connecting to RabbitMQ...")
            rabbit_connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq", port=5672, credentials=credentials)
            )
            print("Success connecting to RabbitMQ!")
            break
        except Exception:
            print("RabbitMQ not ready, retrying in 3s...")
            time.sleep(3)

    channel = rabbit_connection.channel()
    channel.queue_declare(queue="new_movies")

    message = {"Name": "Xmen", "Actors": ["Mark", "Ely"]}

    channel.basic_publish(exchange="", routing_key="new_movies", body=json.dumps(message))

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(data)
        movie_name: str = data["Name"]
        movie_actors: List[str] = data["Actors"]

        while True:
            try:
                print("Connecting to Backend...")
                base_movie_id = requests.get(f"{SERVER_LINK}/get_highest_movie_id").json()["data"]
                print("Success connecting to Backend!")
                break
            except Exception as e:
                print(str(e))
                print("Backend not ready, retrying in 3s...")
                time.sleep(3)

        base_actor_id = requests.get(f"{SERVER_LINK}/get_highest_actor_id").json()["data"]

        movie_id = requests.get(f"{SERVER_LINK}/get_movie_id/{movie_name}").json()["data"]
        movie_id = movie_id[0] if movie_id else base_movie_id + 1
        requests.post(f"{SERVER_LINK}/add_movie/{movie_id}/{movie_name}")

        for index, actor in enumerate(movie_actors):
            actor_id = requests.get(f"{SERVER_LINK}/get_actor_id/{actor}").json()["data"]
            actor_id = actor_id[0] if actor_id else base_actor_id + index + 1
            requests.post(f"{SERVER_LINK}/add_actor/{actor_id}/{actor}")
            requests.post(f"{SERVER_LINK}/add_movie_to_actor/{movie_id}/{actor_id}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="new_movies", on_message_callback=callback)

    channel.start_consuming()
