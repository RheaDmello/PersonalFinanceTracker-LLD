import os
from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor
from model import Transaction

load_dotenv()

class FinanceMySQLService:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_DATABASE"),
                cursorclass=DictCursor
            )
            self.cursor = self.connection.cursor()
            self.table = os.getenv("DB_TABLE", "transactions")
            self.isTableExists()
            print("Database connected successfully.")
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise

    def getMessage(self, key, **kwargs):
        message = os.getenv(key, "")
        if not message:
            return ""
        try:
            return message.format(**kwargs)
        except KeyError as e:
            print(f"Missing placeholder in message {key}: {e}")
            return message

    def isTableExists(self):
        qry = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(10, 2) NOT NULL,
            category VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            type ENUM('income', 'expense') NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        try:
            self.cursor.execute(qry)
            self.connection.commit()
            print(self.getMessage("MSG_TABLE_OK"))
        except Exception as e:
            print(f"Error creating table: {e}")

    def addTransaction(self, transaction):
        qry = f"""
        INSERT INTO {self.table} (amount, category, date, type)
        VALUES (%s, %s, %s, %s)
        """
        try:
            values = (
                transaction.amount,
                transaction.category,
                transaction.date,
                transaction.type
            )
            self.cursor.execute(qry, values)
            self.connection.commit()
            print(self.getMessage("MSG_ADD_TRANSACTION_OK"))
        except Exception as e:
            print(f"Database error: {e}")
            print(self.getMessage("MSG_ADD_TRANSACTION_FAIL"))

    def viewTransactions(self):
        qry = f"SELECT * FROM {self.table} ORDER BY transaction_id"

        try:
            self.cursor.execute(qry)
            transactions = self.cursor.fetchall()

            if not transactions:
                print(self.getMessage("MSG_NO_TRANSACTIONS"))
                return

            print(f"\n{'-'*50}")
            print(" All Transactions")
            print(f"{'-'*50}")
            for transaction in transactions:
                trans_date = transaction["date"]
                print(Transaction(
                    transaction_id=transaction["transaction_id"],
                    amount=transaction["amount"],
                    category=transaction["category"],
                    date=trans_date,
                    type=transaction["type"]
                ))

        except Exception as e:
            print(f"Error fetching all transactions: {e}")

    def filterByCategory(self, category):
        qry=f"SELECT * FROM {self.table} WHERE category=%s ORDER BY date"
        try:
            self.cursor.execute(qry,(category,))
            transactions=self.cursor.fetchall()
            if not transactions:
                print(f"\nNo transactions found for category:{category}")
                return
            print(f"\n{'-'*50}")
            print(f"Transactions in Category:{category}")
            print(f"\n{'-'*50}")
            for transaction in transactions:
                print(Transaction(
                    transaction_id=transaction["transaction_id"],
                    amount=transaction["amount"],
                    category=transaction["category"],
                    date=transaction["date"],
                    type=transaction["type"]))
        except Exception as e:
            print(f"Error:{e}")

    def filterByDate(self, date):
        qry=f"SELECT * FROM {self.table} WHERE date=%s ORDER BY transaction_id"
        try:
            self.cursor.execute(qry,(date,))
            transactions=self.cursor.fetchall()
            if not transactions:
                print(f"\nNo transactions found on date:{date}")
                return
            print(f"\n{'-'*50}")
            print(f"Transactions on date:{date}")
            print(f"\n{'-'*50}")
            for transaction in transactions:
                print(Transaction(
                    transaction_id=transaction["transaction_id"],
                    amount=transaction["amount"],
                    category=transaction["category"],
                    date=transaction["date"],
                    type=transaction["type"]))
        except Exception as e:
            print(f"Error:{e}")

    def calculateMonthlyBalance(self, month, year):
        qry = f"""
        SELECT 
            COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) AS total_income,
            COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS total_expense
        FROM {self.table}
        WHERE MONTH(date) = %s AND YEAR(date) = %s
        """
        try:
            self.cursor.execute(qry, (month, year))
            result = self.cursor.fetchone()

            total_income = float(result["total_income"])
            total_expense = float(result["total_expense"])
            balance = total_income - total_expense

            import calendar
            month_name = calendar.month_name[month]

            print(f"\nMonthly Summary: {month_name} {year}")
            print(f" {'='*40}")
            print(f" Income  : {total_income:,.2f}")
            print(f" Expense : {total_expense:,.2f}")
            print(f" Balance : {balance:,.2f}")
            print(f" {'='*40}\n")

        except Exception as e:
            print(f"Error calculating monthly balance: {e}")
