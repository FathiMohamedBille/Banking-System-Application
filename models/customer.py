from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import re
from utils.tools import Base

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    accounts = relationship('BankAccount', back_populates='customer')
    
    def __init__(self, name, email):
        ##Validate name
        if not name or not name.isalpha():
            raise ValueError("Name must contain only letters and cannot be empty.")
        
        ##Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")
        
        self.name = name
        self.email = email
    
    @classmethod
    def create_customer(cls, name, email, session):
        ##class method to create,save new customer
        try:
            customer = cls(name, email)
            session.add(customer)
            session.commit()
            return customer  
        except Exception as e:
            session.rollback()
            return f"Failed to create customer: {e}"  

    @classmethod
    def delete_customer(cls, customer_id, session):
        ##class method to delete customer by id
        customer = session.query(cls).filter_by(id=customer_id).first()
        if customer:
            session.delete(customer)
            session.commit()
            return f"Customer {customer.name} deleted successfully."  
        else:
            return f"Customer with ID {customer_id} not found."  

    @classmethod
    def find_by_id(cls, customer_id, session):
        ##class method to find a customer by id
        return session.query(cls).filter_by(id=customer_id).first()

    @classmethod
    def get_all(cls, session):
    ##class method to recover all customers
        return session.query(cls).all()

    def get_accounts(self):
        ##return a list of account numbers
        return [account.account_number for account in self.accounts]

    def get_account_dict(self):
        ##return a dictionary with account details
        return {
            account.account_number: {
                'balance': account.balance,
                'transactions': len(account.transactions)
            }
            for account in self.accounts
        }
