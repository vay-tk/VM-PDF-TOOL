import streamlit as st
from PyPDF2 import PdfMerger
from .utils import safe_file_ops, create_temp_file

def merge_section():
    st.header("Merge PDFs")
    
    uploaded_files = st.file_uploader(
        "Upload PDF files to merge",
        type="pdf",
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Merge PDFs"):
            with safe_file_ops() as temp_files:
                try:
                    merger = PdfMerger()
                    
                    # Create temporary files for the uploaded PDFs
                    for uploaded_file in uploaded_files:
                        temp_file = create_temp_file(uploaded_file.read(), '.pdf')
                        temp_files.append(temp_file)
                        merger.append(temp_file)
                    
                    # Save merged PDF
                    output_file = create_temp_file(suffix='.pdf')
                    temp_files.append(output_file)
                    merger.write(output_file)
                    merger.close()
                    
                    # Provide download link
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="Download Merged PDF",
                            data=file,
                            file_name="merged.pdf",
                            mime="application/pdf"
                        )
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please upload PDF files to merge")