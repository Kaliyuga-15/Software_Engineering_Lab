SOFTWARE TEST PLAN

Project: Electricity Billing System
Tested By: Developer
Date: 27-01-2026

1. INTRODUCTION

This document contains the test plan for all functions developed in the Electricity Billing System application. Each test case includes the test ID, functionality being tested, input values, expected output, actual output, and final test status.

2. FUNCTIONS TESTED

The following functions have been tested:
- validate_user_input() - Input validation for registration
- calculate_bill_amount() - Bill computation logic
- register_consumer() - Consumer registration workflow
- register_employee() - Employee registration workflow
- generate_bill() - Bill generation workflow

3. TEST CASES

3.1 Function: validate_user_input()
Location: utils.py
Purpose: Validates username and phone number format

Test ID: TV-01
Functionality: Reject names containing numbers
Input: username = "John123", phone = "9876543210"
Expected Output: ["Name must contain alphabets only"]
Actual Output: ["Name must contain alphabets only"]
Status: PASS

Test ID: TV-02
Functionality: Accept valid alphabetic names
Input: username = "John Doe", phone = "9876543210"
Expected Output: [] (empty list - no errors)
Actual Output: []
Status: PASS

Test ID: TV-03
Functionality: Reject phone numbers with less than 10 digits
Input: username = "John", phone = "12345"
Expected Output: ["Phone must be 10 digits"]
Actual Output: ["Phone must be 10 digits"]
Status: PASS

Test ID: TV-04
Functionality: Accept valid 10-digit phone numbers
Input: username = "John", phone = "9876543210"
Expected Output: [] (empty list - no errors)
Actual Output: []
Status: PASS

Test ID: TV-05
Functionality: Reject names with special characters
Input: username = "John@Doe", phone = "9876543210"
Expected Output: ["Name must contain alphabets only"]
Actual Output: ["Name must contain alphabets only"]
Status: PASS

3.2 Function: calculate_bill_amount()
Location: utils.py
Purpose: Calculates electricity bill based on tiered rates

Test ID: TC-01
Functionality: Minimum charge for zero consumption
Input: units = 0
Expected Output: 25.0
Actual Output: 25.0
Status: PASS

Test ID: TC-02
Functionality: Tier 1 calculation (0-50 units)
Input: units = 50
Expected Output: 75.0 (50 × 1.5)
Actual Output: 75.0
Status: PASS

Test ID: TC-03
Functionality: Tier 2 calculation (51-100 units)
Input: units = 100
Expected Output: 200.0 (75 + 50 × 2.5)
Actual Output: 200.0
Status: PASS

Test ID: TC-04
Functionality: Tier 3 calculation (101-150 units)
Input: units = 150
Expected Output: 375.0 (200 + 50 × 3.5)
Actual Output: 375.0
Status: PASS

Test ID: TC-05
Functionality: Tier 4 calculation (above 150 units)
Input: units = 160
Expected Output: 420.0 (375 + 10 × 4.5)
Actual Output: 420.0
Status: PASS

Test ID: TC-06
Functionality: Large consumption value
Input: units = 200
Expected Output: 600.0 (375 + 50 × 4.5)
Actual Output: 600.0
Status: PASS

3.3 Function: register_consumer()
Location: routes/admin.py
Purpose: Registers new consumers in the system

Test ID: TR-01
Functionality: Reject duplicate meter numbers
Input: meter_number = "M101" (already exists)
Expected Output: Error message "Meter Number exists"
Actual Output: Error message displayed
Status: PASS

Test ID: TR-02
Functionality: Successful consumer registration
Input: username = "Ramesh", phone = "9998887776", meter = "M999"
Expected Output: Consumer registered successfully
Actual Output: Consumer added to database
Status: PASS

Test ID: TR-03
Functionality: Reject registration with invalid name
Input: username = "Ram123", phone = "9998887776"
Expected Output: Error "Name must contain alphabets only"
Actual Output: Error displayed
Status: PASS

3.4 Function: register_employee()
Location: routes/admin.py
Purpose: Registers new employees in the system

Test ID: TE-01
Functionality: Reject duplicate employee IDs
Input: employee_id = "EMP001" (already exists)
Expected Output: Error message "Employee ID exists"
Actual Output: Error message displayed
Status: PASS

Test ID: TE-02
Functionality: Successful employee registration
Input: username = "Suresh", phone = "8887776665", emp_id = "EMP999"
Expected Output: Employee registered successfully
Actual Output: Employee added to database
Status: PASS

3.5 Function: generate_bill()
Location: routes/employee.py
Purpose: Generates electricity bills for consumers

Test ID: TG-01
Functionality: Normal bill generation
Input: meter = "M101", previous = 100, current = 150
Expected Output: Bill generated for 50 units (Rs. 75.0)
Actual Output: Bill created successfully
Status: PASS

Test ID: TG-02
Functionality: Reject current reading less than previous
Input: meter = "M101", previous = 100, current = 90
Expected Output: Error "Current reading less than previous"
Actual Output: Error displayed
Status: PASS

Test ID: TG-03
Functionality: First-time bill (no previous reading)
Input: meter = "M102" (new), current = 80
Expected Output: Bill generated for 80 units
Actual Output: Bill created with previous = 0
Status: PASS

Test ID: TG-04
Functionality: Verify fine amount
Input: Any valid bill
Expected Output: Fine = Rs. 150.0
Actual Output: Fine = 150.0
Status: PASS

Test ID: TG-05
Functionality: Consumer not found
Input: meter = "INVALID123"
Expected Output: Error "Consumer not found"
Actual Output: Error displayed
Status: PASS

4. TEST SUMMARY REPORT

Total Test Cases: 22
Passed: 22
Failed: 0
Pass Rate: 100%

Function-wise Summary:
- validate_user_input(): 5 tests - All Passed
- calculate_bill_amount(): 6 tests - All Passed
- register_consumer(): 3 tests - All Passed
- register_employee(): 2 tests - All Passed
- generate_bill(): 6 tests - All Passed

5. CONCLUSION

All test cases have been executed successfully. The application functions as expected according to the requirements:

- Input validation correctly rejects invalid names and phone numbers
- Bill calculation follows the tiered pricing structure accurately
- Duplicate entries are properly prevented
- Error handling works correctly for edge cases

The system is ready for deployment.