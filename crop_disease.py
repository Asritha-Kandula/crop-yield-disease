import streamlit as st
import numpy as np
from PIL import Image

def disease_detection():

    st.header("📷 AI Crop Disease Detection")

    uploaded_file = st.file_uploader(
        "Upload Crop Leaf Image",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Leaf", use_column_width=True)

        img = np.array(image)
        avg_color = img.mean()

        # Simple AI logic
        if avg_color < 80:
            disease = "Leaf Blight"
            suggestion = "Use fungicide and avoid excess watering"

        elif avg_color < 120:
            disease = "Brown Spot"
            suggestion = "Spray Mancozeb fungicide"

        elif avg_color < 160:
            disease = "Rust Disease"
            suggestion = "Apply copper fungicide"

        else:
            disease = "Healthy Leaf"
            suggestion = "No disease detected"

        st.subheader("🧪 Diagnosis")
        st.success(f"Disease: {disease}")
        st.write(f"Suggestion: {suggestion}")