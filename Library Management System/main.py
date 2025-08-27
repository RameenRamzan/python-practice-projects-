# MODULES AND PACKAGES:
import json # JSON {Javascript Object Notation} File: 
import random
import string
from pathlib import Path

# LIBRARAY CLASS:
class Library:
    database = 'data.json' # Path of data file
    data = [] # List
    bookDatabase = 'books.json'

    try:
        if Path(database).exists():
            with open(database  , "r") as fs:
                data = json.loads(fs.read()) # Loading the data in the data.json file
        else:
            print("No such file exists !!")
    except Exception as err:
        print(f"An exception occured: {err}")

    @classmethod # Private Method
    def __update(cls):
        with open(cls.database , "w") as fs:
            fs.write(json.dumps(Library.data, indent = 4))

    @classmethod # Private Method
    def __generateAccount(cls):
        alpha = random.choices(string.ascii_letters, k = 3) 
        num = random.choices(string.digits , k = 3)
        specialChars = random.choices("!@#$%^&*" , k = 1)
        user_id = alpha + num + specialChars
        random.shuffle(user_id) # It will give you a list
        return "".join(user_id) # Converting that list into string

    def createAccount(self):
        print("\n---==== CREATE LIBRARY ACCOUNT ====---")
        name = input("Enter your name: ").strip() # Name

        while True:
            email = input("Enter your email: ").strip() # Email Validation
            if '@' not in email or "." not in email:
                print("Invalid email format.")
                return
            else :
                break 
        
        try:
            while True:
                phone = input("Enter your phone number: ").strip() # Phone number Validation
                if not phone.isdigit() or len(phone) != 11:
                    raise ValueError("Phone number must be of 11 digits.")
                else:
                    break
        except ValueError as err:
            print("An exception occured: {err}")

 
        while True:
            password = input("Enter your password (minimum 6 characters): ") # Password
            if len(password) < 6:
                print("Password too short. Try again !!")
            else:
                break

        while True:
            pin = input("Enter a 4-digit pin: ")
            if not (pin.isdigit() and len(pin) == 4):
                print("Pin should be 4 digits.")
            else:
                break


        info = {
            "Id": Library.__generateAccount(),
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Password": password, 
            "Pin" : pin,
            "Books" : []
        }

        print("Account has been created successfully !!")
        for i in info:
            if i == "Books":
                continue
            print(f"{i} : {info[i]}")
        print("Kindly note down your id.")

        Library.data.append(info)

        Library.__update()

    def issueBook(self):

        print("\n---==== ISSUING A BOOK ====---")

        userId = input("Enter your user ID: ")
        pin = input("Enter your 4-digit PIN: ")

        userData = [i for i in Library.data  if i['Id'] == userId and i['Pin'] == pin ] # List Comprehension

        if not userData:
            print("Sorry, user doesn't exists or invalid credentials.")
            return
        
        bookName = input("Enter book name to be issued: ").strip()
        found = False

        try:
            if Path(Library.bookDatabase).exists():
                with open(Library.bookDatabase , "r") as fs:
                    books = json.loads(fs.read()) # Loading the data in books.json file
            else:
                print("No such file exists !!")
        except Exception as err:
            print(f"An exception occured: {err}")

        for book in books:
            if book['title'].lower() == bookName.lower():
                found = True
                if book['quantity'] > 0:
                    # Issue the book:
                    userData[0]['Books'].append({
                        "title":book['title'],
                        "author":book['author']
                    })
                    book['quantity'] -= 1

                    print(f"Book '{book['title']}' issued successfully!!")
                else:
                    print("Book is out of stock.")
                    return
                
        if not found:
            print("Book not found.")

        # Save updated quantity to books.json
        with open(Library.bookDatabase, "w") as f:
            json.dump(books, f, indent=4)

        # Also update user record in data.json
        Library.__update()


    def returnBook(self):
        userId = input("Enter your user ID: ")
        pin = input("Enter your 4-digit PIN: ")
        bookName = input("Enter book name to be returned: ").strip()

        try:
            if Path(Library.bookDatabase).exists():
                with open(Library.bookDatabase, "r") as fs:
                    books = json.load(fs)
            else:
                print("Books database file does not exist.")
                return
        except Exception as err:
            print(f"Error reading books database: {err}")
            return

        user_found = False
        book_returned = False

        for user in Library.data:
            if user['Id'] == userId and user['Pin'] == pin:
                user_found = True
                for issued_book in user["Books"]:
                    if issued_book["title"].lower() == bookName.lower():
                        # Update quantity in book database
                        for book in books:
                            if book["title"].lower() == bookName.lower():
                                book["quantity"] += 1
                                break

                        user["Books"].remove(issued_book)
                        print(f"{bookName} has been successfully returned.")
                        book_returned = True
                        break  # Stop checking more issued books
                if not book_returned:
                    print(f"You have not issued '{bookName}'.")
                break  # Stop checking more users

        if not user_found:
            print("User not found.")

        # Save updated books
        with open(Library.bookDatabase, "w") as f:
            json.dump(books, f, indent=4)

        # Update user record
        Library.__update()


    def showDetails(self):
        print("\n---==== PERSONAL INFORMATION ====---")
        userId = input("Enter your user ID: ")
        pin = input("Enter your 4-digit PIN: ")

        userData = [i for i in Library.data  if i['Id'] == userId and i['Pin'] == pin ] # List Comprehension

        if not userData:
            print("Sorry, user doesn't exists or invalid credentials.")
            return
        
        print("YOUR INFORMATION")
        
        for i in userData[0]:
            if i == "Books":
                books = userData[0].get("Books", [])
                if books:
                    print(f"{i}: {books}")
                else:
                    print(f"{i}: No books issued yet")
            else:
                print(f"{i}: {userData[0][i]}")


    def updateDetails (self):

        print("\n---==== UPDATING ACCOUNT DETAILS ====---")
        userId = input("Enter your user ID: ")
        pin = input("Enter your 4-digit PIN: ")

        userData = [i for i in Library.data  if i['Id'] == userId and i['Pin'] == pin ] # List Comprehension

        if not userData:
            print("Sorry, user doesn't exists or invalid credentials.")
            return
        
        print("You can't update the phone number and id.")
        print("Enter the new details and press enter if don't want to change: ")

        newData = {
            "Name" : input("Enter new name or enter to skip: "),
            "Email" : input("Enter new email or enter to skip: "),
            "Password" : input("Enter new password or enter to skip: "),
            "Pin" : input("Enter new pin or enter to skip: ")
        }
        

        if newData["Name"] == "":
            newData["Name"] = userData[0]["Name"]
        if newData["Email"] == "":
            newData["Email"] = userData[0]["Email"]
        if newData["Password"] == "":
            newData["Password"] = userData[0]["Password"]
        if newData["Pin"] == "":
            newData["Pin"] = userData[0]["Pin"]
 

        newData["Id"] = userData[0]["Id"]
        newData["Phone"] = userData[0]["Phone"]

        for i in newData:
            if newData[i] == userData[0][i]:
                continue
            else:
                userData[0][i] = newData[i]

        print("Details have been updated successfully!!")

        Library.__update()

    def deleteAccount(self):

        print("\n---==== DELETEING LIBRARY ACCOUNT ====---")
        userId = input("Enter your user ID: ")
        pin = input("Enter your 4-digit PIN: ")

        userData = [i for i in Library.data  if i['Id'] == userId and i['Pin'] == pin ] # List Comprehension

        if not userData:
            print("Sorry, user doesn't exists or invalid credentials.")
            return
        else:
            check = input("Do you really want to delete this account (Y / N): ")

            if check == 'N' or check == "n":
                pass
            else:
                index = Library.data.index(userData[0])

                Library.data.pop(index)

        print("Account has been deleted successfully !!")

        Library.__update()
        

    def showList(self):

        print("\n---==== LIST OF ISSUED BOOKS ====---")
        userId = input("Enter your user ID: ")
        pin = input("Enter your 4-digit PIN: ")

        userData = [i for i in Library.data if i['Id'] == userId and i['Pin'] == pin]

        if not userData:
            print("Sorry, user doesn't exist or credentials are invalid.")
            return

        books = userData[0].get("Books", [])
        if books:
            print("Books issued:")
            for book in books:
                print(f"- {book['title']} by {book['author']}")
        else:
            print("No books issued yet.")


user = Library()


# MENU:
while True:
    print("\n-=-@@@==== LIBRARY MANAGEMENT SYSTEM ====@@@---")
    print("📚 Welcome to the Library Management System 📚")
    print("1. Create Account")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. Delete Account")
    print("5. Update Account Details")
    print("6. List of issued books")
    print("7. Show Details")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        user.createAccount()
    elif choice == "2":
        user.issueBook()
    elif choice == "3":
        user.returnBook()
    elif choice == "4":
        user.deleteAccount()
    elif choice == "5":
        user.updateDetails()
    elif choice == "6":
        user.showList()
    elif choice == "7":
        user.showDetails()
    elif choice == "8":
        print("Thank you so much for coming!!")
        print("Exiting the program.....")
        break
    else:
        print("Invalid choice !!")
