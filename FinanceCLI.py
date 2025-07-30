import os
from dotenv import load_dotenv
from FinanceService import FinanceService
from datetime import datetime

load_dotenv()

WELCOME = os.getenv("WELCOME")
MENU = """
1. Add Transaction
2. View Transactions
3. Filter by Category
4. Filter by Date
5. View Monthly Balance
6. Exit
"""

def main():
    print(os.getenv("WELCOME"))
    service = FinanceService()

    while True:
        print(MENU)
        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            date_str = input("Enter date (YYYY-MM-DD): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            type_ = input("Enter type (income/expense): ").lower()
            service.addTransaction(amount, category, date, type_)

        elif choice == "2":
            service.viewTransactions()

        elif choice == "3":
            category = input("Enter category: ")
            service.filterByCategory(category)

        elif choice == "4":
            date_str = input("Enter date (YYYY-MM-DD): ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            service.filterByDate(date)

        elif choice == "5":
            try:
                month = int(input("Enter month (1-12): "))
                year = int(input("Enter year (e.g. 2025): "))
                if 1 <= month <= 12:
                    service.calculateMonthlyBalance(month, year)
                else:
                    print("Invalid month. Enter 1-12.")
            except ValueError:
                print("Please enter valid numbers for month and year.")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()