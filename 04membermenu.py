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


# ADD NEW MEMBER
def add_new_member():
    try:
        print(Fore.CYAN + Style.BRIGHT + "\n🧑‍🤝‍🧑 ADD NEW MEMBER\n" + Fore.LIGHTBLACK_EX + "─" * 40)
        member_no = int(input(Fore.BLUE + "🆔 Member Number: "))

        cursor.execute("SELECT * FROM member WHERE member_no = %s", (member_no,))
        existing = cursor.fetchone()
        if existing:
            print(Fore.YELLOW + Style.BRIGHT + "⚠️  Member already exists!")
            return

        member_name = input(Fore.BLUE + "📖 Member Name: ")
        mobile_no = input(Fore.BLUE + "📱 Mobile Number: ")
        member_type = input(Fore.BLUE + "🏷️ Member Type (S, T, F): ").upper()
        roll_no = None
        standard = None
        if member_type == "S":
            roll_no = input(Fore.BLUE + "🎓 Roll Number: ")
            standard = input(Fore.BLUE + "🏫 Class: ")

        cursor.execute("""
        INSERT INTO member(member_no, member_name, mobile_no, member_type, roll_no, standard)
        VALUES(%s, %s, %s, %s, %s, %s)
        """, (member_no, member_name, mobile_no, member_type, roll_no, standard))

        conn.commit()
        print(Fore.GREEN + Style.BRIGHT + "✅ Member added successfully!")

    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"❌ Error: {e}")


# MODIFY MEMBER
def modify_member():
    print(Fore.CYAN + Style.BRIGHT + "\n📝 MODIFY MEMBER DETAILS\n" + Fore.LIGHTBLACK_EX + "─" * 40)
    member_no = int(input(Fore.WHITE + "🆔 Member Number to Modify: "))
    cursor.execute("SELECT * FROM member WHERE member_no = %s", (member_no,))
    member = cursor.fetchone()
    if not member:
        print(Fore.RED + Style.BRIGHT + "❌ Member not found.")
        return

    print(Fore.YELLOW + Style.BRIGHT + "ℹ️  Leave blank to keep current value.")
    member_name = input(Fore.BLUE + "📖 New Member Name " + Fore.LIGHTWHITE_EX + f"[{member[1]}]: ") or member[1]
    mobile_no = input(Fore.BLUE + "📱 New Mobile Number " + Fore.LIGHTWHITE_EX + f"[{member[3]}]: ") or member[3]
    member_type = input(
        Fore.BLUE + "🏷️ New Member Type (S, T, F) " + Fore.LIGHTWHITE_EX + f"[{member[2]}]: ").upper() or member[2]
    roll_no = None
    standard = None
    if member_type == "S":
        roll_no = input(Fore.BLUE + "🎓 Roll Number " + Fore.LIGHTWHITE_EX + f"[{member[4]}]: ") or member[4]
        standard = input(Fore.BLUE + "🏫 Class " + Fore.LIGHTWHITE_EX + f"[{member[5]}]: ") or member[5]

    cursor.execute("""
        UPDATE member SET
            member_name = %s,
            mobile_no = %s,
            member_type = %s,
            roll_no = %s,
            standard = %s
        WHERE member_no = %s
    """, (member_name, mobile_no, member_type, roll_no, standard, member_no))

    conn.commit()
    print(Fore.GREEN + Style.BRIGHT + "✅ Member updated successfully!")


