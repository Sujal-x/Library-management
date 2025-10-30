from colorama import Fore, Style, init
import subprocess
import sys
import pymysql

init(autoreset=True)

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="sujal1"
)
cursor = conn.cursor()

def execute(a):
    subprocess.run([sys.executable, a])

def main_menu():
    while True:
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '╔═════════════════════════════════════════════════════╗')
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '║            🏠🏠 M A I N   M E N U  🏠🏠            ║')
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '╠═════════════════════════════════════════════════════╣')
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '║           1. BOOK MENU                              ║')
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '║           2. MEMBER MENU                            ║')
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '║           3. TRANSACTION MENU                       ║')
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '║           4. REPORT                                 ║')
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '║           5. ADMIN                                  ║')
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '║           6. EXIT                                   ║')
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + '╚═════════════════════════════════════════════════════╝')

        choice = input(Fore.CYAN + Style.BRIGHT + "🔹 Enter your choice: ")
        if choice == '1':
            execute("02bookmenu.py")
        elif choice == '2':
            execute("04membermenu.py")
        elif choice == '3':
            execute("06transactionmenu.py")
        elif choice == '4':
            execute("07report.py")
        elif choice == '5':
            pw = input("Enter your password: ")
            if pw == "1234":
                print(Fore.LIGHTGREEN_EX + "✅ Access Granted")
                execute("08admin.py")
            else:
                print(Fore.LIGHTRED_EX + "⚠️ Invalid password")
        elif choice == '6':
            print(Fore.YELLOW + Style.BRIGHT + "👋 Exiting...")
            break
        else:
            print(Fore.RED + Style.BRIGHT + "❌ Invalid choice! Try again.")

if __name__ == "__main__":
    main_menu()
    cursor.close()
    conn.close()