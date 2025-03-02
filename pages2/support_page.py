import streamlit as st



import streamlit as st
import base64

# Function to set the background image using a Base64-encoded data URL
def set_background_image_from_file(image_file):
    """
    Function to set a background image from an uploaded file.
    :param image_file: Uploaded file object from st.file_uploader.
    """
    if image_file is not None:
        # Read the file and encode it as Base64
        encoded_image = base64.b64encode(image_file.read()).decode()
        
        # Create the CSS with the Base64-encoded image
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """
        # Inject the CSS into the Streamlit app
        st.markdown(css, unsafe_allow_html=True)




def support_page(config):
    # Support page
    st.title(config.translations["support_title"])
    st.write(config.translations["support_text"])

    # Display bank account details based on language
    if config.language == "en":
        st.text_area("Bank Account Details (English)", config.translations["bank_account_en"])

    elif config.language == "kz":
        st.text_area("Банк шотының деректері (Қазақша)", config.translations["bank_account_kz"])


    # Add a file uploader for the user to upload an image
    uploaded_file = st.file_uploader("Upload a background image (PNG or JPG)", type=["png", "jpg", "jpeg"])

    # Set the background image if a file is uploaded
    #set_background_image_from_file(uploaded_file)

    # Add some content to your app
    #st.title("Streamlit App with Dynamic Background Image")
    #st.write("Upload an image using the file uploader above to set it as the background.")
