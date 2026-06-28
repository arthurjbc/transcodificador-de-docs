import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stubs"))

import grpc
import transcoder_pb2
import transcoder_pb2_grpc
from flask import Flask, jsonify, render_template, request, Response

GRPC_TARGET = os.environ.get("GRPC_TARGET", "localhost:50051")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    return jsonify()

@app.route("/stats")
def stats():
    interval = request.args.get("interval", default=0.0, type=float)

    def event_stream():
        with grpc.insecure_channel(GRPC_TARGET) as channel:
            stub = transcoder_pb2_grpc.TranscoderServiceStub(channel)
            grpc_request = transcoder_pb2.StatsRequest(interval_seconds=interval)
            try:
                for snap in stub.Stats(grpc_request):
                    payload = json.dumps({
                        "active": snap.active,
                        "peak": snap.peak,
                        "total": snap.total,
                        "failed": snap.failed,
                        "bytes_in": snap.bytes_in,
                        "bytes_out": snap.bytes_out,
                    })
                    yield f"data: {payload}\n\n"
            except grpc.RpcError as exc:
                err = json.dumps({"error": f"{exc.code()}: {exc.details()}"})
                yield f"event: error\ndata: {err}\n\n"

    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )

app.run(host="127.0.0.1", port=5000, debug=True, threaded=True)
