#Import crypto.py library. This is used for hashing and verification
import crypto

#Import db.py library. This is used to do all MySQL interaction
import db

#Creates a variable to store the username_password in memory after login to application
memory_username_password = None

#Creating the function register_user
#Asks the end user for username and a password
#Hashes the password with hash_password in crypto.py
#Saves the new user in the database via db.add_user
#Returns user_id if success. If not None
def register_user():
    global memory_username_password
    username = input("Write username: ")
    username_password = input("Write user password: ")
    username_password_hash = crypto.hash_password(username_password)

    user_id = db.add_user(username, username_password_hash)
    if user_id:
        memory_username_password = username_password
        print(f"New user created. Your user_id is {user_id}\n")
    else:
        print("Username already in databasae \n")
    return user_id


#Creating the function login
#Ask for user_id. 0 if register new user
#If user exists get hash from database and verify password
#Returns user_id on success. If not None
def login():
    global memory_username_password
    try:
        user_id = int(input("Enter user_id. If you are a new user enter 0 "))
    except ValueError:           
        print("user_id must be number value")
        return None
    
#If user_id 0 run register_user function
    if user_id == 0:
        return register_user()
    
#Get hash for user_id from database. If no result return None and print message
    stored_user_password_hash = db.get_username_password_hash(user_id)
    if stored_user_password_hash is None:
        print("No users with that user_id is in the database \n")
        return None
    
#Verifies the user password. If wrong return None and print message
#Stores the try_user_password value to the variable memory_username_password
    try_user_password = input("User passoword: ")
    if crypto.verify_password(try_user_password, stored_user_password_hash):
        memory_username_password = try_user_password
        print("Login success \n")
        return user_id
    else:
        print("Wrong password \n")
        return None


#Creating the function add_application
#Adds a new application row with password for the user
#Encrypts the application password before storing
def add_application(user_id):
    application_name = input("Application name: ")
    new_application_password = input("Application password: ")
    application_password_cipher = crypto.encrypt_password(
        new_application_password, memory_username_password
    )

    try:
        item_id = db.add_item(user_id, application_name, application_password_cipher)
        print(f"added {application_name} with item_id {item_id}\n")
    except Exception as fail:
        print("Update fail.", fail, "\n")


#Creating the function update_application_password
#Updates an application password for the user
def update_application_password(user_id):
    application_name = input("Application name: ")
    new_application_password = input("New application password: ")
    application_password_cipher = crypto.encrypt_password(
        new_application_password, memory_username_password
    )

    if db.update_item(user_id, application_name, application_password_cipher):
        print("Updated application password \n")
    else:
        print("Update failed \n")

#Creates the function show_application_password
#Decrypts and prints password in clear text
def show_application_password(user_id):
    application_name = input("Application name: ")
    cipher = db.get_application_cipher(user_id, application_name)
    if cipher:
        plain = crypto.decrypt_password(cipher, memory_username_password)
        print(f"Password for {application_name} is {plain}\n")
    else:
        print("Cant find that application\n")


#Creating the function menu
#Shows a menu for the end user after login
def menu(user_id):
    while True:
        print("MENU")
        print("1) Add application and password")
        print("2) Update password for application")
        print("3) Show password for application")   # <-- NEW
        print("4) Quit")
        choice = input("Choose 1, 2 or 4: ")

        if choice == "1":
            add_application(user_id)
        elif choice == "2":
            update_application_password(user_id)
        elif choice == "3":
            show_application_password(user_id)      # <-- NEW
        elif choice == "4":
            print("Program closed")
            break
        else:
            print("Cant choose that number.\n")

#Program start
#Runs login first
#Start menu if login was success
if __name__ == "__main__":
    print("Password Vault")
    uid = login()
    if uid:
        menu(uid)