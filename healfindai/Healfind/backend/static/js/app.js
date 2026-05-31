// HealFind AI - Frontend JavaScript
class HealFindApp {
    constructor() {
        this.currentMode = 'medicine';
        this.uploadedFiles = [];
        this.isProcessing = false;
        
        this.initializeElements();
        this.bindEvents();
        this.setupDragAndDrop();
        this.autoResizeTextarea();
    }

    initializeElements() {
        // Navigation
        this.navButtons = document.querySelectorAll('.nav-btn');
        
        // Sections
        this.welcomeSection = document.getElementById('welcomeSection');
        this.chatContainer = document.getElementById('chatContainer');
        this.resultsSection = document.getElementById('resultsSection');
        this.chatMessages = document.getElementById('chatMessages');
        
        // Input modes
        this.medicineMode = document.getElementById('medicineMode');
        this.assistantMode = document.getElementById('assistantMode');
        
        // Medicine search elements
        this.medicineInput = document.getElementById('medicineInput');
        this.manufacturerInput = document.getElementById('manufacturerInput');
        this.medicineSearchBtn = document.getElementById('medicineSearchBtn');
        
        // Assistant mode elements
        this.fileInput = document.getElementById('fileInput');
        this.fileUploadArea = document.getElementById('fileUploadArea');
        this.uploadedFilesContainer = document.getElementById('uploadedFiles');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        
        // Loading spinner
        this.loadingSpinner = document.getElementById('loadingSpinner');
    }

