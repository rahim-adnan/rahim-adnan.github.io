from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

SYSTEM_PROMPT = """You are Adnan Rahim's personal AI assistant on his portfolio website. Answer questions about Adnan warmly and professionally. Keep answers SHORT (2-4 sentences max).

ABOUT ADNAN:
- Name: Adnan Rahim
- Role: AI Engineer & Builder
- Location: Budapest, Hungary (open to relocate in Europe)
- Education: BSc Computer Science, ELTE University, 2022-2026
- Scholarship: Stipendium Hungaricum

SKILLS: Python, OpenCV, LangChain, FAISS, HuggingFace, spaCy, RAG, Ollama, LLaMA 3, Groq, Flask, FastAPI, Streamlit, React, pandas, NumPy, Git, Docker, SQL

PROJECTS:
1. Autonomous Drone Control (BSc Thesis) - Python, OpenCV, Flask
2. AI PDF Q&A RAG App - live at ai-pdf-qa.vercel.app
3. Tech Career Skill Tracker - live at tech-career-skill-tracker.onrender.com
4. AI Research Tracker & Interview Coach - Streamlit, Ollama

EXPERIENCE:
- President, AI Development Club at ELTE (50+ members, 10+ workshops)
- Front-End Developer Intern at Limelight Renhold AS, Oslo, Norway
- Learning Methodology Demonstrator at ELTE
- International Student Ambassador at ELTE

CONTACT: rahim.adnanr@gmail.com
AVAILABILITY: Actively seeking AI/ML internships and entry-level roles in Europe.
"""

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 200
        }
    )
    print("Groq response:", response.json())

    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})



@app.route("/")
def home():
    return "Adnan's Portfolio Chatbot API is running!"

if __name__ == "__main__":
    app.run(debug=True)