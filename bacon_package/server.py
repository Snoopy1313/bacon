from flask import Flask, abort, request
from bacon_package.bacon_distance import bacon_distance
from flask_cors import CORS

app = Flask("rpyc")
CORS(app)


@app.get("/get_bacon_distance/<source_id>/<target_id>")
def get_bacon_distance(source_id: str, target_id: str):
    try:
        return str(bacon_distance(int(source_id), int(target_id)))
    except LookupError:
        return abort(400)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)