import warnings

warnings.filterwarnings("ignore", category=UserWarning, message="You are using pip version 22.0.3; however, version 24.0 is available.")

import streamlit as st
import psycopg2


st.title("Test Your Math Skills with Sanghamitra Learning!")
st.subheader("This basic math quiz is designed to help you practice your fundamental arithmetic operations, geometry, algebra, and more.")

def connect_to_database():
    """Connects to the PostgreSQL database using provided credentials.

    Raises:
        psycopg2.OperationalError: If an error occurs while connecting to the database.

    Returns:
        psycopg2.connect: A connection object to the PostgreSQL database.
    """
    try:
        # Replace placeholders with your actual database credentials
        conn = psycopg2.connect(
        dbname='postgres',
        user='postgres.vefsrnhnzjtpgrqppoml',
        password='6~p9yT.YZq*tE64',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to database: {e}")
        raise  # Re-raise the exception for handling in the main program

# Sample quiz data structure (can be replaced with database connection)
quiz_data = []  # Empty list to store quiz data from the database

def fetch_quiz_data(conn):
    """Fetches quiz data from the database and stores it in the quiz_data list.

    Args:
        conn (psycopg2.connect): The database connection object.
    """

    cursor = conn.cursor()

    # Replace with your actual SQL query to fetch quiz data
    cursor.execute("""
        SELECT id, question, option_a, option_b, option_c, option_d, correct_option
        FROM quiz1;
    """)

    # Process the fetched data and store it in quiz_data
    for row in cursor.fetchall():
        id, question, option_a, option_b, option_c, option_d, correct_option = row
        options = [option_a, option_b, option_c, option_d]

        # Convert correct_option (letter) to index
        correct_option_index = ord(correct_option.lower()) - ord('a')

        quiz_data.append({
            "id": id,
            "question": question,
            "options": options,
            "correct_option": correct_option_index
        })

    cursor.close()
    return quiz_data

def display_question(question, options, current_question_index):
    """Displays a single question with radio buttons and stores the user's answer.

    Args:
        question (str): The question text.
        options (list): A list of answer options (e.g., ["a", "b", "c", "d"]).
        current_question_index (int): The index of the current question.

    Returns:
        int: The user's chosen answer index (0-based).
    """
    st.subheader(question)
    user_answer_label = st.radio("Options", options, index=None, key=f"question_{current_question_index}")
    st.divider()
    
    if user_answer_label is not None:
        user_answer_index = options.index(user_answer_label)
        return user_answer_index
        
    else:
        return None  # Indicate that no option was selected

# Function to calculate the quiz score

def main():
    st.header("Test your knowledge!")

    # Connect to the database
    try:
        conn = connect_to_database()
        quiz_data = fetch_quiz_data(conn)
    except Exception as e:
        st.error(f"An error occurred while fetching quiz data: {e}")
        return  # Exit the main function if there's an error

    # Track user answers and current question index
    user_answers = []
    current_question_index = 0

    # Display questions one by one using quiz_data (fetched from database)
    for i, question_data in enumerate(quiz_data):
        question = question_data["question"]
        options = question_data["options"]

        # Display question number with bold formatting
        st.write(f"**Question {i+1}:**", unsafe_allow_html=True)

        # Display the actual question text
        user_answer = display_question(question, options, current_question_index)
        user_answers.append(user_answer)
        current_question_index += 1

    # Submit button and score display with explanations
    if st.button("Submit Quiz"):
        score = calculate_score(user_answers, quiz_data)
        total_questions = len(quiz_data)

        st.success(f"Your score is {score} out of {total_questions}")

        # Optional: Provide explanations for correct and incorrect answers

    # Close the database connection if it was opened successfully
    if conn:
        conn.close()

# ... other functions (display_question, calculate_score) as before (update calculate_score)

def calculate_score(user_answers, quiz_data):
    """Calculates the quiz score based on user answers and correct options.

    Args:
        user_answers (list): A list of user-selected answer indices.
        quiz_data (list): A list of dictionaries containing quiz data.

    Returns:
        int: The user's score (number of correct answers).
    """

    score = 0
    for i, user_answer in enumerate(user_answers):
        correct_option_index = quiz_data[i]["correct_option"]
        if user_answer == correct_option_index:
            score += 1
    return score

if __name__ == "__main__":
    main()
