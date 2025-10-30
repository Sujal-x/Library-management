from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, landscape
from colorama import Fore, Style, init
from reportlab.lib import colors
from datetime import datetime
import pymysql
import platform
import os

init(autoreset=True)


conn = pymysql.connect(
    host="localhost",
    user="root",
    password="sujal1",
    database="library"
)
cursor = conn.cursor()


# PDF GENERATOR
def generate_pdf_report(title, headers, data, filename_prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.pdf"

    pdf = SimpleDocTemplate(filename, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"<b>{title}</b>", styles['Title']))
    elements.append(Spacer(1, 20))

    # Handle empty data
    if not data:
        elements.append(Paragraph("No records found.", styles['Normal']))
    else:
        table_data = [headers] + [list(row) for row in data]
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

    pdf.build(elements)
    print(Fore.GREEN + f"\n✅ PDF generated: {filename}\n" + Style.RESET_ALL)

    # Auto-open PDF
    try:
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin":
            os.system(f"open '{filename}'")
        else:
            os.system(f"xdg-open '{filename}'")
    except Exception as e:
        print(Fore.YELLOW + f"⚠️ Could not open PDF: {e}" + Style.RESET_ALL)



#  BOOK REPORTS
def report_all_books():
    cursor.execute("SELECT * FROM book")
    data = cursor.fetchall()
    headers = ["Book No", "Book Name", "Author", "Publisher", "Page", "Price", "Total Copies", "Avaliable Copies"]
    generate_pdf_report(" Library Report: All Books", headers, data, "All_Books_Report")

def report_book_by_id():
    book_no = input(Fore.BLUE + "🆔 Enter Book No: ")
    cursor.execute("SELECT * FROM book WHERE book_no = %s", (book_no,))
    data = cursor.fetchall()
    headers = ["Book No", "Book Name", "Author", "Publisher", "Page", "Price", "Total Copies", "Avaliable Copies"]
    generate_pdf_report(f" Book Report (ID: {book_no})", headers, data, f"Book_{book_no}_Report")

