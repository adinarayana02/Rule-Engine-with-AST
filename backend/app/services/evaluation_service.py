#services/evaluation_service.py
from app.models.rule import Rule

from app.utils.ast_utils import evaluate_rule, combine_rules
import ast

def evaluate_rules_service(user_data):
    rules = Rule.query.all()
    ast_rules = [ast.literal_eval(rule.ast) for rule in rules]
    combined_rule = combine_rules(ast_rules)
    return evaluate_rule(combined_rule, user_data)