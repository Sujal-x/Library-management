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
CREATE TABLE IF NOT EXISTS member (
    member_no INT PRIMARY KEY,
    member_name VARCHAR(100) NOT NULL,
    member_type ENUM('S', 'T', 'F') NOT NULL,
    mobile_no VARCHAR(15),
    roll_no VARCHAR(50),
    standard VARCHAR(50)
)
"""

cursor.execute(create_table_query)
print(Fore.GREEN + Style.BRIGHT + "✅ Table 'member' created sucessfully .")

members = [
    (1, 'Riya Sharma', 'S', '9876543210', 'ST101', '10th A'),
    (2, 'Amit Patel', 'S', '9988776655', 'ST102', '12th B'),
    (3, 'Sunita Joshi', 'T', '9123456788', None, None),
    (4, 'Rajiv Menon', 'F', '9001122334', None, None),
    (5, 'Kunal Mehra', 'T', '9876501234', None, None)
]

insert_query = """
INSERT INTO member (member_no, member_name, member_type, mobile_no, roll_no, standard)
VALUES (%s, %s, %s, %s, %s, %s)
"""

try:
    cursor.executemany(insert_query, members)
    conn.commit()
    print(Fore.GREEN + Style.BRIGHT + "✅ Sample members inserted successfully.")
except pymysql.IntegrityError:
    print(Fore.GREEN + Style.BRIGHT + "✅ Some records may already exist. Skipping duplicates.")

cursor.close()
conn.close()