# DELETE MEMBER
def delete_member():
    print(Fore.CYAN + Style.BRIGHT + "\n🗑️ DELETE MEMBER\n" + Fore.LIGHTBLACK_EX + "─" * 30)
    member_no = input(Fore.WHITE + "🆔 Member Number to Delete: ")
    cursor.execute("SELECT * FROM member WHERE member_no = %s", (member_no,))
    member = cursor.fetchone()

    if not member:
        print(Fore.RED + Style.BRIGHT + "❌ Member not found.")
        return

    print(Fore.LIGHTCYAN_EX + "\n🧑‍🤝‍🧑 Member Details:")
    print(Fore.LIGHTBLACK_EX + "─" * 25)
    print(Fore.BLUE + "🆔 Member No:", member[0])
    print(Fore.BLUE + "📖 Name:", member[1])
    print(Fore.BLUE + "🏷️ Type:", member[2])
    print(Fore.BLUE + "📱 Mobile:", member[3])
    if member[2] == "S":
        print(Fore.BLUE + "🎓 Roll No:", member[4])
        print(Fore.BLUE + "🏫 Class:", member[5])

    choice = input(Fore.YELLOW + "\n⚠️  Confirm delete? (Y/N): ").lower()
    if choice != "y":
        print(Fore.GREEN + Style.BRIGHT + "❎ Deletion cancelled.")
        return

    try:
        cursor.execute("DELETE FROM member WHERE member_no = %s", (member_no,))
        conn.commit()
        print(Fore.GREEN + Style.BRIGHT + "✅ Member deleted successfully.")
    except pymysql.err.IntegrityError:
        print(Fore.RED + Style.BRIGHT + "⚠️  Cannot delete — active transactions exist.")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"❌ Error: {e}")


# LIST ALL MEMBERS
def list_all_members():
    print(Fore.CYAN + Style.BRIGHT + "\n🧑‍🤝‍🧑 ALL MEMBERS\n" + Fore.LIGHTBLACK_EX + "─" * 80)
    cursor.execute("SELECT * FROM member")
    members = cursor.fetchall()
    if not members:
        print(Fore.YELLOW + Style.BRIGHT + "⚠️  No members found.")
        return

    header = "{:<8} {:<25} {:<10} {:<15} {:<10} {:<10}".format(
        "MemberNo", "Name", "Type", "Mobile", "RollNo", "Class"
    )
    print(Fore.LIGHTCYAN_EX + header)
    print(Fore.LIGHTBLACK_EX + "─" * 80)

    for m in members:
        print(Fore.WHITE + "{:<8} {:<25} {:<10} {:<15} {:<10} {:<10}".format(
            m[0], m[1], m[2], m[3], m[4] if m[4] else "-", m[5] if m[5] else "-"
        ))

    print(Fore.GREEN + Style.BRIGHT + "\n✅ All members displayed successfully!\n")


# SEARCH BY MEMBER NO
def find_by_member_no():
    print("Search by: \n1.Member No \n2.Member Type:")
    choice = input("Enter your choice: ")
    if choice == "1":
        print(Fore.CYAN + Style.BRIGHT + "\n🔍 SEARCH MEMBER BY NUMBER\n" + Fore.LIGHTBLACK_EX + "─" * 30)
        member_no = int(input(Fore.WHITE + "🆔 Member Number: "))
        cursor.execute("SELECT * FROM member WHERE member_no = %s", (member_no,))
        member = cursor.fetchone()
        if member:
            print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n🧑‍🤝‍🧑 Member Details:")
            print(Fore.LIGHTBLACK_EX + "─" * 25)
            print(Fore.BLUE + "🆔 Member No:", member[0])
            print(Fore.BLUE + "📖 Name:", member[1])
            print(Fore.BLUE + "🏷️ Type:", member[2])
            print(Fore.BLUE + "📱 Mobile:", member[3])
            if member[2] == "S":
                print(Fore.BLUE + "🎓 Roll No:", member[4])
                print(Fore.BLUE + "🏫 Class:", member[5])
        else:
            print(Fore.RED + Style.BRIGHT + "❌ Member not found.")

    elif choice == "2":
        print(Fore.CYAN + Style.BRIGHT + "\n🔍 SEARCH MEMBER BY TYPE\n" + Fore.LIGHTBLACK_EX + "─" * 30)
        member_type = input(Fore.WHITE + "🏷️ Enter Member Type (S/T/F): ")
        cursor.execute("SELECT * FROM member WHERE member_type = %s", (member_type,))
        member = cursor.fetchall()
        if member:
            print(Fore.LIGHTBLACK_EX + "─" * 80)
            header = "{:<8} {:<25} {:<10} {:<15} {:<10} {:<10}".format(
                "MemberNo", "Name", "Type", "Mobile", "RollNo", "Class"
            )
            print(Fore.LIGHTCYAN_EX + header)
            print(Fore.LIGHTBLACK_EX + "─" * 80)

            for m in member:
                print(Fore.WHITE + "{:<8} {:<25} {:<10} {:<15} {:<10} {:<10}".format(
                    m[0], m[1], m[2], m[3], m[4] if m[4] else "-", m[5] if m[5] else "-"
                ))
        else:
            print(Fore.RED + Style.BRIGHT + "❌ Member not found.")


