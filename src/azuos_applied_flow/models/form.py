from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Form(db.Model):
  __tablename__ = 'form'
  id = db.Column(db.Integer, primary_key=True)
  usuario_id = db.Column(db.Integer, nullable=True)
  pergunta_id = db.Column(db.Integer, nullable=True)
  dt_envio = db.Column(db.DateTime, default=datetime.now)
  resposta = db.Column(db.String(1), nullable=True)
