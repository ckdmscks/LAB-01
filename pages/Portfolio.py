import streamlit as st
from pathlib import Path
import importlib
import inspect

# =========================
# Page setup
# =========================
st.set_page_config(page_title="Portfolio", page_icon="👋", layout="wide")

# =========================
# Load info.py (DO NOT CHANGE info.py)
# =========================
try:
    info = importlib.import_module("info")
except Exception as e:
    st.error("Couldn't import info.py. Make sure an info.py file is in the same folder.")
    st.exception(e)
    st.stop()

# =========================
# Helpers (super tolerant to ANY info.py shape)
# =========================
SKIP_KEYS = {
    "__builtins__","__cached__","__doc__","__file__","__loader__","__name__","__package__","__spec__",
}

def exists(pathstr: str) -> bool:
    try:
        return bool(pathstr) and isinstance(pathstr, str) and Path(pathstr).expanduser().exists()
    except Exception:
        return False


def as_list(x):
    if x is None:
        return []
    if isinstance(x, (list, tuple, set)):
        return list(x)
    if isinstance(x, str):
        if "\n" in x:
            return [ln.strip() for ln in x.splitlines() if ln.strip()]
        return [x]
    return [x]


def key_title(k: str) -> str:
    return k.replace("_", " ").strip().title()


def is_url(s: str) -> bool:
    return isinstance(s, str) and (s.startswith("http://") or s.startswith("https://"))


def pill(text: str):
    st.markdown(
        f"""
        <span style='display:inline-block;padding:6px 12px;border-radius:999px;border:1px solid var(--accent,#e0e0e0);margin:4px 6px 0 0'>
            {text}
        </span>
        """,
        unsafe_allow_html=True,
    )

# (Full rendering functions for dicts, lists, values, etc.)
def render_list_of_dicts(items, section_guess: str = "Items"):
    for d in items:
        if not isinstance(d, dict):
            st.write("- ", d)
            continue
        with st.container(border=True):
            title = d.get("title") or d.get("name") or d.get("role") or d.get("position") or d.get("school") or d.get("company")
            subtitle = d.get("company") or d.get("organization") or d.get("school") or d.get("location")
            start = d.get("start") or d.get("from")
            end = d.get("end") or d.get("to")
            dates = f"{start or ''} – {end or 'Present'}" if (start or end) else None
            image = d.get("image") or d.get("logo")
            link = d.get("link") or d.get("url")
            repo = d.get("repo") or d.get("github")
            desc = d.get("description") or d.get("summary") or d.get("details")
            tools = d.get("tools") or d.get("tech")

            cols = st.columns([1.2, 2.8]) if image and (exists(image) or is_url(image)) else [st]
            if cols != [st]:
                with cols[0]:
                    st.image(image, use_container_width=True)
                body = cols[1]
            else:
                body = st

            with body:
                if title: st.subheader(str(title))
                if subtitle or dates: st.caption(" | ".join([s for s in [subtitle, dates] if s]))
                if link or repo:
                    links = []
                    if link: links.append(f"[Live]({link})")
                    if repo: links.append(f"[Code]({repo})")
                    st.markdown(" ".join(links))
                if isinstance(desc, (list, tuple)):
                    for x in desc: st.markdown(f"- {x}")
                elif isinstance(desc, str):
                    st.write(desc)
                if tools:
                    for t in as_list(tools): pill(str(t))


def render_value(key: str, val):
    if isinstance(val, (int, float)):
        st.write(f"**{key_title(key)}:** {val}")
    elif isinstance(val, str):
        if (is_url(val) and val.lower().endswith((".png",".jpg",".jpeg",".gif",".svg"))) or exists(val):
            st.image(val, use_container_width=True)
        elif "\n" in val:
            st.markdown(val)
        else:
            st.write(val)
    elif isinstance(val, (list, tuple, set)):
        if val and all(isinstance(x, dict) for x in val):
            render_list_of_dicts(list(val))
        else:
            for x in val: st.write("- ", x)
    elif isinstance(val, dict):
        for subk, subv in val.items():
            st.subheader(key_title(subk))
            render_value(subk, subv)
    else:
        st.write(f"**{key_title(key)}:** {val}")

# =========================
# Sidebar
# =========================
with st.sidebar:
    # Profile photo ONLY in sidebar
    profile = getattr(info, "profile_picture", None) or getattr(info, "photo", None)
    if profile and (exists(profile) or is_url(profile)):
        st.image(profile, use_container_width=True)

    st.markdown("### Contact")
    email = getattr(info, "my_email_address", None) or getattr(info, "email", None)
    if email: st.write(f"📧 {email}")
    phone = getattr(info, "phone", None)
    if phone: st.write(f"📞 {phone}")
    loc = getattr(info, "location", None)
    if loc: st.write(f"📍 {loc}")

    # Optional website (only if provided)
    website = getattr(info, "website", None) or getattr(info, "site", None) or getattr(info, "portfolio", None)
    if website: st.write(f"🔗 {website}")

    # Optional resume (only if path exists)
    resume_candidates = [getattr(info, "resume_path", None), getattr(info, "resume", None), getattr(info, "cv", None)]
    for rp in resume_candidates:
        if isinstance(rp, str) and rp and exists(rp):
            with open(Path(rp).expanduser(), "rb") as f:
                st.download_button("📄 Download Résumé", f, file_name=Path(rp).name)
            break

    st.markdown("### Social")
    # Only show social links if there's a non-empty URL
    any_social = False
    for k, v in info.__dict__.items():
        if k.endswith("_url") and isinstance(v, str) and v.strip():
            any_social = True
            st.markdown(f"[{k[:-4].replace('_',' ').title()}]({v})")
    if not any_social:
        st.caption("Add any *_url fields in info.py to show social links.")

# =========================
# Header
# =========================
name = getattr(info, "name", None) or getattr(info, "full_name", None) or "Your Name"
role = getattr(info, "headline", None) or getattr(info, "title", None) or ""
intro = getattr(info, "tagline", None) or getattr(info, "summary", None) or ""

st.title(name)
if role: st.subheader(role)
if intro: st.write(intro)

# =========================
# Render all attributes (skip empties and already shown basics)
# =========================
BASIC_KEYS = {"profile_picture","photo","my_email_address","email","phone","location","website","site","portfolio","resume_path","resume","cv"}

for k, v in info.__dict__.items():
    if k in SKIP_KEYS or k in BASIC_KEYS:
        continue
    # Skip empty values (None, empty str, empty list/dict)
    if v is None:
        continue
    if isinstance(v, str) and not v.strip():
        continue
    if isinstance(v, (list, tuple, set, dict)) and len(v) == 0:
        continue

    st.markdown("---")
    st.header(key_title(k))
    render_value(k, v)

# =========================
# Footer
# =========================
st.markdown("---")
st.caption("Built with ❤️ using Streamlit. All fields are read from info.py exactly as-is.")
