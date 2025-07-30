from datetime import datetime

class Transaction:
    def __init__(self, transaction_id=None, amount=None, category=None, date=None, type=None):
        self.transaction_id = transaction_id
        self.amount = amount
        self.category = category
        self.date = date
        self.type = type  

    def __str__(self):
        return (
            f"Transaction ID: {self.transaction_id}, "
            f"Amount: {self.amount}, "
            f"Category: {self.category}, "
            f"Date: {self.date}, "
            f"Type: {self.type}"
        )