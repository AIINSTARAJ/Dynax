document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const newChatBtn = document.getElementById('new-chat-btn');
    const deleteChatBtn = document.getElementById('delete-chat-btn');
    const chatHistoryContainer = document.getElementById('chat-history-container');
    const chatLogo = document.getElementById('chat-logo');
    const chatTitle = document.getElementById('chat-title');

    // Initialize GSAP animations
    gsap.registerPlugin(ScrollTrigger);
    
    // Initialize chat history from localStorage
    let chatHistory = JSON.parse(localStorage.getItem('dynaxChatHistory')) || [];
    let currentChatId = localStorage.getItem('currentChatId');
    
    // Generate a unique ID for chats
    function generateChatId() {
        return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    // Initialize with a chat if none exists
    if (chatHistory.length === 0) {
        createNewChat();
    } else {
        renderChatHistory();
        loadCurrentChat();
    }
    
    // Animate the logo on load
    gsap.from(chatLogo, { 
        duration: 1, 
        rotation: 360, 
        ease: "elastic.out(1, 0.3)",
        onComplete: () => {
            // Add subtle continuous animation
            gsap.to(chatLogo, {
                rotation: 10,
                duration: 2,
                ease: "sine.inOut",
                repeat: -1,
                yoyo: true
            });
        }
    });

    // Function to create a new chat
    function createNewChat() {
        const chatId = generateChatId();
        const timestamp = new Date();
        const newChat = {
            id: chatId,
            title: 'Research',
            timestamp: timestamp.toISOString(),
            messages: [{
                type: 'bot',
                content: "Hello! I'm Dynax, your AI assistant. How can I help you today?",
                timestamp: timestamp.toISOString()
            }]
        };
        
        chatHistory.unshift(newChat);
        currentChatId = chatId;
        
        // Save to localStorage
        saveChatsToStorage();
        
        // Update UI
        renderChatHistory();
        loadChat(newChat);
        
        // Animate the new chat button
        gsap.from(newChatBtn, {
            scale: 1.2,
            duration: 0.5,
            ease: "back.out(1.7)"
        });
    }
    
    // Function to render chat history sidebar
    function renderChatHistory() {
        chatHistoryContainer.innerHTML = '';
        
        if (chatHistory.length === 0) {
            const emptyState = document.createElement('div');
            emptyState.className = 'empty-state';
            emptyState.innerHTML = `
                <i class="fas fa-comments"></i>
                <h3>No Conversations</h3>
                <p>Start a new chat to begin</p>
            `;
            chatHistoryContainer.appendChild(emptyState);
            return;
        }
        
        chatHistory.forEach(chat => {
            const historyItem = document.createElement('div');
            historyItem.className = `chat-history-item ${chat.id === currentChatId ? 'active' : ''}`;
            historyItem.dataset.chatId = chat.id;
            
            const date = new Date(chat.timestamp);
            const formattedDate = date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
            
            historyItem.innerHTML = `
                <i class="fas fa-comment-dots history-icon"></i>
                <div class="history-text">${chat.title}</div>
                <div class="delete-history" data-chat-id="${chat.id}">
                    <i class="fas fa-times"></i>
                </div>
            `;
            
            historyItem.addEventListener('click', (e) => {
                if (!e.target.closest('.delete-history')) {
                    loadChatById(chat.id);
                }
            });
            
            chatHistoryContainer.appendChild(historyItem);
        });
        
        // Add event listeners to delete icons
        document.querySelectorAll('.delete-history').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const chatId = btn.dataset.chatId;
                deleteChat(chatId);
            });
        });
        
        // Animate history items
        gsap.from('.chat-history-item', {
            y: 20,
            opacity: 0,
            duration: 0.4,
            stagger: 0.1,
            ease: "power2.out"
        });
    }
    
    // Function to load a chat by ID
    function loadChatById(chatId) {
        const chat = chatHistory.find(c => c.id === chatId);
        if (chat) {
            currentChatId = chatId;
            localStorage.setItem('currentChatId', currentChatId);
            loadChat(chat);
            
            // Update active class
            document.querySelectorAll('.chat-history-item').forEach(item => {
                item.classList.toggle('active', item.dataset.chatId === chatId);
            });
        }
    }
    
    // Function to load the current chat
    function loadCurrentChat() {
        if (currentChatId) {
            const chat = chatHistory.find(c => c.id === currentChatId);
            if (chat) {
                loadChat(chat);
                return;
            }
        }
        
        // If no current chat or it doesn't exist, load the first one
        if (chatHistory.length > 0) {
            loadChat(chatHistory[0]);
            currentChatId = chatHistory[0].id;
            localStorage.setItem('currentChatId', currentChatId);
        }
    }
    
    // Function to load a chat into the UI
    function loadChat(chat) {
        chatMessages.innerHTML = '';
        chatTitle.textContent = chat.title;
        
        // Add chat messages
        chat.messages.forEach((msg, index) => {
            const isIntro = index === 0 && msg.type === 'bot';
            addMessageToUI(msg.content, msg.type === 'user', isIntro, false);
        });
        
        // Scroll to bottom
    }
    
    // Function to delete a chat
    function deleteChat(chatId) {
        // Create a fade-out animation for the item being deleted
        const item = document.querySelector(`.chat-history-item[data-chat-id="${chatId}"]`);
        
        gsap.to(item, {
            opacity: 0,
            x: -30,
            duration: 0.3,
            onComplete: () => {
                // Remove from array
                chatHistory = chatHistory.filter(chat => chat.id !== chatId);
                
                // If we're deleting the current chat, select another one
                if (chatId === currentChatId) {
                    if (chatHistory.length > 0) {
                        currentChatId = chatHistory[0].id;
                        localStorage.setItem('currentChatId', currentChatId);
                        loadChat(chatHistory[0]);
                    } else {
                        // No chats left, create a new one
                        createNewChat();
                    }
                }
                
                // Save and rerender
                saveChatsToStorage();
                renderChatHistory();
            }
        });
    }
    
    // Function to save chats to localStorage
    function saveChatsToStorage() {
        localStorage.setItem('dynaxChatHistory', JSON.stringify(chatHistory));
        localStorage.setItem('currentChatId', currentChatId);
    }
    
    // Function to add a message to the UI
    function addMessageToUI(content, isUser = false, isIntro = false, animate = true) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        
        if (isIntro) {
            messageDiv.classList.add('intro-message');
        }
        
        if (animate) {
            messageDiv.classList.add('message-new');
        }
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerHTML = content;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        
        return messageDiv;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'message-new');
        typingDiv.id = 'typing-indicator';
        
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('typing-dot');
            typingIndicator.appendChild(dot);
        }
        
        typingDiv.appendChild(typingIndicator);
        chatMessages.appendChild(typingDiv);
        

    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Function to scroll chat to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to get bot response (with actual API call)
    async function getBotResponse(message) {
        try {
            const res = await fetch('/bot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ msg: message }),
            });
        
            if (!res.ok) {
                throw new Error(`HTTP error! Status: ${res.status}`);
            }
        
            const data = await res.json();
            return data.response;
        } catch (error) {
            console.error("Error getting bot response:", error);
            return "Sorry, I encountered an error processing your request. Please try again later.";
        }
    }
    
    // Function to update chat title based on first user message
    function updateChatTitle(message) {
        const currentChat = chatHistory.find(c => c.id === currentChatId);
        if (currentChat && currentChat.title === 'Research') {
            // Use first 20 chars of first user message as title
            const title = message.length > 20 ? message.substring(0, 20) + '...' : message;
            currentChat.title = title;
            chatTitle.textContent = title;
            saveChatsToStorage();
            renderChatHistory();
        }
    }
    
    // Function to handle sending a message
    async function sendMessage() {
        const message = messageInput.value.trim();
        
        if (message === '') return;
        
        // Add user message to UI
        addMessageToUI(message, true);
        
        // Add user message to chat history
        const currentChat = chatHistory.find(c => c.id === currentChatId);
        if (currentChat) {
            currentChat.messages.push({
                type: 'user',
                content: message,
                timestamp: new Date().toISOString()
            });
            
            // Update chat title if first user message
            if (currentChat.messages.filter(m => m.type === 'user').length === 1) {
                updateChatTitle(message);
            }
            
            saveChatsToStorage();
        }
        
        // Clear input
        messageInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Get bot response
            const content = await getBotResponse(message);
            
            // Sanitize the content to ensure no harmful code
            const cleanRes = DOMPurify.sanitize(content);
            
            // Decode HTML entities to allow rendering of tags
            const decodedContent = decodeHtmlEntities(cleanRes);
            
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add bot message div to the chat
            const botMessageDiv = addMessageToUI('', false);
            
            // Add to chat history
            if (currentChat) {
                currentChat.messages.push({
                    type: 'bot',
                    content: decodedContent,
                    timestamp: new Date().toISOString()
                });
                
                saveChatsToStorage();
            }
            
            // Typewriter effect
            const messageContent = botMessageDiv.querySelector('.message-content');
            let i = 0;
            let typedContent = '';
    
            let typingInterval = setInterval(() => {
                if (i < decodedContent.length) {
                    typedContent += decodedContent.charAt(i);
                    messageContent.innerHTML = typedContent;
                    i++;
                } else {
                    clearInterval(typingInterval);
                }
            }, 10);
        } catch (error) {
            // Handle error
            removeTypingIndicator();
            addMessageToUI("Sorry, I encountered an error processing your request. Please try again.", false);
            console.error("Error in chat flow:", error);
        }
    }
    
    // Decode HTML entities back to proper HTML
    function decodeHtmlEntities(text) {
        const textArea = document.createElement('textarea');
        textArea.innerHTML = text;
        return textArea.value;
    }
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    newChatBtn.addEventListener('click', createNewChat);
    
    deleteChatBtn.addEventListener('click', () => {
        if (currentChatId) {
            // Confirm delete
            if (confirm('Are you sure you want to delete this chat?')) {
                deleteChat(currentChatId);
            }
        }
    });
    
    chatLogo.addEventListener('click', () => {
        // Easter egg: clicking the logo pulses the logo
        gsap.to(chatLogo, {
            scale: 1.2,
            duration: 0.3,
            ease: "back.out(2)",
            yoyo: true,
            repeat: 1
        });
    });
    
    // Focus input on page load
    messageInput.focus();
    
    // Initialize with focus indicator
    messageInput.addEventListener('focus', () => {
        messageInput.style.borderColor = '#5229e9';
        messageInput.style.boxShadow = '0 0 0 2px rgba(82, 41, 233, 0.2), 0 4px 12px rgba(0, 0, 0, 0.1)';
    });
    
    messageInput.addEventListener('blur', () => {
        messageInput.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        messageInput.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
    });
    
    // Window resize handler for mobile responsiveness
    window.addEventListener('resize', () => {
        // Adjust UI for mobile if needed
        const isMobile = window.innerWidth <= 768;
        if (isMobile) {
            // Mobile-specific adjustments can go here
        }
    });
    
    // Add smooth animations on scroll
    gsap.utils.toArray('.message').forEach(message => {
        ScrollTrigger.create({
            trigger: message,
            start: 'top bottom-=100',
            onEnter: () => {
                gsap.to(message, {
                    y: 0,
                    opacity: 1,
                    duration: 0.4,
                    ease: 'power2.out'
                });
            }
        });
    });
    
    // Animate floating shapes for extra coolness
    gsap.to('.shape-1', {
        x: '+=30',
        y: '+=20',
        rotation: 15,
        duration: 10,
        ease: 'sine.inOut',
        repeat: -1,
        yoyo: true
    });
    
    gsap.to('.shape-2', {
        x: '-=20',
        y: '-=30',
        rotation: -10,
        duration: 8,
        ease: 'sine.inOut',
        repeat: -1,
        yoyo: true
    });
    
    gsap.to('.shape-5', {
        x: '+=40',
        y: '-=20',
        rotation: 20,
        duration: 12,
        ease: 'sine.inOut',
        repeat: -1,
        yoyo: true
    });
    
    gsap.to('.shape-6', {
        x: '-=30',
        y: '+=40',
        rotation: -15,
        duration: 15,
        ease: 'sine.inOut',
        repeat: -1,
        yoyo: true
    });
});