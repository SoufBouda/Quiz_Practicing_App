document.addEventListener('DOMContentLoaded', function () {
    fetch('http://127.0.0.1:5000/get-questions')  // Use localhost for testing
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Use data to dynamically create quiz questions in the HTML
            let quizContainer = document.getElementById('quiz-container');
            data.forEach((question, index) => {
                let questionElement = document.createElement('div');
                questionElement.innerHTML = `<p>${index + 1}. ${question.question_text}</p>`;
                quizContainer.appendChild(questionElement);
            });
        })
        .catch(error => console.error('Error fetching questions:', error));
});
