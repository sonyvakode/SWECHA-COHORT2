import streamlit as st
import os
import zipfile
from io import BytesIO
from pathlib import Path
import shutil

# Categories
CATEGORIES = ["agriculture", "food", "places", "songs", "historical_people", "education", "events", "skills"]
DATA_DIR = "audio_data"

# Ensure all category folders exist
for category in CATEGORIES:
    os.makedirs(os.path.join(DATA_DIR, category), exist_ok=True)

st.set_page_config(page_title="Audio Dataset App", layout="wide")
st.title("🎧 Audio Dataset Manager")

# Tabs: Input and View
tab1, tab2 = st.tabs(["📥 Input", "📂 View / Download / Edit / Delete"])

# --- INPUT TAB ---
with tab1:
    st.header("Upload Audio to Category")
    selected_category = st.selectbox("Choose Category", CATEGORIES)

    uploaded_files = st.file_uploader("Upload audio file(s)", type=["mp3", "wav", "m4a"], accept_multiple_files=True)
    if st.button("Upload"):
        if uploaded_files:
            for file in uploaded_files:
                save_path = os.path.join(DATA_DIR, selected_category, file.name)
                with open(save_path, "wb") as f:
                    f.write(file.read())
            st.success(f"Uploaded {len(uploaded_files)} file(s) to '{selected_category}'")
        else:
            st.warning("Please select at least one file.")

# --- VIEW TAB ---
with tab2:
    st.header("View / Download / Edit / Delete Files by Category")
    view_category = st.selectbox("Select Category to View", CATEGORIES)

    category_path = Path(DATA_DIR) / view_category
    files = list(category_path.glob("*"))

    if not files:
        st.info("No files found in this category.")
    else:
        for audio_file in files:
            col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
            with col1:
                st.markdown(f"📄 **{audio_file.name}**")
            with col2:
                with open(audio_file, "rb") as f:
                    st.download_button(label="⬇️ Download", data=f, file_name=audio_file.name)
            with col3:
                new_file = st.file_uploader(f"Replace {audio_file.name}", type=["mp3", "wav", "m4a"], key=f"edit_{audio_file}")
                if new_file:
                    with open(audio_file, "wb") as f:
                        f.write(new_file.read())
                    st.success(f"{audio_file.name} replaced successfully.")
            with col4:
                if st.button("🗑️ Delete", key=f"delete_{audio_file}"):
                    os.remove(audio_file)
                    st.warning(f"{audio_file.name} deleted.")
                    st.experimental_rerun()

        # Download all as ZIP
        st.subheader("📦 Download All Files in ZIP")
        if st.button("Download ZIP"):
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for file in category_path.iterdir():
                    zipf.write(file, arcname=file.name)
            st.download_button("⬇️ Download All as ZIP", data=zip_buffer.getvalue(),
                               file_name=f"{view_category}_audio.zip", mime="application/zip")
