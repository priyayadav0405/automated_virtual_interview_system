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
import json

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

def save_to_file(file_path, question, answer):
    import json
    import os

    # Initialize empty data structure
    data = {"responses": []}

    # Check if the file exists
    if os.path.exists(file_path):
        # Load existing data with proper encoding
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except UnicodeDecodeError:
            # Handle non-UTF-8 encoding or corrupted file
            with open(file_path, "rb") as file:
                content = file.read()
            try:
                # Attempt to decode as UTF-16 (common with BOM issues)
                data = json.loads(content.decode("utf-16"))
            except Exception:
                # Fallback to an empty JSON if all decoding fails
                data = {"responses": []}
        except json.JSONDecodeError:
            # Handle empty or malformed JSON file
            data = {"responses": []}

    # Append the new question and answer
    data["responses"].append({"question": question, "answer": answer})

    # Save the updated data back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)




resume_file="resume.pdf"
if resume_file is not None:
    # Read the content of the uploaded resume
    import PyPDF2
    pdf_reader = PyPDF2.PdfReader(resume_file)
    resume_text = ''
    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    # Analyze the resume and generate questions using ChatGroq
    prompt = f"Analyze this resume and generate three technical interview question based on its content directly without any starting:\n\n{resume_text}"
    questions_response = llm.invoke(input=prompt)
    print(questions_response.content)
    # Assuming questions_response returns a list of questions in string format
    questions = questions_response.content.strip().split('\n')  # Adjust based on actual response format
    

    # Display questions one by one and collect answers
    # Display questions one by one and collect answers
    file_path="answer.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump({"responses": []}, file, indent=4, ensure_ascii=False)





    if questions:
        for index, question in enumerate(questions):
            st.markdown(f"**Question {index + 1}:** {question}")

            # Create an empty container for the timer
            timer_placeholder = st.empty()

            # Text input for the answer
            answer = st.text_input(f"Your Answer for Question {index + 1}:", key=f"answer_{index}")

            # Start the countdown (60 seconds)
            start_time = time.time()
            countdown_duration = 60  # in seconds

            while (time.time() - start_time) < countdown_duration:
                remaining_time = countdown_duration - int(time.time() - start_time)
                timer_placeholder.markdown(f"⏳ Time remaining: **{remaining_time} seconds**")

                # Check if the user provided an answer
                if answer:
                    save_to_file(file_path, question, answer)
                    st.success(f"Your answer for Question {index + 1} has been saved!")
                    break

                time.sleep(1)  # Wait for a second to update the timer
            else:
                st.warning("⏰ Time is up for this question.")
        
                # Clear the timer after the loop ends
                timer_placeholder.empty()







if st.button("Submit Interview Responses"):
    st.success("Thank you for your responses! 🎉 Our team will review them.")
