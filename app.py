import streamlit as st
from components.merge import merge_section
from components.split import split_section
from components.extract import extract_section
from components.encrypt import encrypt_section
from components.convert import convert_section
from components.compress import compress_section

st.set_page_config(
    page_title="PDF Tools",
    page_icon="📄",
    layout="wide"
)

def main():
    st.title("PDF Tools")
    
    with st.sidebar:
        st.header("Navigation")
        tool = st.selectbox(
            "Select Tool",
            ["Merge PDFs", "Split PDF", "Extract Text", 
             "Encrypt/Decrypt", "Convert Format", "Compress PDF"]
        )
    
    if tool == "Merge PDFs":
        merge_section()
    elif tool == "Split PDF":
        split_section()
    elif tool == "Extract Text":
        extract_section()
    elif tool == "Encrypt/Decrypt":
        encrypt_section()
    elif tool == "Convert Format":
        convert_section()
    else:
        compress_section()

if __name__ == "__main__":
    main()