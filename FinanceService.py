from FinanceDbDao import FinanceMySQLService
from model import Transaction

class FinanceService:
    def __init__(self, source="db"):
        if source == "db":
            self.repo = FinanceMySQLService()

    def addTransaction(self, amount, category, date, type):
        transaction = Transaction(amount=amount, category=category, date=date, type=type)
        self.repo.addTransaction(transaction)

    def viewTransactions(self):
        self.repo.viewTransactions()

    def filterByCategory(self, category):
        self.repo.filterByCategory(category)

    def filterByDate(self, date):
        self.repo.filterByDate(date)

    def calculateMonthlyBalance(self, month, year):
        self.repo.calculateMonthlyBalance(month, year)