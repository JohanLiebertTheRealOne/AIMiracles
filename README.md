# ⚡ Content Idea Generator — 1-Hour MVP

A **fast, AI-powered content idea generator** built with **Streamlit** and the **OpenAI API**.  
Generate actionable, creative content ideas in seconds for blogs, social media, newsletters, video hooks, or marketing campaigns.

---

## 📝 Features

- Generate **5–20 content ideas** per topic.
- Supports **custom styles** (Listicle, How-to, Twitter thread, Video hook, Newsletter subject).
- Supports **tones** like Practical, Persuasive, Funny, Curious, or Controversial.
- **Copy or download** ideas as TXT or CSV.
- Minimalistic **1-hour MVP** designed for rapid iteration.
- Powered by **OpenAI GPT models** for creative, high-quality outputs.

---

## 🚀 Demo

![Screenshot](screenshot.png)  
*Example: generating content ideas for “Vegan Breakfast Recipes”.*

---

## 🛠 Installation

### Prerequisites
- Python **3.10+**
- OpenAI API key (get one from the OpenAI dashboard)

### Quick Setup

1. Clone the repository:
    
    - git clone https://github.com/yourusername/content-idea-generator.git
    - cd content-idea-generator

2. Make the setup script executable and run it:

    chmod +x setup_and_run.sh
    ./setup_and_run.sh

This script will create a virtual environment, install dependencies, and launch the app automatically.

### Manual Setup (alternative)

    # Create and activate virtual environment
    python3 -m venv .venv
    source .venv/bin/activate

    # Upgrade pip and install dependencies
    pip install --upgrade pip
    pip install streamlit openai

    # Set your OpenAI API key
    export OPENAI_API_KEY="YOUR_KEY_HERE"  # macOS / Linux
    REM set OPENAI_API_KEY=YOUR_KEY_HERE   # Windows (cmd)
    $env:OPENAI_API_KEY="YOUR_KEY_HERE"    # Windows (PowerShell)

    # Run the app
    streamlit run main.py

---

## 🖱 Usage

    Enter your topic or niche in the main input box.

    Adjust settings in the sidebar:
        - Number of ideas
        - Creativity (temperature)
        - Style and Tone

    Click "Generate Ideas".

Optional actions:
    - Generate more ideas with “Generate More (append)”
    - Copy all ideas or download as TXT/CSV
    - Clear ideas to start a new topic

> For best results, use specific topics (e.g., “AI tools for content creators” rather than just “AI”).

---

## ⚡ Tips

    - Higher temperature → more creative ideas.
    - Lower temperature → more practical, focused ideas.
    - Narrow topics + specific style → higher-quality outputs.

---

## 🧩 Tech Stack

    - Python 3.10+
    - Streamlit — Rapid UI for Python
    - OpenAI GPT API — AI content generation

---

## 🔒 Security

    - Never share your OpenAI API key publicly.
    - Recommended: store it in an environment variable or enter it in the app sidebar at runtime.

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

---

## ✨ Contribution

    - Feel free to fork, star, and submit PRs!
    - Suggest new features, styles, or templates via issues or pull requests.

---

## 📌 References

    - OpenAI Python SDK v1.0+
    - Streamlit Documentation
