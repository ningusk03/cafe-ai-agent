import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Bean & Brew Cafe AI", page_icon="☕", layout="centered")

# Groq API Key
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# Cafe rules
SYSTEM_INSTRUCTION = """
You are the friendly, witty, and efficient AI Assistant for 'Bean & Brew Cafe'.
Your goal is to assist customers with menu inquiries, coffee recommendations, pricing, store hours, and taking mock orders.

Menu:
- Espresso: $3.00
- Cappuccino: $4.50
- Cafe Latte: $4.50
- Cold Brew: $4.00
- Croissant (Butter/Chocolate): $3.50
- Blueberry Muffin: $3.00
- Avocado Toast: $6.50

Opening Hours: Mon-Sun: 7:00 AM - 8:00 PM.
Location: 123 Coffee Lane, Silicon Valley.

Keep answers crisp, conversational, polite, and coffee-enthusiastic!
"""

st.title("☕ Bean & Brew - Customer AI Agent")
st.write("Welcome to Bean & Brew! Ask about our menu, specials, or hours.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something (e.g., 'What is on the menu?')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Brewing a response..."):
            try:
                messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
                for m in st.session_state.messages:
                    messages.append({"role": m["role"], "content": m["content"]})

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                )
                bot_reply = response.choices[0].message.content
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Error: {e}")
