#routes/rule_routes.py
from flask import Blueprint, request, jsonify
from app.services.rule_service import create_rule_service, get_all_rules_service

rule_bp = Blueprint('rule', __name__)

@rule_bp.route('/rule', methods=['POST'])
def add_rule():
    data = request.json
    name = data['name']
    rule_string = data['rule']
    result = create_rule_service(name, rule_string)
    return jsonify(result), 201

@rule_bp.route('/rules', methods=['GET'])
def get_rules():
    rules = get_all_rules_service()
    return jsonify(rules), 200