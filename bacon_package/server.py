from flask import Flask, abort, jsonify
from bacon_package.bacon_distance import bacon_distance, get_actor_id, initialize_connection
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


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
