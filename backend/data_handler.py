import pandas as pd
import os

def load_questions():
    # Set the path to the Excel file
    excel_path = os.path.join('..', 'resources', 'DE_Test_Translations.xlsx')
    
    try:
        # Load the Excel file into a DataFrame
        questions_df = pd.read_excel(excel_path)
        questions = questions_df.to_dict(orient='records')
        return questions

    except Exception as e:
        print(f"Error loading questions: {e}")
        return []

# Example usage
if __name__ == '__main__':
    questions = load_questions()
    print(questions)
