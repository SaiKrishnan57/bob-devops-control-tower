def login(username, password):
    if username == "admin" and password == "admin123":
        return True
    return False


def calculate_total(price, tax):
    return price + tax + (price * tax)


def divide_numbers(a, b):
    return a / b


def get_user_role(user):
    if user == "admin":
        return "admin"
    if user == "manager":
        return "manager"
    return "user"