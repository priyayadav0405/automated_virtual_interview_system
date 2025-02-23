import streamlit as st
from streamlit_lottie import st_lottie
import requests
import os
from io import BytesIO
from gtts import gTTS
import time


# Function to load Lottie animation
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


st.set_page_config(page_title="interview_experience",layout="centered",page_icon="dice")

# st.title("🎤🎤🎤 Hello Candidate!! Welcome to the Virtual Interview 💬")


st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 24px;
        font-size: 16px;
        border-radius: 8px;
        transition: transform 0.2s ease;
    }
    .stButton > button:hover {
        transform: scale(1.1);
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Load a Lottie animation for the header
lottie_animation = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_3rwasyjy.json")
def text_to_audioos(text):
    """Convert text to audio and return it as a BytesIO object."""
    tts = gTTS(text, lang='en')
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)  # Reset the stream to the beginning
    return audio_bytes


def text_to_audio(text, filename):
    """Convert text to audio using gTTS and save it to a file."""
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename



text="Hello Candidate"
start_message_file = text_to_audio(text, "welcome_message.mp3")
st.title("🎤🎤🎤 Hello Candidate!!")

with open(start_message_file, "rb") as f:
        audio_bytes = f.read()
        st.audio(audio_bytes, format='audio/mp3', autoplay=True)

time.sleep(0.4)
text="Welcome to the Virtual Interview"
start_message_file = text_to_audio(text, "welcome_again_message.mp3")
st.title("Welcome to the Virtual Interview!")
with open(start_message_file, "rb") as f:
        audio_bytes = f.read()
        st.audio(audio_bytes, format='audio/mp3', autoplay=True,)
# st.title("Welcome to the Virtual Interview!")

# Show Lottie Animation
if lottie_animation:
    st_lottie(lottie_animation, height=250, key="interview_lottie")

st.markdown(("### Please fill in your details: "))

# Form for user input
with st.form(key='candidate_form'):
    full_name = st.text_input("👤 Enter your Full Name:")
    college_name = st.text_input("🎓 Enter your College Name:")
    qualification = st.text_input("📚 Enter your Highest Qualification:")
    cv_file = st.file_uploader("📄 Upload your CV in PDF form:", type=["pdf"])
    submit_button = st.form_submit_button(label='🚀 Submit')

if submit_button:
    if not full_name or not college_name or not qualification or not cv_file:
        st.error("⚠️ Please fill in all the fields and upload your CV.")
    else:
        # Save the uploaded CV
        file_path = "resume.pdf"  # Set the desired filename
        
        with open(file_path, "wb") as f:
            f.write(cv_file.read())
        st.success("✅ CV uploaded successfully! Redirecting to the Virtual Interview...")
        
        # Redirect to the Virtual Interview page by displaying questions directly below
        st.switch_page("pages/page_1.py")

st.markdown("---")
st.markdown("Thank you for participating in this virtual interview experience! 🌟")
