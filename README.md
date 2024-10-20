Rule Engine with AST
This project implements a simple 3-tier rule engine application using Abstract Syntax Trees (AST) to determine user eligibility based on various attributes such as age, department, income, and experience.

Table of Contents
Project Overview
System Requirements
Database Configuration
Database Schema
API Design
Getting Started
Testing
Additional Features
Contributing
License
Project Overview
The Rule Engine application evaluates rules based on user attributes. It utilizes Abstract Syntax Trees (AST) to represent and manipulate these rules dynamically. This allows for efficient evaluation and easy modification of rules.

System Requirements
To run this application, you need the following:

Microsoft SQL Server installed and configured
Python (version 3.8 or higher)
pip (Python package manager)
Required Python packages (listed in requirements.txt)
ODBC Driver for SQL Server (ensure that it's properly installed)
Database Configuration
The application uses Microsoft SQL Server as its database. Ensure that you have a running instance of SQL Server and create a database named RuleEngineDB.

Connection String
Update the connection string in the configuration file to connect to your database. The format is:

rust
Copy code
DATABASE_URI = 'mssql+pyodbc://username:password@server_instance/database_name?driver=ODBC+Driver+17+for+SQL+Server'
Replace username, password, server_instance, and database_name with your actual database credentials.
