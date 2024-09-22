from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
import random as r
from utils.tools import Base

##defining the models
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    accounts = relationship('BankAccount', back_populates='customer')

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True)
    account_name = Column(String, nullable=False)
    account_number = Column(Integer, unique=True, nullable=False)
    balance = Column(Integer, default=0)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship('Customer', back_populates='accounts')
    transactions = relationship('TransactionHistory', back_populates='account', cascade="all, delete-orphan")

class TransactionHistory(Base):
    __tablename__ = "transaction_history"
    id = Column(Integer, primary_key=True)
    transaction_type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey('bank_accounts.id'), nullable=False)
    account = relationship('BankAccount', back_populates='transactions')

##database settingup
engine = create_engine("sqlite:///bank.db")
Base.metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
session = Session()

##bank class to manage bank operations
class Bank:
    def __init__(self):
        print("WELCOME TO LUXE LADY BANK")
        ##list to store account details
        self.accounts_list = []  
        ##dictionary to store account details
        self.accounts_dict = {}  

    def create_account(self):
        try:
            first_name = input("Enter Your First Name: ").strip().upper()
            last_name = input("Enter Your Last Name: ").strip().upper()
            if not first_name.isalpha() or not last_name.isalpha():
                raise ValueError("Name must contain only letters.")
            
            account_name = f"{first_name} {last_name}"
            account_number = r.randint(10000, 99999)
            balance = 0

            email = input("Enter your email: ").strip().lower()
            if '@' not in email:
                raise ValueError("Invalid email address.")

            ##to check if customer already exists
            existing_customer = session.query(Customer).filter_by(email=email).first()
            if existing_customer:
                print("Customer already exists. Using existing profile.")
                customer = existing_customer
            else:
                customer = Customer(name=account_name, email=email)
                session.add(customer)
                session.commit()
                print(f"Customer {account_name} created successfully!")

            ##create a new bank account and then add it to the session
            new_account = BankAccount(account_name=account_name, account_number=account_number, balance=balance, customer_id=customer.id)
            session.add(new_account)
            session.commit()
            self.accounts_list.append((account_name, account_number, balance))  # Using tuples
            self.accounts_dict[account_number] = {'name': account_name, 'balance': balance}  # Dictionary
            print(f"Account for {account_name} created successfully!")
            print(f"Please note down your account number: {account_number}")
        except ValueError as ve:
            print(ve)

    def open_account(self):
        try:
            account_number = int(input("Enter your account number: "))
        except ValueError:
            print("Invalid input. Account number must be a number.")
            return

        account = session.query(BankAccount).filter_by(account_number=account_number).first()
        if account:
            self.accounts_dict[account_number] = {'name': account.account_name, 'balance': account.balance}
            self.accounts_list.append((account.account_name, account.account_number, account.balance))
            print("(d) - Deposit")
            print("(w) - Withdraw")
            print("(c) - Check Balance")
            print("(del) - Delete Account")
            print("(v) - View Transactions")
            action = input("Enter any of the operations (c)/(d)/(w)/(del)/(v): ").lower()
            if action == 'd':
                self.deposit(account)
            elif action == 'w':
                self.withdraw(account)
            elif action == 'c':
                self.check_balance(account)
            elif action == 'del':
                self.delete_account(account)
            elif action == 'v':
                self.view_transactions(account)
            else:
                print("Invalid option. Please select 'c', 'd', 'w', 'del', or 'v'.")
        else:
            print("Account not found. Please check your account number and try again.")

    def deposit(self, account):
        try:
            deposit_amount = int(input("Enter the amount to deposit: "))
            if deposit_amount <= 0:
                raise ValueError("Deposit amount must be positive.")
            account.balance += deposit_amount
            session.add(TransactionHistory(transaction_type="Deposit", amount=deposit_amount, account_id=account.id))
            self.accounts_dict[account.account_number]['balance'] = account.balance
            self.update_account_in_list(account.account_number, account.balance)
            session.commit()
            print(f"Deposited {deposit_amount} Ksh. New balance: {account.balance} Ksh")
        except ValueError as e:
            print(f"Invalid amount. {e}")

    def withdraw(self, account):
        try:
            withdrawal_amount = int(input("Enter the amount to withdraw: "))
            if withdrawal_amount <= 0:
                raise ValueError("Withdrawal amount must be positive.")
            if withdrawal_amount > account.balance:
                raise ValueError("Insufficient balance.")
            account.balance -= withdrawal_amount
            session.add(TransactionHistory(transaction_type="Withdrawal", amount=withdrawal_amount, account_id=account.id))
            self.accounts_dict[account.account_number]['balance'] = account.balance
            self.update_account_in_list(account.account_number, account.balance)
            session.commit()
            print(f"Withdrawn {withdrawal_amount} Ksh. New balance: {account.balance} Ksh")
        except ValueError as e:
            print(f"Invalid amount. {e}")

    def check_balance(self, account):
        print(f"Account balance: {account.balance} Ksh")
        account_details = (self.accounts_dict[account.account_number]['name'], self.accounts_dict[account.account_number]['balance'])
        print(f"Account Holder: {account_details[0]}, Balance: {account_details[1]} Ksh")

    def delete_account(self, account):
        confirm = input(f"Are you sure you want to delete the account {account.account_name} (Account No: {account.account_number})? (yes/no): ").strip().lower()
        if confirm == 'yes':
            customer_id = account.customer_id
            session.delete(account)
            session.commit()
            
            customer = session.query(Customer).filter_by(id=customer_id).first()
            if customer and not session.query(BankAccount).filter_by(customer_id=customer_id).count():
                session.delete(customer)
                session.commit()
                print(f"Customer {customer.name} deleted successfully since they have no more accounts.")
            else:
                print(f"Account {account.account_name} deleted successfully.")
            
            self.accounts_list = [acc for acc in self.accounts_list if acc[1] != account.account_number]
            self.accounts_dict.pop(account.account_number, None)

        else:
            print("Account deletion canceled.")

    def update_account_in_list(self, account_number, new_balance):
        for i, account in enumerate(self.accounts_list):
            if account[1] == account_number:
                self.accounts_list[i] = (account[0], account[1], new_balance)
                break

    def view_customers(self):
        customers = session.query(Customer).all()
        if customers:
            print("Customer List:")
            for customer in customers:
                print(f"Name: {customer.name}, Email: {customer.email}")
                for account in customer.accounts:
                    print(f"  Account No: {account.account_number}, Balance: {account.balance} Ksh")
        else:
            print("No customers found.")

    def view_transactions(self, account):
        transactions = session.query(TransactionHistory).filter_by(account_id=account.id).all()
        if transactions:
            print(f"Transactions for Account No: {account.account_number}")
            for transaction in transactions:
                print(f"{transaction.transaction_type}: {transaction.amount} Ksh")
        else:
            print("No transactions found for this account.")

if __name__ == "__main__":
    bank = Bank()
    while True:
        print("(c) - Create account")
        print("(o) - Open Account")
        print("(v) - View Customers")
        print("(q) - Quit")
        choice = input("Enter your choice (c)/(o)/(v) or 'q' to quit: ").lower()
        if choice == 'c':
            bank.create_account()
        elif choice == 'o':
            bank.open_account()
        elif choice == 'v':
            bank.view_customers()
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please select 'c', 'o', 'v', or 'q'.")
