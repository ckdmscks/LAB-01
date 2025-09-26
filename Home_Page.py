# Home_Page.py
import streamlit as st
import importlib
from pathlib import Path

# -----------------------------
# Title of App
# -----------------------------
st.title("Web Development Lab01")

# -----------------------------
# Assignment Data
# -----------------------------
st.header("CS 1301")
st.subheader("Web Development - Section X")  # ← change X to your section

# Try to get your name from info.py; fallback to a placeholder
try:
    info = importlib.import_module("info")
    your_name = getattr(info, "name", None) or getattr(info, "full_name", None) or "Your Name"
except Exception:
    your_name = "Your Name"

st.subheader(your_name)

# -----------------------------
# Discover pages in /pages
# -----------------------------
base_dir = Path(__file__).parent.resolve()
pages_dir = base_dir / "pages"

def pretty_title(fname: str) -> str:
    # "PhaseII.py" -> "Phase II"; "Portfolio.py" -> "Portfolio"
    stem = Path(fname).stem
    pretty = "".join((" " + c if c.isupper() else c) for c in stem).strip().title()
    return " ".join(pretty.split())

found_pages = []
portfolio_exists = False
phase2_exists = False

if pages_dir.exists():
    for p in sorted(pages_dir.glob("*.py")):
        if p.name.startswith("_"):
            continue
        if p.name.lower() == "portfolio.py":
            portfolio_exists = True
            found_pages.append(p.name)
        elif p.name.lower() == "phaseii.py":
            phase2_exists = True
            found_pages.append(p.name)

# Build the numbered list for the intro block
lines = []
for i, name in enumerate(found_pages, start=1):
    title = pretty_title(name)
    if name.lower() == "portfolio.py":
        desc = "My personal portfolio with skills, projects, and experience."
    elif name.lower() == "phaseii.py":
        desc = "Neuro-themed BuzzFeed-style quiz (≥5 questions, ≥3 input types, ≥3 images)."
    else:
        desc = "Custom page."
    lines.append(f"{i}. **{title}** — {desc}")

# -----------------------------
# Introduction (now filled)
# -----------------------------
intro_numbered = "\n".join(lines) if lines else "1.\n2.\n3."
st.write(f"""
Welcome to our Streamlit Web Development Lab01 app! You can navigate between the pages using the sidebar to the left. The following pages are:

{intro_numbered}

""")

# -----------------------------
# Quick open buttons (no tips)
# -----------------------------
if found_pages:
    st.markdown("### Open a page")
    has_switch = hasattr(st, "switch_page")

    # Dedicated Portfolio button first (uses info.py)
    if portfolio_exists:
        if has_switch:
            if st.button("👤 Open Portfolio (info.py)"):
                st.switch_page("pages/Portfolio.py")
        else:
            st.markdown("- **Portfolio** — open it from the sidebar.")

    # Phase II button
    if phase2_exists:
        if has_switch:
            if st.button("🧠 Open Phase II (Quiz)"):
                st.switch_page("pages/PhaseII.py")
        else:
            st.markdown("- **Phase II (Quiz)** — open it from the sidebar.")
