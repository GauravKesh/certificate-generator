import io
import zipfile
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(
    page_title="Certificate Generator Pro",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------
# DARK THEME
# -----------------------------------------------------------
st.markdown(
    """
    <style>
        :root {
            --bg-primary: #0D1117;
            --bg-secondary: #161B22;
            --bg-card: rgba(255, 255, 255, 0.04);
            --border: rgba(255, 255, 255, 0.08);
            --text-main: #E6E6E6;
            --text-soft: #A6A6A6;

            --accent: #2D8AE8;     /* clean blue */
            --accent-soft: #4AA4FF;
            --accent-glow: rgba(45, 138, 232, 0.35);

            --success: #2ECC71;
        }

        /* ------------------------ Global ------------------------ */
        .stApp {
            background: var(--bg-primary) !important;
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }

        section[data-testid="stSidebar"] {
            background: var(--bg-secondary) !important;
            border-right: 1px solid var(--border);
            backdrop-filter: blur(10px);
        }

        /* ------------------------ Header ------------------------ */
        .main-header {
            text-align: center;
            # padding: 3rem 2rem;
            background: linear-gradient(135deg, #1F2730, #161B22);
            border-radius: 18px;
            margin-bottom: 2rem;
            padding: 2rem
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }
        .main-header h1 {
            font-size: 2.8rem;
            font-weight: 200;
            color: white;
            margin: 0;
            letter-spacing: -1px;
        }
        .main-header p {
            color: var(--text-soft);
            margin-top: 0.1rem;
        }

        /* ------------------------ Cards ------------------------ */
        .preview-container {
            background: var(--bg-card);
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid var(--border);
            backdrop-filter: blur(18px);
            box-shadow: 0 6px 22px rgba(0,0,0,0.25);
        }

        /* ------------------------ Buttons ------------------------ */
        .stButton > button {
            background: var(--accent);
            border-radius: 10px;
            padding: 0.75rem 1.6rem;
            font-weight: 600;
            color: white;
            border: none;
            box-shadow: 0 4px 16px var(--accent-glow);
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            background: var(--accent-soft);
            transform: translateY(-2px);
            box-shadow: 0 6px 24px var(--accent-glow);
        }

        .stDownloadButton > button {
            background: var(--success);
            border-radius: 10px;
            padding: 0.75rem 1.6rem;
            color: white;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 16px rgba(46, 204, 113, 0.25);
        }

        /* ------------------------ Inputs ------------------------ */
        input, select, textarea {
            background: var(--bg-secondary) !important;
            border-radius: 10px !important;
            color: var(--text-main) !important;
            padding: 0.65rem !important;
            border: 1px solid var(--border) !important;
        }
        input:focus, select:focus, textarea:focus {
            border: 1px solid var(--accent) !important;
            box-shadow: 0 0 10px var(--accent-glow);
        }

        /* ------------------------ Section Titles ------------------------ */
        .section-title {
            font-size: 1.55rem;
            font-weight: 700;
            margin-top: 2rem;
            color: var(--accent);
        }

        /* ------------------------ Footer ------------------------ */
        .footer-text {
            text-align: center;
            color: var(--text-soft);
            margin-top: 2.5rem;
            padding-bottom: 1.5rem;
            opacity: 0.7;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------
# HEADER
# -----------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1>Certificate Generator Pro</h1>
        <p>Generate professional certificates in seconds</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------
st.sidebar.title("Configuration")

template_file = st.sidebar.file_uploader(
    "Upload Template Image", type=["png", "jpg", "jpeg"]
)
template = Image.open(template_file).convert("RGBA") if template_file else None

name_file = st.sidebar.file_uploader("Upload Names (Excel/CSV)", type=["xlsx", "csv"])
df = None

if name_file:
    df = (
        pd.read_excel(name_file)
        if name_file.name.endswith("xlsx")
        else pd.read_csv(name_file)
    )
    st.sidebar.write(f"Loaded **{len(df)}** recipients")

mode = st.sidebar.radio(
    "Name Format", ["Single Column", "Combine Two Columns", "Combine Three Columns"]
)
separator = st.sidebar.selectbox("Separator", [" ", " - ", " | ", ", ", " • "])

if df is not None:
    cols = list(df.columns)

    if mode == "Single Column":
        col1 = st.sidebar.selectbox("Column", cols)
        formatter = lambda r: str(r[col1])

    elif mode == "Combine Two Columns":
        col1 = st.sidebar.selectbox("Column 1", cols)
        col2 = st.sidebar.selectbox("Column 2", cols)
        formatter = lambda r: f"{r[col1]}{separator}{r[col2]}"

    else:
        col1 = st.sidebar.selectbox("Column 1", cols)
        col2 = st.sidebar.selectbox("Column 2", cols)
        col3 = st.sidebar.selectbox("Column 3", cols)
        formatter = lambda r: f"{r[col1]}{separator}{r[col2]}{separator}{r[col3]}"
else:
    formatter = lambda r: ""

font_size = st.sidebar.slider("Font Size", 20, 200, 60)
font_color = st.sidebar.color_picker("Font Color", "#000000")
alignment = st.sidebar.radio("Alignment", ["Center", "Left", "Right"], horizontal=True)

st.sidebar.markdown("### Position Controls")
pos_x_col, pos_y_col = st.sidebar.columns(2)
x_offset = pos_x_col.number_input("X Offset", -2000, 2000, 0, 5)
y_offset = pos_y_col.number_input("Y Offset", -2000, 2000, 0, 5)

font_file = st.sidebar.file_uploader(
    "Upload Custom Font (TTF/OTF)", type=["ttf", "otf"]
)
if font_file:
    font = ImageFont.truetype(io.BytesIO(font_file.read()), font_size)
else:
    font = ImageFont.truetype("fonts/Roboto-Regular.ttf", font_size)


# -----------------------------------------------------------
# DRAW FUNCTION
# -----------------------------------------------------------
def draw_text(img, text):
    img = img.copy()
    draw = ImageDraw.Draw(img)

    w, h = img.size
    tb = draw.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]

    if alignment == "Center":
        x = (w - tw) / 2
    elif alignment == "Left":
        x = 80
    else:
        x = w - tw - 80

    x += x_offset
    y = (h / 2) - th + y_offset

    draw.text((x, y), text, font=font, fill=font_color)
    return img


# -----------------------------------------------------------
# PREVIEW
# -----------------------------------------------------------
st.markdown("<div class='section-title'>Live Preview</div>", unsafe_allow_html=True)

if template and df is not None:
    sample = formatter(df.iloc[0]).upper()
    preview = draw_text(template, sample)

    buf = io.BytesIO()
    preview.save(buf, "PNG")

    st.write(f"Preview: **{sample}**")
    st.markdown('<div class="preview-container">', unsafe_allow_html=True)
    st.image(buf.getvalue(), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Upload template and name list to see preview.")

# -----------------------------------------------------------
# GENERATE
# -----------------------------------------------------------
st.markdown(
    "<div class='section-title'>Generate Certificates</div>", unsafe_allow_html=True
)

if st.button("Generate All Certificates"):
    if template is None or df is None:
        st.error("Upload template and recipient list first.")
    else:
        progress = st.progress(0)
        output_files = {}

        for idx, (_, row) in enumerate(df.iterrows()):
            name = formatter(row).upper()
            filename = name.replace(" ", "_") + ".png"

            cert_img = draw_text(template, name)
            mem = io.BytesIO()
            cert_img.save(mem, "PNG")

            output_files[filename] = mem.getvalue()
            progress.progress((idx + 1) / len(df))

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as z:
            for fn, data in output_files.items():
                z.writestr(fn, data)
        zip_buffer.seek(0)

        st.success(f"Generated {len(output_files)} certificates!")
        st.download_button(
            "Download ZIP", zip_buffer, "certificates.zip", mime="application/zip"
        )

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.markdown(
    "<div class='footer-text'>Built with Streamlit</div>", unsafe_allow_html=True
)
