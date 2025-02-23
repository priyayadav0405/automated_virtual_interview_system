import streamlit as st
from audio_recorder_streamlit import audio_recorder
import base64
# import whisper
import os
from langchain_groq import ChatGroq
from gtts import gTTS
from PIL import Image,ImageSequence
import time
import requests
from streamlit_lottie import st_lottie
import PyPDF2


os.environ["GROQ_API_KEY"] = "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"
# Initialize the ChatGroq model
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0.6, max_tokens=500)

st.set_page_config(
    page_title="Virtual Interview App",
    # page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
    
)


# Function to load Lottie animation
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Load a Lottie animation for the header
lottie_animation = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_3rwasyjy.json")

# Show Lottie Animation
if lottie_animation:
    st_lottie(lottie_animation, height=250, key="interview_lottie")
# st.set_page_config(page_title="Virtual Interview", layout="centered")

st.title("🤖 Virtual Interview Room")
st.markdown("Welcome to the Virtual Interview! 🎤 Please answer the following questions:")



file_path="welcome_message.mp3"
# Play the TTS audio file in Streamlit
audio_file = open(file_path, 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3',start_time=0)




resume_file="resume.pdf"
if resume_file is not None:
    # Read the content of the uploaded resume
    import PyPDF2
    pdf_reader = PyPDF2.PdfReader(resume_file)
    resume_text = ''
    for page in pdf_reader.pages:
        resume_text += page.extract_text()



    print(resume_text,"------------------------------------------------------------------------------------------------------***************")


    # Analyze the resume and generate questions using ChatGroq
    prompt = f"Analyze this resume and generate three interview questions based on its content:\n\n{resume_text}"
    questions_response = llm.invoke(input=prompt)
    print(questions_response,"-----------------------------------------------------------------------------------------------")
   
    print(type(questions_response.content))

    questions_text = questions_response.content 
    # questions_text=str(questions_text) # Adjust based on actual attribute name
    questions = questions_text.strip()  # Split into individual questions
    print("++++++++++++++++++++++++++++++") 
    if questions:
         for question in questions:
            st.markdown(f"**Question:** {question}")
            answer = st.text_input("Your Answer:")
            if st.button("Submit Answer"):
                st.success("Your answer has been recorded!")



