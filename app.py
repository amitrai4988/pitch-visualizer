import os
import random
from flask import Flask, render_template, request
from nltk.tokenize import sent_tokenize
import nltk
from dotenv import load_dotenv
import google.generativeai as genai

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

# -------------------------------
# Download NLTK data
# -------------------------------
nltk.download('punkt')
nltk.download('punkt_tab')

app = Flask(__name__)

# -------------------------------
# Gemini Setup
# -------------------------------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    model = None


# -------------------------------
# 1. Split story into scenes
# -------------------------------
def split_story(text):
    return sent_tokenize(text)[:5]


# -------------------------------
# 2. Generate VISUAL PROMPT 🔥
# -------------------------------
def generate_prompt(sentence, style):
    try:
        if model:
            response = model.generate_content(
                f"""
                Convert this into a short visual description (max 12 words).

                Scene: {sentence}
                Style: {style}

                Focus on: people, environment, action.
                """
            )
            return response.text.strip()

        else:
            return f"{sentence}, office, people, business"

    except Exception as e:
        print("❌ Gemini Error:", e)
        return "office, people, business"


# -------------------------------
# 3. Generate IMAGE (SMART SEED 🔥)
# -------------------------------
def generate_image(prompt):
    try:
        # Clean prompt → convert to seed
        cleaned = "".join(e for e in prompt if e.isalnum())
        
        # Add randomness + meaning
        seed = cleaned[:20] + str(random.randint(1, 9999))

        return f"https://picsum.photos/seed/{seed}/512/512"

    except Exception as e:
        print("❌ Image Error:", e)
        return "https://picsum.photos/512/512"


# -------------------------------
# 4. Create storyboard
# -------------------------------
def create_storyboard(text, style):
    scenes = split_story(text)
    storyboard = []

    for scene in scenes:
        prompt = generate_prompt(scene, style)
        image_url = generate_image(prompt)

        print("\n--- DEBUG ---")
        print("Scene:", scene)
        print("Visual Prompt:", prompt)
        print("Image URL:", image_url)

        storyboard.append({
            "text": scene,
            "prompt": prompt,
            "image": image_url
        })

    return storyboard


# -------------------------------
# ROUTES
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['story']
    style = request.form['style']

    if not text.strip():
        return "⚠️ Please enter a story."

    storyboard = create_storyboard(text, style)
    return render_template('result.html', storyboard=storyboard)


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)