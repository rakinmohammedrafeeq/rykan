import streamlit as st
import speech_recognition as sr
from gtts import gTTS
# import transformers
import os
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import openai

openai.api_key = "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"
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

st.set_page_config(page_title="Rykan", page_icon="🤖", layout="wide")

st.markdown("<h1 style='text-align: center;'>🤖 Rykan</h1>", unsafe_allow_html=True)

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
        sound = AudioSegment.from_file(temp_path, format="mp3")
        play(sound)
        os.remove(temp_path)
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
    # default_value = "" if st.session_state.reset_input else st.session_state.get("text_input", "")
    user_input = st.chat_input(
        # "Message input",
        # key="text_input",
        # value=default_value,
        placeholder="Send a message to Rykan...",
        # label_visibility="collapsed"
    )

elif mode == "🎙️ Voice":
    if st.button("🎧 Start Talking", use_container_width=True):
        user_input = speech_to_text()

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

if st.session_state.latest_response and st.button("🔈 Listen to Rykan", use_container_width=True):
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

    st.markdown("---")
    st.markdown("**Chat Options**")

    if st.session_state.history:
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
    .user-msg, .bot-msg {{
        padding: 14px 18px;
        border-radius: 18px;
        max-width: 100%;
        font-size: 15px;
        line-height: 1.4;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .user-msg {{
        align-self: flex-end;
        background: {'#007AFF' if theme == 'light' else '#2196F3'};
        color: white;
        text-align:right;
    }}
    .bot-msg {{
        align-self: flex-start;
        background: {'#F1F1F1' if theme == 'light' else '#2c2c2c'};
        color: {'black' if theme == 'light' else 'white'};
    }}
    </style>
""", unsafe_allow_html=True)