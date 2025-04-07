# verbi_irregolari_app come pagina multipla
import streamlit as st
import random
import json
import os

MAX_QUESTIONS = 10
PDF_FILE = "IrregularVerbs.pdf"
JSON_FILE = "all_verbs.json"

motivazioni = {
    10: "👏 Perfetto! Continua così!",
    9: "🌟 Distinto! Ottimo lavoro!",
    8: "💪 Buono! Hai studiato bene.",
    7: "👍 Discreto! Qualche ripasso e sei al top.",
    6: "🙂 Sufficiente! Hai le basi, continua ad allenarti.",
    5: "⚠️ Insufficiente, ma ci sei quasi!",
    4: "😅 C'è da lavorare un po', forza!",
    3: "💤 Serve più allenamento, non mollare!",
    2: "😕 Forse è il momento di ripassare...",
    1: "🔁 Dai, riprova: la pratica rende perfetti!",
    0: "🤯 Forza! Ogni errore è un passo avanti."
}

with open(JSON_FILE, "r") as f:
    verbs = json.load(f)

if "index" not in st.session_state:
    st.session_state.index = random.randint(0, len(verbs) - 1)
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "show_next" not in st.session_state:
    st.session_state.show_next = False
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "errors" not in st.session_state:
    st.session_state.errors = []

st.title("📘 Irregular Verbs – Training")

if st.session_state.question_count >= MAX_QUESTIONS:
    voto = round(st.session_state.score * 10 / MAX_QUESTIONS)
    giudizio = (
        "🔴 Gravemente insufficiente" if voto <= 3 else
        "🟠 Insufficiente" if voto == 4 else
        "🟡 Quasi sufficiente" if voto == 5 else
        "🟢 Sufficiente" if voto == 6 else
        "🔵 Discreto" if voto == 7 else
        "🔵 Buono" if voto == 8 else
        "🔵 Distinto" if voto == 9 else
        "🟣 Ottimo"
    )

    st.subheader("✅ Test completato!")
    st.write(f"**Punteggio:** {st.session_state.score} su {MAX_QUESTIONS}")
    st.write(f"**Voto:** {voto}/10 – {giudizio}")
    st.write(motivazioni.get(voto, ""))

    if st.session_state.errors:
        st.markdown("---")
        st.subheader("📊 Errori commessi")
        for err in st.session_state.errors:
            st.markdown(
                f"""<div style='color: red; margin-bottom: 1em;'>
                <b>{err['Base Form']}</b><br>
                ❌ Your Past: <i>{err['Your Past']}</i> — ✅ Correct: {err['Correct Past']}<br>
                ❌ Your Participle: <i>{err['Your Participle']}</i> — ✅ Correct: {err['Correct Participle']}
                </div>""",
                unsafe_allow_html=True
            )
    else:
        st.success("👏 Nessun errore! Complimenti!")

    if st.button("🔁 Nuova partita"):
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.index = random.randint(0, len(verbs) - 1)
        st.session_state.show_next = False
        st.session_state.feedback = ""
        st.session_state.errors = []
        st.rerun()
    st.stop()

verb = verbs[st.session_state.index]
st.write(f"**Base form:** `{verb['base']}`")

if not st.session_state.show_next:
    with st.form("quiz"):
        past_input = st.text_input("Simple Past")
        part_input = st.text_input("Past Participle")
        submitted = st.form_submit_button("Check")

        if submitted:
            past_clean = past_input.strip().lower()
            part_clean = part_input.strip().lower()
            past_ok = past_clean in verb["past"]
            part_ok = part_clean in verb["participle"]
            st.session_state.question_count += 1

            risposta = (
                f"**Simple Past:** {', '.join(verb['past'])}<br>"
                f"**Past Participle:** {', '.join(verb['participle'])}"
            )

            if past_ok and part_ok:
                st.session_state.feedback = f"✅ Corretto!<br>{risposta}"
                st.session_state.score += 1
            else:
                st.session_state.feedback = f"❌ Sbagliato!<br>{risposta}"
                st.session_state.errors.append({
                    "Base Form": verb["base"],
                    "Your Past": past_input,
                    "Correct Past": ", ".join(verb["past"]),
                    "Your Participle": part_input,
                    "Correct Participle": ", ".join(verb["participle"])
                })

            st.session_state.show_next = True
            st.rerun()
else:
    st.markdown(st.session_state.feedback, unsafe_allow_html=True)
    if st.button("➡️ Prossima domanda"):
        st.session_state.index = random.randint(0, len(verbs) - 1)
        st.session_state.show_next = False
        st.session_state.feedback = ""
        st.rerun()

st.divider()
with open(PDF_FILE, "rb") as f:
    st.download_button("📥 Scarica PDF", f, file_name=PDF_FILE, mime="application/pdf")
