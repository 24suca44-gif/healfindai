from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
import uuid
from datetime import datetime
import base64
from werkzeug.utils import secure_filename
import sqlite3
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import re

# For AI document processing (we'll use mock implementation)
# In production, you would use actual AI libraries like OpenAI, Hugging Face, etc.

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class HealFindDatabase:
    def __init__(self):
        self.init_database()
        self.populate_sample_data()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect('healfind.db')
        cursor = conn.cursor()
        
        # Medical shops table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_shops (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT,
                latitude REAL,
                longitude REAL,
                rating REAL DEFAULT 4.0,
                operating_hours TEXT
            )
        ''')
        
        # Medicines table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                manufacturer TEXT,
                category TEXT,
                description TEXT
            )
        ''')
        
        # Medicine inventory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicine_inventory (
                id INTEGER PRIMARY KEY,
                shop_id INTEGER,
                medicine_id INTEGER,
                stock_quantity INTEGER,
                price REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (shop_id) REFERENCES medical_shops (id),
                FOREIGN KEY (medicine_id) REFERENCES medicines (id)
            )
        ''')
        
        # Doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                experience_years INTEGER,
                success_rate REAL,
                total_operations INTEGER,
                hospital TEXT,
                address TEXT,
                phone TEXT,
                latitude REAL,
                longitude REAL,
                rating REAL DEFAULT 4.5
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def populate_sample_data(self):
        """Populate database with sample data"""
        conn = sqlite3.connect('healfind.db')
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute('SELECT COUNT(*) FROM medical_shops')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Sample medical shops
        shops_data = [
            ("HealthPlus Pharmacy", "123 Health Street, Medical District", "+1-555-0101", 28.6139, 77.2090, 4.5, "08:00-22:00"),
            ("MediCare Store", "456 Care Avenue, City Center", "+1-555-0102", 28.6129, 77.2080, 4.3, "24/7"),
            ("QuickMed Pharmacy", "789 Quick Lane, Downtown", "+1-555-0103", 28.6149, 77.2100, 4.7, "09:00-21:00"),
            ("CityMed Pharmacy", "321 Medical Plaza, Business District", "+1-555-0104", 28.6159, 77.2110, 4.2, "08:30-20:30"),
            ("WellCare Drugs", "654 Wellness Road, Suburb Area", "+1-555-0105", 28.6119, 77.2070, 4.6, "24/7"),
            ("Apollo Pharmacy", "987 Apollo Circle, Tech Park", "+1-555-0106", 28.6169, 77.2120, 4.8, "07:00-23:00"),
            ("Guardian Health", "147 Guardian Street, Mall Road", "+1-555-0107", 28.6109, 77.2060, 4.4, "10:00-22:00"),
            ("LifeLine Pharmacy", "258 Life Avenue, Hospital Zone", "+1-555-0108", 28.6179, 77.2130, 4.9, "24/7")
        ]
        
        cursor.executemany('''
            INSERT INTO medical_shops (name, address, phone, latitude, longitude, rating, operating_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', shops_data)
        
        # Sample medicines
        medicines_data = [
            # Common Pain Relief
            ("Paracetamol", "Generic Pharma", "Analgesic", "Pain relief and fever reducer"),
            ("Paracetamol", "MedLife Ltd", "Analgesic", "Pain relief and fever reducer"),
            ("Ibuprofen", "PainFree Corp", "NSAID", "Anti-inflammatory pain relief"),
            ("Aspirin", "HealthCorp", "Analgesic", "Pain relief and blood thinner"),
            ("Diclofenac", "FlexiCare", "NSAID", "Joint pain and inflammation"),
            
            # Antibiotics
            ("Amoxicillin", "MedLife Ltd", "Antibiotic", "Bacterial infection treatment"),
            ("Amoxicillin", "BioPharm", "Antibiotic", "Bacterial infection treatment"),
            ("Azithromycin", "InfecCure", "Antibiotic", "Respiratory infections"),
            ("Ciprofloxacin", "MicroKill", "Antibiotic", "UTI and bacterial infections"),
            ("Cephalexin", "BactFree", "Antibiotic", "Skin and soft tissue infections"),
            
            # Diabetes & Heart
            ("Metformin", "DiabetesCore", "Antidiabetic", "Type 2 diabetes management"),
            ("Metformin", "GlucoControl", "Antidiabetic", "Blood sugar control"),
            ("Insulin", "DiabetesCore", "Hormone", "Type 1 diabetes treatment"),
            ("Lisinopril", "CardioMed", "ACE Inhibitor", "Blood pressure medication"),
            ("Atenolol", "HeartCare", "Beta Blocker", "Hypertension treatment"),
            ("Simvastatin", "CholesterolCare", "Statin", "Cholesterol management"),
            
            # Stomach & Digestion
            ("Omeprazole", "GastroHealth", "PPI", "Acid reflux treatment"),
            ("Ranitidine", "StomachEase", "H2 Blocker", "Heartburn relief"),
            ("Domperidone", "DigestWell", "Antiemetic", "Nausea and vomiting"),
            ("Loperamide", "GutCare", "Antidiarrheal", "Diarrhea control"),
            
            # Allergies & Cold
            ("Cetirizine", "AllergyFree", "Antihistamine", "Allergy relief"),
            ("Loratadine", "SneezeStop", "Antihistamine", "Seasonal allergies"),
            ("Dextromethorphan", "CoughAway", "Cough Suppressant", "Dry cough relief"),
            ("Phenylephrine", "ClearNose", "Decongestant", "Nasal congestion"),
            
            # Vitamins & Supplements
            ("Vitamin D3", "VitaLife", "Vitamin", "Bone health supplement"),
            ("Vitamin B12", "EnergyPlus", "Vitamin", "Energy and nerve health"),
            ("Calcium", "BoneStrong", "Mineral", "Bone and teeth health"),
            ("Iron", "BloodBoost", "Mineral", "Anemia treatment"),
            ("Omega-3", "HeartOil", "Supplement", "Heart and brain health"),
            
            # Mental Health
            ("Sertraline", "MoodLift", "Antidepressant", "Depression and anxiety"),
            ("Alprazolam", "CalmMind", "Anxiolytic", "Anxiety disorders"),
            ("Zolpidem", "SleepWell", "Sedative", "Insomnia treatment"),
            
            # Skin & External
            ("Clotrimazole", "SkinCure", "Antifungal", "Fungal skin infections"),
            ("Hydrocortisone", "SkinSoothe", "Corticosteroid", "Skin inflammation"),
            ("Betadine", "WoundCare", "Antiseptic", "Wound cleaning"),
            
            # Emergency & First Aid
            ("Epinephrine", "LifeSave", "Emergency", "Severe allergic reactions"),
            ("Salbutamol", "BreathEasy", "Bronchodilator", "Asthma inhaler"),
            ("Nitroglycerin", "HeartRescue", "Vasodilator", "Chest pain relief")
        ]
        
        cursor.executemany('''
            INSERT INTO medicines (name, manufacturer, category, description)
            VALUES (?, ?, ?, ?)
        ''', medicines_data)
        
        # Sample inventory (more realistic pricing and stock)
        import random
        
        # Define price ranges for different medicine categories
        price_ranges = {
            'Analgesic': (25, 150),
            'NSAID': (40, 200),
            'Antibiotic': (80, 400),
            'Antidiabetic': (120, 600),
            'ACE Inhibitor': (150, 350),
            'Beta Blocker': (100, 300),
            'Statin': (200, 500),
            'PPI': (180, 450),
            'H2 Blocker': (60, 180),
            'Antiemetic': (90, 250),
            'Antidiarrheal': (35, 120),
            'Antihistamine': (30, 100),
            'Cough Suppressant': (50, 150),
            'Decongestant': (40, 130),
            'Vitamin': (150, 800),
            'Mineral': (200, 700),
            'Supplement': (300, 1200),
            'Antidepressant': (250, 800),
            'Anxiolytic': (180, 600),
            'Sedative': (200, 500),
            'Antifungal': (120, 400),
            'Corticosteroid': (80, 300),
            'Antiseptic': (25, 80),
            'Emergency': (500, 2000),
            'Bronchodilator': (300, 800),
            'Vasodilator': (400, 1000),
            'Hormone': (800, 2500)
        }
        
        for shop_id in range(1, 9):  # Updated for 8 shops
            for medicine_id in range(1, len(medicines_data) + 1):
                # 85% chance of having the medicine (more realistic)
                if random.random() > 0.15:
                    # Get medicine category for pricing
                    cursor.execute('SELECT category FROM medicines WHERE id = ?', (medicine_id,))
                    category_result = cursor.fetchone()
                    category = category_result[0] if category_result else 'Analgesic'
                    
                    # Get price range for category
                    min_price, max_price = price_ranges.get(category, (50, 200))
                    
                    # Generate realistic stock and pricing
                    stock = random.randint(2, 80)  # More varied stock levels
                    base_price = random.uniform(min_price, max_price)
                    
                    # Add some shop-specific pricing variation
                    price_variation = random.uniform(0.85, 1.15)  # ±15% price variation
                    final_price = round(base_price * price_variation, 2)
                    
                    cursor.execute('''
                        INSERT INTO medicine_inventory (shop_id, medicine_id, stock_quantity, price)
                        VALUES (?, ?, ?, ?)
                    ''', (shop_id, medicine_id, stock, final_price))
        
        # Sample doctors
        doctors_data = [
            ("Dr. Sarah Johnson", "Cardiologist", 15, 96.5, 1200, "City General Hospital", "123 Medical Center Dr", "+1-555-0201", 28.6140, 77.2095, 4.8),
            ("Dr. Michael Chen", "Internal Medicine", 12, 94.2, 800, "Metro Health Center", "456 Health Plaza", "+1-555-0202", 28.6130, 77.2085, 4.6),
            ("Dr. Emily Rodriguez", "Neurologist", 18, 97.1, 950, "NeuroScience Institute", "789 Brain Ave", "+1-555-0203", 28.6150, 77.2105, 4.9),
            ("Dr. David Park", "Orthopedist", 14, 95.3, 1100, "Bone & Joint Center", "321 Movement St", "+1-555-0204", 28.6160, 77.2115, 4.7),
            ("Dr. Lisa Thompson", "Endocrinologist", 11, 93.8, 600, "Diabetes Care Center", "654 Hormone Rd", "+1-555-0205", 28.6120, 77.2075, 4.5),
            ("Dr. James Wilson", "Gastroenterologist", 16, 96.0, 850, "Digestive Health Clinic", "987 Stomach St", "+1-555-0206", 28.6135, 77.2090, 4.6),
            ("Dr. Maria Garcia", "Dermatologist", 10, 92.5, 500, "Skin Health Center", "147 Beauty Blvd", "+1-555-0207", 28.6145, 77.2100, 4.4),
            ("Dr. Robert Lee", "Psychiatrist", 20, 94.7, 750, "Mental Wellness Institute", "258 Mind Ave", "+1-555-0208", 28.6125, 77.2080, 4.7)
        ]
        
        cursor.executemany('''
            INSERT INTO doctors (name, specialty, experience_years, success_rate, total_operations, hospital, address, phone, latitude, longitude, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', doctors_data)
        
        conn.commit()
        conn.close()

class MedicalAI:
    """Enhanced AI class for medical document analysis"""
    
    def __init__(self):
        self.medical_keywords = {
            'cardiology': {
                'keywords': ['heart', 'cardiac', 'ecg', 'ekg', 'chest pain', 'blood pressure', 'hypertension', 'arrhythmia', 'coronary', 'myocardial', 'atrial', 'ventricular', 'pulse', 'angina', 'tachycardia', 'bradycardia'],
                'symptoms': ['chest pain', 'shortness of breath', 'palpitations', 'dizziness', 'fatigue'],
                'urgency': 'high'
            },
            'neurology': {
                'keywords': ['brain', 'neurological', 'headache', 'seizure', 'mri brain', 'ct brain', 'stroke', 'migraine', 'epilepsy', 'alzheimer', 'parkinson', 'dementia', 'tremor'],
                'symptoms': ['headache', 'confusion', 'memory loss', 'seizures', 'tremors'],
                'urgency': 'high'
            },
            'orthopedics': {
                'keywords': ['bone', 'fracture', 'joint', 'arthritis', 'x-ray', 'orthopedic', 'spine', 'knee', 'shoulder', 'hip', 'back pain', 'ligament', 'tendon'],
                'symptoms': ['joint pain', 'stiffness', 'swelling', 'limited mobility', 'back pain'],
                'urgency': 'medium'
            },
            'gastroenterology': {
                'keywords': ['stomach', 'digestive', 'endoscopy', 'gastric', 'intestinal', 'liver', 'colon', 'bowel', 'acid reflux', 'ulcer', 'ibs', 'crohn'],
                'symptoms': ['abdominal pain', 'nausea', 'vomiting', 'diarrhea', 'constipation'],
                'urgency': 'medium'
            },
            'endocrinology': {
                'keywords': ['diabetes', 'thyroid', 'hormone', 'blood sugar', 'insulin', 'metabolic', 'glucose', 'endocrine', 'adrenal', 'pituitary'],
                'symptoms': ['excessive thirst', 'frequent urination', 'weight changes', 'fatigue'],
                'urgency': 'medium'
            },
            'dermatology': {
                'keywords': ['skin', 'rash', 'dermatitis', 'lesion', 'mole', 'acne', 'eczema', 'psoriasis', 'melanoma', 'dermal'],
                'symptoms': ['skin irritation', 'rash', 'itching', 'skin changes', 'lesions'],
                'urgency': 'low'
            },
            'internal_medicine': {
                'keywords': ['general', 'internal', 'fever', 'fatigue', 'blood test', 'general checkup', 'routine', 'physical exam'],
                'symptoms': ['general fatigue', 'fever', 'malaise', 'general weakness'],
                'urgency': 'low'
            },
            'psychiatry': {
                'keywords': ['mental', 'depression', 'anxiety', 'psychiatric', 'mood', 'stress', 'bipolar', 'schizophrenia', 'panic', 'ptsd'],
                'symptoms': ['mood changes', 'anxiety', 'depression', 'sleep issues', 'stress'],
                'urgency': 'medium'
            }
        }
        
        self.response_templates = {
            'cardiology': [
                "Your symptoms and test results indicate potential cardiovascular concerns. The {findings} suggest cardiac evaluation is needed.",
                "Based on the {findings} in your reports, I recommend immediate cardiology consultation for proper heart assessment.",
                "The cardiac indicators show {findings}. A cardiologist consultation is essential for comprehensive evaluation."
            ],
            'neurology': [
                "Neurological symptoms detected. The {findings} require specialist attention for proper brain/nervous system evaluation.",
                "Your reports show {findings} which indicate the need for neurological assessment.",
                "Based on {findings}, I strongly recommend consulting a neurologist for comprehensive evaluation."
            ],
            'orthopedics': [
                "Musculoskeletal issues identified. The {findings} suggest orthopedic consultation would be beneficial.",
                "Your symptoms indicate {findings}. An orthopedic specialist can provide proper joint/bone assessment.",
                "Based on {findings}, orthopedic evaluation is recommended for your mobility concerns."
            ],
            'gastroenterology': [
                "Digestive system concerns detected. The {findings} indicate gastroenterological evaluation is needed.",
                "Your symptoms suggest {findings}. A gastroenterologist can provide specialized digestive health assessment.",
                "Based on {findings}, I recommend consulting a gastroenterology specialist."
            ],
            'endocrinology': [
                "Metabolic/hormonal indicators detected. The {findings} suggest endocrine system evaluation.",
                "Your reports show {findings} which may require endocrinologist consultation.",
                "Based on {findings}, hormonal/metabolic assessment by an endocrinologist is recommended."
            ],
            'dermatology': [
                "Skin-related concerns identified. The {findings} require dermatological assessment.",
                "Your symptoms indicate {findings}. A dermatologist can provide proper skin evaluation.",
                "Based on {findings}, dermatological consultation is recommended."
            ],
            'internal_medicine': [
                "General health concerns detected. The {findings} would benefit from internal medicine evaluation.",
                "Your symptoms suggest {findings}. An internal medicine specialist can provide comprehensive assessment.",
                "Based on {findings}, general medical evaluation is recommended."
            ],
            'psychiatry': [
                "Mental health indicators detected. The {findings} suggest psychiatric consultation would be beneficial.",
                "Your symptoms indicate {findings}. A psychiatrist can provide proper mental health assessment.",
                "Based on {findings}, mental health evaluation is recommended."
            ]
        }
    
    def analyze_documents(self, files_content: List[str], user_message: str = "") -> Dict[str, Any]:
        """Analyze medical documents and return recommendations"""
        
        # Combine all text content
        combined_text = " ".join(files_content + [user_message]).lower()
        
        # If no content, provide general guidance
        if not combined_text.strip():
            return {
                'primary_specialty': 'internal_medicine',
                'analysis': "Please provide more details about your symptoms or upload medical documents for a more specific analysis.",
                'confidence': 30,
                'findings': 'insufficient information provided'
            }
        
        # Enhanced keyword matching with scoring
        specialty_scores = {}
        detected_findings = []
        
        for specialty, data in self.medical_keywords.items():
            score = 0
            specialty_findings = []
            
            # Check for keywords
            for keyword in data['keywords']:
                if keyword in combined_text:
                    score += 2
                    specialty_findings.append(keyword)
            
            # Check for symptoms
            for symptom in data['symptoms']:
                if symptom in combined_text:
                    score += 3  # Symptoms weighted higher
                    specialty_findings.append(symptom)
            
            if score > 0:
                specialty_scores[specialty] = {
                    'score': score,
                    'findings': specialty_findings,
                    'urgency': data['urgency']
                }
        
        # Determine primary specialty
        if not specialty_scores:
            # Try partial matching for common words
            if any(word in combined_text for word in ['pain', 'hurt', 'ache', 'sick', 'feel bad']):
                primary_specialty = 'internal_medicine'
                findings = 'general discomfort or pain'
                confidence = 50
            else:
                primary_specialty = 'internal_medicine'
                findings = 'general health concerns'
                confidence = 40
        else:
            # Get specialty with highest score
            best_specialty = max(specialty_scores.keys(), key=lambda x: specialty_scores[x]['score'])
            primary_specialty = best_specialty
            findings = ', '.join(specialty_scores[best_specialty]['findings'][:3])  # Top 3 findings
            confidence = min(specialty_scores[best_specialty]['score'] * 15, 95)
        
        # Generate contextual analysis
        analysis = self.generate_contextual_analysis(primary_specialty, findings, combined_text, user_message)
        
        return {
            'primary_specialty': primary_specialty,
            'analysis': analysis,
            'confidence': confidence,
            'findings': findings,
            'urgency': specialty_scores.get(primary_specialty, {}).get('urgency', 'medium')
        }
    
    def generate_contextual_analysis(self, specialty: str, findings: str, full_text: str, user_message: str) -> str:
        """Generate contextual analysis based on specialty and findings"""
        
        import random
        
        # Get appropriate template
        templates = self.response_templates.get(specialty, self.response_templates['internal_medicine'])
        base_response = random.choice(templates).format(findings=findings)
        
        # Add contextual information based on detected content
        additional_context = []
        
        # Check for urgency indicators
        urgent_words = ['severe', 'intense', 'emergency', 'urgent', 'critical', 'acute', 'sudden']
        if any(word in full_text for word in urgent_words):
            additional_context.append("Given the severity indicated, I recommend seeking medical attention promptly.")
        
        # Check for chronic conditions
        chronic_words = ['chronic', 'ongoing', 'persistent', 'recurring', 'long-term']
        if any(word in full_text for word in chronic_words):
            additional_context.append("This appears to be an ongoing condition that requires consistent medical management.")
        
        # Check for specific medications mentioned
        if any(med in full_text for med in ['medication', 'prescription', 'drug', 'treatment']):
            additional_context.append("Please bring all current medications and treatment history to your appointment.")
        
        # Add user message context if provided
        if user_message and len(user_message.strip()) > 10:
            if 'family history' in user_message.lower():
                additional_context.append("Your family history is important information to share with the specialist.")
            if any(word in user_message.lower() for word in ['worried', 'concerned', 'scared', 'anxious']):
                additional_context.append("Your concerns are valid, and seeking professional medical advice is the right step.")
        
        # Combine base response with context
        if additional_context:
            return base_response + " " + " ".join(additional_context)
        
        return base_response

# Initialize components
db = HealFindDatabase()
medical_ai = MedicalAI()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points (simplified)"""
    # Simple distance calculation (in real app, use proper geolocation)
    return round(((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 * 100, 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/search-medicine', methods=['POST'])
def search_medicine():
    try:
        data = request.get_json()
        medicine_name = data.get('medicine', '').strip()
        manufacturer = data.get('manufacturer', '').strip()
        
        # User location (mock - in real app, get from request)
        user_lat, user_lon = 28.6139, 77.2090
        
        conn = sqlite3.connect('healfind.db')
        cursor = conn.cursor()
        
        # Build query
        query = '''
            SELECT 
                ms.name as shop_name,
                ms.address,
                ms.phone,
                ms.rating,
                ms.latitude,
                ms.longitude,
                m.name as medicine_name,
                m.manufacturer,
                mi.stock_quantity,
                mi.price
            FROM medicine_inventory mi
            JOIN medical_shops ms ON mi.shop_id = ms.id
            JOIN medicines m ON mi.medicine_id = m.id
            WHERE LOWER(m.name) LIKE LOWER(?)
        '''
        
        params = [f'%{medicine_name}%']
        
        if manufacturer:
            query += ' AND LOWER(m.manufacturer) LIKE LOWER(?)'
            params.append(f'%{manufacturer}%')
        
        query += ' AND mi.stock_quantity > 0 ORDER BY ms.rating DESC'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Format results
        medicine_results = []
        for row in results:
            distance = calculate_distance(user_lat, user_lon, row[4], row[5])
            
            medicine_results.append({
                'shopName': row[0],
                'address': row[1],
                'phone': row[2],
                'rating': row[3],
                'medicine': row[6],
                'manufacturer': row[7],
                'stock': row[8],
                'price': f"{row[9]:.2f}",
                'distance': f"{distance} km away"
            })
        
        conn.close()
        
        # Sort by distance
        medicine_results.sort(key=lambda x: float(x['distance'].split()[0]))
        
        return jsonify({
            'success': True,
            'results': medicine_results[:10],  # Limit to top 10 results
            'total_found': len(medicine_results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze-documents', methods=['POST'])
def analyze_documents():
    try:
        message = request.form.get('message', '')
        uploaded_files = request.files.getlist('files')
        
        # Process uploaded files
        files_content = []
        file_info = []
        
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
                file.save(file_path)
                
                # Mock file content extraction (in real app, use proper document parsing)
                if filename.lower().endswith(('.txt',)):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        files_content.append(content)
                else:
                    # For other file types, use filename and message as content
                    files_content.append(f"Medical document: {filename}")
                
                file_info.append({
                    'filename': filename,
                    'size': os.path.getsize(file_path),
                    'type': file.content_type
                })
                
                # Clean up file after processing
                os.remove(file_path)
        
        # If no files but has message, treat as general inquiry
        if not files_content and message:
            return jsonify({
                'success': True,
                'type': 'general_response',
                'response': generate_chat_response(message)
            })
        
        # Analyze documents with AI
        ai_analysis = medical_ai.analyze_documents(files_content, message)
        
        # Get doctor recommendations based on specialty
        doctors = get_doctor_recommendations(ai_analysis['primary_specialty'])
        
        return jsonify({
            'success': True,
            'type': 'doctor_recommendations',
            'analysis': ai_analysis['analysis'],
            'confidence': ai_analysis['confidence'],
            'specialty': ai_analysis['primary_specialty'],
            'doctors': doctors,
            'files_processed': len(file_info),
            'urgency': ai_analysis.get('urgency', 'medium')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_chat_response(message: str) -> str:
    """Generate contextual chat responses based on user message"""
    msg_lower = message.lower()
    
    # Greetings
    if any(greeting in msg_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good evening']):
        return "Hello! I'm HealFind AI, your medical assistant. I can help you find medicines at nearby pharmacies or analyze medical documents to recommend doctors. How can I assist you today?"
    
    # Questions about symptoms
    if any(word in msg_lower for word in ['symptom', 'feel', 'pain', 'hurt', 'sick', 'ache']):
        return "I understand you're experiencing symptoms. For the most accurate recommendations, please upload any medical documents you have (lab reports, X-rays, etc.) and describe your symptoms in detail. This will help me suggest the most appropriate specialists for your condition."
    
    # Specific medical conditions
    if any(word in msg_lower for word in ['diabetes', 'heart', 'cardiac', 'blood pressure']):
        return "I can see you're dealing with a serious medical condition. Please upload your recent medical reports, test results, or prescriptions. I'll analyze them and recommend specialists who are experts in treating your specific condition."
    
    # Questions about doctors
    if any(word in msg_lower for word in ['doctor', 'specialist', 'physician', 'recommend']):
        return "I can recommend doctors based on your medical condition! To provide personalized recommendations, please upload your medical documents or describe your symptoms. I'll analyze them and suggest specialists ranked by experience and success rate in your area."
    
    # Questions about medicines
    if any(word in msg_lower for word in ['medicine', 'pharmacy', 'drug', 'medication', 'prescription']):
        return "For medicine searches, please switch to 'Medicine Search' mode using the tab above. You can search for specific medicines and find nearby pharmacies with stock availability and pricing information."
    
    # Emergency indicators
    if any(word in msg_lower for word in ['emergency', 'urgent', 'critical', 'severe', 'intense']):
        return "⚠️ For medical emergencies, please contact emergency services immediately (911) or visit the nearest emergency room. I'm designed to help with non-emergency medical consultations and recommendations."
    
    # Questions about how it works
    if 'how' in msg_lower and ('work' in msg_lower or 'use' in msg_lower):
        return "HealFind AI works in two modes:\n\n**1. Medicine Search** - Find medicines at nearby pharmacies with prices and stock info\n\n**2. AI Assistant** - Upload medical documents for analysis and get personalized doctor recommendations\n\nWhich would you like to try?"
    
    # Thank you messages
    if any(word in msg_lower for word in ['thank', 'thanks', 'appreciate']):
        return "You're welcome! I'm here to help with your healthcare needs. Feel free to ask me anything about finding medicines or getting doctor recommendations based on your medical documents."
    
    # Default contextual responses
    responses = [
        "I'm here to help with your medical queries! Please upload medical documents for personalized doctor recommendations, or switch to Medicine Search to find nearby pharmacies.",
        "To provide the best assistance, could you tell me more about your medical concerns? You can also upload reports, X-rays, or other medical documents for analysis.",
        "I can analyze medical documents and recommend specialists based on your condition. Please share more details about your symptoms or upload relevant medical files.",
        "For accurate medical recommendations, I'd need more specific information. You can describe symptoms, upload medical reports, or ask about finding medicines at nearby pharmacies."
    ]
    
    # Choose response based on message length and content
    if len(message.split()) > 10:  # Longer messages get more detailed responses
        return responses[1]  # More detailed response
    else:
        return responses[0]  # General response

def get_doctor_recommendations(specialty: str) -> List[Dict[str, Any]]:
    """Get doctor recommendations based on specialty"""
    
    # Map AI specialties to database specialties
    specialty_mapping = {
        'cardiology': 'Cardiologist',
        'neurology': 'Neurologist',
        'orthopedics': 'Orthopedist',
        'gastroenterology': 'Gastroenterologist',
        'endocrinology': 'Endocrinologist',
        'dermatology': 'Dermatologist',
        'internal_medicine': 'Internal Medicine',
        'psychiatry': 'Psychiatrist'
    }
    
    target_specialty = specialty_mapping.get(specialty, 'Internal Medicine')
    user_lat, user_lon = 28.6139, 77.2090
    
    conn = sqlite3.connect('healfind.db')
    cursor = conn.cursor()
    
    # Get doctors of the recommended specialty, ranked by success rate and experience
    cursor.execute('''
        SELECT name, specialty, experience_years, success_rate, total_operations, 
               hospital, address, phone, latitude, longitude, rating
        FROM doctors
        WHERE specialty = ?
        ORDER BY (success_rate * 0.6 + (experience_years * 3) * 0.4) DESC
        LIMIT 5
    ''', (target_specialty,))
    
    doctors = cursor.fetchall()
    
    # If no specialists found, get general practitioners
    if not doctors:
        cursor.execute('''
            SELECT name, specialty, experience_years, success_rate, total_operations, 
                   hospital, address, phone, latitude, longitude, rating
            FROM doctors
            WHERE specialty = 'Internal Medicine'
            ORDER BY (success_rate * 0.6 + (experience_years * 3) * 0.4) DESC
            LIMIT 3
        ''')
        doctors = cursor.fetchall()
    
    conn.close()
    
    # Format doctor recommendations
    doctor_recommendations = []
    for doctor in doctors:
        distance = calculate_distance(user_lat, user_lon, doctor[8], doctor[9])
        
        doctor_recommendations.append({
            'name': doctor[0],
            'specialty': doctor[1],
            'experience': doctor[2],
            'successRate': round(doctor[3], 1),
            'operations': doctor[4],
            'hospital': doctor[5],
            'address': doctor[6],
            'phone': doctor[7],
            'distance': f"{distance} km",
            'rating': doctor[10]
        })
    
    return doctor_recommendations

@app.route('/api/reset-database')
def reset_database():
    """Reset database with fresh sample data"""
    try:
        conn = sqlite3.connect('healfind.db')
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute('DELETE FROM medicine_inventory')
        cursor.execute('DELETE FROM medicines')
        cursor.execute('DELETE FROM medical_shops')
        cursor.execute('DELETE FROM doctors')
        
        conn.commit()
        conn.close()
        
        # Reinitialize with new data
        db.populate_sample_data()
        
        return jsonify({
            'success': True,
            'message': 'Database reset with fresh sample data',
            'medicines_count': 35,
            'shops_count': 8,
            'doctors_count': 8
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Create template directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Copy index.html to templates folder for Flask
    import shutil
    if os.path.exists('index.html'):
        shutil.copy('index.html', 'templates/')
    
    print("🏥 HealFind AI Backend Starting...")
    print("📍 Medicine Search API: /api/search-medicine")
    print("🤖 Document Analysis API: /api/analyze-documents")
    print("💊 Sample medicines loaded in database")
    print("👨‍⚕️ Sample doctors loaded with ranking system")
    print("\n🚀 Starting server on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)