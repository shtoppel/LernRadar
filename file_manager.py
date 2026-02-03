import os
import streamlit as st
import time

UPLOAD_DIR = "uploads"


def save_uploaded_files(uploaded_files, selected_date):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    saved_paths = []
    for up_file in uploaded_files:
        # timestamp to avoid name's conflicts
        timestamp = int(time.time())
        file_name = f"{selected_date}_{timestamp}_{up_file.name}"
        full_path = os.path.join(UPLOAD_DIR, file_name)

        with open(full_path, "wb") as f:
            f.write(up_file.getbuffer())
        saved_paths.append(full_path)
    return saved_paths


def delete_file(file_path):
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            st.error(f"Deletion Error: {e}")
    return False


def show_image_gallery(images):
    if not images:
        st.info("There is no fotos yet.")
        return None

    image_urls = [f"http://localhost:8000/{os.path.basename(img.path)}" for img in images]

    st.write(f"🖼 **Galery ({len(images)}):**")
    st.caption("Select and Click for expand")

    images_html = "".join([
        f'<li><img src="{url}" alt="Screenshot" style="width:100px; height:70px; object-fit:cover; cursor:pointer; margin:2px; border-radius:4px;"></li>'
        for url in image_urls
    ])

    viewer_html = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.6/viewer.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.6/viewer.min.js"></script>

    <ul id="images" style="display: flex; flex-wrap: wrap; list-style: none; padding: 0; margin: 0;">
        {images_html}
    </ul>

    <script>
        const viewer = new Viewer(document.getElementById('images'), {{
            url: 'src',
            navbar: true,
            title: false,
            toolbar: true,
            backdrop: true,
        }});
    </script>
    <style>
        body {{ margin: 0; padding: 0; overflow: hidden; }}
        .viewer-container {{ background-color: rgba(0,0,0,0.9); }}
    </style>
    """

    st.components.v1.html(viewer_html, height=400)

    # --- Delete Function ---
    if len(images) > 1:
        selected_to_manage = st.selectbox(
            "Select for options:",
            options=range(len(images)),
            format_func=lambda x: f"Foto №{x + 1}"
        )
        current_img = images[selected_to_manage]
    else:
        current_img = images[0]
        st.info(f"Selected: {os.path.basename(current_img.path)}")

    return current_img