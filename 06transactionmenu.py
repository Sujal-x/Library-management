from datetime import date, timedelta
import pymysql
from colorama import Fore, Style, init

init(autoreset=True)

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="sujal1",
    database="library"
)
cursor = conn.cursor()


#  ISSUE BOOK
def issue_book():
    print(Fore.CYAN + Style.BRIGHT + "\n📚 ISSUE BOOK\n" + Fore.LIGHTBLACK_EX + "─" * 40)
    try:
        member_no = input(Fore.BLUE + "🆔 Member No: ")
        book_no = input(Fore.BLUE + "🆔 Book No: ")

        # Check member
        cursor.execute("SELECT member_type FROM member WHERE member_no=%s", (member_no,))
        member = cursor.fetchone()
        if not member:
            print(Fore.RED + Style.BRIGHT + "❌ Member not found!")
            return
        member_type = member[0]

        # Check book
        cursor.execute("SELECT available_copies FROM book WHERE book_no=%s", (book_no,))
        book = cursor.fetchone()
        if not book:
            print(Fore.RED + Style.BRIGHT + "❌ Book not found!")
            return
        available_copies = book[0]
        if available_copies <= 0:
            print(Fore.YELLOW + Style.BRIGHT + "⚠️  No available copies!")
            return

        # Issue limit
        cursor.execute(
            "SELECT COUNT(*) FROM transaction WHERE member_no=%s AND actual_return_date IS NULL",
            (member_no,)
        )
        current_issues = cursor.fetchone()[0]
        max_limit = 3 if member_type == 'S' else 5
        if current_issues >= max_limit:
            print(Fore.YELLOW + Style.BRIGHT + f"⚠️  Issue limit reached ({max_limit} books allowed).")
            return

        # Dates
        issue_date = date.today()
        return_date = issue_date + timedelta(days=7 if member_type == 'S' else 10)

        # Insert transaction
        cursor.execute("""
            INSERT INTO transaction (book_no, member_no, issue_date, return_date)
            VALUES (%s, %s, %s, %s)
        """, (book_no, member_no, issue_date, return_date))
        conn.commit()

        # Update book copies
        cursor.execute("UPDATE book SET available_copies = available_copies - 1 WHERE book_no = %s", (book_no,))
        conn.commit()

        print(Fore.GREEN + Style.BRIGHT + f"✅ Book issued successfully! Return by {return_date}.")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"❌ Error: {e}")
        conn.rollback()


#  RETURN BOOK
def return_book():
    print(Fore.CYAN + Style.BRIGHT + "\n📖↩️ RETURN BOOK\n" + Fore.LIGHTBLACK_EX + "─" * 40)
    try:
        transaction_no = int(input(Fore.BLUE + "🆔 Transaction No: "))

        cursor.execute("""
            SELECT book_no, return_date
            FROM transaction
            WHERE transaction_no=%s AND actual_return_date IS NULL
        """, (transaction_no,))
        record = cursor.fetchone()
        if not record:
            print(Fore.RED + Style.BRIGHT + "❌ Transaction not found or already returned!")
            return

        book_no, return_date_expected = record
        actual_return_date = date.today()

        # Fine
        fine_per_day = 5
        days_late = (actual_return_date - return_date_expected).days
        fine = fine_per_day * days_late if days_late > 0 else 0

        cursor.execute("""
            UPDATE transaction
            SET actual_return_date=%s, fine=%s
            WHERE transaction_no=%s
        """, (actual_return_date, fine, transaction_no))
        conn.commit()

        # Update book copies
        cursor.execute("UPDATE book SET available_copies = available_copies + 1 WHERE book_no = %s", (book_no,))
        conn.commit()

        print(Fore.GREEN + Style.BRIGHT + f"✅ Book returned successfully! Fine: ₹{fine}")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"❌ Error: {e}")
        conn.rollback()


