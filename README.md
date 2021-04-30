# Book-Store
Project Description:
This project implements a simple online bookstore. You can login, signup, order a book and see some book suggestions like other web bookstores.  You can also login as manager to control the database like add books, change book stock.

Stack Used:
Frontend: HTML,CSS
Backend: Python3, Jinja2
Database: SQLite


For set up:
pip install -r requirements.txt(Install everything from requirement.txt in server folder)
Pip install flask flask-sqlalchemy(install flask,python)(install after activate virtual environment)
easy_install flask-bcrypt(this is for hashed password that needs to be install)
In terminal direct to bookstore/backend folder
source venv/bin/activate
cd server
Python3 
from app import db
db.create_all()
Init the super manager at beginning(Optional since the data is already populated)

To Run:
Direct to bookstore/backend
source venv/bin/activate
Cd server
Python3 app.py
The system will be available at localhost:8000 in the browser(use google chrome)
(if the browser does not load the css file, try to hard reload the browser(command shift r) or (control r))


Following account can be used for manager control and user login:

Manager ID:644132

User ID:644132
Password:1234


After Login to Manager:
We can add manager, add book, manage customer, manage book stock, and see statistics

User can sign up in the sign up button and that account can be used right away

After Login to Customer:
There are 6 main tabs for all the functionality:
Home: User can search a book by given author and/or publisher and/or language and/or book title.  The section below is a list of books that are in the database in date from oldest to newest order.  Users can click the view button on each book to see the detail of the book and order the book with a specified number of copies.
Degree of Separation: Users can give an author's name and the program will show a list of authors that are in degree of separation of the given author(search John, you will get authors that are in degree of separation of John).
Book Suggestions: Here we have suggested books for the author(popular sale books, cheapest books etc...).
Other People: Users can see all the other Users in the database and mark them as trust or untrusted.
My Order: Users can see a list of orders that he(she) have ordered.
My Profile: Users can see their profile include their name, address etc...


(If you want to browse the database, you can download the DB Browser for sqlite, You can test it by using data in their, it is connected to the system, database file name is data.db)
