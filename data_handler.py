import pandas as pd
import os
import random

def get_available_quizzes():
    """
    Scans the resources directory for available quizzes (Excel files).
    """
    quizzes = []
    for filename in os.listdir('resources'):
        if filename.endswith('.xlsx'):
            quizzes.append(os.path.splitext(filename)[0])
    return quizzes

def load_questions(quiz_name='DE_Test_Translations'):
    """
    Loads questions from a specified Excel file.
    """
    excel_path = os.path.join('resources', f'{quiz_name}.xlsx')

    try:
        questions_df = pd.read_excel(excel_path)
        return questions_df.to_dict(orient='records')
    except Exception as e:
        print(f"Error loading questions for {quiz_name}: {e}")
        return []

def get_random_questions(questions, num_questions=10):
    """
    Returns a random subset of questions.
    """
    return random.sample(questions, min(num_questions, len(questions)))
