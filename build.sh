#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies if needed
if [ -f "package.json" ]; then
    npm install
fi

# Build static assets if needed
if [ -d "static" ]; then
    # Add any static asset build commands here
    echo "Building static assets..."
fi

select.form-control {
    height: 48px;
    background-position: right 12px center;
    padding-right: 30px;
    -webkit-appearance: none;
    appearance: none;
} 

.submit-button {
    width: 100%;
    padding: 14px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    margin-top: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.add-entry-button {
    width: 100%;
    padding: 12px;
    margin-top: 10px;
    border: 2px solid #007bff;
    color: #007bff;
    background: white;
    border-radius: 8px;
} 

.form-container {
    width: 100%;
    padding: 16px;
    margin: 0 auto;
}

.form-group {
    margin-bottom: 16px;
}

.form-control {
    width: 100%;
    padding: 12px;
    font-size: 16px; /* Better for mobile touch */
    border-radius: 8px;
    border: 1px solid #ddd;
}

/* Make buttons more tappable */
button {
    min-height: 48px;
    width: 100%;
    margin-top: 8px;
    font-size: 16px;
    border-radius: 8px;
}

/* Larger touch targets for dropdowns */
select {
    height: 48px;
    padding: 0 12px;
}

/* Then add laptop styles with media query */
@media (min-width: 1024px) {
    .form-container {
        max-width: 600px;
        padding: 24px;
    }
} 

.input-with-voice {
    position: relative;
    display: flex;
    align-items: center;
}

.voice-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #007bff;
    color: white;
    border: none;
    margin-left: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.voice-btn.listening {
    background: #dc3545;
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
} 

function showLoading(button) {
    button.innerHTML = '<div class="spinner"></div>';
    button.disabled = true;
}

function hideLoading(button) {
    button.innerHTML = '<i class="fas fa-microphone"></i>';
    button.disabled = false;
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    // Show error for 3 seconds
    setTimeout(() => errorDiv.remove(), 3000);
} 

<div class="form-group">
    <div class="input-with-voice">
        <input type="text" id="customerName" class="form-control" placeholder="Customer Name *">
        <button class="voice-btn" type="button" data-field="customerName">
            <i class="fas fa-microphone"></i>
        </button>
    </div>
</div>