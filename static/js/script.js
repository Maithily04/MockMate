// ==========================================================================
// DYNAMIC CHEATSHEET RENDERER
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
    const gridContainer = document.getElementById("cheatsheet-content");
    if (!gridContainer) return;

    // 1. Automatically detect the current subject from the URL parameter
    // Example URL: yourpage.html?subject=python or yourpage.html?subject=html
    const urlParams = new URLSearchParams(window.location.search);
    const subject = urlParams.get('subject') || 'python'; // Fallback to python if none specified

    // 2. Set headers and metadata titles dynamically
    updateDynamicHeaders(subject);

    // 3. Fetch the respective JSON data file from your 'data' folder
    // Note: Adjust the fetch path relative to where your HTML templates are served!
    fetch(`/data/${subject}_cheatsheet.json`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Could not load data for subject: ${subject}`);
            }
            return response.json();
        })
        .then(data => {
            renderCheatsheetCards(data, gridContainer);
        })
        .catch(error => {
            console.error("Error loading cheatsheet:", error);
            gridContainer.innerHTML = `<p class="error-msg">Failed to load ${subject.toUpperCase()} cheatsheet content.</p>`;
        });
});

// Helper function to update page titles based on selected subject
function updateDynamicHeaders(subject) {
    const titleElement = document.querySelector(".header-title-block h1");
    if (titleElement) {
        titleElement.innerText = `${subject.toUpperCase()} CHEAT SHEET`;
    }
}

// Helper function to build and render the cards
function renderCheatsheetCards(data, container) {
    container.innerHTML = ""; // Clear existing fallback content

    data.forEach((item, index) => {
        // Cycles color banners dynamically (theme-0 to theme-3)
        const themeIndex = index % 4; 
        
        const cardElement = document.createElement("div");
        cardElement.className = `cheatsheet-card theme-${themeIndex}`;
        
        // Handle fields safely whether they use "example" or standard definitions
        const codeBlock = item.example ? `<pre class="card-example"><code>${escapeHTML(item.example)}</code></pre>` : '';

        cardElement.innerHTML = `
            <div class="card-header">${item.id}. ${item.title.toUpperCase()}</div>
            <div class="card-body">
                <p class="card-definition">${item.definition || ''}</p>
                ${codeBlock}
            </div>
        `;
        
        container.appendChild(cardElement);
    });
}

// Safeguard layout formatting against HTML breaking elements
function escapeHTML(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}