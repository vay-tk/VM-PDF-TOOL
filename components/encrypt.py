import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from .utils import safe_file_ops, create_temp_file

def encrypt_section():
    st.header("Encrypt/Decrypt PDF")
    
    action = st.radio(
        "Select Action",
        ["Encrypt PDF", "Decrypt PDF"]
    )
    
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
    password = st.text_input("Enter password", type="password")
    
    if uploaded_file and password:
        if st.button("Process PDF"):
            with safe_file_ops() as temp_files:
                try:
                    # Create temporary file for the uploaded PDF
                    input_file = create_temp_file(uploaded_file.getvalue(), '.pdf')
                    temp_files.append(input_file)
                    
                    reader = PdfReader(input_file)
                    writer = PdfWriter()
                    
                    if action == "Encrypt PDF":
                        # Copy pages to writer
                        for page in reader.pages:
                            writer.add_page(page)
                        
                        # Encrypt with password
                        writer.encrypt(password)
                        output_filename = "encrypted.pdf"
                    
                    else:  # Decrypt PDF
                        # Check if PDF is encrypted
                        if reader.is_encrypted:
                            reader.decrypt(password)
                        
                        # Copy decrypted pages to writer
                        for page in reader.pages:
                            writer.add_page(page)
                        
                        output_filename = "decrypted.pdf"
                    
                    # Save processed PDF
                    output_file = create_temp_file(suffix='.pdf')
                    temp_files.append(output_file)
                    writer.write(output_file)
                    
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label=f"Download {output_filename}",
                            data=file,
                            file_name=output_filename,
                            mime="application/pdf"
                        )
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please upload a PDF file and enter a password")