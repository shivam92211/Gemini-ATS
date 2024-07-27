from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    if pdf_content is not None:  # Check if content exists
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Assuming generate_content takes only the input text
        response = model.generate_content(prompt)
        return response.text
    else:
        # Handle empty pdf_content case (e.g., display an error message)
        return None

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the pdf to image
        image = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = image[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_part = [
            {
                "mine_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_part
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...")

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about the resume")
submit2 = st.button("How can I improve my skills")

input_prompt1 = """
 You are an experienced Human Resource Manager with expertise in the fields of 
 any one job role from Data Science, Full Stack web development, Big Data Engineering, DEVOPS, Data 
 Analyst. Your task is to review the provided resume against the job description for these profiles. 
 Please share your professional evaluation on whether the candidate's profile 
 aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the 
 specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding 
of any one job role data science, Full Stack web development, Big Data Engineering, DEVOPS, Data 
Analyst and ATS functionality. Your task is to evaluate the resume against the 
provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage, then keywords 
missing, and lastly final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else: 
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.warning("Please upload your resume (PDF) first.")
