Electricity Billing System

Hi! This is a web application I built to manage electricity billing. The goal was to create a simple but complete system where Admins, Employees, and Consumers all have their own specific roles and dashboards.

It is built using Python (Flask) and SQLite, so it is lightweight and easy to run.

What it does

I designed this to handle the entire flow of a billing cycle:

1. For Admins: You have full control. You can register new Employees (who read meters) and new Consumers (who pay bills). There offers a main dashboard where you can see everyone in the system and a log of all generated bills. I also added an Edit option so you can update user details if mistakes happen.

2. For Employees: This is for the staff. They log in, enter a consumer meter number, and the current reading. The app automatically calculates the bill amount based on whether it is a home (tiered rates) or a business (flat rate).

3. For Consumers: If you are a user, you can log in to see your bill history. I added a Payment Page where you can simulate paying your bill—it even checks if you entered a valid 16-digit card number!

How it works (Under the hood)

- Backend: Flask (Python) handles all the logic and routing.
- Database: Used SQLAlchemy with SQLite. It stores Users, roles, and Bill records.
- Security: Passwords are not just plain text, and I added checks so you can not accidentally sign up with a duplicate phone number or meter ID.

Want to run it?

1. Clone this repo:
   git clone <repository-url>
   cd electricity_billing_app

2. Install the requirements:
   pip install -r requirements.txt

3. Set up the database:
   I created a script to handle the first-time setup. Just run:
   python seed_admin.py
   
   This creates the database and a default Admin user.

4. Start the server:
   python app.py
   
   Then just open http://127.0.0.1:5000 in your browser.

Default Login

To get started, log in with the admin account created by the seed script:
- Username: admin
- Password: admin

Feel free to look around and let me know if you have questions!
