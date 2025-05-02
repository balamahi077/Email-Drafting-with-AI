import streamlit as st
from openai import OpenAI

import requests

st.set_page_config(page_title="Email Drafting Assistant", layout="centered")
st.title("📧 Email Drafting Assistant")
st.markdown("Generate well-written emails with the help of AI.")

# Initialize session state
if "email" not in st.session_state:
    st.session_state.email = ""
if "translated_email" not in st.session_state:
    st.session_state.translated_email = ""

# API key input
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# Language options
language = st.selectbox("🌍 Choose Language for Output", ["English", "Hindi", "Telugu", "Spanish", "French", "German", "Japanese"])

# Proceed only if API key is provided
if api_key:
    client = OpenAI(api_key=api_key)

    recipient = st.text_input("Recipient (e.g. John, Hiring Manager)")
    purpose = st.text_area("What’s the purpose of the email?")
    tone = st.selectbox("Tone of the email", ["Formal", "Friendly", "Persuasive", "Apologetic", "Thankful", "Neutral"])
    extra = st.text_area("Any additional information to include?")

    if st.button("Generate Email"):
        if not purpose:
            st.warning("Please provide the purpose of the email.")
        else:
            with st.spinner("Drafting your email..."):
                prompt = (
                    f"Write an email to {recipient or 'a recipient'}.\n"
                    f"Purpose: {purpose}\n"
                    f"Tone: {tone}\n"
                    f"Additional Info: {extra}\n"
                    f"Format it like a professional email with greeting and closing."
                )

                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    st.session_state.email = response.choices[0].message.content
                    st.success("Here's your draft:")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    # Show generated email
    if st.session_state.email:
        st.text_area("Generated Email", st.session_state.email, height=300)

    # Translation logic
    if st.session_state.email and language != "English":
        if st.button("🌐 Translate Email"):
            translate_prompt = f"Translate the following email to {language}:\n\n{st.session_state.email}"
            try:
                with st.spinner(f"Translating to {language}..."):
                    translation = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": translate_prompt}],
                        temperature=0.3
                    )
                    st.session_state.translated_email = translation.choices[0].message.content
            except Exception as e:
                st.error(f"Translation error: {e}")

    # Show translated email
    if st.session_state.translated_email:
        st.text_area(f"📜 Translated Email in {language}", st.session_state.translated_email, height=300)
