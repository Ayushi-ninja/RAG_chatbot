const API_URL =
    "http://127.0.0.1:8000";


// ============================================================
// ELEMENTS
// ============================================================

const fileInput =
    document.getElementById("fileInput");

const uploadButton =
    document.getElementById("uploadButton");

const uploadStatus =
    document.getElementById("uploadStatus");

const documentList =
    document.getElementById("documentList");

const documentSelect =
    document.getElementById("documentSelect");

const selectedDocumentText =
    document.getElementById(
        "selectedDocumentText"
    );

const messages =
    document.getElementById("messages");

const questionInput =
    document.getElementById("question");

const sendButton =
    document.getElementById("sendButton");


// ============================================================
// APPLICATION STATE
// ============================================================

let documents = [];

let selectedDocumentId = null;


// ============================================================
// LOAD DOCUMENTS
// ============================================================

async function loadDocuments() {

    try {

        const response =
            await fetch(
                `${API_URL}/documents`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load documents."
            );

        }


        const data =
            await response.json();


        documents =
            data.documents || [];


        renderDocuments();

        renderDocumentSelect();


    } catch (error) {

        console.error(error);

        documentList.innerHTML = `
            <div class="loading">
                Failed to load documents.
            </div>
        `;

    }

}


// ============================================================
// RENDER DOCUMENT SIDEBAR
// ============================================================

function renderDocuments() {

    if (documents.length === 0) {

        documentList.innerHTML = `
            <div class="loading">
                No documents uploaded yet.
            </div>
        `;

        return;
    }


    documentList.innerHTML = "";


    documents.forEach(
        function(doc) {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "document-item";


            if (
                doc.document_id ===
                selectedDocumentId
            ) {

                item.classList.add(
                    "selected"
                );

            }


            item.innerHTML = `

                <div class="document-name">
                    📄 ${escapeHtml(
                        doc.source
                    )}
                </div>

                <div class="document-pages">
                    ${doc.pages} page(s)
                </div>

                <div class="document-actions">

                    <button
                        class="select-document-button"
                    >
                        Select
                    </button>

                    <button
                        class="delete-document-button"
                    >
                        Delete
                    </button>

                </div>

            `;


            const selectButton =
                item.querySelector(
                    ".select-document-button"
                );


            const deleteButton =
                item.querySelector(
                    ".delete-document-button"
                );


            selectButton.addEventListener(
                "click",
                function() {

                    selectDocument(
                        doc.document_id
                    );

                }
            );


            deleteButton.addEventListener(
                "click",
                function() {

                    deleteDocument(
                        doc.document_id,
                        doc.source
                    );

                }
            );


            documentList.appendChild(
                item
            );

        }
    );

}


// ============================================================
// RENDER DOCUMENT SELECT
// ============================================================

function renderDocumentSelect() {

    documentSelect.innerHTML = `
        <option value="">
            All documents
        </option>
    `;


    documents.forEach(
        function(doc) {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                doc.document_id;


            option.textContent =
                doc.source;


            documentSelect.appendChild(
                option
            );

        }
    );


    documentSelect.value =
        selectedDocumentId || "";

}


// ============================================================
// SELECT DOCUMENT
// ============================================================

function selectDocument(
    documentId
) {

    selectedDocumentId =
        documentId;


    documentSelect.value =
        documentId;


    const document =
        documents.find(
            function(item) {

                return (
                    item.document_id ===
                    documentId
                );

            }
        );


    if (document) {

        selectedDocumentText.textContent =
            `Searching ${document.source}`;

    }


    renderDocuments();

}


// ============================================================
// SELECT FROM DROPDOWN
// ============================================================

documentSelect.addEventListener(
    "change",
    function() {

        selectedDocumentId =
            documentSelect.value ||
            null;


        if (selectedDocumentId) {

            const document =
                documents.find(
                    function(item) {

                        return (
                            item.document_id ===
                            selectedDocumentId
                        );

                    }
                );


            if (document) {

                selectedDocumentText.textContent =
                    `Searching ${document.source}`;

            }

        } else {

            selectedDocumentText.textContent =
                "Searching all documents";

        }


        renderDocuments();

    }
);


// ============================================================
// UPLOAD BUTTON
// ============================================================

uploadButton.addEventListener(
    "click",
    function() {

        fileInput.click();

    }
);


// ============================================================
// FILE SELECTION
// ============================================================

