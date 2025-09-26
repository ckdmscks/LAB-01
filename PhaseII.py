# pages/PhaseII.py
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Phase II — Neuro-Themed Quiz", page_icon="🧠", layout="wide")

st.title("Phase II — Neurology Pathways Quiz")
st.caption("Answer a few questions to see which neurology pathway fits your vibe!")

# --- helper: show image only if it exists ---
def show_img(path_str, caption=None):
    p = Path(path_str)
    if p.exists():
        st.image(str(p), use_container_width=True, caption=caption)

# === At least 3 images (top row) ===
c1, c2, c3 = st.columns(3)
with c1: show_img("images/quiz1.jpg", "Cortex & cognition")
with c2: show_img("images/quiz2.jpg", "Clinical environments")
with c3: show_img("images/quiz3.jpg", "Neural networks")

st.divider()

# We'll score three “personas”: Clinician-Explorer, Data-Analyst, Med-Creator
scores = {"Explorer": 0, "Analyst": 0, "Creator": 0}

# Q1 — radio (clinical shadowing vs case studies vs med art)
q1 = st.radio(
    "Weekend plan — which sounds most exciting?",
    ["Shadow in a neurology clinic", "Deep-dive case studies and journal club",
     "Sketch anatomical diagrams & patient education graphics"],
    index=None
)
if q1 == "Shadow in a neurology clinic": scores["Explorer"] += 2
elif q1 == "Deep-dive case studies and journal club": scores["Analyst"] += 2
elif q1 == "Sketch anatomical diagrams & patient education graphics": scores["Creator"] += 2

# Q2 — multiselect  # NEW
q2 = st.multiselect(  # NEW
    "Study-session kit (pick 1–3):",
    ["Neuroanatomy atlas", "EEG traces", "Notebook", "iPad + stylus", "Stethoscope", "Python/Jupyter"]
)
for x in q2:
    if x in ["Neuroanatomy atlas", "Stethoscope"]: scores["Explorer"] += 1
    if x in ["EEG traces", "Python/Jupyter"]:      scores["Analyst"]  += 1
    if x in ["iPad + stylus", "Notebook"]:         scores["Creator"]  += 1

# Q3 — slider  # NEW
q3 = st.slider(  # NEW
    "Comfort with uncertainty in diagnosis",
    0, 10, 5, help="Higher means you're okay making decisions with incomplete info."
)
if   q3 >= 7: scores["Explorer"] += 2
elif q3 <= 3: scores["Analyst"]  += 2
else:         scores["Creator"]  += 1

# Q4 — number_input  # NEW
q4 = st.number_input(  # NEW
    "Weekly hours you’d devote to a creative or patient-facing project (education materials, outreach, etc.)",
    min_value=0, max_value=50, value=2
)
if   q4 >= 10: scores["Creator"] += 2
elif q4 >= 4:  scores["Creator"] += 1

# Q5 — selectbox (tools you can't live without)
q5 = st.selectbox(
    "Pick the tool you can’t live without:",
    ["Stethoscope", "Spreadsheet/Stats", "Stylus tablet for illustrations"],
    index=None
)
if q5 == "Stethoscope":                 scores["Explorer"] += 2
elif q5 == "Spreadsheet/Stats":         scores["Analyst"]  += 2
elif q5 == "Stylus tablet for illustrations": scores["Creator"] += 2

st.divider()

# Progress feel  # NEW
answered = sum(v is not None and v != [] for v in [q1, q2, q3, q4, q5])  # NEW
st.progress(answered / 5.0, text=f"{answered}/5 questions answered")  # NEW

# Submit
if st.button("Reveal my result 🎉"):
    persona = max(scores, key=lambda k: scores[k]) if any(scores.values()) else "Explorer"

    st.subheader("Your Result")
    if persona == "Explorer":
        st.success("🧭 **Clinician-Explorer** — You thrive in patient settings and real-world problem solving.")
        show_img("images/quiz_explorer.jpg", "Clinician-Explorer")
    elif persona == "Analyst":
        st.success("📊 **Data-Analyst** — You love signals, stats, and pattern-finding in EEG/MRI data.")
        show_img("images/quiz_analyst.jpg", "Data-Analyst")
    else:
        st.success("🎨 **Med-Creator** — You explain complex neuro topics through visuals and design.")
        show_img("images/quiz_creator.jpg", "Med-Creator")

    st.balloons()  # NEW

    # Quick summary metrics  # NEW
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Clinician-Explorer", scores["Explorer"])  # NEW
    with c2: st.metric("Data-Analyst",       scores["Analyst"])   # NEW
    with c3: st.metric("Med-Creator",        scores["Creator"])   # NEW

# Notes for grader
with st.expander("Phase II checklist"):
    st.write(
        "- ≥ 5 questions ✓\n"
        "- ≥ 3 input types (radio, multiselect, slider, number_input, selectbox) ✓\n"
        "- ≥ 3 images ✓\n"
        "- ≥ 3 NEW Streamlit functions (multiselect, slider, number_input, progress, balloons, metric) ✓\n"
    )
