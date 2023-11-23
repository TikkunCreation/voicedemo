import openai
import requests
import json
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("No OPENAI_API_KEY found in the environment. Make sure to set it in the .env file.")

# Set the OpenAI API key for the openai library
openai.api_key = openai_api_key

# Function to transcribe MP3 to text
def transcribe_mp3_to_text(file_path):
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
    }

    response = requests.post(
        'https://api.openai.com/v1/audio/transcriptions',
        files={
            'file': open(file_path, 'rb'),
        },
        data={
            'model': 'whisper-1',
        },
        headers=headers,
    )
    return response.json()['text']

# Function to get chat completion response
def get_chat_completion(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ],
    )
    return response.choices[0].message['content']

# Additional imports
from pydub import AudioSegment
import simpleaudio as sa
import io

# Update the text_to_speech function to stream response and play audio
def text_to_speech(text, voice='alloy'):
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json",
    }

    data = json.dumps({
        "model": "tts-1",
        "input": text,
        "voice": voice
    })

    response = requests.post(
        "https://api.openai.com/v1/audio/speech",
        headers=headers,
        data=data,
        stream=True  # Enable response streaming
    )

    if response.status_code == 200:
        # Stream and load into audio segment
        audio_stream = io.BytesIO(response.content)
        sound = AudioSegment.from_file(audio_stream, format="mp3")
        
        # Export the audio segment to a playable format for simpleaudio
        playable_audio = sound.export(format="wav")
        wave_obj = sa.WaveObject.from_wave_file(playable_audio)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing
    else:
        raise Exception(f"Failed to convert text to speech: {response.text}")

# Main logic
if __name__ == '__main__':
    # Example MP3 file path
    mp3_file_path = "output_speech.mp3"

    subprocess.run(["afplay", mp3_file_path])

    # Step 1: Transcribe MP3 to text
    raw_transcribed_text = transcribe_mp3_to_text(mp3_file_path)
    print(f"Raw transcribed text: {raw_transcribed_text}")

    # Step 3: Send the transcribed text to GPT-4 for chat completion
    chat_response = get_chat_completion(raw_transcribed_text)
    print(f"GPT-4 response: {chat_response}")

    # Step 4: Send the chat response to GPT text-to-speech
    tts_response = text_to_speech(chat_response)