import asyncio
import os
import tempfile
import requests
import edge_tts
from playsound import playsound   # ← import the function directly

# 🧠 Settings
MODEL = "friday"
OLLAMA_URL = "http://localhost:11434/api/generate"
VOICE = "en-US-JennyNeural"  # pick any Edge TTS voice you like
RATE  = "+10%"               # +10 % faster speech

async def tts_to_file(text: str, path: str) -> None:
    """Generate TTS and save to MP3."""
    communicator = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE)
    await communicator.save(path)

def speak(text: str) -> None:
    """Convert text to speech, play it, then clean up temp file."""
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    asyncio.run(tts_to_file(text, path))  # generate audio
    playsound(path)                       # play it

    os.remove(path)                       # delete temp file

def ask_friday(prompt: str) -> str:
    """Send prompt to local Ollama model and return Friday’s reply."""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    return response.json()["response"].strip()

print("🛡️  Friday Activated. Type 'exit' to quit.\n")

while True:
    user_input = input("🗣️  You (Boss): ")
    if user_input.lower() in {"exit", "quit"}:
        break

    reply = ask_friday(user_input)
    print(f"🤖 Friday: {reply}")
    speak(reply)
