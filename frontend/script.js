const questionInput =
    document.getElementById("question");

const sendButton =
    document.getElementById("sendButton");

const messages =
    document.getElementById("messages");


function addMessage(text, type) {

    const message =
        document.createElement("div");

    message.className =
        `message ${type}`;

    message.textContent = text;

    messages.appendChild(message);

    messages.scrollTop =
        messages.scrollHeight;
}


async function sendQuestion() {

    const question =
        questionInput.value.trim();

    if (!question) {
        return;
    }


    addMessage(question, "user");

    questionInput.value = "";


    addMessage("Thinking...", "bot");


    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        const data =
            await response.json();


        const botMessages =
            document.querySelectorAll(
                ".message.bot"
            );


        botMessages[
            botMessages.length - 1
        ].textContent =
            data.answer;


    } catch (error) {

        console.error(error);

        addMessage(
            "Something went wrong.",
            "bot"
        );
    }
}


sendButton.addEventListener(
    "click",
    sendQuestion
);


questionInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendQuestion();

        }

    }
);