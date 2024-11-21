import time
import random
import os

# File paths
user_data_file = "users.txt"
questions_file = "questions.txt"
results_file = "results.txt"

# Function to register a user
def register():
    print("\n--- Register ---")
    name = input("Enter your name: ")
    enrollment = input("Enter your enrollment number: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Save user data to file
    with open(user_data_file, "a") as f:
        f.write(f"{enrollment},{password},{name},{email}\n")
    print("Registration successful!")

# Function to login a user
# Function to login a user
def login():
    print("\n--- Login ---")
    enrollment = input("Enter your enrollment number: ")
    password = input("Enter your password: ")

    # Verify user credentials
    with open(user_data_file, "r") as f:
        users = f.readlines()
        for user in users:
            user_data = user.strip().split(",")
            
            # Ensure the line has exactly 4 values (enrollment, password, name, email)
            if len(user_data) == 4:
                stored_enrollment, stored_password, _, _ = user_data
                if stored_enrollment == enrollment and stored_password == password:
                    print("Login successful!")
                    return enrollment
            else:
                print(f"Invalid user data format: {user}")
    print("Invalid enrollment number or password!")
    return None


# Function to load questions from file
def load_questions():
    questions = []
    with open(questions_file, "r") as f:
        data = f.readlines()
        for line in data:
            question, *options, correct = line.strip().split(",")
            questions.append({
                "question": question,
                "options": options,
                "correct": correct
            })
    random.shuffle(questions)
    return questions

# Function to attempt the quiz
def attempt_quiz(enrollment):
    print("\n--- Quiz ---")
    questions = load_questions()
    correct_answers = 0
    total_questions = len(questions)
    
    start_time = time.time()
    for i, q in enumerate(questions, start=1):
        print(f"\nQ{i}: {q['question']}")
        for j, option in enumerate(q['options'], start=1):
            print(f"{j}. {option}")
        
        answer = input("Your answer (1-4): ")
        if q['options'][int(answer) - 1] == q['correct']:
            correct_answers += 1
    
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)
    score = f"{correct_answers}/{total_questions}"

    # Save result to file
    with open(results_file, "a") as f:
        f.write(f"{enrollment},{score},{time_taken} seconds\n")
    
    print(f"\nQuiz finished! Your score: {score}")
    print(f"Time taken: {time_taken} seconds")

# Function to view the result
def view_result(enrollment):
    print("\n--- Results ---")
    with open(results_file, "r") as f:
        results = f.readlines()
        found = False
        for result in results:
            result_enrollment, score, time_taken = result.strip().split(",")
            if result_enrollment == enrollment:
                print(f"Score: {score}, Time: {time_taken}")
                found = True
        if not found:
            print("No result found!")

# Main menu
def main():
    if not os.path.exists(user_data_file):
        open(user_data_file, 'w').close()  # Create the file if not exists
    if not os.path.exists(questions_file):
        # Example questions to store in file (Question, Options, Correct Answer)
        with open(questions_file, 'w') as f:
            f.write("What is the capital of France?,Paris,London,Berlin,Rome,Paris\n")
            f.write("What is 5 + 5?,7,10,15,20,10\n")
            f.write("What is the largest planet?,Earth,Mars,Jupiter,Saturn,Jupiter\n")
            f.write("Which year did the Titanic sink?,1905,1912,1920,1915,1912\n")
    
    while True:
        print("\n--- Quiz Application ---")
        print("1. Register")
        print("2. Login")
        print("3. Attempt Quiz")
        print("4. View Results")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            enrollment = login()
            if enrollment:
                while True:
                    print("\n1. Attempt Quiz")
                    print("2. View Results")
                    print("3. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == '1':
                        attempt_quiz(enrollment)
                    elif sub_choice == '2':
                        view_result(enrollment)
                    elif sub_choice == '3':
                        break
                    else:
                        print("Invalid choice!")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
