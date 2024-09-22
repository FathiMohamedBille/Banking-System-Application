## Banking-System-Application
## Bank Management System Project
## Description
This project is a Command Line Interface (CLI) application for managing bank accounts, developed in Python using SQLAlchemy ORM. The system allows users to create bank accounts, deposit money, withdraw money, and check their account balance,view their trasactions history and can delete their account. Data storage is managed through a SQLite database, and the project follows object-oriented programming principles.

## Features
**Account Creation** Users can create accounts by providing their first and last names.
**Deposit** Users can deposit money into their accounts.
**Withdrawal** Users can withdraw money from their accounts, with validation to ensure sufficient balance.
**Check Balance** Users can view their account balances.
**Delete**Users can delete their account.
**view customers**users can view cutsomer.
**view transactionshistory**users can view their transactionshistory.
## Project Structure
**app.py** Contains the main program logic, separated into functions and classes.
**models** Defines the SQLAlchemy ORM models for the database tables and their relationships.
**db/** Directory containing the SQLite database and Alembic migration files.
**Pipfile** Contains the project’s dependencies, including SQLAlchemy and Alembic.
## requirements
Python 3.x
SQLAlchemy
Alembic for migrations
## Instructions
Clone the repository to your local machine.
Ensure you have Python 3.x installed, and install the dependencies using Pipenv
pipenv install

alembic init migration
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

Run  python app.py
pipenv run python app.py

## Documentation
The project is structured to separate scripted elements from object-oriented code. All functions and classes are properly documented in the codebase.
The CLI includes input validation and clear prompts to guide users through the banking operations.
**Here is my table diagram link https://dbdiagram.io/d/66eaeb80a0828f8aa645fe85**
## Relationship
Customer-Account One to Many
BankAccount-TransactionHistory One to Many
TransactionHistory-BankAccount Many to One