#app/models/rules.py
from app import db

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ast = db.Column(db.Text, nullable=False)
