from flask import Flask, abort, request
from bacon_package.bacon_distance import bacon_distance, get_actor_id, initialize_connection
from flask_cors import CORS

app = Flask("rpyc")
CORS(app)
conn = initialize_connection()

@app.get("/get_bacon_distance/<source_name>/<target_name>")
def get_bacon_distance(source_name: str, target_name: str):
    try:
        source_id = get_actor_id(source_name, conn)[0]
        target_id = get_actor_id(target_name, conn)[0]
        return str(bacon_distance(source_id, target_id))
    except LookupError:
        return abort(400)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)