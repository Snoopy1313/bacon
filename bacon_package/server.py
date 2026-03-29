from flask import Flask, abort, jsonify
from bacon_package.bacon_distance import bacon_distance, initialize_connection
from bacon_package.db_generate import (
    get_movie_id,
    add_movie,
    get_actor_id,
    add_actor,
    add_movie_to_actor,
    get_highest_actor_id,
    get_highest_movie_id,
)
from flask_cors import CORS
from http import HTTPStatus

app = Flask("server")
CORS(app)
conn = initialize_connection()


@app.get("/get_bacon_distance/<source_name>/<target_name>")
def get_bacon_distance(source_name: str, target_name: str):
    source_id = get_actor_id(source_name, conn)
    if not source_id:
        return jsonify(error="Bad Request", message=f"No such actor as: {source_name}"), 400

    target_id = get_actor_id(target_name, conn)
    if not target_id:
        return jsonify(error="Bad Request", message=f"No such actor as: {target_name}"), 400
    
    try:
        return jsonify(distance=str(bacon_distance(source_id[0], target_id[0]))), 200
    except LookupError as e:
        return jsonify(error="Bad Request", message=str(e)), 400

@app.get("/get_movie_id/<movie_name>/")
def get_movie_id_from_db(movie_name: str):
    return jsonify(data=get_movie_id(movie_name, conn))

@app.get("/get_actor_id/<actor_name>/")
def get_actor_id_from_db(actor_name: str):
    return jsonify(data=get_actor_id(actor_name, conn))

@app.get("/get_highest_actor_id/")
def get_highest_actor_id_from_db():
    return jsonify(data=get_highest_actor_id(conn))

@app.get("/get_highest_movie_id/")
def get_highest_movie_id_from_db():
    return jsonify(data=get_highest_movie_id(conn))

@app.post("/add_movie/<movie_id>/<movie_name>/")
def add_movie_to_db(movie_id: str, movie_name: str):
    return jsonify(data=add_movie(int(movie_id), movie_name, conn))

@app.post("/add_actor/<actor_id>/<actor_name>/")
def add_actor_to_db(actor_id: str, actor_name: str):
    return jsonify(data=add_actor(int(actor_id), actor_name, conn))

@app.post("/add_movie_to_actor/<movie_id>/<actor_id>/")
def add_movie_to_actor_to_db(movie_id: str, actor_id: str):
    return jsonify(add_movie_to_actor(int(movie_id), int(actor_id), conn))

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
