
from app import db

from app.models.rule import Rule
from app.utils.ast_utils import create_rule

def create_rule_service(name, rule_string):
    ast = create_rule(rule_string)
    new_rule = Rule(name=name, ast=str(ast))
    db.session.add(new_rule)
    db.session.commit()
    return {"message": "Rule added successfully", "id": new_rule.id}

def get_all_rules_service():
    rules = Rule.query.all()
    return [{"id": rule.id, "name": rule.name, "rule": rule.ast} for rule in rules]