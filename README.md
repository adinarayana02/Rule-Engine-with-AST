# Rule Engine with Abstract Syntax Tree (AST)

## Introduction

The Rule Engine with Abstract Syntax Tree (AST) project is designed to evaluate user eligibility based on various dynamic rules. The use of an AST enables the application to parse and evaluate complex logical expressions effectively. This project is beneficial in sectors like human resources, finance, and marketing, where decisions must be made quickly based on specific criteria.

### Goals
- **Dynamic Rule Creation:** Allow users to define rules in a natural language format.
- **Efficient Evaluation:** Use AST to represent rules for fast evaluations.
- **Historical Data Logging:** Store evaluation results for auditing and analysis.

## Project Overview

This project implements a three-tier architecture, consisting of a web interface, a RESTful API, and a backend data storage system. The following key components are central to the system:

### Components
- **User Interface:** A web-based application that allows users to input rules, view results, and manage rule settings.
- **API Layer:** Built using Flask, this layer handles requests between the user interface and the database, ensuring smooth communication.
- **Database:** Utilizes Microsoft SQL Server for storing rules, attributes, evaluation results, and historical data.

### Expected Output
Upon evaluating user data against defined rules, the application will output whether the user qualifies according to the specified criteria.


## System Configuration

### Overview
The Rule Engine with AST project is built using several key components, each serving a specific function:

- **Web Interface (HTML, CSS, JS)**
  - **HTML:** Structures the layout and content of the web pages. It includes forms for users to input rules and view evaluation results.
  - **CSS:** Styles the web pages, making them visually appealing and user-friendly. It ensures a good layout and responsive design.
  - **JavaScript:** Adds interactivity to the web interface, allowing dynamic updates, such as validating user inputs and making API calls without reloading the page.

- **API (Flask)**
  - The API is built using Flask, which handles requests from the web interface.
  - **Key functions include:**
    - Creating Rules: Receives new rules from users and processes them.
    - Evaluating Rules: Checks user data against existing rules and returns results.
    - Retrieving Rules: Provides a list of all rules for the user to view.

- **Backend (Python)**
  - The backend contains the main logic of the application, including:
    - Rule Processing: Converts rules into an Abstract Syntax Tree (AST) for evaluation.
    - Data Handling: Manages how data is processed and passed to the API.

- **Database (MSSQL)**
  - The database (Microsoft SQL Server) stores all the persistent data, such as:
    - Rules: Holds the rules defined by users.
    - Attributes: Lists valid attributes that can be used in the rules.
    - Evaluation History: Records the results of rule evaluations.

### Database Configuration

#### Setting Up the Database
1. **Install SQL Server:**
   - If not already installed, download and install Microsoft SQL Server from the official website. Follow the installation wizard to set it up correctly.

2. **Create a Database:**
   - Open SQL Server Management Studio (SSMS) or a similar tool.
   - Connect to your SQL Server instance.
   - Create a new database named `RuleEngineDB`. Right-click on the "Databases" node and select "New Database."

3. **Set Up Connection String:**
   - In your application’s configuration file (e.g., `config.py`), set the `DATABASE_URI` variable with the correct connection string that includes your SQL Server credentials.
   - Ensure that the user account specified has sufficient permissions to create tables and manage data in the database.

### Database Schema
To effectively manage the application data, define the necessary tables in the `RuleEngineDB`. Each table serves a specific purpose, allowing for organized data management.

- **Rules Table:** Stores the individual rules input by users.
- **ASTNodes Table:** Represents the nodes of the Abstract Syntax Tree corresponding to the rules.
- **RuleEvaluationHistory Table:** Logs the history of rule evaluations, including timestamps and results.
- **Attributes Table:** Contains a catalog of valid attributes that can be referenced in rules.
- **UserData Table:** Holds sample or real user data for testing the rules against various conditions.
- **CombinedRules Table:** Stores rules that have been combined for evaluation.
- **RuleCombinations Table:** Manages many-to-many relationships between individual rules and combined rules.

### Package Dependencies and Libraries
To manage the project’s dependencies efficiently, utilize a `requirements.txt` file. This file should list all the necessary libraries that the application needs to run correctly. Common dependencies include:

- **Flask:** A lightweight web framework for building the API.
- **Flask-SQLAlchemy:** An ORM (Object-Relational Mapping) library that simplifies interactions with the SQL database.
- **PyODBC:** A library that enables Python to connect to SQL Server using ODBC.

## Environment Setup

### Step 1: Clone the Repository
Use Git to clone the repository containing the Rule Engine application code to your local machine. Open a terminal and run the following command:

```bash
git clone https://github.com/adinarayana02/Rule-Engine-with-AST.git
