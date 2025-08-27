import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Konversi Gambar ke PDF", layout="centered")

st.title("Konversi Gambar (JPEG, WEBP, PNG, dll) ke PDF")

st.markdown("""
Unggah satu atau beberapa gambar (JPEG, WEBP, PNG, dll), lalu klik **Konversi ke PDF** untuk mengunduh file PDF hasil konversi.
""")

uploaded_files = st.file_uploader(
    "Pilih gambar yang ingin dikonversi",
    type=["jpg", "jpeg", "png", "webp", "bmp"],
    accept_multiple_files=True
)

if uploaded_files:
    images = []
    for uploaded_file in uploaded_files:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            images.append(img)
        except Exception as e:
            st.warning(f"Gagal membaca gambar: {uploaded_file.name} ({e})")

    if images:
        if st.button("Konversi ke PDF"):
            pdf_bytes = io.BytesIO()
            if len(images) == 1:
                images[0].save(pdf_bytes, format="PDF")
            else:
                images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes.seek(0)
            st.success("Konversi berhasil!")
            st.download_button(
                label="Unduh PDF",
                data=pdf_bytes,
                file_name="hasil_konversi.pdf",
                mime="application/pdf"
            )
else:
    st.info("Unggah satu atau beberapa gambar terlebih dahulu.")
