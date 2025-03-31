const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const typingIndicator = document.getElementById('typing-indicator');

// Sample suggested questions for AI career guidance
const suggestedQuestions = [
    "What career paths are available in AI?",
    "What skills do I need for an AI career?",
    "Which AI career pays the most?",
    "How do I transition into AI from another field?",
    "What education is required for AI jobs?",
    "Which AI specialization is most in demand?",
    "What companies hire AI professionals?",
    "How do I prepare for AI job interviews?"
];

function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}-message`;
    messageDiv.innerHTML = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    typingIndicator.classList.remove('d-none');
}

function hideTypingIndicator() {
    typingIndicator.classList.add('d-none');
}

function simulateTyping(callback) {
    // Simulate typing delay (500-1500ms)
    const delay = Math.floor(Math.random() * 1000) + 500;
    setTimeout(callback, delay);
}

async function sendMessage(message) {
    try {
        showTypingIndicator();

        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (data.status === 'success') {
            simulateTyping(() => {
                hideTypingIndicator();
                addMessage(data.response, 'assistant');
            });
        } else {
            simulateTyping(() => {
                hideTypingIndicator();
                addMessage('Sorry, I encountered an error. Please try again.', 'system');
            });
        }
    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again.', 'system');
    }
}

// Add click event handlers to suggested questions
function addSuggestedQuestion(question) {
    const questionEl = document.createElement('button');
    questionEl.className = 'suggested-question btn btn-sm btn-outline-primary mb-1 me-1';
    questionEl.textContent = question;
    questionEl.addEventListener('click', () => {
        userInput.value = question;
        chatForm.dispatchEvent(new Event('submit'));
    });
    return questionEl;
}

function displaySuggestedQuestions() {
    const suggestionsContainer = document.getElementById('suggested-questions');
    suggestionsContainer.innerHTML = '';

    // Get 3 random questions
    const randomQuestions = [...suggestedQuestions]
        .sort(() => 0.5 - Math.random())
        .slice(0, 3);

    randomQuestions.forEach(question => {
        suggestionsContainer.appendChild(addSuggestedQuestion(question));
    });
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, 'user');
        userInput.value = '';
        await sendMessage(message);
    }
});

// Enable sending message with Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// Initialize with suggested questions
window.addEventListener('load', () => {
    displaySuggestedQuestions();
});