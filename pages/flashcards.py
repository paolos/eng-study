import streamlit as st
import random
import json

JSON_FILE = "all_verbs.json"

# Load data
with open(JSON_FILE, "r") as f:
    verbs = json.load(f)

# Init session state
if "card_index" not in st.session_state:
    st.session_state.card_index = random.randint(0, len(verbs) - 1)
if "question_type" not in st.session_state:
    st.session_state.question_type = random.choice(["past", "participle"])
if "flipped" not in st.session_state:
    st.session_state.flipped = False

# Select current verb
verb = verbs[st.session_state.card_index]
tense = st.session_state.question_type
tense_label = "SIMPLE PAST" if tense == "past" else "PAST PARTICIPLE"
answer = ", ".join(verb[tense])

# Page setup
st.set_page_config(page_title="Flashcard", layout="centered")
st.markdown("<h2 style='text-align:center;'>🃏 Flashcard – Irregular Verbs</h2>", unsafe_allow_html=True)

# --- Styles ---
st.markdown("""
<style>
.flashcard {
    background-color: #E8F6F3;
    color: #1B4F72;
    font-size: 1.6rem;
    font-weight: bold;
    border-radius: 15px;
    padding: 2rem;
    min-height: 200px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    text-align: center;
    width: 340px;
    margin: 2rem auto 1rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 2.2rem;
}
.center-button {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# --- CARD ---
if not st.session_state.flipped:
    st.markdown(f"""
    <div class='flashcard'>
        <div>
        ❓<br>
        What is the<br>
        {tense_label}<br>
        of<br>
        {verb['base'].upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='center-button'>", unsafe_allow_html=True)
        if st.button("💡 Answer"):
            st.session_state.flipped = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div class='flashcard'>
        ✅ {answer}
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='center-button'>", unsafe_allow_html=True)
        if st.button("➡️ Next"):
            st.session_state.card_index = random.randint(0, len(verbs) - 1)
            st.session_state.question_type = random.choice(["past", "participle"])
            st.session_state.flipped = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
