/**
 * Potato Disease Classification Frontend
 * Main application logic
 */

const API_BASE_URL = "http://localhost:8000";
const API_PREDICT_URL = `${API_BASE_URL}/api/v1/predict`;

let selectedFile = null;

// ============================================
// DOM Elements
// ============================================

const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const selectBtn = document.getElementById("selectBtn");
const previewSection = document.getElementById("previewSection");
const previewImage = document.getElementById("previewImage");
const predictBtn = document.getElementById("predictBtn");
const removeBtn = document.getElementById("removeBtn");
const loadingState = document.getElementById("loadingState");
const resultsSection = document.getElementById("resultsSection");
const errorState = document.getElementById("errorState");
const errorMessage = document.getElementById("errorMessage");
const newPredictionBtn = document.getElementById("newPredictionBtn");
const downloadResults = document.getElementById("downloadResults");

// ============================================
// Event Listeners - Upload
// ============================================

selectBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

// Drag and drop
uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
        handleFileSelect(file);
    } else {
        showError("Please select a valid image file");
    }
});

removeBtn.addEventListener("click", resetForm);
predictBtn.addEventListener("click", makePrediction);
newPredictionBtn.addEventListener("click", resetForm);
downloadResults.addEventListener("click", downloadPredictionResults);

// ============================================
// File Handling
// ============================================

function handleFileSelect(file) {
    // Validate file
    const maxSize = 10 * 1024 * 1024; // 10MB
    const validTypes = ["image/jpeg", "image/png", "image/webp", "image/gif"];
    
    if (!validTypes.includes(file.type)) {
        showError("Invalid file type. Please select JPG, PNG, or WebP");
        return;
    }
    
    if (file.size > maxSize) {
        showError("File size exceeds 10MB limit");
        return;
    }
    
    selectedFile = file;
    displayPreview(file);
}

function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadArea.style.display = "none";
        previewSection.style.display = "flex";
        resultsSection.style.display = "none";
        errorState.style.display = "none";
    };
    reader.readAsDataURL(file);
}

function resetForm() {
    selectedFile = null;
    fileInput.value = "";
    previewSection.style.display = "none";
    resultsSection.style.display = "none";
    errorState.style.display = "none";
    uploadArea.style.display = "block";
    uploadArea.classList.remove("dragover");
}

// ============================================
// Prediction
// ============================================

async function makePrediction() {
    if (!selectedFile) {
        showError("Please select an image first");
        return;
    }
    
    try {
        // Show loading state
        previewSection.style.display = "none";
        resultsSection.style.display = "none";
        errorState.style.display = "none";
        loadingState.style.display = "flex";
        
        // Prepare form data
        const formData = new FormData();
        formData.append("file", selectedFile);
        
        // Make request
        const response = await fetch(API_PREDICT_URL, {
            method: "POST",
            body: formData,
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Prediction failed");
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        console.error("Prediction error:", error);
        showError(error.message || "Failed to make prediction. Please try again.");
    } finally {
        loadingState.style.display = "none";
    }
}

function displayResults(result) {
    // Hide other sections
    previewSection.style.display = "none";
    loadingState.style.display = "none";
    errorState.style.display = "none";
    resultsSection.style.display = "block";
    
    // Update main prediction
    document.getElementById("predictedClass").textContent = result.predicted_class;
    document.getElementById("confidencePercentage").textContent = 
        result.confidence_percentage.toFixed(1) + "%";
    document.getElementById("confidenceValue").textContent = 
        result.confidence_percentage.toFixed(2) + "%";
    
    // Animate progress bar
    const confidenceProgress = document.getElementById("confidenceProgress");
    setTimeout(() => {
        confidenceProgress.style.width = result.confidence_percentage + "%";
    }, 100);
    
    // Display all predictions
    displayPredictionsBreakdown(result.all_predictions);
    
    // Display disease information
    displayDiseaseInfo(result.predicted_class);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function displayPredictionsBreakdown(predictions) {
    const predictionsTable = document.getElementById("predictionsTable");
    
    // Sort predictions by confidence (descending)
    const sortedPredictions = Object.entries(predictions)
        .sort(([, a], [, b]) => b - a);
    
    let html = "";
    
    for (const [className, confidence] of sortedPredictions) {
        const percentage = (confidence * 100).toFixed(2);
        const displayPercentage = percentage + "%";
        
        html += `
            <div class="prediction-row">
                <div class="prediction-class">${className}</div>
                <div class="prediction-bar-container">
                    <div class="prediction-bar-fill" style="width: ${percentage}%">
                        ${displayPercentage}
                    </div>
                </div>
                <div class="prediction-value">${percentage}%</div>
            </div>
        `;
    }
    
    predictionsTable.innerHTML = html;
}

function displayDiseaseInfo(className) {
    const diseaseInfo = document.getElementById("diseaseInfo");
    
    const info = {
        "Early Blight": {
            name: "Early Blight",
            description: "Early Blight is caused by Alternaria solani. It appears as small, circular brown spots with concentric rings on lower leaves.",
            recommendation: "Remove infected leaves, improve air circulation, and apply fungicide treatments if needed."
        },
        "Late Blight": {
            name: "Late Blight",
            description: "Late Blight is caused by Phytophthora infestans. It shows as water-soaked lesions with white mold on leaf undersides.",
            recommendation: "Use resistant varieties, remove infected foliage, and apply copper or chlorothalonil fungicides."
        },
        "Healthy": {
            name: "Healthy",
            description: "Your potato plant appears to be healthy with no signs of disease detected.",
            recommendation: "Continue with regular monitoring and maintenance practices."
        }
    };
    
    const diseaseData = info[className] || info.Healthy;
    
    diseaseInfo.innerHTML = `
        <h4>🌿 ${diseaseData.name}</h4>
        <p><strong>Description:</strong> ${diseaseData.description}</p>
        <p style="margin-top: 1rem;"><strong>Recommendation:</strong> ${diseaseData.recommendation}</p>
    `;
}

// ============================================
// Error Handling
// ============================================

function showError(message) {
    errorState.style.display = "block";
    errorMessage.textContent = message;
    previewSection.style.display = "none";
    resultsSection.style.display = "none";
    loadingState.style.display = "none";
    uploadArea.style.display = "none";
}

// ============================================
// Download Results
// ============================================

function downloadPredictionResults() {
    const predictedClass = document.getElementById("predictedClass").textContent;
    const confidence = document.getElementById("confidenceValue").textContent;
    const timestamp = new Date().toLocaleString();
    
    const content = `
Potato Disease Classification Results
=====================================
Predicted Disease: ${predictedClass}
Confidence: ${confidence}
Date & Time: ${timestamp}
Model Version: 1.0

Note: This is an AI-based prediction and should be verified by domain experts.
    `.trim();
    
    const element = document.createElement("a");
    element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(content));
    element.setAttribute("download", `potato-classification-${Date.now()}.txt`);
    element.style.display = "none";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// ============================================
// Initialization
// ============================================

document.addEventListener("DOMContentLoaded", () => {
    console.log("Potato Disease Classification System loaded");
    console.log("API Base URL:", API_BASE_URL);
    
    // Check API connectivity
    checkApiHealth();
});

async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log("✓ API is healthy");
        }
    } catch (error) {
        console.warn("⚠ API is not accessible. Make sure the backend is running.");
    }
}

// ============================================
// Utility Functions
// ============================================

function formatDate(date) {
    return new Date(date).toLocaleString();
}
