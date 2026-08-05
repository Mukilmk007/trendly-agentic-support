document.addEventListener("DOMContentLoaded", () => {

    lucide.createIcons();

    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-btn");
    let pendingAction = null;

    function addMessage(message, sender) {

        const row = document.createElement("div");
        row.classList.add("message-row", sender);

        const bubble = document.createElement("div");
        bubble.classList.add(
            "message",
            sender === "user"
                ? "user-message"
                : "bot-message"
        );

        bubble.textContent = message;

        row.appendChild(bubble);
        chatBox.appendChild(row);

        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {

        const row = document.createElement("div");

        row.className = "message-row bot";
        row.id = "typing-indicator";

        const bubble = document.createElement("div");

        bubble.className = "typing";

        bubble.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;

        row.appendChild(bubble);

        chatBox.appendChild(row);

        chatBox.scrollTop = chatBox.scrollHeight;
    }
    function hideTypingIndicator() {

        const typing = document.getElementById("typing-indicator");

        if (typing) {
            typing.remove();
        }

    }

    async function sendMessage() {

            let userMessage = messageInput.value.trim();

            if (!userMessage) return;

            let message = userMessage;

            if (pendingAction) {

                switch (pendingAction) {

                    case "track":

                        message = `Where is my order ${userMessage}?`;

                        break;

                    case "return":

                        message = `Can I return order ${userMessage}?`;

                        break;

                    case "exchange":

                        message = `Can I exchange order ${userMessage}?`;

                        break;
                }

                pendingAction = null;
            }

            // Show exactly what the user typed
            addMessage(userMessage, "user");

            messageInput.value = "";

            showTypingIndicator();

            messageInput.disabled = true;
            sendButton.disabled = true;

            try {

                const response = await fetch("/chat", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })

                });

                const data = await response.json();

                hideTypingIndicator();

                addMessage(
                    data.response,
                    "bot"
                );

            }

            catch (error) {

                hideTypingIndicator();

                addMessage(
                    "Sorry, something went wrong.",
                    "bot"
                );

                console.error(error);

            }

            finally {

                messageInput.disabled = false;
                sendButton.disabled = false;

                messageInput.focus();

            }

        }

    sendButton.addEventListener(
        "click",
        sendMessage
    );
    const resetButton = document.getElementById("reset-btn");

    resetButton.addEventListener(
        "click",
        resetConversation
    );
    

    messageInput.addEventListener(
        "keydown",
        (event) => {

            if (event.key === "Enter") {

                sendMessage();

            }

        }
    );

    addMessage(
        "👋 Hi! I'm Nova. How can I help you today?",
        "bot"
    );
    showQuickActions();
    async function resetConversation() {

    try {

        await fetch("/reset", {

            method: "POST"

        });

    } catch (error) {

        console.error(error);

    }

    chatBox.innerHTML = "";

    addMessage(
            "👋 Hi! I'm Nova. How can I help you today?",
            "bot"
        );
        showQuickActions();
        messageInput.value = "";

        messageInput.focus();

    }
    function showQuickActions() {

            const row = document.createElement("div");

            row.className = "message-row bot";

            row.innerHTML = `
                <div class="quick-actions">

                    <button class="quick-btn" data-action="track">
                        Track Order
                    </button>

                    <button class="quick-btn" data-action="return">
                        Return Item
                    </button>

                    <button class="quick-btn" data-action="exchange">
                        Exchange Item
                    </button>

                    <button class="quick-btn" data-action="refund">
                        Refund Policy
                    </button>

                    <button class="quick-btn" data-action="human">
                        Talk to Human
                    </button>

                </div>
            `;

            chatBox.appendChild(row);

            attachQuickButtonEvents();

            chatBox.scrollTop = chatBox.scrollHeight;
        }
        function attachQuickButtonEvents() {

        document.querySelectorAll(".quick-btn").forEach(button => {

           button.onclick = () => {

                const quickActions = document.querySelector(".quick-actions");

                        if (quickActions) {
                            quickActions.parentElement.remove();
                        }

                        const action = button.dataset.action;

                switch (action) {

                    case "track":

                        pendingAction = "track";

                        addMessage(
                            "Sure! Please enter your Order ID.",
                            "bot"
                        );

                        messageInput.placeholder = "Enter your Order ID...";

                        messageInput.focus();

                        break;

                    case "return":

                        pendingAction = "return";

                        addMessage(
                            "Sure! Please enter your Order ID so I can check whether it's eligible for return.",
                            "bot"
                        );

                        messageInput.placeholder = "Enter your Order ID...";

                        messageInput.focus();

                        break;

                    case "exchange":

                        pendingAction = "exchange";

                        addMessage(
                            "Sure! Please enter your Order ID so I can check whether it's eligible for exchange.",
                            "bot"
                        );

                        messageInput.placeholder = "Enter your Order ID...";

                        messageInput.focus();

                        break;

                    case "refund":

                        messageInput.value = "What is your refund policy?";

                        sendMessage();

                        break;

                    case "human":

                        messageInput.value = "I want to talk to a human.";

                        sendMessage();

                        break;
                }

            };

        });

    }

});