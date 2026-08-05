document.addEventListener("DOMContentLoaded", () => {

    lucide.createIcons();

    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-btn");

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

        const message = messageInput.value.trim();

        if (!message) return;

        addMessage(message, "user");

        messageInput.value = "";

        showTypingIndicator();

        messageInput.disabled = true;
        sendButton.disabled = true;

        try {

            console.log("Sending request...");

            const response = await fetch("/chat", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })

            });

            console.log("Fetch completed");

            const data = await response.json();

            console.log("JSON parsed");

            console.log(data);

            hideTypingIndicator();

            addMessage(
                data.response,
                "bot"
            );

            console.log("Bot message added");

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

        messageInput.value = "";

        messageInput.focus();

    }
    

});