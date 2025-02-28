function initializeAssessment(type, questions) {
    const questionsContainer = document.querySelector('.questions');

    // Render questions
    questions.forEach(question => {
        const questionEl = document.createElement('div');
        questionEl.className = 'mb-4';

        questionEl.innerHTML = `
            <label class="form-label">${question.question}</label>
            ${getInputHtml(question)}
        `;

        questionsContainer.appendChild(questionEl);
    });

    // Handle form submission
    document.getElementById('assessment-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const answers = {};
        questions.forEach(question => {
            if (question.type === 'text') {
                answers[question.id] = document.querySelector(`#q${question.id}`).value;
            } else if (question.type === 'multiple') {
                const selected = Array.from(document.querySelectorAll(`input[name="q${question.id}"]:checked`))
                    .map(el => el.value);
                answers[question.id] = selected;
            } else if (question.type === 'scale') {
                answers[question.id] = document.querySelector(`#q${question.id}`).value;
            }
        });

        try {
            const response = await fetch('/assessment/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    type: type,
                    answers: answers,
                    score: calculateScore(answers, questions)
                })
            });

            if (response.ok) {
                window.location.href = '/recommendations';
            }
        } catch (error) {
            console.error('Error submitting assessment:', error);
        }
    });
}

function getInputHtml(question) {
    switch (question.type) {
        case 'text':
            return `<textarea class="form-control" id="q${question.id}" rows="3" required></textarea>`;

        case 'multiple':
            return question.options.map(option => `
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" name="q${question.id}" value="${option}" id="q${question.id}_${option}">
                    <label class="form-check-label" for="q${question.id}_${option}">${option}</label>
                </div>
            `).join('');

        case 'scale':
            return `
                <div class="range-container">
                    <input type="range" class="form-range" id="q${question.id}" 
                        min="${question.min}" max="${question.max}" step="1" required>
                    <div class="d-flex justify-content-between">
                        <small class="text-muted">${question.labels[0]}</small>
                        <small class="text-muted">${question.labels[1]}</small>
                    </div>
                </div>
            `;
    }
}

function calculateScore(answers, questions) {
    let totalScore = 0;
    let maxPossibleScore = 0;

    questions.forEach(question => {
        switch (question.type) {
            case 'text':
                // Score based on length and content
                const textLength = answers[question.id].trim().length;
                const textScore = Math.min(textLength / 100, 1) * 100; // Max 100 chars for full score
                totalScore += textScore;
                maxPossibleScore += 100;
                break;

            case 'multiple':
                // Score based on number of selected options
                const selectedCount = answers[question.id].length;
                const multipleScore = (selectedCount / question.options.length) * 100;
                totalScore += multipleScore;
                maxPossibleScore += 100;
                break;

            case 'scale':
                // Convert scale to percentage
                const scaleScore = ((answers[question.id] - question.min) / (question.max - question.min)) * 100;
                totalScore += scaleScore;
                maxPossibleScore += 100;
                break;
        }
    });

    // Return percentage score
    return (totalScore / maxPossibleScore) * 100;
}