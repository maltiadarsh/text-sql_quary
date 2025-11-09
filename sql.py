import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Create the table (if not already created)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
    Name VARCHAR(25),
    Class VARCHAR(25),
    Section VARCHAR(25),
    Marks INTEGER
)
""")

# 20 dummy student records
students = [
    ("Adarsh", "10th", "A", 88),
    ("Riya", "10th", "B", 92),
    ("Arjun", "9th", "A", 85),
    ("Sneha", "8th", "C", 91),
    ("Karan", "10th", "A", 79),
    ("Meena", "9th", "B", 83),
    ("Raj", "8th", "A", 76),
    ("Pooja", "9th", "C", 89),
    ("Amit", "10th", "B", 95),
    ("Isha", "8th", "A", 82),
    ("Manish", "9th", "B", 87),
    ("Nisha", "10th", "C", 90),
    ("Rohan", "8th", "A", 73),
    ("Kavita", "9th", "C", 84),
    ("Tanya", "10th", "B", 96),
    ("Vikram", "9th", "A", 81),
    ("Divya", "8th", "C", 78),
    ("Suresh", "10th", "A", 85),
    ("Anjali", "9th", "B", 93),
    ("Deepak", "8th", "A", 80)
]

# Insert all records at once
cursor.executemany("INSERT INTO Student VALUES (?, ?, ?, ?)", students)


print("The inserted records are :")

# Retrieve and display all records
data = cursor.execute("SELECT * FROM Student")
# rows = cursor.fetchall()

for row in data:
    print(row)

# Commit changes
connection.commit()

# Close connection
connection.close()
