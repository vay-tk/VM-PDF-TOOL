import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from .utils import safe_file_ops, create_temp_file

def split_section():
    st.header("Split PDF")
    
    uploaded_file = st.file_uploader("Upload PDF file to split", type="pdf")
    
    if uploaded_file:
        with safe_file_ops() as temp_files:
            try:
                # Create temporary file for the uploaded PDF
                input_file = create_temp_file(uploaded_file.getvalue(), '.pdf')
                temp_files.append(input_file)
                
                # Read PDF info
                pdf = PdfReader(input_file)
                num_pages = len(pdf.pages)
                
                st.write(f"Total pages: {num_pages}")
                
                # Page range selection
                split_method = st.radio(
                    "Split method",
                    ["Range", "Individual Pages"]
                )
                
                if split_method == "Range":
                    start_page = st.number_input("Start page", min_value=1, max_value=num_pages, value=1)
                    end_page = st.number_input("End page", min_value=start_page, max_value=num_pages, value=num_pages)
                    
                    if st.button("Split PDF"):
                        try:
                            writer = PdfWriter()
                            for page_num in range(start_page-1, end_page):
                                writer.add_page(pdf.pages[page_num])
                            
                            output_file = create_temp_file(suffix='.pdf')
                            temp_files.append(output_file)
                            writer.write(output_file)
                            
                            with open(output_file, "rb") as file:
                                st.download_button(
                                    label="Download Split PDF",
                                    data=file,
                                    file_name=f"split_{start_page}-{end_page}.pdf",
                                    mime="application/pdf"
                                )
                            
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                
                else:
                    pages = st.multiselect(
                        "Select pages to extract",
                        range(1, num_pages + 1)
                    )
                    
                    if st.button("Split PDF"):
                        try:
                            for page in pages:
                                writer = PdfWriter()
                                writer.add_page(pdf.pages[page-1])
                                
                                output_file = create_temp_file(suffix='.pdf')
                                temp_files.append(output_file)
                                writer.write(output_file)
                                
                                with open(output_file, "rb") as file:
                                    st.download_button(
                                        label=f"Download Page {page}",
                                        data=file,
                                        file_name=f"page_{page}.pdf",
                                        mime="application/pdf",
                                        key=f"page_{page}"
                                    )
                            
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please upload a PDF file to split")