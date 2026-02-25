# ✈️ TripFluencer — AI Travel Itinerary Generator

TripFluencer is an AI-powered travel planning web application that generates personalized travel itineraries based on user preferences.  
The project combines a FastAPI backend with a dynamic HTML/CSS/JavaScript frontend and integrates Google's Gemini API for intelligent itinerary generation.

---

## 🚀 Features

- 🤖 AI-generated travel itineraries using Gemini API
- ⚡ FastAPI backend for high-performance API handling
- 🎨 Interactive frontend built with HTML, CSS, and JavaScript
- 🔄 Dynamic request–response workflow
- 📁 Structured production-style project architecture

---

## 🛠️ Tech Stack

**Backend**
- FastAPI
- Python
- Google Generative AI (Gemini)

**Frontend**
- HTML5
- CSS3
- JavaScript

**Tools**
- Git & GitHub
- REST APIs

---

## 📂 Project Structure
```TripFluencer/
│
├── main.py # FastAPI backend
├── requirements.txt # Dependencies
│
├── templates/
│ └── index.html # Frontend UI
│
├── static/
│ ├── styles.css # Styling
│ └── script.js # Frontend logic
```
---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
git clone https://github.com/AnanyaGupta07/TRIPFLUENCER.git

cd TRIPFLUENCER

### 2️⃣ Create virtual environment
```python -m venv .venv
source .venv/bin/activate # Mac/Linux
```

### 3️⃣ Install dependencies
```pip install -r requirements.txt```

### 4️⃣ Add Environment Variable

Create a `.env` file:
```GEMINI_API_KEY=your_api_key_here```

## ▶️ Run the Application
```uvicorn main:app --reload```

Open in browser:```http://127.0.0.1:8000```

---

## 🧠 How It Works

1. User enters travel preferences in the UI.
2. Frontend sends request to FastAPI backend.
3. Backend calls Gemini API to generate itinerary.
4. AI response is returned and displayed dynamically.

---

## 📌 Future Improvements

- Add user authentication
- Save itineraries to database
- Deploy on cloud (Render / Railway / AWS)
- Improve prompt engineering for smarter travel plans

---

## 👩‍💻 Author

**Ananya Gupta**  
BTech (AI & Data Science) 
Linkedin:(https://www.linkedin.com/in/ananya-gupta-4a5a81332/)




