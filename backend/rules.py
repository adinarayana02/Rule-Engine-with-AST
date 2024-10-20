class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # 'operator' or 'operand'
        self.value = value  # The value of the operand or the operator ('AND', 'OR')
        self.left = left  # Reference to the left child Node
        self.right = right  # Reference to the right child Node (for operators)


def parse_rule(rule_string):
    """
    Parse the rule string into an Abstract Syntax Tree (AST).
    This method splits the rule based on AND/OR operators and creates nodes.
    """
    if "AND" in rule_string:
        parts = rule_string.split(" AND ")
        left = parse_rule(parts[0].strip())
        right = parse_rule(parts[1].strip())
        return Node("operator", "AND", left, right)
    elif "OR" in rule_string:
        parts = rule_string.split(" OR ")
        left = parse_rule(parts[0].strip())
        right = parse_rule(parts[1].strip())
        return Node("operator", "OR", left, right)
    else:
        value = rule_string.split(' ')
        return Node("operand", value[0], None, value[1:])  # Assuming format "attribute operator value"


def evaluate_ast(ast_node, user_data):
    """
    Evaluate the AST against user data.
    """
    if ast_node.type == "operand":
        attr, operator, value = ast_node.value
        user_value = user_data.get(attr)
        if operator == ">":
            return user_value > int(value)
        elif operator == "<":
            return user_value < int(value)
        elif operator == "=":
            return user_value == value.strip("'")
    elif ast_node.type == "operator":
        if ast_node.value == "AND":
            return evaluate_ast(ast_node.left, user_data) and evaluate_ast(ast_node.right, user_data)
        elif ast_node.value == "OR":
            return evaluate_ast(ast_node.left, user_data) or evaluate_ast(ast_node.right, user_data)


def combine_rules(rules):
    """
    Combine multiple rules into a single rule string.
    """
    combined_rule_string = " AND ".join(rule.RuleString for rule in rules)
    return combined_rule_string


def validate_attributes(rule_string, valid_attributes):
    """
    Validate the attributes used in the rule string against valid attributes.
    Raise ValueError if any attribute is invalid.
    """
    for attr in valid_attributes:
        if attr not in rule_string:
            raise ValueError(f"Invalid attribute: {attr} is not in the rule string.")


def create_rule(rule_string):
    """
    Create a rule by parsing the rule string into an AST.
    This function can be used to validate and create a rule.
    """
    return parse_rule(rule_string)  # Parse the rule string into an AST

def evaluate_rule(rule_string, user_data):
    """
    Evaluate a rule against user data.

    :param rule_string: The rule as a string.
    :param user_data: A dictionary of user attributes.
    :return: Evaluation result (True or False).
    """
    # Parse the rule string into an AST
    ast = parse_rule(rule_string)

    # Evaluate the AST
    return evaluate_ast(ast, user_data)
