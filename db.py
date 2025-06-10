#Import mysql.connector library. This is used to connect to the vaultdb_test MySQL database
import mysql.connector

#Creating the function called connect_database
#Login values are read from login.txt file
def connect_database():

#Opens login.txt
#Encoding utf-8 supports norwegian æøå if used
#Function creates a dictionary named Login
#The for loops throigh each line in the file and stores key value pairs in the dictionary named login
    login = {}
    with open("login.txt", encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split("=", 1)
            login[key] = value

#Return connection using the values from the login.txt file
    return mysql.connector.connect(
        host=login["host"],
        user=login["user"],
        password=login["password"],
        database=login["database"],
    )

#Creating a function called add_item
#The function saves data in one row in the Vault table for user_id, application_name and application_password_cipher from crypto.py file
#Returns the itemID value that mySQL automaticly generates
def add_item(user_id, application_name, application_password_cipher):
   
#Opens a connection to the databasex
#Opens a cursor
    database_connection = connect_database()
    cursor = database_connection.cursor()

#Inserts data to the Vault tablex
    sql = (
        "INSERT INTO Vault (user_id, application_name, application_password_cipher) "
        "VALUES (%s, %s, %s)"
    )
    cursor.execute(sql, (user_id, application_name, application_password_cipher))

#Saves the changes to the database
    database_connection.commit()

#Gets the item_id value for the new row and close the cursor and database connection
    item_id = cursor.lastrowid
    cursor.close()
    database_connection.close()
    return item_id


#Creating the function get_username_password_hash
#Gets the column username_password_hash from the table User for a specific user_id
#Returns the hash string if the user exists. If not returns None
def get_username_password_hash(user_id):

#Opens a connection to the database
#Opens a cursor
    database_connection = connect_database()
    cursor = database_connection.cursor()

#Creates a variable named sql. The variable is a string that contains the username_password_hash from a specific user_id
#Cursor execute sends the sql variable to to MySQL server
    sql = "SELECT username_password_hash FROM User WHERE user_id = %s"
    cursor.execute(sql, (user_id,))

#Cursor.fetchone lets the cursor get the first row of the result
#application_password_hash variable is the value from the first row or None if no result
    row = cursor.fetchone()           
    application_password_hash = row[0] if row else None

#Close cursor and connection to the MySQL database
#Returns the value of application_password_hash variable
    cursor.close()
    database_connection.close()

    return application_password_hash

#Creates the function update_item
#Updates the cipher password (application_password_cipher) for the specified user and appliaction
#Adds date and time value to "updated" in vault table
#Returns True of one row was updated, if not it returns False
def update_item(user_id, application_name , new_application_password_cipher):

#Opens a connection to the database
#Opens a cursor
    database_connection = connect_database()
    cursor = database_connection.cursor()

#Creates a variable named sql
#Sets application_password_cipher and updated timestamp for a specific user_id and application
    sql = (
        "UPDATE Vault "
        "SET application_password_cipher = %s, updated = CURRENT_TIMESTAMP "
        "WHERE user_id = %s AND application_name = %s"
    )

#Runs the update with new values
    cursor.execute(sql, (new_application_password_cipher, user_id, application_name ))
    database_connection.commit()

#Close cursor and connection
    rows = cursor.rowcount       
    cursor.close()
    database_connection.close()

#Returns True if one row was updated
    return rows == 1  

#Creates the function add_user
def add_user(username, username_password_hash):

    database_connection = connect_database()
    cursor = database_connection.cursor() 
    sql = (
        "INSERT INTO User (username, username_password_hash) "
        "VALUES (%s, %s)"
    )
    cursor.execute(sql, (username, username_password_hash))
    database_connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    database_connection.close()
    return user_id

#Creates the function get_application_cipher
#Returns cipher text for a application. None if not found
def get_application_cipher(user_id, application_name):
    database_connection = connect_database()
    cursor = database_connection.cursor()

    sql = (
        "SELECT application_password_cipher "
        "FROM Vault WHERE user_id = %s AND application_name = %s"
    )
    cursor.execute(sql, (user_id, application_name))
    row = cursor.fetchone()

    cursor.close()
    database_connection.close()
    return row[0] if row else None