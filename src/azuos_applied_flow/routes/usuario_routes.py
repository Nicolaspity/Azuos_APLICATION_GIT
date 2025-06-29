from flask import Blueprint, request, jsonify
from azuos_applied_flow.models.usuario import db, Usuario
from datetime import datetime

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route("/cadastrar_usuario", methods=["POST"])
def cadastrar_usuario():
    data = request.get_json()
    try:
        usuario = Usuario(
            nome=data.get("nome"),
            email=data.get("email"),
            nascimento=datetime.strptime(data.get("nascimento"), "%Y-%m-%d").date(),
            cargo=data.get("cargo"),
            setor=data.get("setor"),
            empresa=data.get("empresa"),
            ramo=data.get("ramo"),
            categoria=data.get("categoria"),
            senha=data.get("senha"),
        )
        db.session.add(usuario)
        db.session.commit()
        return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400

@usuario_bp.route("/login_usuario", methods=["POST"])
def login_usuario():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios."}), 400

    usuario = Usuario.query.filter_by(email=email, senha=senha).first()

    if usuario:
        return jsonify({"mensagem": "Login realizado com sucesso!", "usuario_id": usuario.id}), 200
    else:
        return jsonify({"erro": "Email ou senha inválidos."}), 401

