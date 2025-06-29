from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(80))
    nascimento = db.Column(db.Date)
    cargo = db.Column(db.String(30))
    setor = db.Column(db.String(30))
    empresa = db.Column(db.String(30))
    ramo = db.Column(db.String(50))
    categoria = db.Column(db.String(30))
