import streamlit as st
from audio_recorder_streamlit import audio_recorder
import base64
import os
from langchain_groq import ChatGroq
from gtts import gTTS
import time
import requests
from streamlit_lottie import st_lottie
import PyPDF2
import json
from io import BytesIO
import whisper

# Set your API key for Groq
os.environ["GROQ_API_KEY"] = "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"
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0.6, max_tokens=500)

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Virtual Interview App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to load Lottie animation
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Load a Lottie animation for the header
lottie_animation = load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_3rwasyjy.json")
if lottie_animation:
    st_lottie(lottie_animation, height=250, key="interview_lottie")

st.title("🤖 Virtual Interview Room")
st.markdown("Welcome to the Virtual Interview! 🎤 Please answer the following questions:")

# Initialize session state for tracking audio playback and responses
if 'audio_played' not in st.session_state:
    st.session_state.audio_played = False

if 'question_audio_played' not in st.session_state:
    st.session_state.question_audio_played = {}

def text_to_audio(text, filename):
    """Convert text to audio using gTTS and save it to a file."""
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

starting_message = "Welcome to the Virtual Interview! 🎤 Please answer the following questions."
start_message_file = text_to_audio(starting_message, "start_message.mp3")

# Play the starting message audio only once
if not st.session_state.audio_played:
    with open(start_message_file, "rb") as f:
        audio_bytes = f.read()
        st.audio(audio_bytes, format='audio/mp3', autoplay=True)
    st.session_state.audio_played = True

time.sleep(0.5)


def create_text_card(text, title="Response"):
    st.markdown(f"""
        <div style="
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            padding: 20px;
            border-radius: 10px;
            background-color: rgb(200, 195, 195);
            margin: 10px 0;
            color:rgb(0,0,0);
            text-align:center; 
        ">
            <h4 style="margin-bottom: 10px;">{title}</h4>
            <p style="font-size: 14px; color: #430606;">{text}</p>
        </div>
    """, unsafe_allow_html=True)



st.markdown("""
    <style>
        h1 {
            text-align: center;
            background-color:rgb(220, 169, 107);
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)






def text_to_audioos(text):
    """Convert text to audio and return it as a BytesIO object."""
    tts = gTTS(text, lang='en')
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)  # Reset the stream to the beginning
    return audio_bytes




def save_to_file(file_path, question, answer):
    """Save question and answer pairs to a JSON file."""
    data = {"responses": []}

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (UnicodeDecodeError, json.JSONDecodeError):
            data = {"responses": []}

    data["responses"].append({"question": question, "answer": answer})

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)





def transcribe_audio(audio_file):
    """Transcribe audio using the Whisper model."""
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file)
    return result["text"]





file_path = "answer.json"
with open(file_path, "w", encoding="utf-8") as file:
    json.dump({"responses": []}, file, indent=4, ensure_ascii=False)



global_var_to_store_ans="anythng"

resume_file = "resume.pdf"
if resume_file is not None:
    pdf_reader = PyPDF2.PdfReader(resume_file)
    resume_text = ''.join(page.extract_text() for page in pdf_reader.pages)


    if "questions" not in st.session_state:
        prompt = f"Analyze this resume and generate three technical interview questions based on its content directly without any starting:\n\n{resume_text}"
        questions_response = llm.invoke(input=prompt)
        st.session_state["questions"] = questions_response.content.strip().split('\n')



    questions = st.session_state["questions"]

    if "interview_start_time" not in st.session_state:
        st.session_state["interview_start_time"] = time.time()

    interview_start_time = st.session_state["interview_start_time"]
    total_duration = 30 * 60  # 30 minutes in seconds

    elapsed_time = time.time() - interview_start_time
    remaining_time = total_duration - int(elapsed_time)

    if remaining_time <= 0:
        st.warning("⏰ The total interview time has ended. Please submit your responses.")
        st.stop()

    st.markdown(f"⏳ Remaining Interview Time: **{remaining_time // 60} minutes {remaining_time % 60} seconds**")



    if questions:
        for index, question in enumerate(questions):
            if remaining_time <= 0:
                st.warning("⏰ Time is up for the interview!")
                break
            
            # Check if this question's audio has been played before
            if index not in st.session_state.question_audio_played or not st.session_state.question_audio_played[index]:
                question_bytes = text_to_audioos(question)  # Play audio of the question
                st.audio(question_bytes, format="audio/mp3", autoplay=True)
                # Mark this question's audio as played
                st.session_state.question_audio_played[index] = True

            st.markdown(f"**Question {index + 1}:** {question}")

            timer_placeholder = st.empty()
            start_time = time.time()
            countdown_duration = 120  # in seconds


            recorded_audio = audio_recorder(key=f"audio_recorder{index+1}")
            if recorded_audio:
                audio_file = f"audio{index+1}.mp3"
                with open(audio_file, "wb") as f:
                    f.write(recorded_audio)

                st.write("Processing your audio....")


                # transcribed_text = transcribe_audio(audio_file)
                time.sleep(0.2)
                # global_var_to_store_ans=transcribed_text
                # print(global_var_to_store_ans)
                # create_text_card(transcribed_text, "Transcribed Text")


            answer = st.text_input(f"Your Answer for Question {index + 1}:", key=f"answer_{index+1}", disabled=False)




            while (time.time() - start_time) < countdown_duration:
                remaining_time_for_question = countdown_duration - int(time.time() - start_time)
                timer_placeholder.markdown(f"⏳ Time remaining for this question: **{remaining_time_for_question} seconds**")

                if answer:
                    save_to_file("answer.json", question, answer)
                    st.success(f"Your answer for Question {index + 1} has been saved!")
                    break

                time.sleep(1)



            if remaining_time_for_question <= 0:
                st.warning("⏰ Time is up for this question.")
                timer_placeholder.empty()
                # Disable input after time is over
                st.text_input(f"Your Answer for Question {index + 1}:", key=f"answer_{index}", disabled=True)

            remaining_time -= countdown_duration




if remaining_time <= 0 and 'questions' in st.session_state:
    st.success("⏰ The total interview time has ended. Submitting your responses...")


    
if st.button("Regenerate Questions"):
    if "questions" in st.session_state:
        del st.session_state["questions"]
        del st.session_state.question_audio_played  # Reset audio playback tracking
        
        st.rerun()




if st.button("Submit Interview Responses"):
    st.success("Thank you for your responses! 🎉 Our team will review them.")


