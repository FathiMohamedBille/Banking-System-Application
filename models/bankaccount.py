from sqlalchemy import Column, Integer, String, ForeignKey
from utils.tools import Base
from sqlalchemy.orm import relationship
import random as r

class BankAccount(Base):
    __tablename__ = 'bank_accounts'
    
    id = Column(Integer, primary_key=True)
    account_name = Column(String, nullable=False)
    account_number = Column(Integer, unique=True, nullable=False)
    balance = Column(Integer, default=0)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    
    ##relationship with transactions
    transactions = relationship('TransactionHistory', back_populates='account', cascade='all, delete-orphan')

    def __init__(self, account_name, balance=0):
        self.account_name = account_name
        self.account_number = r.randint(10000, 99999)
        self.balance = balance

    def deposit(self, amount):
        ##deposit specified amount into the account
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.record_transaction("Deposit", amount)

    def withdraw(self, amount):
        ##withdraw specified amount from account
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        return self.record_transaction("Withdrawal", amount)

    def record_transaction(self, transaction_type, amount):
        ##record a transaction in accounts transaction history
        return f"{transaction_type} of {amount} Ksh recorded for account: {self.account_name}"

    def get_balance(self):
        ##return account balance
        return self.balance

    def get_account_details(self):
        ##return account details as dictionary
        return {
            'account_name': self.account_name,
            'account_number': self.account_number,
            'balance': self.balance,
            'transactions': [transaction.get_details() for transaction in self.transactions]
        }