fileInput.addEventListener(
    "change",
    async function() {

        const file =
            fileInput.files[0];


        if (!file) {

            return;

        }


        await uploadDocument(
            file
        );

    }
);


// ============================================================
// UPLOAD DOCUMENT
// ============================================================

async function uploadDocument(
    file
) {

    if (
        !file.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {

        uploadStatus.textContent =
            "Please select a PDF file.";

        return;

    }


    uploadButton.disabled =
        true;


    uploadStatus.textContent =
        "Uploading and processing...";


    const formData =
        new FormData();


    formData.append(
        "file",
        file
    );


    try {

        const response =
            await fetch(
                `${API_URL}/upload`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Upload failed."
            );

        }


        uploadStatus.textContent =
            `✓ ${data.filename} uploaded`;


        fileInput.value = "";


        await loadDocuments();


        // Automatically select the new document

        if (data.document_id) {

            selectDocument(
                data.document_id
            );

        }


    } catch (error) {

        console.error(error);

        uploadStatus.textContent =
            `❌ ${error.message}`;

    }


    uploadButton.disabled =
        false;

}


// ============================================================
// DELETE DOCUMENT
// ============================================================

async function deleteDocument(
    documentId,
    filename
) {

    const confirmed =
        confirm(
            `Delete "${filename}"?`
        );


    if (!confirmed) {

        return;

    }


    try {

        const response =
            await fetch(
                `${API_URL}/documents/${documentId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Delete failed."
            );

        }


        // If deleted document was selected

        if (
            selectedDocumentId ===
            documentId
        ) {

            selectedDocumentId =
                null;

        }


        await loadDocuments();


        selectedDocumentText.textContent =
            selectedDocumentId
                ? selectedDocumentText.textContent
                : "Searching all documents";


    } catch (error) {

        console.error(error);

        alert(
            `Failed to delete document: ${
                error.message
            }`
        );

    }

}


// ============================================================
// SEND QUESTION
// ============================================================

async function sendQuestion() {

    const question =
        questionInput.value.trim();


    if (!question) {

        return;

    }


    addMessage(
        question,
        "user"
    );


    questionInput.value = "";


    sendButton.disabled =
        true;


    const thinkingMessage =
        addMessage(
            "Thinking...",
            "bot"
        );


    try {

        const response =
            await fetch(
                `${API_URL}/chat`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question:
                            question,

                        document_id:
                            selectedDocumentId

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to get answer."
            );

        }


        thinkingMessage
            .querySelector(
                ".message-content"
            )
            .remove();


        const content =
            document.createElement(
                "div"
            );


        content.className =
            "message-content";


        content.textContent =
            data.answer ||
            "No answer was generated.";


        thinkingMessage.appendChild(
            content
        );


        // Add sources

        if (
            data.sources &&
            data.sources.length > 0
        ) {

            addSources(
                thinkingMessage,
                data.sources
            );

        }


    } catch (error) {

        console.error(error);


        thinkingMessage
            .querySelector(
                ".message-content"
            )
            .textContent =
            `❌ ${error.message}`;

    }


    sendButton.disabled =
        false;


    questionInput.focus();

}


// ============================================================
// ADD MESSAGE
// ============================================================

function addMessage(
    text,
    type
) {

    const message =
        document.createElement(
            "div"
        );


    message.className =
        `message ${type}`;


    const content =
        document.createElement(
            "div"
        );


    content.className =
        "message-content";


    content.textContent =
        text;


    message.appendChild(
        content
    );


    messages.appendChild(
        message
    );


    messages.scrollTop =
        messages.scrollHeight;


    return message;

}


// ============================================================
// ADD SOURCES
// ============================================================

function addSources(
    message,
    sources
) {

    const sourceContainer =
        document.createElement(
            "div"
        );


    sourceContainer.className =
        "sources";


    const title =
        document.createElement(
            "div"
        );


    title.className =
        "sources-title";


    title.textContent =
        "📚 Sources";


    sourceContainer.appendChild(
        title
    );


    sources.forEach(
        function(source) {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "source-item";


            item.textContent =
                `📄 ${source.source} — Page ${source.page}`;


            sourceContainer.appendChild(
                item
            );

        }
    );


    message.appendChild(
        sourceContainer
    );


    messages.scrollTop =
        messages.scrollHeight;

}


// ============================================================
// ENTER KEY
// ============================================================

questionInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendQuestion();

        }

    }
);


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHtml(
    value
) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        value;


    return div.innerHTML;

}


// ============================================================
// INITIALIZE
// ============================================================

loadDocuments();