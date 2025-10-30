from colorama import Fore, Style, init
import pymysql
from datetime import date, timedelta

init(autoreset=True)

def create_transaction_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS transaction (
        transaction_no INT PRIMARY KEY AUTO_INCREMENT,
        book_no INT NOT NULL,
        member_no INT NOT NULL,
        issue_date DATE NOT NULL,
        return_date DATE NOT NULL,
        actual_return_date DATE DEFAULT NULL,
        fine INT DEFAULT 0,
        FOREIGN KEY(book_no) REFERENCES book(book_no),
        FOREIGN KEY(member_no) REFERENCES member(member_no)
    )
    """
    cursor.execute(create_table_query)
    print(Fore.GREEN + Style.BRIGHT + "✅ Table 'transaction' created successfully")

def insert_into_transaction_table(cursor):
    today = date.today()
    demo_transaction = [
        (1, 1, today - timedelta(days=2), today + timedelta(days=5), None, 0),
        (2, 2, today - timedelta(days=15), today - timedelta(days=5), today - timedelta(days=4), 0),
        (3, 3, today - timedelta(days=20), today - timedelta(days=10), today - timedelta(days=3), 10),
        (4, 1, today - timedelta(days=30), today - timedelta(days=15), today - timedelta(days=12), 35),
        (5, 4, today - timedelta(days=5), today + timedelta(days=10), None, 0),
    ]

    insert_query = """
    INSERT INTO transaction (book_no, member_no, issue_date, return_date, actual_return_date, fine)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.executemany(insert_query, demo_transaction)
        print(Fore.GREEN + Style.BRIGHT + "✅ Sample records inserted successfully.")
    except pymysql.IntegrityError as e:
        print(Fore.RED + "Error inserting sample data:", e)

def main():
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="sujal1",
            database="library"
        )
        cursor = conn.cursor()
        create_transaction_table(cursor)
        insert_into_transaction_table(cursor)
        conn.commit()
    except pymysql.Error as e:
        print(Fore.RED + Style.BRIGHT + "Database error:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
