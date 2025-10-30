from colorama import Fore, Style, init
import pymysql

init(autoreset=True)

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="sujal1"
)

cursor = conn.cursor()
cursor.execute("USE library")


create_table_query = """
CREATE TABLE IF NOT EXISTS book (
    book_no INT PRIMARY KEY,
    book_name VARCHAR(255),
    author_name VARCHAR(255),
    publisher_name VARCHAR(255),
    no_of_pages INT,
    price DECIMAL(10,2),
    number_of_copies INT,
    available_copies INT
)
"""

cursor.execute(create_table_query)
print(Fore.GREEN + Style.BRIGHT + "✅ Table 'book' created successfully .")

books =[
    (1, "Wings of Fire", "A.P.J. Abdul Kalam", "Universities Press", 180, 250, 10, 10),
    (2, "The Discovery of India", "Jawaharlal Nehru", "Penguin Books", 650, 499, 15, 7),
    (3, "India 2020", "A.P.J. Abdul Kalam", "Penguin Books", 300, 350, 12, 5),
    (4, "Ignited Minds", "A.P.J. Abdul Kalam", "Penguin Books", 220, 280, 8, 3),
    (5, "My Experiments with Truth", "Mahatma Gandhi", "Navajivan Publishing", 450, 400, 20, 12),
]

insert_query = """
INSERT INTO book (book_no, book_name, author_name, publisher_name, no_of_pages, price, number_of_copies, available_copies)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

try:
    cursor.executemany(insert_query, books)
    conn.commit()
    print(Fore.GREEN + Style.BRIGHT + "✅ Sample books inserted successfully.")
except pymysql.IntegrityError:
    print(Fore.GREEN + Style.BRIGHT + "✅ Some books may already exist. Skipping duplicates.")

cursor.close()
conn.close()