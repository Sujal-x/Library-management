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

def create_database():
    a = "CREATE DATABASE IF NOT EXISTS library"
    cursor.execute(a)
    print(Fore.GREEN + Style.BRIGHT + "✅ Database 'library' created successfully!")

    execute("01booktable.py")
    execute("03memberstable.py")
    execute("05transactiontable.py")

def drop_database():
    cursor.execute("DROP DATABASE IF EXISTS library")
    print(Fore.RED + Style.BRIGHT + "🗑️  Dropped database successfully!")

def backup():
    print(Fore.BLUE + "💾 Backup functionality coming soon...")

def admin_menu():
    while True:
        print(Fore.MAGENTA + Style.BRIGHT + '╔═════════════════════════════════════════════════════╗')
        print(Fore.MAGENTA + Style.BRIGHT + '║           🔐🔐 A D M I N  M E N U 🔐🔐             ║')
        print(Fore.MAGENTA + Style.BRIGHT + '╠═════════════════════════════════════════════════════╣')
        print(Fore.MAGENTA + Style.BRIGHT + '║           1. CREATE DATABSAE                        ║')
        print(Fore.MAGENTA + Style.BRIGHT + '║           2. DROP DATABASE                          ║')
        print(Fore.MAGENTA + Style.BRIGHT + '║           3. BACKUP DATA                            ║')
        print(Fore.MAGENTA + Style.BRIGHT + '║           4. RETURN TO MAIN MENU                    ║')
        print(Fore.MAGENTA + Style.BRIGHT + '╚═════════════════════════════════════════════════════╝')

        try:
            choice = int(input(Fore.CYAN + Style.BRIGHT + "🔹 ENTER YOUR CHOICE (1-4): "))
        except ValueError:
            print(Fore.RED + Style.BRIGHT + "❌ Please enter a valid number!")
            continue

        if choice == 1:
            create_database()
        elif choice == 2:
            drop_database()
        elif choice == 3:
            backup()
        elif choice == 4:
            print(Fore.YELLOW + Style.BRIGHT + "↩️  Returning to Main Menu...")
            break
        else:
            print(Fore.RED + Style.BRIGHT + "❌ Invalid choice. Please choose between 1-4.")

if __name__ == "__main__":
    admin_menu()
    cursor.close()
    conn.close()