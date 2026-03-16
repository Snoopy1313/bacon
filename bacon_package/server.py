from flask import Flask, request
from bacon_package.bacon_distance import bacon_distance

app = Flask("rpyc")


@app.get("/get_bacon_distance/<source_id>/<target_id>")
def get_bacon_distance(source_id: int, target_id: int):
    return bacon_distance(source_id, target_id)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)