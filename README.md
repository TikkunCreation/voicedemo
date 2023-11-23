# Readme for OpenAI Transcription and Chat Completion Script

This script transcribes speech from an MP3 file, sends the transcription to GPT for a chat completion response, and then converts the chat response back into speech using text-to-speech. 

## Setup Instructions

### Environment Variables

1. Create a `.env` file in the root directory of the script.
2. Inside the `.env` file, add the following line:

```
OPENAI_API_KEY='your_openai_api_key_here'
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

### Dependencies Installation

This project requires certain Python libraries to be installed. You can install them using `pip`. Run the following command:

```
pip install openai requests python-dotenv pydub simpleaudio
```

## Usage

To use the script, follow the below steps:

1. Ensure your MP3 file is in the same directory as the script or provide the correct file path to the variable `mp3_file_path` inside the script's main logic.
2. Make sure your `.env` file is configured as mentioned in the setup instructions.
3. Execute the script by running the following command in your terminal:

```
python3 demo.py
```

## Important Notes

- The script uses `afplay` for audio playback which is available on macOS. If you are using a different operating system, you might need to change this command to a compatible audio playback command for your system.
- Please make sure you handle the API responses correctly and that you have sufficient credits/quota available on your OpenAI account to perform the operations.
- The environment variable `OPENAI_API_KEY` is crucial to the operation of this script and must be set correctly for the script to function.
- The `text_to_speech` function plays audio using `simpleaudio`, ensure it is compatible with your operating system.