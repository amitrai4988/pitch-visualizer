# 🎬 Pitch Visualizer

Convert a story into a visual storyboard using AI.

## 🚀 Features
- Text → Scene segmentation
- AI prompt enhancement
- Image generation (DALL·E)
- Visual storyboard output

## 🛠️ Setup

1. Clone repo:
   git clone <your-repo-url>
   cd pitch-visualizer

2. Install dependencies:
   pip install -r requirements.txt

3. Add your OpenAI API key:
   Replace in app.py:
   client = OpenAI(api_key="YOUR_API_KEY")

4. Run app:
   python app.py

5. Open browser:
   http://127.0.0.1:5000/

## 🧠 How it Works
1. Splits story into sentences
2. Enhances each sentence into visual prompts
3. Generates images using AI
4. Displays storyboard

## ✨ Future Improvements
- Better scene detection (LLM)
- Animation support
- Character consistency