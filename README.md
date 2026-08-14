# ☕ AI Coffee Barista Agent

An interactive, AI-powered Coffee Barista application built with **Streamlit**, **Google Agent Development Kit (ADK)**, and **Google Gemini AI**.

The application features a modern, custom-designed coffee shop menu interface alongside an intelligent AI Barista chatbot capable of answering questions about menu items, prices, ingredients, recommendations, and allergen information in real time.

---

## ✨ Features

- **🎨 Modern Coffee Menu Interface**: Interactive horizontal scrolling coffee menu with visual badges, volume details, ratings, and pricing.
- **🤖 Intelligent AI Barista Agent**: Built using Google ADK `LlmAgent` and powered by `gemini-3.5-flash`.
- **🔍 Ground-Truth Tool Calling**: Equipped with a custom `search_menu` function tool to query ground-truth coffee shop dataset (`menu.json`) and prevent hallucinations.
- **🛡️ Custom CSS & Clean UI**: Styled with modern typography, coffee-themed dark/warm color palette, and streamlined interface (Streamlit toolbar hidden).
- **⚡ Session Continuity**: Integrated with ADK `InMemorySessionService` and `Runner` for session management.

---

## 📁 Project Structure

```
coffee-barista-agent/
├── app.py           # Streamlit web application (UI, CSS theme, ADK Runner integration)
├── agent.py         # Google ADK Agent configuration & search_menu function tool
├── menu.json        # Coffee shop menu database (Items, categories, prices, allergens)
├── requirements.txt # Python package dependencies
├── .gitignore       # Git ignore rules for virtual env and secrets
└── README.md        # Project documentation
```


---

## 🛠️ Prerequisites & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd coffee-barista-agent
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```


### 4. Configure Environment Variables
Create or edit the `.env` file in the root directory:
```env
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
GEMINI_MODEL="gemini-3.5-flash"
```

---

## 🚀 Running the Application

Launch the Streamlit app locally:
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` to interact with the AI Barista!

---

## 💡 Example Queries to Ask the Barista

- *"What coffee drinks do you have on the menu?"*
- *"Do you have any vegan milk options?"*
- *"What is your cheapest coffee option?"*
- *"Are there any allergens in the Almond Milk Cappuccino or Butter Croissant?"*
- *"What tea or non-coffee items do you serve?"*

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
