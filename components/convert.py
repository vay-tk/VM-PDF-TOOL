import streamlit as st
from PIL import Image
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path
from .utils import safe_file_ops, create_temp_file

def convert_section():
    st.header("Convert Format")
    
    conversion_type = st.selectbox(
        "Select Conversion Type",
        ["Image to PDF", "PDF to Image"]
    )
    
    if conversion_type == "Image to PDF":
        uploaded_files = st.file_uploader(
            "Upload image files",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("Convert to PDF"):
                with safe_file_ops() as temp_files:
                    try:
                        # Create temporary PDF
                        output_file = create_temp_file(suffix='.pdf')
                        temp_files.append(output_file)
                        c = canvas.Canvas(output_file)
                        
                        for uploaded_file in uploaded_files:
                            # Save uploaded image temporarily
                            temp_img = create_temp_file(uploaded_file.read(), '.png')
                            temp_files.append(temp_img)
                            
                            # Open image and get size
                            img = Image.open(temp_img)
                            img_width, img_height = img.size
                            
                            # Scale image to fit on PDF page
                            aspect = img_height / float(img_width)
                            if aspect > 1:
                                img_width = 500
                                img_height = 500 * aspect
                            else:
                                img_width = 500 / aspect
                                img_height = 500
                            
                            # Add image to PDF
                            c.setPageSize((img_width, img_height))
                            c.drawImage(temp_img, 0, 0, width=img_width, height=img_height)
                            c.showPage()
                        
                        c.save()
                        
                        with open(output_file, "rb") as file:
                            st.download_button(
                                label="Download PDF",
                                data=file,
                                file_name="converted.pdf",
                                mime="application/pdf"
                            )
                        
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    
    else:  # PDF to Images
        uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
        
        if uploaded_file:
            if st.button("Convert to Images"):
                with safe_file_ops() as temp_files:
                    try:
                        # Save uploaded PDF temporarily
                        input_file = create_temp_file(uploaded_file.getvalue(), '.pdf')
                        temp_files.append(input_file)
                        
                        # Convert PDF to images
                        images = convert_from_path(input_file)
                        
                        for i, image in enumerate(images):
                            # Save image temporarily
                            temp_img = create_temp_file(suffix='.png')
                            temp_files.append(temp_img)
                            image.save(temp_img, 'PNG')
                            
                            with open(temp_img, "rb") as file:
                                st.download_button(
                                    label=f"Download Page {i+1}",
                                    data=file,
                                    file_name=f"page_{i+1}.png",
                                    mime="image/png",
                                    key=f"page_{i+1}"
                                )
                                st.image(temp_img, caption=f"Page {i+1}")
                    
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
        else:
            st.info("Please upload a PDF file to convert")
