# 🏥 HealFind AI - Medical Search & Doctor Recommendations

A comprehensive web application that combines medicine search with AI-powered doctor recommendations based on medical document analysis.

![HealFind AI Logo](static/images/heallogo.jpg)

## ✨ Features

### 🔍 Medicine Search
- **Smart Search**: Find medicines by name with optional manufacturer filtering
- **Real-time Inventory**: Check stock availability across nearby medical shops
- **Location-based Results**: Get distance-sorted results from your location
- **Price Comparison**: Compare prices across different pharmacies
- **Shop Details**: Contact information, ratings, and operating hours

### 🤖 AI Medical Assistant
- **Document Analysis**: Upload medical reports, X-rays, lab results, and scans
- **AI-Powered Recommendations**: Get personalized doctor suggestions based on your medical documents
- **Specialty Matching**: Automatically identify the required medical specialty
- **Doctor Ranking**: Doctors ranked by experience years and success rate
- **Conversational Interface**: ChatGPT-style interaction for natural communication

### 🏥 Doctor Recommendations
Doctors are intelligently ranked based on:
- **Success Rate**: Percentage of successful treatments/operations
- **Experience**: Years of medical practice
- **Specialization Match**: Relevance to your medical condition
- **Location**: Distance from your current location

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask
- **Database**: SQLite3
- **AI Processing**: Custom medical document analysis
- **Styling**: Responsive design with modern CSS Grid and Flexbox
- **File Handling**: Secure file upload and processing

## 📁 Project Structure

```
Healfind/
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── app.js             # Frontend JavaScript
│   └── images/
│       └── heallogo.jpg       # Logo/background image
├── backend/
│   └── app.py                 # Flask backend server
├── templates/
│   └── index.html             # Template (auto-copied)
├── uploads/                   # Temporary file uploads
├── index.html                 # Main HTML file
├── requirements.txt           # Python dependencies
├── run.bat                    # Windows startup script
├── healfind.db               # SQLite database (auto-created)
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Web browser (Chrome, Firefox, Safari, Edge)

### Installation & Setup

#### Option 1: Automatic Setup (Windows)
1. **Double-click `run.bat`** - This will automatically:
   - Create a virtual environment
   - Install all dependencies
   - Set up the database
   - Start the server

#### Option 2: Manual Setup
1. **Clone or download the project**
2. **Open Command Prompt/Terminal** in the project directory
3. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```
4. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
6. **Start the server**:
   ```bash
   cd backend
   python app.py
   ```

### 🌐 Access the Application
Open your browser and navigate to: **http://localhost:5000**

## 📱 How to Use

### Medicine Search Mode
1. **Switch to Medicine Search** (default mode)
2. **Enter Medicine Name** in the search box
3. **Optional**: Add manufacturer name for specific filtering
4. **Click Search** to find nearby pharmacies
5. **View Results**: See shops sorted by distance with price and stock info

### AI Assistant Mode
1. **Switch to AI Assistant** using the top navigation
2. **Upload Medical Documents**:
   - Drag & drop files or click to browse
   - Supported formats: PDF, images (JPG, PNG), text files, Word docs
3. **Describe Symptoms** (optional): Add context in the message box
4. **Send Message**: The AI will analyze your documents
5. **Get Recommendations**: Receive ranked doctor suggestions with detailed profiles

## 🔬 AI Analysis Features

### Document Processing
The AI system analyzes various medical documents:
- **Lab Reports**: Blood tests, urine analysis, biochemical reports
- **Imaging**: X-rays, MRI scans, CT scans, ultrasounds
- **ECG/EKG**: Heart rhythm analysis
- **Medical History**: Previous diagnoses and treatments

### Specialty Detection
Automatically identifies the required medical specialty:
- **Cardiology**: Heart and cardiovascular issues
- **Neurology**: Brain and nervous system
- **Orthopedics**: Bones, joints, and musculoskeletal
- **Gastroenterology**: Digestive system
- **Endocrinology**: Hormones and metabolism
- **Dermatology**: Skin conditions
- **Internal Medicine**: General health concerns
- **Psychiatry**: Mental health

### Doctor Ranking Algorithm
```
Score = (Success Rate × 0.6) + (Experience Years × 3 × 0.4)
```
- Prioritizes proven success while valuing experience
- Location proximity as secondary factor
- Specialty relevance as primary filter

## 💾 Database Schema

### Medical Shops
- Shop information, location, ratings, operating hours
- Real-time inventory tracking

### Medicines
- Comprehensive medicine database with manufacturers
- Category classification and descriptions

### Doctors
- Detailed doctor profiles with specializations
- Performance metrics and contact information

### Medicine Inventory
- Stock levels and pricing across different shops
- Last updated timestamps for freshness

## 🎨 Design Features

### Visual Design
- **Background Integration**: Your logo serves as an elegant background
- **Modern UI**: Clean, professional medical interface
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Accessibility**: High contrast, readable fonts, intuitive navigation

### User Experience
- **Dual-Mode Interface**: Easy switching between search and AI modes
- **ChatGPT-style Chat**: Familiar conversational interface
- **Real-time Feedback**: Loading states and progress indicators
- **File Management**: Drag & drop with visual feedback

### Performance
- **Optimized Loading**: Efficient resource management
- **Smooth Animations**: CSS-based transitions and effects
- **Mobile Responsive**: Touch-friendly interface for mobile users

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional) for production:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///healfind.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Database Configuration
The SQLite database is automatically created with sample data including:
- 5 medical shops with realistic locations
- 8 common medicines with multiple manufacturers
- 8 specialist doctors with performance metrics
- Random inventory data across shops

## 🚀 Production Deployment

### For Production Use:
1. **Set environment variables** for security
2. **Use PostgreSQL** instead of SQLite for better performance
3. **Implement real geolocation** for accurate distance calculations
4. **Add authentication** for user accounts and history
5. **Integrate real AI services** (OpenAI, Google Health AI, etc.)
6. **Add payment processing** for medicine orders
7. **Implement real-time inventory** updates from pharmacies

### Scalability Considerations:
- **API Rate Limiting**: Implement for production use
- **Caching**: Redis for frequent queries
- **CDN**: For static assets and images
- **Load Balancing**: For high traffic scenarios

## 🔐 Security Features

- **File Upload Validation**: Secure file type checking
- **SQL Injection Protection**: Parameterized queries
- **XSS Prevention**: Input sanitization
- **CORS Configuration**: Controlled cross-origin requests
- **File Size Limits**: Prevents large file attacks

## 📊 Sample Data

The application comes pre-loaded with:
- **5 Medical Shops** with realistic addresses and ratings
- **8 Common Medicines** (Paracetamol, Amoxicillin, Aspirin, etc.)
- **8 Specialist Doctors** across different medical fields
- **Random Inventory** with realistic pricing and stock levels

## 🛠️ Troubleshooting

### Common Issues:
1. **Port 5000 in use**: Change port in `app.py` or kill existing process
2. **Permission errors**: Run as administrator or check file permissions
3. **Module not found**: Ensure virtual environment is activated
4. **Database errors**: Delete `healfind.db` to recreate with fresh data

### Debug Mode:
- Set `debug=True` in `app.py` for detailed error messages
- Check browser console for frontend JavaScript errors
- Monitor Flask console for backend error logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the console logs
3. Ensure all dependencies are installed
4. Verify Python version compatibility

---

**🎉 Enjoy using HealFind AI for your medical search and doctor recommendation needs!**