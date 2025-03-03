
import streamlit as st


def about_us(config):

    # read markdown file
    txt_readme = open("README.md", "r").read()

    # display markdown file
    st.markdown(txt_readme)
