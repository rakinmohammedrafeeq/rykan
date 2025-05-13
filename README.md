# Rykan – Voice & Text AI Chatbot

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rakinmohammedrafeeq-rykan.streamlit.app/)

**Rykan** is a Streamlit-based chatbot that supports both **voice and text** communication, powered by **LLaMA3-70B via Groq API**. Rykan responds with synthesized speech using **gTTS** and offers a clean, interactive UI for seamless human-AI conversation.

---

## Features

- **Text Mode** – Type your messages and get intelligent replies
- **Voice Mode** – Speak directly and hear Rykan respond
- **Voice Output** – Converts replies into natural speech (gTTS + pydub)
- **Non-blocking Playback** – Uses `simpleaudio` for smooth, responsive experience
- **Theme Toggle** – Switch between light and dark modes
- **Chat Export** – Save conversation history as a `.txt` file
- **Reset Chat** – Start fresh with a click
- **API Integration** – Connects to Groq’s blazing-fast LLaMA3-70B model

---

## Live Demo

Experience Rykan in action – [Launch the Streamlit App](https://rakinmohammedrafeeq-rykan.streamlit.app)

---

## Technologies Used

- **Python 3.x**
- **Streamlit** – Interactive web interface
- **Groq API (LLaMA3-70B)** – High-performance LLM responses
- **gTTS** – Google Text-to-Speech for voice output
- **pydub + simpleaudio** – Audio playback without blocking the UI
- **SpeechRecognition** – Converts microphone input into text

---

## File Structure

```
Rykan/
│
├── Rykan.py                  # Main Streamlit app
├── utils/
│   ├── chat_utils.py         # Handles Groq API interaction and formatting
│   ├── audio_utils.py        # Converts text to audio and plays it
│   └── voice_input.py        # Captures microphone input and converts to text
├── assets/                   # Contains icons, sounds, or images (if any)
├── .streamlit/
│   └── secrets.toml          # Stores your Groq API key securely
├── requirements.txt          # Python dependencies
├── README.md                 # Project overview and setup guide
└── LICENSE                   # MIT License
```

---

## Requirements

- Python 3.8+
- `streamlit`
- `openai` (used for Groq client)
- `gtts`
- `pydub`
- `simpleaudio`
- `SpeechRecognition`

Install all dependencies via:

```bash
pip install -r requirements.txt
```

> **Note:** Make sure `ffmpeg` is installed and added to your system path. It’s required for `pydub` to play audio.

---

## Installation & Usage

1. **Clone the repository:**

```bash
git clone https://github.com/rakinmohammedrafeeq/Rykan
cd Rykan
```

2. **Add Groq API key:**

Create `.streamlit/secrets.toml` and add:

```toml
GROQ_API_KEY = "your_api_key_here"
```

3. **Run the chatbot:**

```bash
streamlit run Rykan.py
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## How It Works

- **Text Interaction**  
  Type in the chat box and Rykan responds instantly using Groq’s LLaMA3-70B model.

- **Voice Interaction**  
  Upload an audio file (`.wav`, `.mp3`, or `.m4a`). Rykan converts your voice to text, generates a reply, and optionally plays it back using gTTS.

- **Audio Handling**  
  gTTS generates speech, and playback is handled directly in-browser using Streamlit’s audio support.

- **Mode Switching & Theme**  
  Easily switch between light/dark UI and voice/text input modes with a single click via the sidebar.

---

## Contact  

**For any questions or suggestions, feel free to reach out:**  
**Email**: rakinmohammedrafeeq@gmail.com  
**LinkedIn**: [Rakin Mohammed Rafeeq](https://www.linkedin.com/in/rakinmohammedrafeeq)  
**GitHub**: [rakinmohammedrafeeq](https://github.com/rakinmohammedrafeeq)

---

## Support

If you found this project helpful, please consider giving it a ⭐ on GitHub!