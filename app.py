from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, # Get the mime type of the uploaded file
                "data": bytes_data, # Get the data of the uploaded file
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Initialize our streamlit app
    
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
uploaded_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
submit = st.button("Tell me the total calories", disabled=uploaded_file is None)

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
Finally you can also mention whether the food is healthy or not


"""



if submit:
    image_data = input_image_setup(uploaded_file)

    with st.spinner("Fetching data..."):
        response = get_gemini_response(input_prompt, image_data)

    st.subheader("The response is")
    st.write(response)
