import os


def login(username, password):
    """
    Authenticate user credentials against environment variables.
    
    Args:
        username: The username to authenticate
        password: The password to authenticate
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    # Credentials should be stored in environment variables or a secure credential store
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD")
    
    if admin_password is None:
        # If no password is set in environment, deny access for security
        return False
    
    if username == admin_username and password == admin_password:
        return True
    return False


def calculate_total(price, tax):
    """
    Calculate the total amount including tax.
    
    Args:
        price: The base price
        tax: The tax rate (as a decimal, e.g., 0.1 for 10%)
        
    Returns:
        float: The total amount (price + tax + price*tax)
    """
    return price + tax + (price * tax)


def divide_numbers(a, b):
    """
    Safely divide two numbers with zero-division handling.
    
    Args:
        a: The numerator
        b: The denominator
        
    Returns:
        float: The result of a/b, or None if b is zero
        
    Raises:
        ZeroDivisionError: If b is zero
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def get_user_role(user):
    """
    Determine the role of a user based on their username.
    
    Args:
        user: The username to check
        
    Returns:
        str: The user's role ('admin', 'manager', or 'user')
    """
    if user == "admin":
        return "admin"
    if user == "manager":
        return "manager"
    return "user"

# Made with Bob
