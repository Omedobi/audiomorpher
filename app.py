import streamlit as st
from pathlib import Path
import tempfile
import zipfile
from pydub import AudioSegment
from pydub.effects import normalize as norm
from utils.audio_convert import SUPPORTED_FORMATS, BITRATES, convert_audio

st.set_page_config(page_title="🎵 AudioMorpher", page_icon="🎶", layout="centered")

st.title("🎶 AudioMorpher")
st.markdown(
    "Convert and batch process your audio files with ease. "
    "Supports MP3, WAV, FLAC, OGG, and more formats."
)

# === Layout Tabs ===
tab1, tab2 = st.tabs(["🎧 Single File Conversion", "📦 Batch File Conversion"])

# === SINGLE FILE TAB ===
with tab1:
    st.subheader("Upload an Audio File")

    uploaded = st.file_uploader("📂 Upload a single file", type=SUPPORTED_FORMATS)

    input_file_path = None
    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp:
            tmp.write(uploaded.read())
            input_file_path = tmp.name
            st.success(f"Uploaded: {uploaded.name}")
            st.audio(input_file_path)

    if input_file_path:
        with st.form("single_convert_form"):
            format_choice = st.selectbox("🎚️ Convert to format", SUPPORTED_FORMATS)
            bitrate = st.selectbox("🎵 Bitrate (for lossy formats)", BITRATES, index=6)
            normalize = st.checkbox("🔊 Normalize audio", value=False)
            submitted = st.form_submit_button("🔁 Convert")

        if submitted:
            try:
                output_name = Path(uploaded.name).stem  # Use original uploaded name
                output_path = convert_audio(
                    input_file_path,
                    format_choice,
                    bitrate,
                    normalize=normalize,
                    output_name=output_name
                )
                st.success("✅ Conversion complete!")
                st.audio(str(output_path))
                with open(output_path, "rb") as f:
                    st.download_button("⬇️ Download", f, file_name=output_path.name)
            except Exception as e:
                st.error(f"❌ Error: {e}")

# === BATCH TAB ===
with tab2:
    st.subheader("Upload Multiple Audio Files")

    uploaded_files = st.file_uploader("📂 Upload audio files", type=SUPPORTED_FORMATS, accept_multiple_files=True)

    if uploaded_files:
        st.info(f"{len(uploaded_files)} file(s) selected.")

        with st.form("multi_batch_form"):
            fmt = st.selectbox("🎚️ Output format", SUPPORTED_FORMATS)
            br = st.selectbox("🎵 Bitrate", BITRATES, index=6)
            normalize = st.checkbox("🔊 Normalize all audio files", value=False)
            submitted = st.form_submit_button("🚀 Convert All")

        if submitted:
            try:
                temp_dir = Path(tempfile.mkdtemp())
                out_dir = temp_dir / "converted"
                out_dir.mkdir(exist_ok=True)

                progress = st.progress(0.0)
                converted_files = []

                for i, uploaded in enumerate(uploaded_files):
                    try:
                        input_path = temp_dir / uploaded.name
                        input_path.write_bytes(uploaded.read())

                        audio = AudioSegment.from_file(input_path)
                        if normalize:
                            audio = norm(audio)

                        output_file = out_dir / f"{input_path.stem}.{fmt}"
                        audio.export(output_file, format=fmt, bitrate=br)
                        converted_files.append(output_file)

                    except Exception as e:
                        st.warning(f"⚠️ Skipped {uploaded.name}: {e}")

                    progress.progress((i + 1) / len(uploaded_files))

                zip_path = temp_dir / "converted_audio.zip"
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for f in converted_files:
                        zipf.write(f, arcname=f.name)

                st.success("✅ Batch conversion complete!")
                with open(zip_path, "rb") as f:
                    st.download_button("⬇️ Download as ZIP", f, file_name="converted_audio.zip")
                progress.empty()

            except Exception as e:
                st.error(f"❌ Batch conversion failed: {e}")

# === Footer ===
st.markdown("---")
st.caption("Sweet Melody!.")
