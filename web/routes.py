import logging
from flask import Blueprint, request, jsonify, Response
import grpc
from web.grpc_client import call_convert_stream, call_monitor_stats

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__)

@api_bp.route("/transcode", methods=["POST"])
def transcode_file():
    if "file" not in request.files:
        return jsonify({"error_message": "Nenhum arquivo enviado na requisição."}), 400

    uploaded_file = request.files["file"]
    if not uploaded_file.filename.endswith(".md"):
        return jsonify({"error_message": "Apenas extensões .md são permitidas."}), 400

    try:
        file_content = uploaded_file.read()
        
        response = call_convert_stream(file_content)
        
        if not response.integrity_ok:
            return jsonify({
                "integrity_ok": False,
                "error_message": response.error_message or "Falha de integridade no servidor gRPC."
            }), 400

        return jsonify({
            "integrity_ok": True,
            "filename": uploaded_file.filename.replace(".md", ".html"),
            "content": response.content.decode("utf-8"),
            "output_size": response.output_size
        })

    except grpc.RpcError as e:
        logger.error(f"Erro na comunicação gRPC: {e.details()}")
        return jsonify({"error_message": f"Servidor gRPC indisponível: {e.details()}"}), 503
    except Exception as e:
        logger.exception("Erro interno no BFF:")
        return jsonify({"error_message": f"Erro interno: {str(e)}"}), 500


@api_bp.route("/stats", methods=["GET"])
def stream_stats():
    def event_stream():
        try:
            for stats in call_monitor_stats():
                yield f"data: {{\"active\": {stats.active}, \"peak\": {stats.peak}, \"total\": {stats.total}, \"failed\": {stats.failed}, \"bytes_in\": {stats.bytes_in}, \"bytes_out\": {stats.bytes_out}}}\n\n"
        except grpc.RpcError:
            yield "data: {\"error\": \"Conexão gRPC de monitoramento perdida.\"}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")