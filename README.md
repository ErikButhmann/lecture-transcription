# Transcribe a lecture video

The code provided in this repository allows to transcribe a lecture video (or another kind of video, but this has not been tested).
It makes use of OpenAI's [transriptions API](https://platform.openai.com/docs/guides/speech-to-text).

## General Workflow

1. Load the video, for example a .mp4 file and extract its audio.
2. Split the audio in smaller chunks since the API cannot work with audio files larger than 25 MB.
3. Send each chunk to the API and get the transcription.
4. Combine the transcriptions of the chunks in one text-file.

## Setup

1. Download or clone this repository
2. (optional but recommended) Create a virtual environment. [venv](https://docs.python.org/3/library/venv.html) was used when writing the code.
3. Install dependencies using `pip install -r requirements.txt`
4. Add your [OpenAI-Key](https://platform.openai.com/docs/overview) in a .env file in the root folder. This .env file should contain a variable called `OPENAI_API_KEY`. I.e. you must add the following line to the .env-file `OPENAI_API_KEY=<Your_Key>`. This key will be used to access OpenAI's services.
5. The function `transcribe_video` in the [main.py](src/main.py) module provides the main interface to transcribe a video. You can input a file path to an existing video. The resulting transcription will be created in the same directory as a .txt file.

## Disclaimer

This code is intended to be used with lecture videos produced by yourself.
Since the audio of the input video is send to the servers and AI-applications of OpenAI you have to consider data privacy issues, especially if the videos you are dealing with were not produced by yourself.
