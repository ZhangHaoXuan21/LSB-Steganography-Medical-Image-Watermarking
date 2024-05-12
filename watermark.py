import streamlit as st
import stepic as lsb_steg
from PIL import Image

def encode_watermark_text_on_image(image, watermark_text):
    watermark_text_bytes = bytes(watermark_text, "utf-8")
    watermark_image = lsb_steg.encode(image, watermark_text_bytes)
    return watermark_image

def extract_watermark_text_from_image(image):
    watermark_text = lsb_steg.decode(image)
    return watermark_text

def main():
    # Display image
    st.image("banner.png")

    st.title("Welcome To Medical Image Watermarking")

    st.header("Please Select an Option")

    # Add buttons for selecting options
    option = st.radio("Select an Option", ("Watermark an Image", "Extract Watermark"))

    if option == "Watermark an Image":
        # Collect image and watermark text
        image = st.file_uploader("Upload Image", type=["png"])
        watermark_text = st.text_input("Enter Watermark Text")
        
        st.write("Original Image:")
        # Display the image
        st.image(image)

        if st.button("Watermark"):
            if image is not None and watermark_text != "":
                st.write("Watermarking image...")
                # Convert uploaded image to PIL Image
                image_pil = Image.open(image)
                # Convert PIL Image to RGB format
                image_pil_rgb = image_pil.convert("RGB")
                # Call function to watermark the image
                watermark_image = encode_watermark_text_on_image(image_pil_rgb, watermark_text)
                watermark_image.save('watermarked_image.png', 'PNG')
                st.write("Finished watermarking image.")

                # Display the watermark image
                st.image(watermark_image)

                # Add button to download watermarked image
                with open("watermarked_image.png", "rb") as file:
                    btn = st.download_button(
                            label="Download watermark image",
                            data=file,
                            file_name="watermarked_image.png",
                            mime="image/png"
                        )
                
            else:
                st.warning("Please upload an image and enter watermark text.")
    elif option == "Extract Watermark":
        # Collect watermark image and original watermark text
        watermark_image = st.file_uploader("Upload Watermarked Image", type=["png"])
        original_watermark_text = st.text_input("Enter Original Watermark Text")
        st.write("Watermarked Image:")
        # Display the image
        st.image(watermark_image)
        if st.button("Extract"):
            if watermark_image is not None and original_watermark_text != "":
                st.write("Extracting watermark...")
                # Convert uploaded watermark image to PIL Image
                watermark_pil = Image.open(watermark_image)
                # Convert PIL Image to RGB format
                watermark_pil_rgb = watermark_pil.convert("RGB")
                # Call function to extract watermark from the image
                extracted_watermark_text = extract_watermark_text_from_image(watermark_pil_rgb)
            
                st.write("Extraction completed.")
                st.write(f"Extracted watermark text: {extracted_watermark_text}")
                 # Display success or warning message based on extracted watermark text
                # Display success or warning message based on extracted watermark text
                if extracted_watermark_text != original_watermark_text:
                    st.markdown("<h1 style='color:red;'>Warning: Extracted watermark does not match the original watermark text!</h1>", unsafe_allow_html=True)
                else:
                    st.markdown("<h1 style='color:green;'>Good News: Extracted watermark matches the original watermark text!</h1>", unsafe_allow_html=True)
            else:
                st.warning("Please upload the watermarked image and enter the original watermark text.")

if __name__ == "__main__":
    main()
