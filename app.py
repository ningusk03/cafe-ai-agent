import streamlit as st
import requests

st.set_page_config(page_title="Bean & Brew Cafe AI", page_icon="☕")
st.title("☕ Bean & Brew - Customer AI Agent")

API_KEY = "AQ.Ab8RN6JUxJI9eDQgrQ3C9NHiyyUusfEchBrb-jECOsqlJE_hRw"

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

def get_gemini_reply(user_msg):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_msg}]
            }
        ]
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error ({res.status_code}): {res.text}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about the menu or place an order..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = get_gemini_reply(prompt)

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
