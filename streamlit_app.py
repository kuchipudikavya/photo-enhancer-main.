import streamlit as st
from PIL import Image
import numpy as np
from enhancer.enhancer import Enhancer

# App title and layout
st.set_page_config(page_title="Image Enhancer", layout="wide")
st.header('Image Enhancer App')
st.divider()

# Sidebar settings
st.sidebar.header("App Settings:")
method = st.sidebar.selectbox(
    "Enhancement Method:",
    options=["gfpgan", "RestoreFormer", "codeformer"],
    index=0  # Default to first option
)
background_enhancement = st.sidebar.toggle(
    "Background Enhancement", 
    value=True  # Default to True
)
upscale = st.sidebar.selectbox(
    "Upscale Factor:",
    options=[2, 4],
    index=0  # Default to 2x
)
picture_width = st.sidebar.slider(
    'Display Width', 
    min_value=100, 
    max_value=800,  # Increased max width
    value=400  # Default width
)

# Main content
uploaded_file = st.file_uploader(
    "Upload an image:", 
    type=['png', 'jpg', 'jpeg'],
    help="Supported formats: PNG, JPG, JPEG"
)

if uploaded_file is not None:
    try:
        # Load and validate image
        with Image.open(uploaded_file) as img:
            image = np.array(img.convert('RGB'))  # Ensure RGB format
        
        # Create enhancer with selected settings
        enhancer = Enhancer(
            method=method,
            background_enhancement=background_enhancement,
            upscale=upscale  # Use the selected upscale factor
        )
        
        # Process image
        restored_image = enhancer.enhance(image)
        final_image = Image.fromarray(restored_image)
        
        # Display results in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(
                image, 
                width=picture_width,
                use_column_width='auto',
                clamp=True
            )
            
        with col2:
            st.subheader("Enhanced Image")
            st.image(
                final_image, 
                width=picture_width,
                use_column_width='auto',
                clamp=True
            )
            
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.stop()
else:
    st.info("Please upload an image to get started")