import re
from datetime import datetime, timedelta

def validate_consumer_input(username, phone, meter_number):
    """
    Validates consumer input.
    Returns: (is_valid, error_message)
    """
    # Name validation: Alphabets only
    if not re.match(r'^[a-zA-Z]+$', username):
        return False, "Name must contain alphabets only (no numbers or special characters)."
    
    # Phone validation: Exactly 10 digits
    if not re.match(r'^\d{10}$', phone):
        return False, "Phone number must be exactly 10 digits."
    
    # Service Number validation: Basic check (Uniqueness checked in DB query)
    if not meter_number:
        return False, "Service Number (Meter Number) is required."

    return True, None

def calculate_bill_amount(units_consumed):
    """
    Computes bill amount based on tiered rates.
    1. First 50 units – 1.5
    2. Second 50 units – 2.5 (51-100)
    3. Third 50 units – 3.5 (101-150)
    4. Later onwards – 4.5 (>150)
    
    Min charge: 25/- if units 0
    """
    if units_consumed <= 0:
        return 25.0
    
    amount = 0.0
    remaining_units = units_consumed
    
    # Tier 1: 0-50 @ 1.5
    tier1 = min(remaining_units, 50)
    amount += tier1 * 1.5
    remaining_units -= tier1
    
    # Tier 2: 51-100 @ 2.5
    if remaining_units > 0:
        tier2 = min(remaining_units, 50)
        amount += tier2 * 2.5
        remaining_units -= tier2
        
    # Tier 3: 101-150 @ 3.5
    if remaining_units > 0:
        tier3 = min(remaining_units, 50)
        amount += tier3 * 3.5
        remaining_units -= tier3
        
    # Tier 4: >150 @ 4.5
    if remaining_units > 0:
        amount += remaining_units * 4.5
        
    return amount

def get_due_dates(bill_date):
    """
    Returns (due_date, fine_amount)
    """
    due_date = bill_date + timedelta(days=15) # Assuming 15 days to pay
    fine_amount = 150.0
    return due_date, fine_amount