#  LIST ALL TRANSACTIONS
def list_all_transaction():
    print(Fore.CYAN + Style.BRIGHT + "\n📚 ALL TRANSACTIONS\n" + Fore.LIGHTBLACK_EX + "─" * 90)
    try:
        cursor.execute("SELECT * FROM transaction")
        rows = cursor.fetchall()
        if not rows:
            print(Fore.YELLOW + Style.BRIGHT + "⚠️  No transactions.")
            return

        # Header
        print(Fore.LIGHTCYAN_EX + "{:<10} {:<8} {:<10} {:<12} {:<12} {:<15} {:<5}".format(
            "Trans No", "Book No", "Member No", "Issue Date", "Return Date", "Actual Return", "Fine"
        ))
        print(Fore.LIGHTBLACK_EX + "─" * 90)

        for row in rows:
            # Convert None values to '—' and everything to string
            safe_row = tuple("—" if val is None else str(val) for val in row)
            print(Fore.WHITE + "{:<10} {:<8} {:<10} {:<12} {:<12} {:<15} {:<5}".format(*safe_row))

    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"❌ Error: {e}")


#  ALL UNRETURNED BOOKS
def all_unreturned_books():
    print(Fore.CYAN + Style.BRIGHT + "\n📚 ALL UNRETURNED BOOKS")
    print(Fore.LIGHTBLACK_EX + "─" * 120)
    try:
        cursor.execute("""
            SELECT t.transaction_no,
                   b.book_name,
                   m.member_no,
                   m.member_name,
                   m.mobile_no,
                   t.issue_date,
                   t.return_date
            FROM transaction t
            JOIN book b ON t.book_no = b.book_no
            JOIN member m ON t.member_no = m.member_no
            WHERE t.actual_return_date IS NULL
        """)
        rows = cursor.fetchall()
        if not rows:
            print(Fore.YELLOW + Style.BRIGHT + "📭 No unreturned books.")
            return

        print(Fore.LIGHTCYAN_EX + "{:<10} {:<30} {:<10} {:<20} {:<15} {:<12} {:<12}".format(
            "Trans No", "Book Name", "Member No", "Member Name", "Mobile No", "Issue Date", "Return Date"
        ))
        print(Fore.LIGHTBLACK_EX + "─" * 120)

        for row in rows:
            safe_row = tuple("—" if val is None else str(val) for val in row)
            print(Fore.WHITE + "{:<10} {:<30} {:<10} {:<20} {:<15} {:<12} {:<12}".format(*safe_row))

    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"⚠️ Error: {e}")


#  UNRETURNED BOOKS BY MEMBER
def unreturned_books_by_member():
    print(Fore.CYAN + Style.BRIGHT + "\n📚 UNRETURNED BOOKS BY MEMBER / CATEGORY")
    print(Fore.LIGHTBLACK_EX + "─" * 45)
    try:
        choice = input(Fore.WHITE + "Search by:\n1. Member No\n2. Member Type\nEnter choice: ").strip()

        if choice == '1':
            member_no = input(Fore.BLUE + "🆔 Member No: ").strip()
            cursor.execute("""
                SELECT t.transaction_no, b.book_name, m.member_no, m.member_name, 
                       m.mobile_no, t.issue_date, t.return_date
                FROM transaction t
                JOIN book b ON t.book_no = b.book_no
                JOIN member m ON t.member_no = m.member_no
                WHERE t.member_no = %s AND t.actual_return_date IS NULL
            """, (member_no,))

        elif choice == '2':
            member_type = input(Fore.BLUE + "🏷️  Member Type (S/T/F): ").strip().upper()
            cursor.execute("""
                SELECT t.transaction_no, b.book_name, m.member_no, m.member_name, 
                       m.mobile_no, t.issue_date, t.return_date
                FROM transaction t
                JOIN book b ON t.book_no = b.book_no
                JOIN member m ON t.member_no = m.member_no
                WHERE m.member_type = %s AND t.actual_return_date IS NULL
            """, (member_type,))

        else:
            print(Fore.RED + Style.BRIGHT + "❌ Invalid choice.")
            return

        rows = cursor.fetchall()
        if not rows:
            print(Fore.YELLOW + Style.BRIGHT + "⚠️  No unreturned books found.")
            return

        print(Fore.LIGHTCYAN_EX + "{:<10} {:<30} {:<10} {:<20} {:<15} {:<12} {:<12}".format(
            "Trans No", "Book Name", "Member No", "Member Name", "Mobile No", "Issue Date", "Return Date"
        ))
        print(Fore.LIGHTBLACK_EX + "─" * 120)

        for row in rows:
            safe_row = tuple("—" if val is None else str(val) for val in row)
            print(Fore.WHITE + "{:<10} {:<30} {:<10} {:<20} {:<15} {:<12} {:<12}".format(*safe_row))

        print(Fore.LIGHTBLACK_EX + "─" * 120)

    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"❌ Error: {e}")


