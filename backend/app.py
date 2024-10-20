from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import Session
from models import UserData, Rule, CombinedRule, RuleEvaluationHistory, Attribute
from rules import create_rule, combine_rules, evaluate_rule, validate_attributes
import json
from config import SECRET_KEY, DEBUG

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Reference to the left child Node
        self.right = right  # Reference to the right child Node (for operators)
        self.value = value  # Optional value for operand nodes (e.g., number for comparisons)

def parse_rule(rule_string):
    # Implement a proper parser logic
    rule_string = rule_string.replace('(', '').replace(')', '').strip()
    if "AND" in rule_string:
        parts = rule_string.split(" AND ")
        left = parse_rule(parts[0].strip())
        right = parse_rule(parts[1].strip())
        return Node("operator", left, right, "AND")
    elif "OR" in rule_string:
        parts = rule_string.split(" OR ")
        left = parse_rule(parts[0].strip())
        right = parse_rule(parts[1].strip())
        return Node("operator", left, right, "OR")
    else:
        parts = rule_string.split(' ')
        if len(parts) == 3:
            attr = parts[0].strip()  # e.g., 'age'
            operator = parts[1].strip()  # e.g., '>'
            value = parts[2].strip()  # e.g., '30' or '30'
            # Clean up any surrounding quotes if they exist
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            return Node("operand", None, None, [attr, operator, value])  # Return the full parts as value
        else:
            raise ValueError("Invalid rule format. Expected format: 'attribute operator value'")
def evaluate_ast(ast_node, user_data):
    if ast_node.type == "operand":
        attr, operator, value = ast_node.value
        if attr not in user_data:
            raise ValueError(f"Attribute '{attr}' not found in user data.")
        if operator == ">":
            return user_data[attr] > int(value)
        elif operator == "<":
            return user_data[attr] < int(value)
        elif operator == "=":
            return user_data[attr] == value.strip("'")
        else:
            raise ValueError(f"Unsupported operator '{operator}'.")
    elif ast_node.type == "operator":
        if ast_node.value == "AND":
            return evaluate_ast(ast_node.left, user_data) and evaluate_ast(ast_node.right, user_data)
        elif ast_node.value == "OR":
            return evaluate_ast(ast_node.left, user_data) or evaluate_ast(ast_node.right, user_data)

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create_rule', methods=['POST'])
def api_create_rule():
    data = request.json
    rule_name = data.get('rule_name')
    rule_string = data.get('rule_string')
    description = data.get('description')

    session = Session()
    try:
        # Validate attributes
        valid_attributes = [attr.AttributeName for attr in session.query(Attribute).all()]
        validate_attributes(rule_string, valid_attributes)

        # Create rule
        new_rule = Rule(RuleName=rule_name, RuleString=rule_string, Description=description)
        session.add(new_rule)
        session.commit()
        rule_id = new_rule.RuleID
        return jsonify({"message": "Rule created successfully", "rule_id": rule_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route('/api/get_rules', methods=['GET'])
def api_get_rules():
    session = Session()
    rules = session.query(Rule).all()
    rules_list = [{"id": rule.RuleID, "name": rule.RuleName, "string": rule.RuleString, "description": rule.Description}
                  for rule in rules]
    session.close()
    return jsonify(rules_list)

@app.route('/api/combine_rules', methods=['POST'])
def api_combine_rules():
    rule_ids = request.json.get('rule_ids', [])
    session = Session()
    try:
        rules = [session.query(Rule).get(id) for id in rule_ids]
        rule_strings = [rule.RuleString for rule in rules if rule]
        combined_rule_string = " AND ".join(rule_strings)  # Combine rule strings with "AND"

        # Store combined rule in CombinedRules table
        new_combined_rule = CombinedRule(CombinedRuleName=f"Combined Rule {len(rule_ids)}",
                                         CombinedRuleString=combined_rule_string)
        session.add(new_combined_rule)
        session.commit()

        return jsonify({"combined_rule": combined_rule_string})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route('/api/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    rule_id = request.json.get('rule_id')
    data = request.json.get('data')

    session = Session()
    try:
        rule = session.query(Rule).get(rule_id)
        if not rule:
            return jsonify({"error": "Rule not found"}), 404

        # Parse the rule string into an AST
        ast = parse_rule(rule.RuleString)

        # Evaluate the AST
        result = evaluate_ast(ast, data)

        # Store evaluation history
        evaluation_history = RuleEvaluationHistory(
            RuleID=rule_id,
            EvaluationResult=result,
            EvaluatedData=json.dumps(data)
        )
        session.add(evaluation_history)
        session.commit()
        return jsonify({"result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/api/add_user_data', methods=['POST'])
def api_add_user_data():
    data = request.json
    session = Session()
    try:
        new_user_data = UserData(Age=data['age'], Department=data['department'],
                                  Salary=data['salary'], Experience=data['experience'])
        session.add(new_user_data)
        session.commit()
        return jsonify({"message": "User data added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route('/api/add_attribute', methods=['POST'])
def api_add_attribute():
    data = request.json
    attribute_name = data.get('attribute_name')
    attribute_type = data.get('attribute_type')

    session = Session()
    try:
        new_attribute = Attribute(AttributeName=attribute_name, AttributeType=attribute_type)
        session.add(new_attribute)
        session.commit()
        return jsonify({"message": "Attribute added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route('/api/modify_rule', methods=['PUT'])
def api_modify_rule():
    data = request.json
    rule_id = data.get('rule_id')
    new_rule_string = data.get('new_rule_string')

    session = Session()
    try:
        rule = session.query(Rule).get(rule_id)
        if not rule:
            return jsonify({"error": "Rule not found"}), 404

        # Validate attributes
        valid_attributes = [attr.AttributeName for attr in session.query(Attribute).all()]
        validate_attributes(new_rule_string, valid_attributes)

        rule.RuleString = new_rule_string
        session.commit()
        return jsonify({"message": "Rule modified successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=DEBUG)
