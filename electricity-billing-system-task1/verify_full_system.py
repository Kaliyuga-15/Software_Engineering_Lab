from app import create_app
from models import User, Bill, db
from flask import url_for
import unittest
from datetime import datetime, timedelta

class TestElectricityApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB for testing
        self.app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for easier testing
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Admin is auto-created by app.py, but let's confirm/ensure
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin', phone='0000000000', password='admin', role='admin')
                db.session.add(admin)
                db.session.commit()
            
            # Create an Employee for testing
            emp = User(username='Employee1', phone='9999999999', password='emp', role='employee', employee_id='EMP001')
            db.session.add(emp)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_1_validation_rules(self):
        """Test strict validation: Name alphabets only, Phone 10 digits"""
        self.login('admin', 'admin')
        
        # Case 1: Name with numbers (Should Fail)
        response = self.client.post('/admin/register_consumer', data=dict(
            username='User123',
            phone='1234567890',
            password='pass',
            meter_number='M1',
            connection_type='Household'
        ), follow_redirects=True)
        self.assertIn(b'Name must contain alphabets only', response.data)
        
        # Case 2: Phone short (Should Fail)
        response = self.client.post('/admin/register_consumer', data=dict(
            username='ValidUser',
            phone='123',
            password='pass',
            meter_number='M2',
            connection_type='Household'
        ), follow_redirects=True)
        self.assertIn(b'Phone number must be exactly 10 digits', response.data)
        
        # Case 3: Valid Data (Should Success)
        response = self.client.post('/admin/register_consumer', data=dict(
            username='ValidUser',
            phone='1234567890', 
            password='pass',
            meter_number='M_VALID',
            connection_type='Household'
        ), follow_redirects=True)
        self.assertIn(b'Consumer Registered Successfully', response.data)

    def test_2_duplicate_check(self):
        """Test duplicate service number rejection"""
        self.login('admin', 'admin')
        
        # Register first time
        self.client.post('/admin/register_consumer', data=dict(
            username='UserA', phone='1111111111', password='p', meter_number='M_DUP', connection_type='Household'
        ))
        
        # Register duplicate meter
        response = self.client.post('/admin/register_consumer', data=dict(
            username='UserB', phone='2222222222', password='p', meter_number='M_DUP', connection_type='Household'
        ), follow_redirects=True)
        
        self.assertIn(b'Service Number (Meter Number) already exists', response.data)

    def test_3_bill_computation(self):
        """Test tiered calculation: 0-50@1.5, 51-100@2.5, 101-150@3.5, >150@4.5"""
        # Setup consumer
        with self.app.app_context():
            user = User(username='TestBill', phone='1234567890', password='p', role='consumer', meter_number='M_BILL', connection_type='Household')
            db.session.add(user)
            db.session.commit()
            
        self.login('Employee1', 'emp')
        
        # Case 1: 0 Units (Expect Min 25)
        response = self.client.post('/employee/generate_bill', data=dict(
            meter_number='M_BILL',
            current_reading='0' # Previous is 0
        ), follow_redirects=True)
        self.assertIn(b'Rs 25.00', response.data) 
        
        # Case 2: 200 Units (Expect 600)
        # Previous reading was 0. New reading 200. Units = 200.
        # 50*1.5 + 50*2.5 + 50*3.5 + 50*4.5 = 75 + 125 + 175 + 225 = 600
        response = self.client.post('/employee/generate_bill', data=dict(
            meter_number='M_BILL',
            current_reading='200'
        ), follow_redirects=True)
        # Note: Previous reading is now 0 (from previous bill? No, logic gets last bill).
        # Actually logic says: last_bill = query...order_by desc.
        # The first bill (0 units) had current_reading=0. So prev=0.
        # Request current=200. Diff=200.
        self.assertIn(b'Rs 600.00', response.data)

    def test_4_fine_and_dates(self):
        """Test due date (15 days) and fine (150)"""
        with self.app.app_context():
            user = User(username='TestFine', phone='1234567890', password='p', role='consumer', meter_number='M_FINE', connection_type='Household')
            db.session.add(user)
            db.session.commit()
            
        self.login('Employee1', 'emp')
        response = self.client.post('/employee/generate_bill', data=dict(
            meter_number='M_FINE',
            current_reading='100'
        ), follow_redirects=True)
        
        # Check Fine amount in response
        self.assertIn(b'Rs 150.00', response.data) # Fine amount displayed
        
        # Check calculation: 100 units = 50*1.5 + 50*2.5 = 75 + 125 = 200.
        self.assertIn(b'Rs 200.00', response.data)
        
        # Check total after fine: 200 + 150 = 350
        self.assertIn(b'Rs 350.00', response.data)

print("Starting System Verification...")
unittest.main(exit=False)
