const messageInput = document.getElementById('search-bar');

const searchButton = document.getElementById('search-btn');

searchButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') 
        sendMessage();
    }
);

function sendMessage() {
    const userMessage = messageInput.value.trim();

    if (userMessage === '')
        return;

    displayMessage(userMessage, 'user');

    messageInput.value = '';


    fetch('/scrap', {

        method: 'POST',

        headers: { 'Content-Type': 'application/json' },

        body: JSON.stringify({ message: userMessage, profile: sessionStorage.getItem('name')})
    })
    .then(response => response.json())

    .then(data => {
        displayMessage(data.response, 'bot');
    })

    .catch(() => {
        console.log("Error")
    });
}

function displayMessage(message, type) {

    const messageElement = document.createElement('div');

    messageElement.classList.add('message', type === 'user' ? 'user-message' : 'bot-message');

    messageElement.innerText = message;

    chatMessages.appendChild(messageElement);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}