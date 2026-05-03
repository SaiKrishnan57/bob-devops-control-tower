def login(username, password):
    # Hardcoded credentials (security issue)
    if username == "admin" and password == "admin123":
        return True
    return False


def calculate_total(price, tax_rate):
    # No validation for negative values
    total = price + (price * tax_rate)
    return total


def divide_numbers(a, b):
    # Unsafe division (no zero check)
    return a / b


def get_user_role(user):
    # Repetitive logic (can be simplified)
    if user == "admin":
        return "admin"
    elif user == "manager":
        return "manager"
    elif user == "guest":
        return "guest"
    else:
        return "user"


def apply_discount(price, discount):
    # No validation for discount range
    return price - (price * discount)