import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",       # MySQL is running on your local machine
    user="root",            # Your MySQL username
    password="manager", # Replace with your actual MySQL password
    database="multisource"  # The database name you want to connect to
)

cursor = conn.cursor()

# Check if connection is successful
if conn.is_connected():
    print("Connected to MySQL successfully!")
else:
    print("Failed to connect.")

# Close the connection
conn.close()
