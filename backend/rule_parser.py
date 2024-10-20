class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left      # Reference to the left child Node
        self.right = right    # Reference to the right child Node (for operators)
        self.value = value    # Optional value for operand nodes (e.g., number for comparisons)

def parse_rule(rule_string):
    # Placeholder parser logic; implement a proper parser here
    # For example: This could use a library like pyparsing or a simple tokenizer
    # Here, I'm assuming rules are well-formed for simplicity

    # Example parsing for the rule: "(age > 30 AND department = 'Sales')"
    if "AND" in rule_string:
        parts = rule_string.split(" AND ")
        left = parse_rule(parts[0].strip())
        right = parse_rule(parts[1].strip())
        return Node("operator", left, right)
    elif "OR" in rule_string:
        parts = rule_string.split(" OR ")
        left = parse_rule(parts[0].strip())
        right = parse_rule(parts[1].strip())
        return Node("operator", left, right)
    else:
        # Simplified assumption: single condition
        # Example: "age > 30"
        value = rule_string.split(' ')
        return Node("operand", value[0], None, value[1:])

def evaluate_ast(ast_node, user_data):
    if ast_node.type == "operand":
        attr, operator, value = ast_node.value
        if operator == ">":
            return user_data[attr] > int(value)
        elif operator == "<":
            return user_data[attr] < int(value)
        elif operator == "=":
            return user_data[attr] == value.strip("'")
    elif ast_node.type == "operator":
        if ast_node.value == "AND":
            return evaluate_ast(ast_node.left, user_data) and evaluate_ast(ast_node.right, user_data)
        elif ast_node.value == "OR":
            return evaluate_ast(ast_node.left, user_data) or evaluate_ast(ast_node.right, user_data)
