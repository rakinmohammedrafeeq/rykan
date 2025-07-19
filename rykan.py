import streamlit as st
import speech_recognition as sr
from gtts import gTTS
# import transformers
import os
from pydub import AudioSegment
# from pydub.playback import play
# from io import BytesIO
import tempfile
import openai
# import threading
# import simpleaudio as sa
# from audiorecorder import audiorecorder


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
        text-shadow: 0 0 20px rgba(0, 173, 181, 1), 0 0 30px rgba(0, 173, 181, 0.7);
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

def text_to_speech(text):
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
            tts.save(temp_path)

        # audio_bytes = BytesIO()
        # tts = gTTS(text=text, lang='en')
        # tts.write_to_fp(audio_bytes)
        # audio_bytes.seek(0)
        #
        # audio = AudioSegment.from_mp3(audio_bytes)
        # play(audio)

        with open(temp_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

        #     st.session_state.temp_path = temp_path
        #
        # audio = AudioSegment.from_file(temp_path, format="mp3")
        # playback = sa.play_buffer(
        #     audio.raw_data,
        #     num_channels=audio.channels,
        #     bytes_per_sample=audio.sample_width,
        #     sample_rate=audio.frame_rate
        # )

        # st.session_state.playback_obj = playback

    except Exception as e:
        st.error(f"TTS Error: {str(e)}")

def speech_to_text():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            st.info("🎤 Listening... Speak now.")

            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio = recognizer.listen(mic, timeout=5)

            text = recognizer.recognize_google(audio)
            st.success(f"✅ Recognized: {text}")
            return text
    except Exception:
        st.warning("Could not recognize speech.")
        return ""

mode = st.radio("Input Mode", ["💬 Type", "🎙️ Voice"], horizontal=True)

user_input = ""
user_voice_input=""

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
    # if st.button("🎧 Start/Stop Talking", use_container_width=True):
    st.markdown("Upload a voice file (.wav, .mp3, .m4a) to talk to Rykan.")

    audio_file = st.file_uploader("🎙️ Upload Audio", type=["wav", "mp3", "m4a"])

    if audio_file:
        recognizer = sr.Recognizer()
        audio_path = None

        if audio_file.type == "audio/x-m4a" or audio_file.name.endswith(".m4a"):
            audio = AudioSegment.from_file(audio_file, format="m4a")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                audio.export(tmp.name, format="wav")
                audio_path = tmp.name
        elif audio_file.name.endswith(".mp3"):
            audio = AudioSegment.from_file(audio_file, format="mp3")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                audio.export(tmp.name, format="wav")
                audio_path = tmp.name
        else:
            audio_path = audio_file
            # with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            #     tmp.write(audio_file.read())
            #     audio_path = tmp.name

        try:
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
                user_voice_input = recognizer.recognize_google(audio)
                # user_input = recognizer.recognize_google(audio)
                st.success(f"✅ Recognized: {user_voice_input}")
                # st.success(f"✅ Recognized: {user_input}")

        except Exception as e:
            st.error(f"Speech recognition failed: {e}")

        # finally:
        #     if audio_path and os.path.exists(audio_path):
        #         os.remove(audio_path)

if user_voice_input and not st.session_state.processing_download and not st.session_state.history_updated:
    with st.spinner("Rykan is thinking..."):
        try:
            response = ask_rykan_groq(user_voice_input)

            # chat = nlp(user_input, max_length=1000, pad_token_id=50256)
            # response = chat[0]['generated_text'].capitalize()

            if not response.endswith((".", "?", "!")):
                response += "."
            st.session_state.history.append(("You", user_voice_input))
            st.session_state.history.append(("Rykan", response))

            st.session_state.latest_response = response

            # text_to_speech(response)

            st.session_state.history_updated = True

            user_voice_input = ""

        except Exception as e:
            st.error(f"Response Error: {str(e)}")

        # if "playback_obj" in st.session_state:
        #     try:
        #         st.session_state.playback_obj.stop()
        #     except Exception:
        #         pass
        #     st.session_state.playback_obj = None
        #
        # temp_path = st.session_state.get("temp_path", "")
        # if temp_path and os.path.exists(temp_path):
        #     os.remove(temp_path)
        #     st.session_state.temp_path = ""
        #
        # st.session_state.listening = not st.session_state.get("listening", False)
        #
        # if st.session_state.listening:
        #     user_input = speech_to_text()
        #
        #     st.session_state.listening = False

if st.session_state.history:
    if mode == "🎙️ Voice":
        st.markdown("""
        <div class="voice-alert">
            ℹ️ Switch to <b>Text Mode</b> to customize theme, hear responses as audio, or manage chats
        </div>
        <style>
            .voice-alert {
                background: rgba(0, 173, 181, 0.15);
                padding: 10px 16px;
                border-radius: 8px;
                margin: 8px 0 16px 0;
                font-size: 14px;
                border-left: 3px solid #00adb5;
            }
        </style>
        """, unsafe_allow_html=True)

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

            # text_to_speech(response)

            st.session_state.history_updated = True

            user_input = ""

        except Exception as e:
            st.error(f"Response Error: {str(e)}")

if st.session_state.latest_response:
    if "processing_audio" not in st.session_state:
        st.session_state.processing_audio = False

    if not mode == "🎙️ Voice":

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

with (st.sidebar):
    if not mode == "🎙️ Voice":
        if st.session_state.history:
            # and user_input and user_voice_input:
            # st.title("⚙️ Settings")
            # st.markdown("**Theme**")
            st.subheader("Theme")

            dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
            if dark_mode != st.session_state.dark_mode:
                st.session_state.dark_mode = dark_mode
                st.session_state.theme_toggle_triggered = True
                st.rerun()

            # st.session_state.auto_speak = st.toggle("🗣️ Auto-Speak Responses", value=True)

            # st.markdown("---")
            # st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

            # st.markdown("---")
            st.markdown("<br>", unsafe_allow_html=True)
            # st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

    with st.expander("About Rykan"):
        st.markdown("Rykan is your smart AI assistant powered by DialoGPT.")
        st.markdown("Version: 1.0.0")
        st.markdown("Developed by Rakin")

    # st.markdown("**About Rykan**")
    # st.markdown("Rykan is your smart AI assistant powered by DialoGPT.")
    # st.markdown("Version: 1.0.0")
    # st.markdown("Developed by Rakin")

    if not mode == "🎙️ Voice":

        if st.session_state.history:
            # st.markdown("---")
            # st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

            # st.markdown("---")
            # st.markdown("<br>", unsafe_allow_html=True)
            # st.markdown("**Chat Options**")
            st.subheader("Chat Options")

            st.download_button("Export Chat", data=chat_log, file_name="rykan_chat.txt", use_container_width=True)


            # if not mode == "🎙️ Voice":
            if st.button("New Chat", use_container_width=True):
                st.session_state.history = []
                st.session_state.latest_response = ""
                st.session_state.processing_download = False
                st.session_state.history_updated = False
                # if "text_input" in st.session_state:
                #     del st.session_state["text_input"]
                st.success("Conversation reset.")
                # st.toast("🧹 Conversation reset.")

                st.rerun()

theme = "dark" if st.session_state.dark_mode else "light"

st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
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
        padding: 12px 20px;
        border-radius: 12px;
        margin: 8px 0;
        text-align: right;
        color: {'#2c3e50' if theme == 'light' else '#ecf0f1'};  
        border: 1px solid {'#008b8b' if theme == 'light' else '#00adb5'};  
        background-color: {'#ffffff' if theme == 'light' else '#34495e'};  
        box-shadow: 0 0 8px rgba(0, 173, 181, {'0.4' if theme == 'light' else '0.7'});  
    }}
    .user-msg b {{
        color: #00adb5;
    }}
    .bot-msg {{
        align-self: flex-start;
        padding: 12px 20px;
        border-radius: 12px;
        margin: 8px 0;
        text-align: left;
        color: {'#2c3e50' if theme == 'light' else '#f1f1f1'};  
        border: 1px solid {'#ff5c5c' if theme == 'light' else '#ff6363'}; 
        background-color: {'#ffffff' if theme == 'light' else '#3a3f44'};  
        box-shadow: 0 0 8px rgba(255, 99, 99, {'0.4' if theme == 'light' else '0.7'});  
    }}
    .bot-msg b {{
        color: {'#ff6363' if theme == 'light' else '#ff5c5c'}; 
    }}
    </style>
""", unsafe_allow_html=True)