# SEARCH BY KEYWORD
def find_by_keywords():
    print(Fore.CYAN + Style.BRIGHT + "\n🔎 SEARCH MEMBER BY KEYWORD\n" + Fore.LIGHTBLACK_EX + "─" * 30)
    keyword = input(Fore.WHITE + "🔤 Enter Keyword: ")
    like_keywords = f"%{keyword}%"
    cursor.execute("""
        SELECT * FROM member
        WHERE member_name LIKE %s OR member_type LIKE %s OR mobile_no LIKE %s OR roll_no LIKE %s OR standard LIKE %s
    """, (like_keywords, like_keywords, like_keywords, like_keywords, like_keywords))
    members = cursor.fetchall()

    if members:
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n📜 Matching Members:")
        print(Fore.LIGHTBLACK_EX + "─" * 80)
        print(Fore.LIGHTCYAN_EX + "{:<8} {:<25} {:<10} {:<15} {:<10} {:<10}".format(
            "MemberNo", "Name", "Type", "Mobile", "RollNo", "Class"
        ))
        print(Fore.LIGHTBLACK_EX + "─" * 80)
        for m in members:
            print(Fore.WHITE + "{:<8} {:<25} {:<10} {:<15} {:<10} {:<10}".format(
                m[0], m[1], m[2], m[3], m[4] if m[4] else "-", m[5] if m[5] else "-"
            ))
    else:
        print(Fore.YELLOW + Style.BRIGHT + "⚠️  No matching members found.")


# MEMBER MENU
def member_menu():
    while True:
        print(Fore.MAGENTA + Style.BRIGHT + "╔═════════════════════════════════════════════════════╗")
        print(Fore.MAGENTA + Style.BRIGHT + "║              🧑‍🤝‍🧑🧑‍🤝‍🧑 MEMBER MENU 🧑‍🤝‍🧑🧑‍🤝‍🧑                 ║")
        print(Fore.MAGENTA + Style.BRIGHT + "╠═════════════════════════════════════════════════════╣")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 1. Add New Member                                   ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 2. Modify Member Details                            ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 3. Delete Member                                    ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 4. List All Members                                 ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 5. Find Member by No or Type                        ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 6. Find Member by Keyword                           ║")
        print(Fore.MAGENTA + Style.BRIGHT + "║ 7. Return to Main Menu                              ║")
        print(Fore.MAGENTA + Style.BRIGHT + "╚═════════════════════════════════════════════════════╝")

        try:
            choice = int(input(Fore.CYAN + "🔹 Enter your choice (1–7): "))
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "❌ Please enter a valid number.")
            continue

        if choice == 1:
            add_new_member()
        elif choice == 2:
            modify_member()
        elif choice == 3:
            delete_member()
        elif choice == 4:
            list_all_members()
        elif choice == 5:
            find_by_member_no()
        elif choice == 6:
            find_by_keywords()
        elif choice == 7:
            print(Fore.YELLOW + Style.BRIGHT + "↩️ Returning to Main Menu...")
            break
        else:
            print(Fore.RED + Style.BRIGHT + "⚠️  Invalid choice. Please choose between 1–7.")


if __name__ == "__main__":
    member_menu()
    cursor.close()
    conn.close()