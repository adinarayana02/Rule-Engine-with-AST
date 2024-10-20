#routes/evaluation_routes.py
from flask import Blueprint, request, jsonify
from app.services.evaluation_service import evaluate_rules_service

evaluation_bp = Blueprint('evaluation', __name__)

@evaluation_bp.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    user_data = data['user_data']
    result = evaluate_rules_service(user_data)
    return jsonify({"result": result}), 200