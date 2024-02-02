### Health Management APP


import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv




load_dotenv() ## load all the environment variables


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    gemini_response=model.generate_content([input,image[0],prompt])
    
    return gemini_response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="DermAI Health App")

st.header("DermAI Health App")
st.info("""DermAI Health App is a groundbreaking Streamlit app leveraging the power of AI to swiftly identify various skin diseases with just the upload of an image depicting the affected area. By simply uploading the image and clicking on the "Proceed to Detection" button, you can swiftly obtain accurate diagnoses. The app not only detects the disease but also furnishes comprehensive information including symptoms, precautions, and available treatments. With its user-friendly interface and efficient functionality, DermAI Detect streamlines the process of identifying skin conditions, offering users valuable insights into their dermatological health.""")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Proceed to detection")

input_prompt="""
Act as dermatologist who can accurately identify skin conditions from images. 
Additionally, provide detailed information on symptoms, precautions, and remedies associated with the 
detected disease to assist dermatologists and patients in understanding and managing the condition effectively.
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input_prompt)
    st.subheader("The Response is")
    st.write(response)

