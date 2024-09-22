from sqlalchemy import Column, Integer, String, ForeignKey
from utils.tools import Base
from sqlalchemy.orm import relationship

class TransactionHistory(Base):
    __tablename__ = 'transaction_history'

    id = Column(Integer, primary_key=True)
    transaction_type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey('bank_accounts.id'), nullable=False)

    ##relationship  to account
    account = relationship('BankAccount', back_populates='transactions')

    def __init__(self, transaction_type, amount):
        if transaction_type not in ["Deposit", "Withdrawal"]:
            raise ValueError("Transaction type must be 'Deposit' or 'Withdrawal'.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        
        self.transaction_type = transaction_type
        self.amount = amount

    def to_tuple(self):
        ##return transaction details as tuple
        return (self.transaction_type, self.amount)

    def to_dict(self):
        ##return transaction details as dictionary
        return {
            "transaction_type": self.transaction_type,
            "amount": self.amount
        }

    @classmethod
    def get_all_transactions(cls, session, account_id):
        ##recover all transactions for a specific account as list,tuples
        transactions = session.query(cls).filter_by(account_id=account_id).all()
        return [transaction.to_tuple() for transaction in transactions]

    @classmethod
    def get_transaction_summary(cls, session, account_id):
        ##recover transaction summary as list of dictionaries
        transactions = session.query(cls).filter_by(account_id=account_id).all()
        return [transaction.to_dict() for transaction in transactions]
