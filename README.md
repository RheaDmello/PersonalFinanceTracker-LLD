# 💸 Personal Finance Tracker CLI

A simple command-line interface (CLI) application to track your personal income and expenses using Python and MySQL.

---

## 📌 Features

- Add transactions (income or expenses)
- View all transactions
- Filter transactions by category or date
- View monthly income, expenses, and balance
- MySQL database integration
- Environment variable support using `.env` file

---

## 🛠 Tech Stack

- Python 3.x
- MySQL (via `pymysql`)
- `.env` management with `python-dotenv`

---

## 📂 Project Structure

├── FinanceCLI.py # Main CLI app
├── FinanceService.py # Service layer
├── FinanceDbDao.py # Database DAO logic
├── model.py # Transaction model class
├── .env # Environment variables
└── requirements.txt # Python dependencies
