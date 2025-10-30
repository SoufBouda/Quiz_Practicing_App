from flask import Flask, jsonify, render_template, request, redirect, url_for
from data_handler import load_questions, get_random_questions, get_available_quizzes
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    quizzes = get_available_quizzes()
    return render_template('index.html', quizzes=quizzes)

@app.route('/admin')
def admin():
    quizzes = get_available_quizzes()
    return render_template('admin.html', quizzes=quizzes)

@app.route('/upload-quiz', methods=['POST'])
def upload_quiz():
    if 'quiz_file' not in request.files:
        return 'No file part'
    file = request.files['quiz_file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.xlsx'):
        filename = secure_filename(file.filename)
        file.save(os.path.join('resources', filename))
        return redirect(url_for('admin'))
    return 'Invalid file type'

@app.route('/start-quiz', methods=['GET'])
def start_quiz():
    quiz_name = request.args.get('quiz_name', 'DE_Test_Translations')
    num_questions = request.args.get('num_questions', 10, type=int)
    questions = load_questions(quiz_name)
    random_questions = get_random_questions(questions, num_questions)
    return jsonify(random_questions)

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    submitted_answers = request.get_json()
    quiz_name = submitted_answers.get('quiz_name', 'DE_Test_Translations')
    questions = load_questions(quiz_name)
    score = 0
    feedback = []

    for answer in submitted_answers.get('answers', []):
        question_id = answer.get('question_id')
        selected_option = answer.get('selected_option')

        question_data = next((q for q in questions if q['id'] == question_id), None)

        if question_data:
            if selected_option == question_data['correct_answer']:
                score += 1
                feedback.append({'question_id': question_id, 'correct': True})
            else:
                feedback.append({
                    'question_id': question_id,
                    'correct': False,
                    'correct_answer': question_data['correct_answer']
                })

    return jsonify({
        'score': score,
        'total': len(submitted_answers.get('answers', [])),
        'feedback': feedback
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
