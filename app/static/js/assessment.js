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
                    score: calculateScore(answers)
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
            return `<textarea class="form-control" id="q${question.id}" rows="3"></textarea>`;
            
        case 'multiple':
            return question.options.map(option => `
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" name="q${question.id}" value="${option}" id="q${question.id}_${option}">
                    <label class="form-check-label" for="q${question.id}_${option}">${option}</label>
                </div>
            `).join('');
            
        case 'scale':
            return `
                <input type="range" class="form-range" id="q${question.id}" 
                    min="${question.min}" max="${question.max}" step="1">
                <div class="d-flex justify-content-between">
                    <small>${question.labels[0]}</small>
                    <small>${question.labels[1]}</small>
                </div>
            `;
    }
}

function calculateScore(answers) {
    // Simple scoring algorithm - can be made more sophisticated
    return Math.random() * 100;  // Placeholder
}
