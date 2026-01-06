// Leave empty to use the same server as the frontend (Fixes CORS/Port issues)
const API_URL = ""; 

// --- 1. LOGIN FUNCTION (New) ---
async function handleLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const status = document.getElementById("login-status");

    if (!username || !password) {
        status.innerText = "❌ Please enter Username and Password";
        status.style.color = "red";
        return;
    }

    status.innerText = "Logging in...";
    status.style.color = "blue";

    // FastAPI Login requires "Form Data", not JSON
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/auth/token`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        if (response.ok) {
            status.innerText = "✅ Success!";
            // Hide Login Screen, Show Chat Screen
            document.getElementById("login-section").style.display = "none";
            document.getElementById("chat-section").style.display = "flex";
        } else {
            status.innerText = "❌ Login Failed. Check credentials.";
            status.style.color = "red";
        }
    } catch (error) {
        console.error(error);
        status.innerText = "❌ Server Error";
        status.style.color = "red";
    }
}

// --- 2. SIGNUP FUNCTION (Updated) ---
async function handleSignup() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const status = document.getElementById("login-status");

    // Basic validation
    if (!username || !email || !password) {
        status.innerText = "❌ All fields required for Signup";
        status.style.color = "red";
        return;
    }

    status.innerText = "Creating account...";
    status.style.color = "blue";

    try {
        const response = await fetch(`${API_URL}/auth/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });

        if (response.ok) {
            // Success! Ask user to login now.
            status.innerText = "✅ Account Created! Please click Login.";
            status.style.color = "green";
        } else {
            const data = await response.json();
            status.innerText = "❌ Error: " + (data.detail || "Signup failed");
            status.style.color = "red";
        }
    } catch (error) {
        status.innerText = "❌ Connection Error";
        status.style.color = "red";
    }
}

// --- 3. UPLOAD FUNCTION ---
async function handleUpload() {
    const fileInput = document.getElementById("pdf-upload");
    const status = document.getElementById("upload-status");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a PDF file first.");
        return;
    }

    status.innerText = "⏳ Reading file...";
    status.style.color = "blue";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_URL}/chat/upload`, {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            status.innerText = "✅ Learned!";
            status.style.color = "green";
            addMessage("I have read the document. Ask me anything!", "bot-message");
        } else {
            status.innerText = "❌ Error uploading";
            status.style.color = "red";
        }
    } catch (error) {
        status.innerText = "❌ Failed";
        console.error(error);
    }
}

// --- 4. CHAT FUNCTIONS ---
async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value;
    if (!message) return;

    // Add User Message
    addMessage(message, "user-message");
    inputField.value = "";
    
    // Add Loading Indicator
    const loadingId = "loading-" + Date.now();
    addMessage("Thinking...", "bot-message", loadingId);

    try {
        const response = await fetch(`${API_URL}/chat/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: message })
        });

        const data = await response.json();
        
        // Remove Loading, Add Answer
        const loadingElement = document.getElementById(loadingId);
        if(loadingElement) loadingElement.remove();
        
        addMessage(data.answer, "bot-message");

    } catch (error) {
        const loadingElement = document.getElementById(loadingId);
        if(loadingElement) loadingElement.remove();
        addMessage("Error: Could not reach the brain.", "bot-message");
    }
}

function addMessage(text, className, id=null) {
    const div = document.createElement("div");
    div.className = `message ${className}`;
    div.innerText = text;
    if(id) div.id = id;
    const history = document.getElementById("chat-history");
    history.appendChild(div);
    history.scrollTop = history.scrollHeight;
}

function logout() {
    location.reload();
}