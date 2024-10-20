class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

def create_rule(rule_string):
    tokens = rule_string.replace('(', ' ( ').replace(')', ' ) ').split()
    def parse():
        if not tokens:
            return None
        token = tokens.pop(0)
        if token == '(':
            node = Node('operator')
            node.left = parse()
            node.type = tokens.pop(0)  # AND or OR
            node.right = parse()
            tokens.pop(0)  # Remove closing parenthesis
            return node
        else:
            return Node('operand', value=token)
    return parse()

def combine_rules(rules):
    if not rules:
        return None
    if len(rules) == 1:
        return rules[0]
    combined = Node('operator', type='AND')
    combined.left = rules[0]
    combined.right = combine_rules(rules[1:])
    return combined

def evaluate_rule(node, data):
    if node['type'] == 'operator':
        if node['type'] == 'AND':
            return evaluate_rule(node['left'], data) and evaluate_rule(node['right'], data)
        elif node['type'] == 'OR':
            return evaluate_rule(node['left'], data) or evaluate_rule(node['right'], data)
    elif node['type'] == 'operand':
        attribute, operator, value = node['value'].split()
        if operator == '=':
            return data.get(attribute) == value
        elif operator == '>':
            return data.get(attribute) > float(value)
        elif operator == '<':
            return data.get(attribute) < float(value)
    return False
