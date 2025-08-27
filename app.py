import streamlit as st
import zipfile
import os
import io
import tempfile
import shutil

st.title("📂 File Renamer (Leading Zero)")

uploaded_file = st.file_uploader("Upload file ZIP", type=["zip"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as extract_path:
        # Read ZIP into memory
        in_memory = io.BytesIO(uploaded_file.read())
        renamed_files = []
        error_files = []

        try:
            with zipfile.ZipFile(in_memory, 'r') as zip_ref:
                # Prevent zip slip
                for member in zip_ref.namelist():
                    if os.path.isabs(member) or ".." in member:
                        st.warning(f"File {member} in ZIP is unsafe and was skipped.")
                        continue
                    zip_ref.extract(member, extract_path)
        except Exception as e:
            st.error(f"Failed to extract ZIP: {e}")
            st.stop()

        # Rename only files with all-digit base name
        for root, dirs, files in os.walk(extract_path):
            for fname in files:
                base, ext = os.path.splitext(fname)
                if base.isdigit():
                    new_name = f"{int(base):03d}{ext}"
                    old_path = os.path.join(root, fname)
                    new_path = os.path.join(root, new_name)
                    try:
                        os.rename(old_path, new_path)
                        renamed_files.append((fname, new_name))
                    except Exception as e:
                        error_files.append((fname, str(e)))

        st.success("✅ Proses rename selesai!")
        st.write("Contoh hasil rename:")
        st.table(renamed_files[:10])

        if error_files:
            st.error(f"Some files failed to rename: {error_files}")

        # Create ZIP for download
        output_buffer = io.BytesIO()
        with zipfile.ZipFile(output_buffer, 'w') as zipf:
            for root, dirs, files in os.walk(extract_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, extract_path)
                    zipf.write(file_path, arcname)
        output_buffer.seek(0)

        st.download_button(
            label="⬇️ Download ZIP hasil rename",
            data=output_buffer,
            file_name="renamed_files.zip",
            mime="application/zip"
        )
