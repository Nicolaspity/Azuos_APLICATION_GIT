import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from flask import Flask, request, jsonify
from azuos_applied_flow.config.config import Config
from azuos_applied_flow.models.usuario import db
from azuos_applied_flow.routes.usuario_routes import usuario_bp
from azuos_applied_flow.services.azuos_service import processar_kickoff
from flask_cors import CORS
from azuos_applied_flow.models.form import Form

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(usuario_bp)

@app.route("/kickoff", methods=["POST"])
def kickoff():
    data = request.get_json()
    respostas_raw = data.get("respostas", "")
    usuario_id = data.get("usuario_id")

    if not respostas_raw:
        return jsonify({"error": "Campo 'respostas' é obrigatório"}), 400

    if not usuario_id:
        return jsonify({"error": "ID do usuário não enviado"}), 400

    linhas = respostas_raw.strip().split("\n")
    for linha in linhas:
        if not linha.startswith("Pergunta "):
            continue
        try:
            parte1, valor = linha.split(":")
            pergunta_id = int(parte1.strip().split(" ")[1])
            resposta = valor.strip()[0]
        except Exception as e:
            print("Erro ao processar linha: ", linha, e)
            continue
        novo_form = Form(
            usuario_id=usuario_id,
            pergunta_id=pergunta_id,
            resposta=resposta
        )
        db.session.add(novo_form)
    processar_kickoff(respostas_raw)
    db.session.commit()
    return jsonify({"mensagem": "Respostas salvas com sucesso"})

@app.route("/receber", methods=["GET"])
def receber():
    return "FOI"

if __name__ == "__main__":   
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port,debug=False)
