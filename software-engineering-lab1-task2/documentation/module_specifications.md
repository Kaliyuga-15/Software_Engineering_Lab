Electricity Billing System – Module Description
1. Introduction

This document explains the main modules of the Electricity Billing System. The system is built to manage consumer registration, employee management, and electricity bill generation in an organized way.

To avoid repeating the same logic in multiple places, common functions are grouped inside a utility module. This makes the system cleaner, easier to maintain, and more reusable.

2. Utility Module (utils.py)

The utility module works like a shared helper library for the entire application. Instead of rewriting common logic in different files, we define it once here and reuse it wherever needed.

2.1 Input Validation (validate_user_input)

This function is responsible for checking whether the user’s input is valid before saving it to the database.

Purpose:
To prevent incorrect or invalid data (for example, a name containing numbers or an invalid phone number) from being stored.

Inputs:

username (String)

phone (String)

How it works:

First, it checks whether the username is provided.

If it is provided, a Regular Expression (^[a-zA-Z\s]+$) is used to ensure the name contains only alphabets and spaces.

Then, it validates the phone number using the pattern (^\d{10}$) to confirm that it contains exactly 10 digits.

Output:
The function returns a list of error messages.

If the list is empty → the input is valid.

If the list contains messages → those errors must be corrected.

2.2 Bill Calculation (calculate_bill_amount)

This function contains the main logic for calculating the electricity bill based on the number of units consumed.

Purpose:
To correctly apply the tier-based pricing system while calculating the bill amount.

Input:

units (Number of electricity units consumed)

Pricing Logic (Tier System):

Minimum Charge:
If the consumption is 0 units, a base charge of Rs. 25.0 is applied.

0 – 50 Units:
Rs. 1.5 per unit

51 – 100 Units:
Rs. 2.5 per unit

101 – 150 Units:
Rs. 3.5 per unit

Above 150 Units:
Rs. 4.5 per unit

The calculation follows this structure and returns the total amount as a float value.

3. Administrative Module (routes/admin.py)

This module handles operations that only an administrator is allowed to perform. It mainly manages the registration of consumers and employees.

3.1 Consumer Registration

This feature allows the administrator to add new electricity consumers to the system.

Process:

The admin enters details such as:

Username

Phone number

Password

Meter number

Connection type

The system calls the validate_user_input function to verify the name and phone number format.

It checks the database to ensure the meter number is unique (no duplicate meter numbers allowed).

If all validations pass, a new user record is created with the role set as 'consumer'.

3.2 Employee Registration

This feature allows the admin to register new employees (meter readers).

Process:

The system validates the employee’s personal details using the same validation function.

It ensures that the employee_id is unique in the database.

If everything is valid, a new user record is created with the role set as 'employee'.

4. Employee Module (routes/employee.py)

This module is designed specifically for meter readers. Their main responsibility is generating electricity bills based on meter readings.

4.1 Bill Generation

This feature allows an employee to generate a new bill for a particular meter.

Process:

The employee enters:

Meter number

Current meter reading

The system retrieves the last recorded reading for that meter.

If no previous record exists, it assumes the previous reading is 0.

The system validates that the current reading is greater than or equal to the previous reading.
(This prevents incorrect or manipulated entries.)

Units consumed are calculated as:
Units = Current Reading – Previous Reading

The system calls the calculate_bill_amount function to compute the total bill based on units consumed.

A fixed fine of Rs. 150 is noted (applicable only if the bill is paid after the due date).

Finally, the bill is saved in the database with the status set to 'Unpaid'.

5. Algorithms / Pseudo Code

This section presents the core logic in pseudo code format for better understanding.

5.1 Input Validation Algorithm

```
FUNCTION validate_user_input(username, phone)
    errors = empty list
    
    IF username is empty THEN
        ADD "Username is required" to errors
    ELSE IF username contains numbers or special characters THEN
        ADD "Name must contain alphabets only" to errors
    END IF
    
    IF phone is empty THEN
        ADD "Phone is required" to errors
    ELSE IF length of phone is NOT 10 digits THEN
        ADD "Phone must be 10 digits" to errors
    END IF
    
    RETURN errors
END FUNCTION
```

5.2 Bill Calculation Algorithm

```
FUNCTION calculate_bill_amount(units)
    IF units = 0 THEN
        RETURN 25.0    // Minimum charge
    END IF
    
    amount = 0
    remaining = units
    
    // Tier 1: First 50 units at Rs. 1.5
    tier1_units = MINIMUM(remaining, 50)
    amount = amount + (tier1_units * 1.5)
    remaining = remaining - tier1_units
    
    // Tier 2: Next 50 units at Rs. 2.5
    IF remaining > 0 THEN
        tier2_units = MINIMUM(remaining, 50)
        amount = amount + (tier2_units * 2.5)
        remaining = remaining - tier2_units
    END IF
    
    // Tier 3: Next 50 units at Rs. 3.5
    IF remaining > 0 THEN
        tier3_units = MINIMUM(remaining, 50)
        amount = amount + (tier3_units * 3.5)
        remaining = remaining - tier3_units
    END IF
    
    // Tier 4: Remaining units at Rs. 4.5
    IF remaining > 0 THEN
        amount = amount + (remaining * 4.5)
    END IF
    
    RETURN amount
END FUNCTION
```

5.3 Bill Generation Workflow

```
FUNCTION generate_bill(meter_number, current_reading)
    // Step 1: Validate Input
    IF meter_number is empty THEN
        DISPLAY "Meter Number Required"
        EXIT
    END IF
    
    IF current_reading < 0 THEN
        DISPLAY "Invalid Reading"
        EXIT
    END IF
    
    // Step 2: Fetch Consumer
    consumer = FIND user WHERE meter_number matches
    IF consumer NOT FOUND THEN
        DISPLAY "Consumer not found"
        EXIT
    END IF
    
    // Step 3: Get Previous Reading
    last_bill = GET latest bill for consumer
    IF last_bill EXISTS THEN
        previous_reading = last_bill.current_reading
    ELSE
        previous_reading = 0
    END IF
    
    // Step 4: Validate Reading
    IF current_reading < previous_reading THEN
        DISPLAY "Current reading cannot be less than previous"
        EXIT
    END IF
    
    // Step 5: Calculate Bill
    units_consumed = current_reading - previous_reading
    bill_amount = calculate_bill_amount(units_consumed)
    fine = 150.0
    due_date = today + 30 days
    
    // Step 6: Check Previous Pending
    pending_bills = GET all unpaid bills for consumer
    previous_pending = SUM of pending_bills amounts
    
    // Step 7: Save and Display
    SAVE new bill to database
    DISPLAY bill receipt with all details
END FUNCTION
```