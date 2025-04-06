import streamlit as st
import random
import json
import os

# Carica la lista dei verbi dal file JSON
with open("verbi_irregolari_completi.json", "r") as f:
    verbs = json.load(f)

# Stato iniziale
if "index" not in st.session_state:
    st.session_state.index = random.randint(0, len(verbs) - 1)
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

st.title("🧠 Allenamento Verbi Irregolari")

verb = verbs[st.session_state.index]
st.write(f"**Base form:** `{verb['base']}`")

with st.form("quiz"):
    past_input = st.text_input("Simple Past")
    part_input = st.text_input("Past Participle")
    submitted = st.form_submit_button("Check")

    if submitted:
        st.session_state.attempts += 1
        past_ok = past_input.strip().lower() in verb["past"]
        part_ok = part_input.strip().lower() in verb["participle"]

        if past_ok and part_ok:
            st.success("✅ Corretto!")
            st.session_state.score += 1
        else:
            st.error("❌ Sbagliato")
            st.write(f"Risposta corretta:")
            st.write(f"**Simple Past:** {', '.join(verb['past'])}")
            st.write(f"**Past Participle:** {', '.join(verb['participle'])}")

        # Passa al verbo successivo
        st.session_state.index = random.randint(0, len(verbs) - 1)

st.write(f"**Punteggio:** {st.session_state.score} su {st.session_state.attempts}")

# 📄 Download del PDF
pdf_path = "verbi_irregolari_completi.pdf"
if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Scarica tabella completa (PDF)",
            data=f,
            file_name="verbi_irregolari_completi.pdf",
            mime="application/pdf"
        )
else:
    st.warning("PDF non trovato. Assicurati che 'verbi_irregolari_completi.pdf' sia nella stessa cartella.")
