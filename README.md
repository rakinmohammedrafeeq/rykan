# Rykan – Voice & Text AI Chatbot

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

## Demo

🎥 **Coming Soon** – Stay tuned for a walkthrough demo of Rykan in action!

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
├── Rykan.py # Main Streamlit app
├── utils/
│ ├── chat_utils.py # Handles API interaction and message formatting
│ ├── audio_utils.py # Text-to-speech and audio playback
│ └── voice_input.py # Converts audio input to text
├── assets/ # Icons, sound files, or visuals (if any)
├── .streamlit/
│ └── secrets.toml # Contains Groq API key
├── requirements.txt # Python dependencies
├── README.md # Project overview and setup guide
└── LICENSE # MIT License
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

## Installation & Usage

1. **Clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/Rykan
cd Rykan
```

2. **Add Groq API key:**
*Create `.streamlit/secrets.toml` and add:*
```toml
GROQ_API_KEY = "your_api_key_here"
```

3. **Run the chatbot:**

```bash
streamlit run Rykan.py
```

