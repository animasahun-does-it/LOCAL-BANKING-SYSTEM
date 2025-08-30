import sqlite3
import datetime


def create_table():  #   create table
    conn = sqlite3.connect('bank.db')
    a = conn.cursor()
    a.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number INTEGER NOT NULL UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        pin TEXT NOT NULL,
        balance REAL DEFAULT 0.0,
        phone_number TEXT NOT NULL)
    ''')

    a.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            account_number TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            balance_after REAL NOT NULL)
    ''')
    conn.commit()
    conn.close()


def create_user(account_number, firstname, lastname, email, pin, phone_number):  #   create user to table from argument
    conn = sqlite3.connect('bank.db')
    a = conn.cursor()
    a.execute("INSERT INTO users (account_number, first_name, last_name, email, pin, phone_number) VALUES (?,?,?,?,?,?)",(account_number, firstname, lastname, email, pin, phone_number))
    conn.commit()
    conn.close()

def user_login(email, pin):  #   grant user login returns None if user is not found
    conn = sqlite3.connect('bank.db')
    a = conn.cursor()
    a.execute('SELECT * FROM users WHERE email = ? AND pin = ?', (email, pin))
    result = a.fetchone()
    conn.close()
    return result

def check_dup(email = None, phone_number = None):   #   check duplicate to check if user has registered before. each argument is used to check
    conn = sqlite3.connect('bank.db')
    a = conn.cursor()
    if email is not None:
        a.execute('SELECT * FROM users WHERE email = ?', (email,))

    elif phone_number is not None:
        a.execute('SELECT * FROM users WHERE phone_number = ?', (phone_number,))

    check = a.fetchone()
    conn.close()
    return bool(check)


def user_info(email= None, account_number=None):
    conn = sqlite3.connect('bank.db')
    a = conn.cursor()

    if email is not None:
        a.execute('SELECT * FROM users WHERE email = ? ', (email,))
        user = a.fetchone()
        if user:
            firstname = user[2]
            lastname = user[3]
            balance = user[6]
            account_number = user[1]
            conn.close()
            return firstname, lastname, balance, account_number
        else:
            conn.close()
            return None


    elif account_number is not None:
        a.execute('SELECT * FROM users WHERE account_number = ? ', (account_number,))
        user = a.fetchone()
        if user:
            firstname = user[2]
            lastname = user[3]
            conn.close()
            return firstname, lastname

        else:
            conn.close()
            return None


def deposit_user(account_number, amount):
    conn = sqlite3.connect("bank.db")
    a = conn.cursor()

    now = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")  #   set current time
    a.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?", (amount, account_number))

    a.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
    balance_after = a.fetchone()[0]

    a.execute(
        "INSERT INTO transactions (date_time, account_number, type, amount, balance_after) VALUES (?, ?, ?, ?, ?)",
        (now, account_number, "Deposit", amount, balance_after))
    conn.commit()
    conn.close()

def withdraw_user(account_number, amount):
    conn = sqlite3.connect('bank.db')
    a = conn.cursor()

    now = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    a.execute("UPDATE users SET balance = balance - ? WHERE account_number = ?", (amount, account_number))

    a.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
    balance_after = a.fetchone()[0]

    a.execute(
        "INSERT INTO transactions (date_time, account_number, type, amount, balance_after) VALUES (?, ?, ?, ?, ?)",
        (now, account_number, "Withdraw", amount, balance_after))
    conn.commit()
    conn.close()

def transfer_amount(sender_account_number, receiver_account_number, amount):
    conn = sqlite3.connect('bank.db')
    a = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")

    #   update senders balance, add to transaction
    a.execute("SELECT balance FROM users WHERE account_number = ?", (sender_account_number,))
    sender_balance_before = a.fetchone()[0]
    sender_balance_after = sender_balance_before - amount
    a.execute("UPDATE users SET balance = balance - ? WHERE account_number = ?", (amount, sender_account_number))

    #   update receiver balance, add to transaction history
    a.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?", (amount, receiver_account_number))
    a.execute("SELECT balance FROM users WHERE account_number = ?", (receiver_account_number,))
    receiver_balance_after = a.fetchone()[0]

    a.execute(
        "INSERT INTO transactions (date_time, account_number, type, amount, balance_after) VALUES (?, ?, ?, ?, ?)",
        (now, sender_account_number, "Transfer Out", amount, sender_balance_after))


    a.execute(
        "INSERT INTO transactions (date_time, account_number, type, amount, balance_after) VALUES (?, ?, ?, ?, ?)",
        (now, receiver_account_number, "Transfer In", amount, receiver_balance_after))
    conn.commit()
    conn.close()

def get_history(account_number):  #   fetch specify user transaction history
    conn = sqlite3.connect('bank.db')
    a = conn.cursor()
    a.execute("SELECT date_time, type, amount, balance_after FROM transactions WHERE account_number = ?", (account_number,))
    transactions = a.fetchall()
    conn.close()
    return transactions

def get_user_pin(account_number):  #   used to verify user pin
    conn = sqlite3.connect('bank.db')
    a = conn.cursor()
    a.execute("SELECT pin FROM users WHERE account_number = ?", (account_number,))
    row = a.fetchone()
    pin = row[0]
    conn.close()
    return pin


