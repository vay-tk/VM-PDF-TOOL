import streamlit as st
import pdfplumber
from PIL import Image
from .utils import safe_file_ops, create_temp_file

def extract_section():
    st.header("Extract Text")
    
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
    
    if uploaded_file:
        extract_type = st.radio(
            "What would you like to extract?",
            ["Text"]
            # , "Images"
        )
        
        with safe_file_ops() as temp_files:
            try:
                # Create temporary file
                input_file = create_temp_file(uploaded_file.getvalue(), '.pdf')
                temp_files.append(input_file)
                
                if extract_type == "Text":
                    if st.button("Extract Text"):
                        try:
                            with pdfplumber.open(input_file) as pdf:
                                text = ""
                                for page in pdf.pages:
                                    text += page.extract_text() + "\n\n"
                            
                            # Save text to temporary file
                            output_file = create_temp_file(text.encode('utf-8'), '.txt')
                            temp_files.append(output_file)
                            
                            with open(output_file, 'rb') as f:
                                st.download_button(
                                    label="Download Extracted Text",
                                    data=f,
                                    file_name="extracted_text.txt",
                                    mime="text/plain"
                                )
                            
                            st.text_area("Preview:", text, height=300)
                            
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                
                # else:  # Images
                #     if st.button("Extract Images"):
                #         try:
                #             with pdfplumber.open(input_file) as pdf:
                #                 for page_num, page in enumerate(pdf.pages):
                #                     for image_num, image in enumerate(page.images):
                #                         img = Image.open(image['stream'])
                                        
                #                         # Save image to temporary file
                #                         temp_img = create_temp_file(suffix='.png')
                #                         temp_files.append(temp_img)
                #                         img.save(temp_img)
                                        
                #                         with open(temp_img, "rb") as f:
                #                             st.download_button(
                #                                 label=f"Download Image {page_num+1}-{image_num+1}",
                #                                 data=f,
                #                                 file_name=f"image_{page_num+1}_{image_num+1}.png",
                #                                 mime="image/png",
                #                                 key=f"img_{page_num}_{image_num}"
                #                             )
                #                             st.image(temp_img, caption=f"Image {page_num+1}-{image_num+1}")
                        
                #         except Exception as e:
                #             st.error(f"An error occurred: {str(e)}")
                            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please upload a PDF file to extract content")