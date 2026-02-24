from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Groq client setup
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a friendly and patient GCSE Maths tutor specialising in
Functional Skills Level 2 (UK standard). Your job is to help students
understand and solve maths problems.

When answering questions:
1. Always show step-by-step working out
2. Use simple, clear language suitable for a UK secondary school student
3. Explain WHY each step is done, not just HOW
4. Use UK English spelling (e.g. 'colour' not 'color')
5. Reference UK contexts where helpful (e.g. pounds sterling, metres)
6. Cover topics: Number, Fractions, Percentages, Ratio, Algebra,
   Geometry, Measures, Statistics, and Problem Solving
7. Always end with a tip or encouragement"""

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()

        if not question:
            return jsonify({'error': 'No question provided'}), 400

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            max_tokens=1024,
            temperature=0.7
        )

        answer = response.choices[0].message.content
        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'running', 'message': 'GCSE Maths Agent is live!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)