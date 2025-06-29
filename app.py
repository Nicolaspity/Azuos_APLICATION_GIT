from flask import Flask, request, jsonify
from azuos_applied_flow.main import AzuosFlow, ReportState

app = Flask(__name__)

@app.route("/kickoff", methods=["POST"])
def kickoff():
    data = request.get_json()
    respostas = data.get("respostas", "")

    if not respostas:
        return jsonify({"error": "Campo 'respostas' é obrigatório"}), 400

    # Cria estado inicial (opcional, se você quiser pré-popular mais coisas)
    state = ReportState()

    # Cria Flow
    flow = AzuosFlow(state=state)

    # Kickoff com inputs (isso dispara TODOS os steps)
    final_state = flow.kickoff(inputs={"respostas": respostas})

    # Responde estado final
    return jsonify(final_state.dict())
@app.route("/receber", methods=["GET"])
def receber():
    print('FOI')
    return "FOI"
if __name__ == "__main__":
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
