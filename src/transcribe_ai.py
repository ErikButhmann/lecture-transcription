import os
import pathlib as pl

from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

def transcribe_audio(audio_location: pl.Path, spelling: str = '') -> BaseModel:
    '''
    Transcribes the content of an audio file and saves the transcription. This function uses the openai API.
    Therefore, an openai API key is necessary. This key should be saved in a .env-file in the root folder.
    This file must contain a variable called OPENAI_API_KEY that is associated with a working key.

    Args:
        audio_location (Path):  input audio file to transcribe
        spelling (str):         a string containing a list of unfamiliar words with their correct spelling.
                                This can improve the quality of the whisper model since it often faces problems
                                with unfamiliar or unusual words. Default is the empty string.
    '''
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(audio_location, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model='whisper-1',
            language='en',
            response_format='verbose_json',
            timestamp_granularities=["segment"],
            prompt=spelling
        )

    return transcript
