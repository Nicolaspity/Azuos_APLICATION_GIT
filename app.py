import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from flask import Flask, request, jsonify
from azuos_applied_flow.config.config import Config
from azuos_applied_flow.models.usuario import db
from azuos_applied_flow.routes.usuario_routes import usuario_bp
from azuos_applied_flow.services.azuos_service import processar_kickoff

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(usuario_bp)

@app.route("/kickoff", methods=["POST"])
def kickoff():
    data = request.get_json()
    respostas = data.get("respostas", "")
    if not respostas:
        return jsonify({"error": "Campo 'respostas' é obrigatório"}), 400
    return jsonify(processar_kickoff(respostas))

@app.route("/receber", methods=["GET"])
def receber():
    return "FOI"

if __name__ == "__main__":   
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port,debug=False)
