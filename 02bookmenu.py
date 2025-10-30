from colorama import Fore, Style, init
import pymysql

init(autoreset=True)

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="sujal1",
    database="library"
)
cursor = conn.cursor()


#  ADD NEW BOOK
def add_new_book():
    try:
        print(Fore.CYAN + Style.BRIGHT + "\n📘 ADD NEW BOOK\n" + Fore.LIGHTBLACK_EX + "─" * 40)
        book_no = input(Fore.BLUE + "🆔 Book Number: ").lower()

        cursor.execute("SELECT * FROM book WHERE book_no = %s", (book_no,))
        existing = cursor.fetchone()

        if existing:
            print(Fore.YELLOW + Style.BRIGHT + "⚠️  Book number already exists!")
            return
        elif book_no == "exit":
            print(Fore.YELLOW + Style.BRIGHT + "👋 Exiting...")
            return

        book_name = input(Fore.BLUE + "📖 Book Name: ")
        author_name = input(Fore.BLUE + "✍️ Author Name: ")
        publisher = input(Fore.BLUE + "🏢 Publisher Name: ")
        no_of_pages = int(input(Fore.BLUE + "📄 Number of Pages: "))
        no_of_copies = int(input(Fore.BLUE + "📚 Total Copies: "))
        available_copies = int(input(Fore.BLUE + "📦 Available Copies: "))
        price = float(input(Fore.BLUE + "💰 Price: "))

        cursor.execute("""
            INSERT INTO book (book_no, book_name, author_name, publisher_name, no_of_pages, price, number_of_copies, available_copies)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (book_no, book_name, author_name, publisher, no_of_pages, price, no_of_copies, available_copies))

        conn.commit()
        print(Fore.GREEN + Style.BRIGHT + "✅ Book added successfully!")

    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")


#  MODIFY BOOK
def modify_book():
    print(Fore.CYAN + Style.BRIGHT + "\n📝 MODIFY BOOK DETAILS\n" + Fore.LIGHTBLACK_EX + "─" * 40)
    book_no = input(Fore.WHITE + "🆔 Book Number to Modify: ")

    cursor.execute("SELECT * FROM book WHERE book_no = %s", (book_no,))
    book = cursor.fetchone()
    if not book:
        print(Fore.RED + Style.BRIGHT + "❌ Book not found.")
        return

    print(Fore.YELLOW + "ℹ️  Leave blank to keep current value.")
    book_name = input(Fore.BLUE + "📖 New Book Name " + Fore.LIGHTWHITE_EX + f"[{book[1]}]: ") or book[1]
    author_name = input(Fore.BLUE + "✍️ New Author Name" + Fore.LIGHTWHITE_EX + f"[{book[2]}]: ") or book[2]
    publisher_name = input(Fore.BLUE + "🏢 New Publisher Name" + Fore.LIGHTWHITE_EX + f"[{book[3]}]: ") or book[3]
    no_of_pages = int(input(Fore.BLUE + "📄 New Pages" + Fore.LIGHTWHITE_EX + f"[{book[4]}]: ") or book[4])
    price = float(input(Fore.BLUE + "💰 New Price " + Fore.LIGHTWHITE_EX + f"[{book[5]}]: ") or book[5])
    number_of_copies = int( input(Fore.BLUE + "📚 New Total Copies" + Fore.LIGHTWHITE_EX + f"[{book[6]}]: ") or book[6])
    available_copies = int(input(Fore.BLUE + "📦 New Available Copies" + Fore.LIGHTWHITE_EX + f"[{book[7]}]: ") or book[7])

    cursor.execute("""
        UPDATE book SET
            book_name = %s,
            author_name = %s,
            publisher_name = %s,
            no_of_pages = %s,
            price = %s,
            number_of_copies = %s,
            available_copies = %s
        WHERE book_no = %s
    """, (book_name, author_name, publisher_name, no_of_pages, price, number_of_copies, available_copies, book_no))

    conn.commit()
    print(Fore.GREEN + Style.BRIGHT + "✅ Book updated successfully!")


#  DELETE BOOK
def delete_book():
    print(Fore.CYAN + Style.BRIGHT + "\n🗑️ DELETE BOOK\n" + Fore.LIGHTBLACK_EX + "─" * 30)
    book_no = input(Fore.WHITE + "🆔 Book Number to Delete: ")

    cursor.execute("SELECT * FROM book WHERE book_no = %s", (book_no,))
    book = cursor.fetchone()
    if not book:
        print(Fore.RED + Style.BRIGHT + "❌ Book not found.")
        return

    print(Fore.LIGHTCYAN_EX + "\n📘 Book Details:")
    print(Fore.LIGHTBLACK_EX + "─" * 25)
    print(Fore.BLUE +"🆔 Book No:", book[0])
    print(Fore.BLUE +"📖 Name:", book[1])
    print(Fore.BLUE +"✍️ Author:", book[2])
    print(Fore.BLUE +"🏢 Publisher:", book[3])
    print(Fore.BLUE +"📄 Pages:", book[4])
    print(Fore.BLUE +"💰 Price:", book[5])
    print(Fore.BLUE +"📚 Total Copies:", book[6])
    print(Fore.BLUE +"📦 Available Copies:", book[7])

    choice = input(Fore.YELLOW + Style.BRIGHT + "\n⚠️  Confirm delete? (Y/N): ").lower()
    if choice != "y":
        print(Fore.YELLOW + Style.BRIGHT + "❎ Deletion cancelled.")
        return

    try:
        cursor.execute("DELETE FROM book WHERE book_no = %s", (book_no,))
        conn.commit()
        print(Fore.GREEN + Style.BRIGHT + "✅ Book deleted successfully.")
    except pymysql.err.IntegrityError:
        print(Fore.RED + Style.BRIGHT + "⚠️  Cannot delete — active transactions exist.")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"❌ Error: {e}")


#  LIST ALL BOOKS
def list_all_books():
    print(Fore.CYAN + Style.BRIGHT + "\n📚 ALL BOOKS\n" + Fore.LIGHTBLACK_EX + "─" * 125)
    cursor.execute("SELECT * FROM book")
    books = cursor.fetchall()

    if not books:
        print(Fore.YELLOW + Style.BRIGHT + "⚠️  No books found.")
        return

    header = "{:<8} {:<30} {:<20} {:<20} {:<8} {:<8} {:<12} {:<10}".format(
        "BookNo", "Book Name", "Author", "Publisher", "Pages", "Price", "Total", "Available"
    )
    print(Fore.LIGHTCYAN_EX + header)
    print(Fore.LIGHTBLACK_EX + "─" * 125)

    for b in books:
        print(Fore.WHITE + "{:<8} {:<30} {:<20} {:<20} {:<8} {:<8} {:<12} {:<10}".format(*b))

    print(Fore.GREEN + Style.BRIGHT + "\n✅ All books displayed successfully!\n")


#  SEARCH BY BOOK NO
def find_by_book_no():
    print(Fore.CYAN + Style.BRIGHT + "\n🔍 SEARCH BOOK BY NUMBER\n" + Fore.LIGHTBLACK_EX + "─" * 30)
    book_no = input(Fore.WHITE + "🆔 Book Number: ")

    cursor.execute("SELECT * FROM book WHERE book_no = %s", (book_no,))
    book = cursor.fetchone()

    if book:
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n📗 Book Details:")
        print(Fore.LIGHTBLACK_EX + "─" * 25)
        print(Fore.BLUE + "🆔 Book No:", book[0])
        print(Fore.BLUE + "📖 Name:", book[1])
        print(Fore.BLUE + "✍️ Author:", book[2])
        print(Fore.BLUE + "🏢 Publisher:", book[3])
        print(Fore.BLUE + "📄 Pages:", book[4])
        print(Fore.BLUE + "💰 Price:", book[5])
        print(Fore.BLUE + "📚 Total Copies:", book[6])
        print(Fore.BLUE + "📦 Available Copies:", book[7])
    else:
        print(Fore.RED + "❌ Book not found.")


#  SEARCH BY KEYWORD
def find_by_keywords():
    print(Fore.CYAN + Style.BRIGHT + "\n🔎 SEARCH BOOK BY KEYWORD\n" + Fore.LIGHTBLACK_EX + "─" * 30)
    keywords = input(Fore.WHITE + "🔤 Enter Keyword: ")
    like_keywords = f"%{keywords}%"

    cursor.execute("""
        SELECT * FROM book
        WHERE book_name LIKE %s OR author_name LIKE %s OR publisher_name LIKE %s
    """, (like_keywords, like_keywords, like_keywords))
    books = cursor.fetchall()

    if books:
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n📜 Matching Books:")
        print(Fore.LIGHTBLACK_EX + "─" * 125)
        print(Fore.LIGHTCYAN_EX +"{:<8} {:<30} {:<20} {:<20} {:<8} {:<8} {:<12} {:<10}".format(
            "BookNo", "Book Name", "Author", "Publisher", "Pages", "Price", "Total", "Available"
        ))
        print(Fore.LIGHTBLACK_EX + "─" * 125)
        for b in books:
            print(Fore.WHITE + "{:<8} {:<30} {:<20} {:<20} {:<8} {:<8} {:<12} {:<10}".format(*b))
    else:
        print(Fore.YELLOW + Style.BRIGHT + "⚠️  No matching books found.")


#  BOOK MENU
def book_menu():
    while True:
        print(Fore.MAGENTA + Style.BRIGHT + "╔═════════════════════════════════════════════════════╗")
        print(Fore.MAGENTA + Style.BRIGHT + "║                📘📘 BOOK MENU 📘📘                 ║")
        print(Fore.MAGENTA + Style.BRIGHT + "╠═════════════════════════════════════════════════════╣")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 1. Add New Book                                     ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 2. Modify Book Details                              ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 3. Delete Book                                      ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 4. List All Books                                   ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 5. Find Book by Number                              ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 6. Find Book by Keyword                             ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 7. Return to Main Menu                              ║")
        print(Fore.MAGENTA + Style.BRIGHT + "╚═════════════════════════════════════════════════════╝")

        try:
            choice = int(input(Fore.CYAN + Style.BRIGHT + "🔹 Enter your choice (1–7): "))
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "❌ Please enter a valid number.")
            continue

        if choice == 1:
            add_new_book()
        elif choice == 2:
            modify_book()
        elif choice == 3:
            delete_book()
        elif choice == 4:
            list_all_books()
        elif choice == 5:
            find_by_book_no()
        elif choice == 6:
            find_by_keywords()
        elif choice == 7:
            print(Fore.YELLOW + Style.BRIGHT + "↩️ Returning to Main Menu...")
            break
        else:
            print(Fore.RED + Style.BRIGHT + "⚠️  Invalid choice. Please choose between 1–7.")


if __name__ == "__main__":
    book_menu()
    cursor.close()
    conn.close()