def report_book_by_keyword():
    keyword = input(Fore.BLUE + "🔤 Enter keyword : ")
    cursor.execute("SELECT * FROM book WHERE book_name LIKE %s OR author_name LIKE %s OR publisher_name LIKE %s", (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    data = cursor.fetchall()
    headers = ["Book No", "Book Name", "Author", "Publisher", "Page", "Price", "Total Copies", "Avaliable Copies"]
    generate_pdf_report(f" Books Matching '{keyword}'", headers, data, f"Book_Search_{keyword}")


# MEMBER REPORTS
def report_all_members():
    cursor.execute("SELECT * FROM member")
    data = cursor.fetchall()
    headers = ["Member No", "Name", "Type", "Mobile", "RollNo", "Standard"]
    generate_pdf_report(" Library Report: All Members", headers, data, "All_Members_Report")

def report_member_by_id():
    print(Fore.WHITE + "Report by: \n1.Member No \n2.Member Type")
    choice = input(Fore.WHITE + "Enter your choice: ")
    if choice == "1":
        print(Fore.CYAN + Style.BRIGHT + "\nREPORT MEMBER BY No\n" + Fore.LIGHTBLACK_EX + "─" * 30)
        member_no = int(input(Fore.BLUE + "🆔 Member Number: "))
        cursor.execute("SELECT * FROM member WHERE member_no = %s", (member_no,))
        data = cursor.fetchall()
        headers = ["Member No", "Name", "Type", "Mobile", "RollNo", "Standard"]
        generate_pdf_report(f" Member Report (ID: {member_no})", headers, data, f"Member_{member_no}_Report")

    elif choice == "2":
        print(Fore.CYAN + Style.BRIGHT + "\nReport MEMBER BY TYPE\n" + Fore.LIGHTBLACK_EX + "─" * 30)
        member_type = input(Fore.BLUE + "🏷️‍ Enter Member Type (S/T/F): ").strip().upper()
        cursor.execute("SELECT * FROM member WHERE member_type = %s", (member_type,))
        data = cursor.fetchall()

        if not data:
            print(Fore.RED + "❌ No members found for this type.")
        else:
            headers = ["Member No", "Name", "Type", "Mobile", "RollNo", "Standard"]
            generate_pdf_report(f"Member Report (TYPE: {member_type})", headers, data, f"Member_{member_type}_Report")
    else:
        print(Fore.RED + Style.BRIGHT + "⚠️  Invalid choice. Please choose between 1–2.")

def report_member_by_keyword():
    keyword = input(Fore.BLUE + "🔤 Enter keyword : ")
    cursor.execute("SELECT * FROM member WHERE member_name LIKE %s OR member_type LIKE %s OR mobile_no LIKE %s OR roll_no LIKE %s OR standard LIKE %s",
                   (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    data = cursor.fetchall()
    headers = ["Member No", "Name", "Type", "Mobile", "RollNo", "Standard"]
    generate_pdf_report(f" Members Matching '{keyword}'", headers, data, f"Member_Search_{keyword}")


# TRANSACTION REPORTS
def report_all_transactions():
    cursor.execute("SELECT * FROM transaction")
    data = cursor.fetchall()
    headers = ["Trans No", "Book No", "Member No", "Issue Date", "Return Date", "Actual Return Date", "Fine"]
    generate_pdf_report(" Library Report: All Transactions", headers, data, "All_Transactions_Report")

def report_all_unreturned_books():
    cursor.execute("""SELECT transaction_no, book_no, member_no, issue_date, return_date,  actual_return_date 
                      FROM transaction WHERE actual_return_date IS NULL""")
    data = cursor.fetchall()
    headers = ["Trans No", "Book No", "Member No", "Issue Date", "Return Date", "Actual Return Date"]
    generate_pdf_report(" Library Report: All Unreturned Books", headers, data, "All_Unreturned_Books_Report")

def report_unreturned_books_by_member():
    print(Fore.WHITE + "\nReport by:\n1. Member ID\n2. Member Type")
    choice = input(Fore.WHITE + "Enter your choice: ")

    if choice == '1':
        print(Fore.CYAN + Style.BRIGHT + "\nREPORT MEMBER BY No\n" + Fore.LIGHTBLACK_EX + "─" * 30)
        member_no = input(Fore.BLUE + "🆔 Enter Member ID: ")
        query = """
            SELECT t.transaction_no, t.book_no, b.book_name, 
                   m.member_no, m.member_name, m.member_type, t.issue_date, t.return_date, t.actual_return_date
            FROM `transaction` t
            JOIN book b ON t.book_no = b.book_no
            JOIN member m ON t.member_no = m.member_no
            WHERE t.actual_return_date IS NULL
              AND t.member_no = %s
        """
        cursor.execute(query, (member_no,))
        data = cursor.fetchall()
        title = f" Unreturned Books for Member ID {member_no}"
        filename_prefix = f"Unreturned_Books_Member_{member_no}"

    elif choice == '2':
        print(Fore.CYAN + Style.BRIGHT + "\nREPORT MEMBER BY TYPE\n" + Fore.LIGHTBLACK_EX + "─" * 30)
        member_type = input(Fore.BLUE + "🏷️ Enter Member Type (S/T/F): ").upper()
        query = """
            SELECT t.transaction_no, b.book_no, b.book_name,
                   m.member_no, m.member_name, m.member_type, t.issue_date, t.return_date, t.actual_return_date
            FROM `transaction` t
            JOIN book b ON t.book_no = b.book_no
            JOIN member m ON t.member_no = m.member_no
            WHERE t.actual_return_date IS NULL
              AND m.member_type = %s
        """
        cursor.execute(query, (member_type,))
        data = cursor.fetchall()
        title = f" Unreturned Books for Member Type {member_type}"
        filename_prefix = f"Unreturned_Books_Type_{member_type}"

    else:
        print(Fore.RED + "❌ Invalid choice.")
        return

    headers = ["Trans No", "Book No", "Book Name", "Member No", "Member Name", "Member Type", "Issue Date", "Return Date", "Actual Return Date"]

    #no data is found
    if not data:
        print(Fore.YELLOW + "\n⚠️ No unreturned books found for this selection.")
        return

    generate_pdf_report(title, headers, data, filename_prefix)


#  REPORT MENU
def report_menu():
    while True:
        print(Fore.MAGENTA + Style.BRIGHT + "╔═════════════════════════════════════════════════════╗")
        print(Fore.MAGENTA + Style.BRIGHT + "║            📄📄 R E P O R T   M E N U 📄📄         ║")
        print(Fore.MAGENTA + Style.BRIGHT + "╠═════════════════════════════════════════════════════╣")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 1. All Books                                        ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 2. Book by Book No                                  ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 3. Book by Keyword                                  ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 4. All Members                                      ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 5. Member by No / Type                              ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 6. Member by Keyword                                ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 7. All Transactions                                 ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 8. All Unreturned Books                             ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 9. Unreturned Books by Member No / Type             ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 10. Return to Main Menu                             ║")
        print(Fore.MAGENTA + Style.BRIGHT + "╚═════════════════════════════════════════════════════╝")

        choice = input(Fore.CYAN + Style.BRIGHT + "🔹 Enter your choice: ")

        if choice == '1': report_all_books()
        elif choice == '2': report_book_by_id()
        elif choice == '3': report_book_by_keyword()
        elif choice == '4': report_all_members()
        elif choice == '5': report_member_by_id()
        elif choice == '6': report_member_by_keyword()
        elif choice == '7': report_all_transactions()
        elif choice == '8': report_all_unreturned_books()
        elif choice == '9': report_unreturned_books_by_member()
        elif choice == '10':
            print(Fore.YELLOW + Style.BRIGHT + "↩️ Returning to Main Menu...")
            break
        else:
            print(Fore.RED + Style.BRIGHT + "⚠️  Invalid choice. Please choose between 1–10.")


if __name__ == "__main__":
    report_menu()