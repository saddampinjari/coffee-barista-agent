import json
import os
from google.adk.agents import LlmAgent

# Load menu data into memory for RAG lookups
def load_menu():
    with open("menu.json", "r") as f:
        return json.load(f)

# Tool function used by the ADK Agent to retrieve ground-truth menu data
def search_menu(query: str = "") -> list:
    """Searches the coffee shop menu for matching items or allergens."""
    menu = load_menu()
    if not query:
        return menu
    
    query = query.lower()
    results = [
        item for item in menu
        if query in item["name"].lower() or query in item["description"].lower() or query in item["category"].lower()
    ]
    return results if results else menu

# Initialize the ADK Agent
def get_barista_agent():
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    return LlmAgent(
        name="barista_agent",  # Required field
        model=model_name,
        instruction=(          # Changed from system_instruction to instruction
            "You are a friendly and helpful AI Barista for a coffee shop. "
            "Always use the search_menu tool to check prices, items, and allergen information. "
            "Do not make up menu items that are not in the dataset."
        ),
        tools=[search_menu]
    )