
import streamlit as st

# Define a function to set the static background image
def set_static_background(image_path):
    """
    Function to set a static background image for the Streamlit app.
    :param image_path: Relative path to the image file.
    """
    css = f"""
    <style>
    .stApp {{
        background-image: url("{image_path}");
        background-size: cover;  /* Ensures the image covers the entire background */
        background-repeat: no-repeat;  /* Prevents the image from repeating */
        background-position: center;  /* Centers the image */
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

