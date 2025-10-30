document.addEventListener('DOMContentLoaded', function () {
    const quizContainer = document.getElementById('quiz-container');
    const quizSelection = document.getElementById('quiz-selection');
    const quizDropdown = document.getElementById('quiz-dropdown');
    let questions = [];
    let currentQuestionIndex = 0;
    let userAnswers = {};
    let selectedQuiz = '';

    function startQuiz() {
        selectedQuiz = quizDropdown.value;
        quizSelection.style.display = 'none'; // Hide the dropdown
        fetch(`/start-quiz?quiz_name=${selectedQuiz}&num_questions=10`)
            .then(response => response.json())
            .then(data => {
                questions = data;
                displayQuestion(currentQuestionIndex);
            })
            .catch(error => console.error('Error fetching questions:', error));
    }

    function displayQuestion(index) {
        quizContainer.innerHTML = '';
        const question = questions[index];
        const questionElement = document.createElement('div');

        const options = [question.option_a, question.option_b, question.option_c, question.option_d];
        const optionsHTML = options.map(option => `
            <label>
                <input type="radio" name="question${question.id}" value="${option}" ${userAnswers[question.id] === option ? 'checked' : ''}>
                ${option}
            </label>
        `).join('<br>');

        questionElement.innerHTML = `
            <h2>${index + 1}. ${question.question_text}</h2>
            ${optionsHTML}
        `;
        quizContainer.appendChild(questionElement);

        // Add event listeners to radio buttons
        document.querySelectorAll(`input[name="question${question.id}"]`).forEach(radio => {
            radio.addEventListener('change', (event) => {
                userAnswers[question.id] = event.target.value;
            });
        });

        updateNavigation();
    }

    function updateNavigation() {
        let navHTML = '';
        if (currentQuestionIndex > 0) {
            navHTML += '<button id="prev-btn">Previous</button>';
        }
        if (currentQuestionIndex < questions.length - 1) {
            navHTML += '<button id="next-btn">Next</button>';
        }
        if (currentQuestionIndex === questions.length - 1) {
            navHTML += '<button id="submit-btn">Submit</button>';
        }
        quizContainer.insertAdjacentHTML('beforeend', navHTML);

        document.getElementById('prev-btn')?.addEventListener('click', () => {
            currentQuestionIndex--;
            displayQuestion(currentQuestionIndex);
        });

        document.getElementById('next-btn')?.addEventListener('click', () => {
            currentQuestionIndex++;
            displayQuestion(currentQuestionIndex);
        });

        document.getElementById('submit-btn')?.addEventListener('click', submitQuiz);
    }

    function submitQuiz() {
        const submittedAnswers = {
            quiz_name: selectedQuiz,
            answers: Object.keys(userAnswers).map(questionId => ({
                question_id: parseInt(questionId),
                selected_option: userAnswers[questionId]
            }))
        };

        fetch('/submit-quiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(submittedAnswers)
        })
        .then(response => response.json())
        .then(result => {
            displayResults(result);
        })
        .catch(error => console.error('Error submitting quiz:', error));
    }

    function displayResults(result) {
        quizContainer.innerHTML = `
            <h2>Quiz Results</h2>
            <p>Your score: ${result.score} / ${result.total}</p>
        `;
        result.feedback.forEach(item => {
            const question = questions.find(q => q.id === item.question_id);
            quizContainer.innerHTML += `
                <div>
                    <p>${question.question_text}</p>
                    <p>Your answer: ${userAnswers[item.question_id]}</p>
                    ${!item.correct ? `<p>Correct answer: ${item.correct_answer}</p>` : ''}
                </div>
            `;
        });
    }

    // Initial view
    quizContainer.innerHTML = '<button id="start-btn">Start Quiz</button>';
    document.getElementById('start-btn').addEventListener('click', startQuiz);
});
