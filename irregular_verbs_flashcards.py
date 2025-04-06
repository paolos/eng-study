import streamlit as st
import random
import json

JSON_FILE = "all_verbs.json"

with open(JSON_FILE, "r") as f:
    verbs = json.load(f)

# Init session state
if "card_index" not in st.session_state:
    st.session_state.card_index = random.randint(0, len(verbs) - 1)
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# Seleziona un verbo a caso
verb = verbs[st.session_state.card_index]

# Random: tipo domanda
question_type = random.choice(["past", "participle"])
question_text = (
    f"What is the **simple past** of **{verb['base']}**?"
    if question_type == "past"
    else f"What is the **past participle** of **{verb['base']}**?"
)

st.title("🃏 Irregular Verbs Flashcards")

st.markdown(f"### {question_text}")

if not st.session_state.show_answer:
    if st.button("🔄 Show Answer"):
        st.session_state.show_answer = True
else:
    answer = ", ".join(verb[question_type])
    st.markdown(f"### ✅ Answer: `{answer}`")
    if st.button("➡️ Next"):
        st.session_state.card_index = random.randint(0, len(verbs) - 1)
        st.session_state.show_answer = False
        st.rerun()

st.divider()
st.page_link("verbi_irregolari_app.py", label="⬅️ Back to Training App")
