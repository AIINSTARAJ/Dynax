document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const startChatBtn = document.getElementById('start-chat-btn');
    const introPage = document.getElementById('intro-page');
    const chatPage = document.getElementById('chat-page');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button') || document.getElementById('send-btn');
    const newChatBtn = document.getElementById('new-chat-btn');
    const deleteChatBtn = document.getElementById('delete-chat-btn');
    const chatHistoryContainer = document.getElementById('chat-history');
    const chatLogo = document.getElementById('chat-logo');
    const chatTitle = document.getElementById('chat-title');


    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
    }

    if (!chatMessages || !messageInput || !sendButton) {
        console.error('Required chat elements not found');
        return;
    }

    if (startChatBtn && introPage && chatPage) {
        startChatBtn.addEventListener('click', () => {
            introPage.style.display = 'none';
            chatPage.style.display = 'block';
            messageInput.focus();
        });
    }


    if (typeof gsap !== 'undefined' && gsap.registerPlugin) {
        gsap.registerPlugin(ScrollTrigger);
        initAnimations();
    }

    // Chat data
    let chatHistory = [];
    let currentChatId = null;
    let isTyping = false;


    try {
        const savedHistory = localStorage.getItem('dynaxChatHistory');
        const savedCurrentId = localStorage.getItem('currentChatId');
        
        if (savedHistory) {
            chatHistory = JSON.parse(savedHistory);
        }
        if (savedCurrentId) {
            currentChatId = savedCurrentId;
        }
    } catch (error) {
        console.warn('localStorage not available, using memory storage');
    }


    function generateChatId() {
        return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Save chats to storage
    function saveChatsToStorage() {
        try {
            localStorage.setItem('dynaxChatHistory', JSON.stringify(chatHistory));
            localStorage.setItem('currentChatId', currentChatId);
        } catch (error) {
            console.warn('Could not save to localStorage');
        }
    }

    function createNewChat() {
        const chatId = generateChatId();
        const timestamp = new Date().toISOString();
        
        const newChat = {
            id: chatId,
            title: 'Research',
            timestamp: timestamp,
            messages: [{
                type: 'bot',
                content: "Hello! I'm Dynax, your AI assistant. How can I help you today?",
                timestamp: timestamp
            }]
        };
        
        chatHistory.unshift(newChat);
        currentChatId = chatId;
        
        saveChatsToStorage();
        renderChatHistory();
        loadChat(newChat);
        
        if (typeof gsap !== 'undefined' && newChatBtn) {
            gsap.from(newChatBtn, {
                scale: 1.2,
                duration: 0.5,
                ease: "back.out(1.7)"
            });
        }
    }

    // Render chat history sidebar
    function renderChatHistory() {
        if (!chatHistoryContainer) return;
        
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
        
        document.querySelectorAll('.delete-history').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const chatId = btn.dataset.chatId;
                deleteChat(chatId);
            });
        });

        // Animate if GSAP available
        if (typeof gsap !== 'undefined') {
            gsap.from('.chat-history-item', {
                y: 20,
                opacity: 0,
                duration: 0.4,
                stagger: 0.1,
                ease: "power2.out"
            });
        }
    }

    // Load chat by ID
    function loadChatById(chatId) {
        const chat = chatHistory.find(c => c.id === chatId);
        if (chat) {
            currentChatId = chatId;
            saveChatsToStorage();
            loadChat(chat);
            
            // Update active class
            document.querySelectorAll('.chat-history-item').forEach(item => {
                item.classList.toggle('active', item.dataset.chatId === chatId);
            });
        }

        scrollToBottom()
    }

    // Load chat into UI
    function loadChat(chat) {
        chatMessages.innerHTML = '';
        if (chatTitle) {
            chatTitle.textContent = chat.title;
        }
        
        chat.messages.forEach((msg, index) => {
            const isIntro = index === 0 && msg.type === 'bot';
            addMessageToUI(msg.content, msg.type === 'user', isIntro, false);
        });
        
        scrollToBottom();
    }

    // Delete chat
    function deleteChat(chatId) {
        const item = document.querySelector(`.chat-history-item[data-chat-id="${chatId}"]`);
        
        const deleteAction = () => {
            chatHistory = chatHistory.filter(chat => chat.id !== chatId);
            
            if (chatId === currentChatId) {
                if (chatHistory.length > 0) {
                    currentChatId = chatHistory[0].id;
                    loadChat(chatHistory[0]);
                } else {
                    createNewChat();
                }
            }
            
            saveChatsToStorage();
            renderChatHistory();
        };

        if (typeof gsap !== 'undefined' && item) {
            gsap.to(item, {
                opacity: 0,
                x: -30,
                duration: 0.3,
                onComplete: deleteAction
            });
        } else {
            deleteAction();
        }
    }

    // Add message to UI
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

    // Show typing indicator
    function showTypingIndicator() {
        if (document.getElementById('typing-indicator')) return;
        
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

    // Remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Scroll to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Get bot response
    async function getBotResponse(message) {
        try {
            const response = await fetch('/bot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ msg: message }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            return data.response || data.message || 'No response received';
        } catch (error) {
            console.error('Error getting bot response:', error);
            return "Sorry, I encountered an error processing your request. Please try again later.";
        }
    }

    // Update chat title
    function updateChatTitle(message) {
        const currentChat = chatHistory.find(c => c.id === currentChatId);
        if (currentChat && currentChat.title === 'Research') {
            const title = message.length > 20 ? message.substring(0, 20) + '...' : message;
            currentChat.title = title;
            if (chatTitle) {
                chatTitle.textContent = title;
            }
            saveChatsToStorage();
            renderChatHistory();
        }
    }

    // Decode HTML entities
    function decodeHtmlEntities(text) {
        const textArea = document.createElement('textarea');
        textArea.innerHTML = text;
        return textArea.value;
    }

    // Send message
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message || isTyping) return;

        isTyping = true;
        addMessageToUI(message, true);
        
        // Add to chat history
        const currentChat = chatHistory.find(c => c.id === currentChatId);
        if (currentChat) {
            currentChat.messages.push({
                type: 'user',
                content: message,
                timestamp: new Date().toISOString()
            });
            
            // Update title if first user message
            if (currentChat.messages.filter(m => m.type === 'user').length === 1) {
                updateChatTitle(message);
            }
            
            saveChatsToStorage();
        }
        
        messageInput.value = '';
        showTypingIndicator();
        
        try {
            const botResponse = await getBotResponse(message);
            

            const cleanResponse = typeof DOMPurify !== 'undefined' 
                ? DOMPurify.sanitize(botResponse) 
                : botResponse;
            
            const decodedContent = decodeHtmlEntities(cleanResponse);
            
            removeTypingIndicator();
            
            // Add bot message with typewriter effect
            const botMessageDiv = addMessageToUI('', false);
            const messageContent = botMessageDiv.querySelector('.message-content');
            
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
            let i = 0;
            const typingInterval = setInterval(() => {
                if (i < decodedContent.length) {
                    messageContent.innerHTML = decodedContent.substring(0, i + 1);
                    i++;
                } else {
                    clearInterval(typingInterval);
                    isTyping = false;
                }
            }, 10);

            scrollToBottom()
            
        } catch (error) {
            removeTypingIndicator();
            addMessageToUI("Sorry, I encountered an error. Please try again.", false);
            console.error('Error in chat flow:', error);
            isTyping = false;
        }
    }

    // Initialize animations if GSAP available
    function initAnimations() {
        if (chatLogo) {
            gsap.from(chatLogo, { 
                duration: 1, 
                rotation: 360, 
                ease: "elastic.out(1, 0.3)",
                onComplete: () => {
                    gsap.to(chatLogo, {
                        rotation: 10,
                        duration: 2,
                        ease: "sine.inOut",
                        repeat: -1,
                        yoyo: true
                    });
                }
            });
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    if (newChatBtn) {
        newChatBtn.addEventListener('click', createNewChat);
    }

    if (deleteChatBtn) {
        deleteChatBtn.addEventListener('click', () => {
            if (currentChatId && confirm('Are you sure you want to delete this chat?')) {
                deleteChat(currentChatId);
            }
        });
    }

    if (chatLogo) {
        chatLogo.addEventListener('click', () => {
            if (typeof gsap !== 'undefined') {
                gsap.to(chatLogo, {
                    scale: 1.2,
                    duration: 0.3,
                    ease: "back.out(2)",
                    yoyo: true,
                    repeat: 1
                });
            }
        });
    }

    messageInput.addEventListener('focus', () => {
        messageInput.style.borderColor = '#00bcd4';
        messageInput.style.boxShadow = '0 0 0 2px rgba(0, 188, 212, 0.2), 0 4px 12px rgba(0, 0, 0, 0.1)';
        messageInput.style.borderRadius = '9999px';  
        messageInput.style.height = '48px';
        messageInput.style.padding = '0 16px'
        messageInput.style.lineHeight = '48px';   
    });
    
    messageInput.addEventListener('blur', () => {
        messageInput.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        messageInput.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
    });

    // Initialize chat
    if (chatHistory.length === 0) {
        createNewChat();
    } else {
        renderChatHistory();
        
        const currentChat = chatHistory.find(c => c.id === currentChatId) || chatHistory[0];
        if (currentChat) {
            currentChatId = currentChat.id;
            loadChat(currentChat);
        }
    }

    messageInput.focus();
});