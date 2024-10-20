from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Tadi2024@LAPTOP-K55CLBQO\\SQLEXPRESS/RuleEngineDB?driver=ODBC+Driver+17+for+SQL+Server'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.rule_routes import rule_bp
    from app.routes.evaluation_routes import evaluation_bp

    app.register_blueprint(rule_bp, url_prefix='/api')
    app.register_blueprint(evaluation_bp, url_prefix='/api')

    return app
