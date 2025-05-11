import streamlit as st
import speech_recognition as sr
from gtts import gTTS
# import transformers
import os
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import openai
# import threading
import simpleaudio as sa

openai.api_key = st.secrets["GROQ_API_KEY"]

openai.api_base = "https://api.groq.com/openai/v1"

# nlp = transformers.pipeline("text-generation", model="microsoft/DialoGPT-small")

def ask_rykan_groq(prompt):
    response = openai.ChatCompletion.create(

        model = "llama3-70b-8192",

        messages = [
            {
                "role":"system",
                "content":"You are Rykan, a helpful AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

    )
    return response.choices[0].message.content.strip()

st.set_page_config(page_title="Rykan - Unleash the Power of Intelligence", page_icon="🤖", layout="wide")

st.markdown(f"""
    <h1 style="
        text-align: center;
        font-size: 2.8em;
        background: linear-gradient(90deg, #00adb5, #0077ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(0, 173, 181, 0.5);
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 0.2em;
    ">
        🤖 Rykan
    </h1>
    <p style="
        text-align: center;
        font-size: 1.2em;
        color: #cccccc;
        font-weight: 400;
        margin-top: 0;
        text-shadow: 0 0 4px rgba(255, 255, 255, 0.1);
        text-transform: none;
    ">
        — Unleash the Power of Intelligence —
    </p>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.history_updated = False
if "latest_response" not in st.session_state:
    st.session_state.latest_response = ""
if "processing_download" not in st.session_state:
    st.session_state.processing_download = False
if "reset_input" not in st.session_state:
    st.session_state.reset_input = False

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "theme_toggle_triggered" not in st.session_state:
    st.session_state.theme_toggle_triggered = False

if "listening" not in st.session_state:
    st.session_state.listening = False

if st.session_state.reset_input:
    st.session_state.reset_input = False
    if "text_input" in st.session_state:
        del st.session_state["text_input"]
    st.rerun()

def text_to_speech(text):
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)
            st.session_state.temp_path = temp_path

        audio = AudioSegment.from_file(temp_path, format="mp3")
        playback = sa.play_buffer(
            audio.raw_data,
            num_channels=audio.channels,
            bytes_per_sample=audio.sample_width,
            sample_rate=audio.frame_rate
        )

        st.session_state.playback_obj = playback

    except Exception as e:
        st.error(f"TTS Error: {str(e)}")

def speech_to_text():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            st.info("🎤 Listening... Speak now.")
            audio = recognizer.listen(mic, timeout=5)
            text = recognizer.recognize_google(audio)
            st.success(f"✅ Recognized: {text}")
            return text
    except Exception:
        st.warning("Could not recognize speech.")
        return ""

mode = st.radio("Input Mode", ["💬 Type", "🎙️ Voice"], horizontal=True)

user_input = ""

if mode == "💬 Type":
    if "playback_obj" in st.session_state:
        try:
            st.session_state.playback_obj.stop()
        except Exception:
            pass
        st.session_state.playback_obj = None

    temp_path = st.session_state.get("temp_path", "")
    if temp_path and os.path.exists(temp_path):
        os.remove(temp_path)
        st.session_state.temp_path = ""

    # default_value = "" if st.session_state.reset_input else st.session_state.get("text_input", "")
    user_input = st.chat_input(
        # "Message input",
        # key="text_input",
        # value=default_value,
        placeholder="Send a message to Rykan...",
        # label_visibility="collapsed"
    )

elif mode == "🎙️ Voice":
    if "playback_obj" in st.session_state:
        try:
            st.session_state.playback_obj.stop()
        except Exception:
            pass
        st.session_state.playback_obj = None

    temp_path = st.session_state.get("temp_path", "")
    if temp_path and os.path.exists(temp_path):
        os.remove(temp_path)
        st.session_state.temp_path = ""

    if st.button("🎧 Start/Stop Talking", use_container_width=True):
        if "playback_obj" in st.session_state:
            try:
                st.session_state.playback_obj.stop()
            except Exception:
                pass
            st.session_state.playback_obj = None

        temp_path = st.session_state.get("temp_path", "")
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            st.session_state.temp_path = ""

        st.session_state.listening = not st.session_state.get("listening", False)

        if st.session_state.listening:
            user_input = speech_to_text()
            st.session_state.listening = False

if user_input and not st.session_state.processing_download and not st.session_state.history_updated:
    with st.spinner("Rykan is thinking..."):
        try:
            response = ask_rykan_groq(user_input)
            # chat = nlp(user_input, max_length=1000, pad_token_id=50256)
            # response = chat[0]['generated_text'].capitalize()

            if not response.endswith((".", "?", "!")):
                response += "."
            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(("Rykan", response))
            st.session_state.latest_response = response
            st.session_state.history_updated = True

            user_input = ""

        except Exception as e:
            st.error(f"Response Error: {str(e)}")

if st.session_state.latest_response:
    if "processing_audio" not in st.session_state:
        st.session_state.processing_audio = False

    if st.button("🔈 Listen to Rykan", use_container_width=True):
        if "playback_obj" in st.session_state:
            try:
                st.session_state.playback_obj.stop()
            except Exception:
                pass
            st.session_state.playback_obj = None

        temp_path = st.session_state.get("temp_path", "")
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            st.session_state.temp_path = ""

        text_to_speech(st.session_state.latest_response)

if st.session_state.history:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for role, msg in st.session_state.history:
        css_class = "user-msg" if role == "You" else "bot-msg"
        st.markdown(f"<div class='{css_class}'><b>{role}:</b> {msg}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    chat_log = "\n".join([f"{role}: {message}" for role, message in st.session_state.history])
    st.session_state.processing_download = True
    # st.download_button("💾 Export Chat", data=chat_log, file_name="rykan_chat.txt", use_container_width=True)
    st.session_state.processing_download = False


    st.session_state.history_updated = False
    #
    # if st.button("🧼 New Chat", use_container_width=True):
    #     st.session_state.history = []
    #     st.session_state.latest_response = ""
    #     st.session_state.processing_download = False
    #     st.session_state.reset_input = True
    #     st.session_state.history_updated = False
    #     if "text_input" in st.session_state:
    #         del st.session_state["text_input"]
    #     st.success("Conversation reset.")
    #     st.rerun()

with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("**Theme**")
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.session_state.theme_toggle_triggered = True
        st.rerun()

    st.markdown("---")
    st.markdown("**About Rykan**")
    st.markdown("Rykan is your smart AI assistant powered by DialoGPT.")
    st.markdown("Version: 1.0.0")
    st.markdown("Developed by Rakin")

    if st.session_state.history:
        st.markdown("---")
        st.markdown("**Chat Options**")

        st.download_button("💾 Export Chat", data=chat_log, file_name="rykan_chat.txt", use_container_width=True)

        if st.button("🧼 New Chat", use_container_width=True):
            st.session_state.history = []
            st.session_state.latest_response = ""
            st.session_state.processing_download = False
            st.session_state.reset_input = True
            st.session_state.history_updated = False
            if "text_input" in st.session_state:
                del st.session_state["text_input"]
            st.success("Conversation reset.")
            st.rerun()

theme = "dark" if st.session_state.dark_mode else "light"

st.markdown(f"""
    <style>
    html, body, [class*="css"]  {{
        font-family: 'Segoe UI', sans-serif;
        background-color: {'#1e1e1e' if theme == 'dark' else '#ffffff'};
        color: {'#ffffff' if theme == 'dark' else '#000000'};
    }}
    .chat-container {{
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 20px;
    }}
    .user-msg {{
        align-self: flex-end;
        padding: 12px 15px;
        border-radius: 12px;
        margin: 8px 0;
        text-align: right;
        color: #ecf0f1;
        border: 1px solid #00adb5;
        background: linear-gradient(145deg, #2c3e50, #34495e);
        box-shadow: 0 0 8px rgba(0, 173, 181, 0.7);
    }}
    .user-msg b {{
        color: #00adb5;
    }}
    .bot-msg {{
        align-self: flex-start;
        padding: 12px 15px;
        border-radius: 12px;
        margin: 8px 0;
        text-align: left;
        color: #f1f1f1;
        border: 1px solid #ff6363;
        background: linear-gradient(145deg, #3a3f44, #444b52);
        box-shadow: 0 0 8px rgba(255, 99, 99, 0.7);
    }}
    .bot-msg b {{
        color: #ff6363;
    }}
    </style>
""", unsafe_allow_html=True)
