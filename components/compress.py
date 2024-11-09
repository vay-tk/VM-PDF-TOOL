import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import os
from PIL import Image
import io
from .utils import safe_file_ops, create_temp_file

def compress_image(image_stream, max_size=(800, 800), quality=85):
    """Compress image while maintaining reasonable quality"""
    img = Image.open(image_stream)
    
    # Convert to RGB if RGBA
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Calculate new size while maintaining aspect ratio
    ratio = min(max_size[0] / img.size[0], max_size[1] / img.size[1])
    if ratio < 1:  # Only resize if image is larger than max_size
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Save compressed image
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    return output.getvalue()

def compress_section():
    st.header("Compress PDF")
    
    uploaded_file = st.file_uploader("Upload PDF file to compress", type="pdf")
    
    if uploaded_file:
        compression_level = st.slider(
            "Select compression level",
            min_value=1,
            max_value=4,
            value=2,
            help="1: Light compression (better quality)\n4: Maximum compression (smaller size)"
        )
        
        # Compression settings based on level
        compression_settings = {
            1: {"image_size": (1600, 1600), "image_quality": 95},
            2: {"image_size": (1200, 1200), "image_quality": 85},
            3: {"image_size": (800, 800), "image_quality": 75},
            4: {"image_size": (600, 600), "image_quality": 60}
        }
        
        if st.button("Compress PDF"):
            with safe_file_ops() as temp_files:
                try:
                    # Create temporary file for the uploaded PDF
                    input_file = create_temp_file(uploaded_file.getvalue(), '.pdf')
                    temp_files.append(input_file)
                    
                    reader = PdfReader(input_file)
                    writer = PdfWriter()
                    
                    # Get compression settings
                    settings = compression_settings[compression_level]
                    
                    # Process each page
                    for page in reader.pages:
                        # Compress page content streams
                        page.compress_content_streams()
                        
                        # Handle images in the page
                        if '/Resources' in page and '/XObject' in page['/Resources']:
                            xObject = page['/Resources']['/XObject'].get_object()
                            
                            for obj in xObject:
                                if xObject[obj]['/Subtype'] == '/Image':
                                    try:
                                        size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                                        data = xObject[obj].get_data()
                                        
                                        # Convert image data to PIL Image and compress
                                        image_stream = io.BytesIO(data)
                                        compressed_data = compress_image(
                                            image_stream,
                                            max_size=settings["image_size"],
                                            quality=settings["image_quality"]
                                        )
                                        
                                        # Update image data in PDF
                                        xObject[obj]._data = compressed_data
                                    except Exception:
                                        continue
                        
                        writer.add_page(page)
                    
                    # Set compression parameters
                    writer._compress = True
                    
                    # Save compressed PDF
                    output_file = create_temp_file(suffix='.pdf')
                    temp_files.append(output_file)
                    writer.write(output_file)
                    
                    # Show file size comparison
                    original_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
                    compressed_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
                    
                    st.write(f"Original size: {original_size:.2f} MB")
                    st.write(f"Compressed size: {compressed_size:.2f} MB")
                    
                    reduction = ((original_size - compressed_size) / original_size * 100)
                    if reduction > 0:
                        st.success(f"Size reduced by {reduction:.1f}%")
                    else:
                        st.warning("Could not reduce file size further. The PDF might already be well-compressed.")
                    
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="Download Compressed PDF",
                            data=file,
                            file_name="compressed.pdf",
                            mime="application/pdf"
                        )
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please upload a PDF file to compress")