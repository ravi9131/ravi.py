import pyodbc
import random as ran

# Connect to SQL Server (make sure you replace these with your own connection details)
server = 'DESKTOP-U7RDVH2\\SQLEXPRESS'
database = 'QuizApp'  # The database we created above
# username = 'DESKTOP-U7RDVH2\\acer'

# Establish a connection to the SQL Server
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes')
cursor = conn.cursor()

#------------------1------------------
def register_user():
    print("**********          Register Yourself          **************\n")
    username = input("Enter the user name: ").upper()

    print("""
          Your Password Should Contain
          1. 1 lower case letter
          2. 1 upper case letter
          3. 1 digit
          4. 8 > length < 20
          5. 1 special character from one of these (@#%_$)
          """)

    while True:
        userpassword = input("Enter the Password: ")
        length = len(userpassword)
        l, u, d, s = 0, 0, 0, 0
        if length >= 8 and length <= 20:
            for i in userpassword:
                if i.islower():
                    l += 1
                if i.isupper():
                    u += 1
                if i.isdigit():
                    d += 1
                if i in '@#%_$':
                    s += 1

        # Check if username already exists in the database
        cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
        user_exists = cursor.fetchone()

        if user_exists:
            print("\n**********************************************")
            print("You have Already Registered")
            print("**********************************************")
            break
        elif l >= 1 and u >= 1 and d >= 1 and s >= 1:
            print("\n**********************************************")
            print("Your Password is Accepted")
            print("**********************************************")

            # Insert the new user into the database
            cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, userpassword))
            conn.commit()
            print("\n**********************************************")
            print("Registration Successful")
            print("**********************************************")
            break
        else:
            print("**********************************************")
            print("Your Password is not Accepted")
            print("**********************************************")

# ----------------2--------------
def login_user():
    print("**********          Login          **********\n")
    print("****************************************************************")
    username = input("Enter the User Name: ").upper()
    password = input("Enter the Password: ")
    print("****************************************************************")

    # Check if the username exists and the password matches
    cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    if user:
        print("\n**********************************************")
        print(f"Login successful! Welcome, {username}")
        print("**********************************************")
        return username
    else:
        print("\n**********************************************")
        print("Invalid User Name and Password")
        print("**********************************************")
        return None

# ------------3------------------

def attempt_quiz(current_user):
    print("**********          Attempt Quiz          **********\n")
    if current_user:
        quiz_questions = [
            {"question": "In which year was the Python language developed?",
             "choices": ["1. 1991", "2. 1985", "3. 1885"], "answer": 1},
            {"question": "In which language is Python written?", "choices": ["1. Java", "2. C", "3. PHP"], "answer": 2},
            {"question": "Which one of the following is the correct extension of the Python file?",
             "choices": ["1. .python", "2. .p", "3. .py"], "answer": 3},
            {"question": "Single Line comments in Python begin with Symbol", "choices": ["1. #", "2. @", "3. %"],
             "answer": 1},
            {"question": "Which of the Following are the fundamental building block of python Programming",
             "choices": ["1. Constants", "2. Tokens", "3. Identifiers"], "answer": 2},
            {
                "question": "The reserved words used by Pyhton Interpreter to recognize the structure of the Program are termed as",
                "choices": ["1. Tokens", "2. Literals", "3. Keywords"], "answer": 3},
            {"question": "What can be the maximum possible length of the Identifier",
             "choices": ["1. 31", "2. 79", "3. None of these"], "answer": 3},
            {"question": "Which of the following statement is correct about List",
             "choices": ["1. List can contain value of mixed data type",
                         "2. A List with no element is called empty List", "3. All of these"], "answer": 3},
            {"question": "Which opperator can be used with List",
             "choices": ["1. in", "2. not in", "3. both (1) & (2)"], "answer": 3},
            {"question": "Which of the following commands will create a list",
             "choices": ["1. List=list()", "2. List1=[]", "3. All of these"], "answer": 3},
            {"question": "What is the use of append() function in list",
             "choices": ["1. It adds an items to the end of the list", "2. It adds an item anywhere in list",
                         "3. It adds an items to the beginning of the list"], "answer": 1}]
        selected_question = ran.sample(quiz_questions, 5)
        score = 0

        print(f"{current_user}, let's start the quiz!\n")
        for i, question in enumerate(selected_question):
            print(f"Q{i + 1}: {question['question']}")
            for choice in question['choices']:
                print(choice)
            answer = int(input("Choose the correct answer (1, 2, or 3): "))
            if answer == question['answer']:
                score += 1

        print("\n**********************************************")
        print("Quiz completed!")
        print("**********************************************")

        # Check if the user already has a quiz result
        cursor.execute('SELECT * FROM QuizResults WHERE username = ?', (current_user,))
        existing_result = cursor.fetchone()

        if existing_result:
            # If the result exists, update the score
            cursor.execute('UPDATE QuizResults SET score = ?, total_questions = ? WHERE username = ?',
                           (score, len(selected_question), current_user))
            print(f"{current_user}'s score has been updated.")
        else:
            # If no result exists, insert a new record
            cursor.execute('INSERT INTO QuizResults (username, score, total_questions) VALUES (?, ?, ?)',
                           (current_user, score, len(selected_question)))
            print(f"{current_user}'s result has been saved.")

        conn.commit()
        print("\n**********************************************")
        print(f"{current_user}, check your result by pressing 5.")
        print("**********************************************")
    else:
        print("You need to log in first to attempt the quiz.")



# --------4----------------
def view_result(current_user):
    print("**********          Result          **********\n")
    if current_user:
        cursor.execute('SELECT score, total_questions FROM QuizResults WHERE username = ?',
                       (current_user,))
        result = cursor.fetchone()
        if result:
            score, total = result
            print(f"{current_user}'s score: {score}/{total}")
        else:
            print("No quiz results found.")
    else:
        print("Please log in and attempt the quiz first.")

def main():
    current_user = None  # To store the current logged-in user

    while True:
        print("""
        *******************************************************************************
                        1. Registration
                        2. View Users
                        3. Login
                        4. Attempt Quiz
                        5. Result
                        6. Exit
        *******************************************************************************
        """)
        oper = input("Enter the Operation: ")
        print()

        if oper == '1':
            # Call the registration function
            register_user()

        elif oper == '2':
            # View the list of users (you can implement this as needed)
            cursor.execute("SELECT username FROM Users")
            users = cursor.fetchall()
            print("Registered Users:")
            for user in users:
                print(user[0])

        elif oper == '3':
            # Call the login function
            current_user = login_user()

        elif oper == '4':
            # Attempt the quiz if the user is logged in
            attempt_quiz(current_user)

        elif oper == '5':
            # View the quiz result if the user is logged in
            view_result(current_user)

        elif oper == '6':
            # Exit the program
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

main()

conn.close()