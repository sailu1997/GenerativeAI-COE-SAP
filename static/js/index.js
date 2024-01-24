document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    const storedMessages = JSON.parse(localStorage.getItem('chatHistory')) || [];
    storedMessages.forEach(message => displayMessage(message.text, message.sender));

    sendBtn.addEventListener('click', function() {
        event.preventDefault();
        const message = userInput.value;
        userInput.value = '';

        //chartMessages.innerHTML += `<li>You: ${message}</li>`;
        displayMessage(message, 'You');
        saveMessage(message, 'You');

        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            //chartMessages.innerHTML += `<li>AI: ${data.answer}</li>`;
            displayMessage(data.answer, 'Niha');
            saveMessage(data.answer, 'Niha');

        })
        .catch(error => {
            console.log(error);
            displayMessage('Sorry, something went wrong', 'AI');
    });
});

function displayMessage(message, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    
    const messageElement = document.createElement('li');
    messageElement.textContent = `${sender}: ${message}`;
    //chatMessages.appendChild(messageElement);
    //chatMessages.scrollTop = chatMessages.scrollHeight;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function saveMessage(text,sender){
    const message = {text, sender};
    const chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    chatHistory.push(message);
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}
});
