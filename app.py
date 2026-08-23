import streamlit as st
import os
from google import genai

st.set_page_config(page_title="Bean & Brew Cafe AI", page_icon="☕")
st.title("☕ Bean & Brew - Customer AI Agent")

# API Key ಕಾನ್ಫಿಗರೇಶನ್
API_KEY = "AQ.Ab8RN6JUxJI9eDQgrQ3C9NHiyyUusfEchBrb-jECOsqlJE_hRw"
os.environ["GEMINI_API_KEY"] = API_KEY

client = genai.Client(api_key=API_KEY)

SYSTEM_INSTRUCTION = """
You are a friendly and helpful AI Customer Support Agent for a modern Cafe called "Bean & Brew".

Your responsibilities:
1. Greet customers warmly and answer questions about the menu.
2. Menu items and prices:
   - Espresso: $3.00
   - Cappuccino: $4.50
   - Cold Brew: $4.00
   - Blueberry Muffin: $3.50
   - Chocolate Croissant: $4.00
3. Help customers place their order, calculate the total bill, and confirm the order politely.
4. Keep responses concise, clear, and professional.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about the menu or place an order..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        reply = response.text
    except Exception as e:
        reply = f"Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
