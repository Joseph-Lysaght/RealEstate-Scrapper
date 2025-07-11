# Importing module 
import mysql.connector

# Creating connection object
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "seppiesrealestate"
)

# Printing the connection object 
print(mydb)

cursor = mydb.cursor()

# Show database
cursor.execute("SHOW Tables")

for x in cursor:
  print(x)
