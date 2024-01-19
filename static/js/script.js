const chatbox = document.getElementById('chatbox');
const history = [];

function addUserMessage(question) {
    history.push({ role: 'User', content: question });
    renderMessages();
}

function addAssistantMessage(answer) {
    history.push({ role: 'Assistant', content: answer });
    renderMessages();
}

function renderMessages() {
    chatbox.innerHTML = '';
    history.forEach((message) => {
        const messageElement = document.createElement('p');
        messageElement.innerHTML = `<strong>${message.role}:</strong> ${message.content}`;
        chatbox.appendChild(messageElement);
    });
}

