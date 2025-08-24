from pathlib import Path
import os

# Read File and Folder: 
def readFileAndFolder():
        path = Path('')
        items = list(path.rglob('*'))
        print("These are the already existed files: ")
        for i , items in enumerate(items):
                print("{} : {}".format(i+1 , items))

def createAFile():
        # Ask the user to enter name of the file:
        try:
            readFileAndFolder()
            nameOfFile = input("Enter name of your file: ")
            pathOfFile = Path(nameOfFile) 

            if not pathOfFile.exists():
                with open(pathOfFile , "w") as f:
                    content = input("What do you want to write in this file: ")
                    f.write(content)

                print("FILE CREATED SUCCESSFULLY!!\n")
            else:
                  print("This file already exists!!\n")

        except Exception as e:
              print(f"An error occured: {e}")

def readAFile():
      try:
        readFileAndFolder()

        nameOfFile = input("Which file you want to read? Enter the name of the file: ")

        pathOfFile = Path(nameOfFile)
        if pathOfFile.exists() and pathOfFile.is_file():
                print("Here is the content of the file: \n")
                with open(pathOfFile , "r") as file:
                    content = file.read()
                    print(content)

                print("FILE READ SUCCESSFULLY!!\n")
        else:
                print("This file does not exists!!\n") 
      except Exception as e:
            print(f"An error occured: {e}")
            
def updateAFile():
      try: 
           readFileAndFolder()

           nameOfFile = input("Enter the name of the file: ")
           pathOfFile = Path(nameOfFile)

           if pathOfFile.exists and pathOfFile.is_file() :
                 while True:
                    print("\n")
                    print("Press 1 for updating the name of the file")
                    print("Press 2 for overwriting the content of the file") 
                    print("Press 3 for appending the content of the file")
                    print("Press 4 to exit")
                    
                    try:
                        choice = int(input("Enter your choice: "))
                    except:
                        print("Invalid input! Please enter a number.")
                        return
                    
                    if choice == 1:
                        newName = input("Enter new name of the file: ")
                        newPath = Path(newName)

                        pathOfFile.rename(newPath)
                        pathOfFile = newPath

                        print("FILENAME UPDATED SUCCESSFULLY!!")
                    elif choice == 2:
                        content = input("Enter new content to overwrite: ")
                        with open(pathOfFile , "w") as file:
                                file.write(content)
                                print("CONTENT OVERWRITTEN SUCCESSFULLY!!")
                    elif choice == 3:
                        content = input("Enter content to append: ")
                        with open(pathOfFile , "a") as file:
                                file.write(" "+content)
                                print("CONTENT APPENDED SUCCESSFULLY!!")
                    elif choice == 4:
                        print("Exiting....")
                        break
                    else:
                        print("Invalid choice!! Enter between (1-3).")
           else:
                 print("This file does not exists!!")

      except Exception as e:
            print(f"An error occured: {e}")

def deleteAFile():
     try:
          readFileAndFolder()

          nameOfFile = input("Enter the name of the file: ")
          pathOfFile = Path(nameOfFile)

          if pathOfFile.exists and pathOfFile.is_file() :
               os.remove(nameOfFile)

               print("FILE DELETED SUCCESSFULLY!!\n")
          else:
               print("This file does not exists!!")
     except Exception as e:
            print(f"An error occured: {e}")   
    

# Menu: 
print("---==== WELCOME TO CRUD APPLICATION ====---")

while True:
    print("\n")
    print("Press 1 to create a file")
    print("Press 2 to read a file")
    print("Press 3 to update a file")
    print("Press 4 to delete a file")
    print("Press 5 to exit...")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a valid number.\n")
        continue

    if choice == 1:
          createAFile()
    elif choice == 2:
          readAFile()
    elif choice == 3:
          updateAFile()
    elif choice == 4:
          deleteAFile()
    elif choice == 5:
          print("Exiting the program....")
          break
    else:
          print("Invalid choice! Enter a number from (1 - 5)")
        