    bindEvents() {
        // Navigation events
        this.navButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.switchMode(e.target.dataset.mode));
        });

        // Medicine search events
        this.medicineSearchBtn.addEventListener('click', () => this.searchMedicine());
        this.medicineInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchMedicine();
        });
        this.manufacturerInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchMedicine();
        });

        // Assistant mode events
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    setupDragAndDrop() {
        // Drag and drop functionality
        this.fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.fileUploadArea.classList.add('dragover');
        });

        this.fileUploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            this.fileUploadArea.classList.remove('dragover');
        });

        this.fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.fileUploadArea.classList.remove('dragover');
            const files = Array.from(e.dataTransfer.files);
            this.addFiles(files);
        });
    }

    autoResizeTextarea() {
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        });
    }

    switchMode(mode) {
        this.currentMode = mode;
        
        // Update navigation
        this.navButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });
        
        // Switch input modes
        if (mode === 'medicine') {
            this.medicineMode.style.display = 'block';
            this.assistantMode.style.display = 'none';
            this.hideChat();
            this.showWelcome();
        } else {
            this.medicineMode.style.display = 'none';
            this.assistantMode.style.display = 'block';
            this.hideWelcome();
            this.showChat();
        }
        
        this.hideResults();
    }

    showWelcome() {
        this.welcomeSection.style.display = 'block';
        this.welcomeSection.classList.add('fade-in');
    }

    hideWelcome() {
        this.welcomeSection.style.display = 'none';
    }

    showChat() {
        this.chatContainer.style.display = 'block';
        this.chatContainer.classList.add('fade-in');
    }

    hideChat() {
        this.chatContainer.style.display = 'none';
    }

    showResults() {
        this.resultsSection.style.display = 'block';
        this.resultsSection.classList.add('fade-in');
    }

    hideResults() {
        this.resultsSection.style.display = 'none';
    }

    showLoading() {
        this.loadingSpinner.style.display = 'block';
        this.isProcessing = true;
        this.sendBtn.disabled = true;
        this.medicineSearchBtn.disabled = true;
    }

    hideLoading() {
        this.loadingSpinner.style.display = 'none';
        this.isProcessing = false;
        this.sendBtn.disabled = false;
        this.medicineSearchBtn.disabled = false;
    }

    // Medicine search functionality
    async searchMedicine() {
        const medicineName = this.medicineInput.value.trim();
        const manufacturer = this.manufacturerInput.value.trim();

        if (!medicineName) {
            this.showToast('Please enter a medicine name', 'error');
            return;
        }

        this.showLoading();
        this.hideWelcome();
        this.showResults();

        try {
            const response = await fetch('/api/search-medicine', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    medicine: medicineName,
                    manufacturer: manufacturer
                })
            });

            const data = await response.json();
            this.displayMedicineResults(data.results);
        } catch (error) {
            console.error('Error searching medicine:', error);
            this.showToast('Error searching for medicine. Please try again.', 'error');
            this.displayMedicineResults(this.getMockMedicineData(medicineName, manufacturer));
        } finally {
            this.hideLoading();
        }
    }

    displayMedicineResults(results) {
        const html = `
            <h3>Search Results</h3>
            <div class="results-grid">
                ${results.map(result => `
                    <div class="result-card fade-in">
                        <div class="result-header">
                            <div class="result-title">${result.shopName}</div>
                            <div class="result-rating">
                                <div class="stars">${this.generateStars(result.rating)}</div>
                                <span>(${result.rating})</span>
                            </div>
                        </div>
                        <div class="result-details">
                            <p><strong>Medicine:</strong> ${result.medicine}</p>
                            ${result.manufacturer ? `<p><strong>Manufacturer:</strong> ${result.manufacturer}</p>` : ''}
                            <p><strong>Price:</strong> ₹${result.price}</p>
                            <p><strong>Stock:</strong> ${result.stock} units available</p>
                            <p><strong>Address:</strong> ${result.address}</p>
                            <p class="result-distance"><i class="fas fa-map-marker-alt"></i> ${result.distance}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        this.resultsSection.innerHTML = html;
    }

    // File handling
    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        this.addFiles(files);
    }

    addFiles(files) {
        files.forEach(file => {
            if (this.isValidFile(file)) {
                this.uploadedFiles.push(file);
                this.displayUploadedFile(file);
            } else {
                this.showToast(`Invalid file type: ${file.name}. Please upload medical documents (PDF, images, etc.)`, 'error');
            }
        });
    }

    isValidFile(file) {
        const validTypes = [
            'application/pdf',
            'image/jpeg',
            'image/png',
            'image/jpg',
            'text/plain',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ];
        return validTypes.includes(file.type);
    }

    displayUploadedFile(file) {
        const fileTag = document.createElement('div');
        fileTag.className = 'file-tag fade-in';
        fileTag.innerHTML = `
            <i class="fas fa-file"></i>
            <span>${file.name}</span>
            <span class="remove-file" onclick="app.removeFile('${file.name}')">&times;</span>
        `;
        this.uploadedFilesContainer.appendChild(fileTag);
    }

    removeFile(fileName) {
        this.uploadedFiles = this.uploadedFiles.filter(file => file.name !== fileName);
        // Update UI
        const fileTags = this.uploadedFilesContainer.querySelectorAll('.file-tag');
        fileTags.forEach(tag => {
            if (tag.textContent.includes(fileName)) {
                tag.remove();
            }
        });
    }

    // Chat functionality
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message && this.uploadedFiles.length === 0) {
            this.showToast('Please enter a message or upload files', 'error');
            return;
        }

        if (this.isProcessing) return;

        // Add user message to chat
        if (message) {
            this.addMessageToChat('user', message);
        }

        // Show file attachments
        if (this.uploadedFiles.length > 0) {
            const fileNames = this.uploadedFiles.map(f => f.name).join(', ');
            this.addMessageToChat('user', `📎 Uploaded files: ${fileNames}`, 'file');
        }

        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.showLoading();

        try {
            const formData = new FormData();
            formData.append('message', message);
            this.uploadedFiles.forEach(file => {
                formData.append('files', file);
            });

            const response = await fetch('/api/analyze-documents', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.type === 'doctor_recommendations') {
                this.displayDoctorRecommendations(data.doctors, data.analysis);
            } else {
                this.addMessageToChat('assistant', data.response);
            }
        } catch (error) {
            console.error('Error analyzing documents:', error);
            this.handleMockResponse(message);
        } finally {
            this.hideLoading();
            this.uploadedFiles = [];
            this.uploadedFilesContainer.innerHTML = '';
        }
    }

    addMessageToChat(sender, message, type = 'text') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender} fade-in`;
        
        const now = new Date();
        const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messageDiv.innerHTML = `
            <div class="message-content">
                ${type === 'file' ? message : this.formatMessage(message)}
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    formatMessage(message) {
        // Basic markdown-like formatting
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    displayDoctorRecommendations(doctors, analysis) {
        let response = `Based on your medical documents, here's my analysis:\n\n${analysis}\n\nI recommend the following doctors:`;
        this.addMessageToChat('assistant', response);
        
        const doctorCardsHtml = doctors.map(doctor => `
            <div class="doctor-card fade-in">
                <div class="doctor-header">
                    <div class="doctor-avatar">${doctor.name.charAt(0)}</div>
                    <div class="doctor-info">
                        <h3>${doctor.name}</h3>
                        <div class="doctor-specialty">${doctor.specialty}</div>
                    </div>
                </div>
                <div class="doctor-stats">
                    <div class="stat-item">
                        <div class="stat-value">${doctor.experience}</div>
                        <div class="stat-label">Years Experience</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${doctor.successRate}%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${doctor.operations}</div>
                        <div class="stat-label">Operations</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${doctor.distance}</div>
                        <div class="stat-label">Distance</div>
                    </div>
                </div>
                <div class="result-details">
                    <p><strong>Hospital:</strong> ${doctor.hospital}</p>
                    <p><strong>Address:</strong> ${doctor.address}</p>
                    <p><strong>Contact:</strong> ${doctor.phone}</p>
                </div>
            </div>
        `).join('');
        
        const doctorMessage = document.createElement('div');
        doctorMessage.className = 'message assistant fade-in';
        doctorMessage.innerHTML = `
            <div class="message-content">
                ${doctorCardsHtml}
            </div>
            <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
        `;
        
        this.chatMessages.appendChild(doctorMessage);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    // Mock data functions
    getMockMedicineData(medicine, manufacturer) {
        return [
            {
                shopName: "HealthPlus Pharmacy",
                medicine: medicine,
                manufacturer: manufacturer || "Generic Pharma",
                price: "150.00",
                stock: 25,
                address: "123 Health Street, Medical District",
                distance: "0.5 km away",
                rating: 4.5
            },
            {
                shopName: "MediCare Store",
                medicine: medicine,
                manufacturer: manufacturer || "MedLife Ltd",
                price: "145.00",
                stock: 18,
                address: "456 Care Avenue, City Center",
                distance: "1.2 km away",
                rating: 4.3
            },
            {
                shopName: "QuickMed Pharmacy",
                medicine: medicine,
                manufacturer: manufacturer || "HealthCorp",
                price: "155.00",
                stock: 30,
                address: "789 Quick Lane, Downtown",
                distance: "2.1 km away",
                rating: 4.7
            }
        ];
    }

    handleMockResponse(message) {
        if (this.uploadedFiles.length > 0) {
            // Mock doctor recommendations
            const mockDoctors = [
                {
                    name: "Dr. Sarah Johnson",
                    specialty: "Cardiologist",
                    experience: 15,
                    successRate: 96,
                    operations: 1200,
                    hospital: "City General Hospital",
                    address: "123 Medical Center Dr",
                    phone: "+1-555-0123",
                    distance: "2.3 km"
                },
                {
                    name: "Dr. Michael Chen",
                    specialty: "Internal Medicine",
                    experience: 12,
                    successRate: 94,
                    operations: 800,
                    hospital: "Metro Health Center",
                    address: "456 Health Plaza",
                    phone: "+1-555-0456",
                    distance: "3.1 km"
                }
            ];
            
            const analysis = "Based on your medical reports, I've identified potential cardiovascular concerns that require specialist attention. Your ECG shows irregular patterns that should be evaluated by a cardiologist.";
            
            this.displayDoctorRecommendations(mockDoctors, analysis);
        } else {
            // Regular chat response
            const responses = [
                "I'm here to help with your medical queries. Please upload your medical documents for personalized doctor recommendations, or use the medicine search to find nearby pharmacies.",
                "For the best recommendations, please upload your medical reports, X-rays, or test results. I can analyze them and suggest appropriate specialists.",
                "I can help you find the right doctors based on your medical condition. Please share your medical documents for analysis."
            ];
            
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            this.addMessageToChat('assistant', randomResponse);
        }
    }

    // Utility functions
    generateStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        let starsHtml = '';
        
        for (let i = 0; i < fullStars; i++) {
            starsHtml += '<i class="fas fa-star"></i>';
        }
        
        if (hasHalfStar) {
            starsHtml += '<i class="fas fa-star-half-alt"></i>';
        }
        
        const emptyStars = 5 - Math.ceil(rating);
        for (let i = 0; i < emptyStars; i++) {
            starsHtml += '<i class="far fa-star"></i>';
        }
        
        return starsHtml;
    }

    showToast(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} fade-in`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#e74c3c' : '#3498db'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1001;
            max-width: 300px;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new HealFindApp();
});