#  BOOK DETAILS
def book_details():
    try:
        book_no = int(input(Fore.BLUE + "🆔 Book Number to find: "))
        print(Fore.LIGHTBLACK_EX + "─" * 40)
        cursor.execute("""
            SELECT book_no, book_name, author_name, publisher_name, no_of_pages, price, number_of_copies, available_copies
            FROM book WHERE book_no = %s
        """, (book_no,))
        book = cursor.fetchone()
        if not book:
            print(Fore.RED + Style.BRIGHT + "❌ Book not found.")
            return
        book_no, book_name, author_name, publisher_name, no_of_pages, price, total_copies, available_copies = book
        print(Fore.LIGHTCYAN_EX + "🆔 Book No:" + Fore.LIGHTWHITE_EX + f"{book_no}")
        print(Fore.LIGHTCYAN_EX + "📖Name:" + Fore.LIGHTWHITE_EX + f"{book_name}")
        print(Fore.LIGHTCYAN_EX + "✍️Author:" + Fore.LIGHTWHITE_EX + f"{author_name}")
        print(Fore.LIGHTCYAN_EX + "🏢Publisher:" + Fore.LIGHTWHITE_EX + f"{publisher_name}")
        print(Fore.LIGHTCYAN_EX + "📄Pages:" + Fore.LIGHTWHITE_EX + f"{no_of_pages}")
        print(Fore.LIGHTCYAN_EX + "💰Price: Rs:" + Fore.LIGHTWHITE_EX + f"{price}")
        print(Fore.LIGHTCYAN_EX + "📚Total Copies:" + Fore.LIGHTWHITE_EX + f"{total_copies}")
        print(Fore.LIGHTCYAN_EX + "📦Available Copies:" + Fore.LIGHTWHITE_EX + f"{available_copies}")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"❌ Error finding book: {e}")

#  CHECK BOOK AVAILABILITY
def check_book_available():
    try:
        book_no = int(input(Fore.BLUE + "🆔 Book Number to check availability: "))
        print(Fore.LIGHTBLACK_EX + "─" * 40)
        cursor.execute("SELECT book_name, available_copies FROM book WHERE book_no = %s", (book_no,))
        result = cursor.fetchone()
        if not result:
            print(Fore.RED + Style.BRIGHT + "❌ Book not found.")
            return
        book_name, available_copies = result
        print(Fore.LIGHTCYAN_EX + "📖Name:" + Fore.LIGHTWHITE_EX + f"{book_name}")
        print(Fore.LIGHTCYAN_EX + "📦Available Copies:" + Fore.LIGHTWHITE_EX + f"{available_copies}")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"❌ Error checking book availability: {e}")


#  TRANSACTION MENU
def transaction_menu():
    while True:
        print(Fore.MAGENTA + Style.BRIGHT + "╔═════════════════════════════════════════════════════╗")
        print(Fore.MAGENTA + Style.BRIGHT + "║           📜📜 TRANSACTION MENU 📜📜               ║")
        print(Fore.MAGENTA + Style.BRIGHT + "╠═════════════════════════════════════════════════════╣")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 1. Issue Book                                       ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 2. Return Book                                      ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 3. List All Transactions                            ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 4. List All Unreturned Books                        ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 5. Unreturned Books by Member / Type                ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 6. Book Details                                     ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 7. Check Book Availability                          ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 8. Return to Main Menu                              ║")
        print(Fore.MAGENTA + Style.BRIGHT + "╚═════════════════════════════════════════════════════╝")

        choice = input(Fore.CYAN + Style.BRIGHT + "🔹 Enter your choice: ").strip()
        if choice == '1':
            issue_book()
        elif choice == '2':
            return_book()
        elif choice == '3':
            list_all_transaction()
        elif choice == '4':
            all_unreturned_books()
        elif choice == '5':
            unreturned_books_by_member()
        elif choice == '6':
            book_details()
        elif choice == '7':
            check_book_available()
        elif choice == '8':
            print(Fore.YELLOW + Style.BRIGHT + "↩️ Returning to Main Menu...")
            break
        else:
            print(Fore.RED + Style.BRIGHT + "❌ Invalid choice! Try again.")


if __name__ == "__main__":
    transaction_menu()
    cursor.close()
    conn.close()