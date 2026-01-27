import re

def validate_user_input(username, phone):
    """
    Validates user registration input.
    Returns a list of error strings.
    """
    errors = []
    
    if not username:
        errors.append("Username is required")
    elif not re.match(r'^[a-zA-Z\s]+$', username):
        errors.append("Name must contain alphabets only")
        
    if not phone:
        errors.append("Phone is required")
    elif not re.match(r'^\d{10}$', phone):
        errors.append("Phone must be 10 digits")
        
    return errors

def calculate_bill_amount(units):
    """
    Calculates electricity bill based on tiered rates.
    """
    if units == 0:
        return 25.0  # Minimum charge
    
    amount = 0.0
    rem = units
    
    # First 50 units @ 1.5
    s1 = min(rem, 50)
    amount += s1 * 1.5
    rem -= s1
    
    if rem > 0:
        # Second 50 units @ 2.5
        s2 = min(rem, 50)
        amount += s2 * 2.5
        rem -= s2
        
    if rem > 0:
        # Third 50 units @ 3.5
        s3 = min(rem, 50)
        amount += s3 * 3.5
        rem -= s3
        
    if rem > 0:
        # Later onwards @ 4.5
        amount += rem * 4.5
        
    return amount
