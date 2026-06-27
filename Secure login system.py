import sqlite3
import bcrypt
import random

# Database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password BLOB
)
""")

conn.commit()

logged_in_user = None

# Register
def register():
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    if not username or not password:
        print("Username and Password cannot be empty!")
        return

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        print("Registration Successful!")
    except sqlite3.IntegrityError:
        print("Username already exists!")

# Login
def login():
    global logged_in_user

    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    if result:
        stored_password = result[0]

        if bcrypt.checkpw(
            password.encode(),
            stored_password
        ):
            otp = random.randint(100000, 999999)

            print(f"\nOTP: {otp}")  # Simulated OTP

            user_otp = input("Enter OTP: ")

            if user_otp == str(otp):
                logged_in_user = username
                print("Login Successful!")
            else:
                print("Invalid OTP!")
        else:
            print("Wrong Password!")
    else:
        print("User Not Found!")

# Dashboard
def dashboard():
    global logged_in_user

    if logged_in_user:
        print(f"\nWelcome {logged_in_user}")
        print("1. Logout")

        choice = input("Choose: ")

        if choice == "1":
            logged_in_user = None
            print("Logged Out Successfully!")
    else:
        print("Please Login First!")

# Main Menu
while True:
    print("\n===== Secure Login System =====")
    print("1. Register")
    print("2. Login")
    print("3. Dashboard")
    print("4. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        register()

    elif choice == "2":
        login()

    elif choice == "3":
        dashboard()

    elif choice == "4":
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")

conn.close()
