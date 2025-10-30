# Library-management

The Library Management System (LMS) is a console-based application built with Python and backed by a MySQL database. It is designed to efficiently manage the day-to-day operations of a small to medium-sized library, handling book inventory, member records, and borrowing/return transactions, including fine calculation and report generation. The system emphasizes a user-friendly, color-coded interface using the colorama library.

#Modular Structure

The project is broken down into multiple Python files, each responsible for a specific function, ensuring high modularity and maintainability.

01booktable.py	       Database utility: Creates the book table and inserts sample data.
02bookmenu.py	         Book Management Menu. Handles all CRUD operations for the book table.
03memberstable.py	     Database utility: Creates the member table and inserts sample data.
04membermenu.py	       Member Management Menu. Handles all CRUD operations for the member table.
05transactiontable.py	 Database utility: Creates the transaction table and inserts sample data.
06transactionmenu.py 	 Transaction Module. Contains the core business logic for issue_book() and return_book() with fine calculation.
07report.py	           Report Generation Module. Contains functions to fetch data and generate PDF reports.
08admin.py             Administrative Module. Contains functions to create and drop the library database. (Default Admin Password: 1234)
09mainmenu.py	         Application Entry Point. Displays the main menu and manages the flow by executing other scripts.





