import pytest
import os
from unittest.mock import patch
from app import login, calculate_total, divide_numbers, get_user_role


class TestLogin:
    """Tests for the login function."""
    
    @patch.dict(os.environ, {"ADMIN_USERNAME": "admin", "ADMIN_PASSWORD": "secure_pass"})
    def test_login_valid_credentials(self):
        """Test login with valid credentials."""
        assert login("admin", "secure_pass") is True
    
    @patch.dict(os.environ, {"ADMIN_USERNAME": "admin", "ADMIN_PASSWORD": "secure_pass"})
    def test_login_invalid_password(self):
        """Test login with invalid password."""
        assert login("admin", "wrong_pass") is False
    
    @patch.dict(os.environ, {"ADMIN_USERNAME": "admin", "ADMIN_PASSWORD": "secure_pass"})
    def test_login_invalid_username(self):
        """Test login with invalid username."""
        assert login("hacker", "secure_pass") is False
    
    @patch.dict(os.environ, {"ADMIN_USERNAME": "admin"}, clear=True)
    def test_login_no_password_env_var(self):
        """Test login when ADMIN_PASSWORD environment variable is not set."""
        assert login("admin", "any_password") is False


class TestCalculateTotal:
    """Tests for the calculate_total function."""
    
    def test_calculate_total_positive_values(self):
        """Test calculate_total with positive values."""
        result = calculate_total(100, 0.1)
        assert result == 110.0  # 100 + 0.1 + (100 * 0.1)
    
    def test_calculate_total_zero_tax(self):
        """Test calculate_total with zero tax."""
        result = calculate_total(100, 0)
        assert result == 100.0
    
    def test_calculate_total_high_tax(self):
        """Test calculate_total with high tax rate."""
        result = calculate_total(50, 0.25)
        assert result == 62.75  # 50 + 0.25 + (50 * 0.25)
    
    def test_calculate_total_decimal_price(self):
        """Test calculate_total with decimal price."""
        result = calculate_total(99.99, 0.08)
        expected = 99.99 + 0.08 + (99.99 * 0.08)
        assert abs(result - expected) < 0.01


class TestDivideNumbers:
    """Tests for the divide_numbers function."""
    
    def test_divide_numbers_positive(self):
        """Test divide_numbers with positive numbers."""
        assert divide_numbers(10, 2) == 5.0
    
    def test_divide_numbers_negative(self):
        """Test divide_numbers with negative numbers."""
        assert divide_numbers(-10, 2) == -5.0
        assert divide_numbers(10, -2) == -5.0
    
    def test_divide_numbers_decimal_result(self):
        """Test divide_numbers with decimal result."""
        assert divide_numbers(10, 3) == pytest.approx(3.333333, rel=1e-5)
    
    def test_divide_numbers_zero_numerator(self):
        """Test divide_numbers with zero numerator."""
        assert divide_numbers(0, 5) == 0.0
    
    def test_divide_numbers_zero_denominator(self):
        """Test divide_numbers raises ZeroDivisionError for zero denominator."""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            divide_numbers(10, 0)
    
    def test_divide_numbers_large_numbers(self):
        """Test divide_numbers with large numbers."""
        assert divide_numbers(1000000, 1000) == 1000.0


class TestGetUserRole:
    """Tests for the get_user_role function."""
    
    def test_get_user_role_admin(self):
        """Test get_user_role returns 'admin' for admin user."""
        assert get_user_role("admin") == "admin"
    
    def test_get_user_role_manager(self):
        """Test get_user_role returns 'manager' for manager user."""
        assert get_user_role("manager") == "manager"
    
    def test_get_user_role_regular_user(self):
        """Test get_user_role returns 'user' for regular user."""
        assert get_user_role("john_doe") == "user"
    
    def test_get_user_role_empty_string(self):
        """Test get_user_role returns 'user' for empty string."""
        assert get_user_role("") == "user"
    
    def test_get_user_role_case_sensitive(self):
        """Test get_user_role is case-sensitive."""
        assert get_user_role("Admin") == "user"
        assert get_user_role("MANAGER") == "user"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
