from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import pathlib as pl

def transcribe_audio(audio: pl.Path) -> BaseModel:
    '''
    Transcribes the content of an audio file and saves the transcription. This function uses the openai API.
    Therefore, an openai API key is necessary. This key should be saved in a .env-file in the root folder.
    This file must contain a variable called OPENAI_API_KEY that is associated with a working key.

    Args:
        audio (Path):                   input audio file to transcribe
    '''
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(audio, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model='whisper-1',
            language='en',
            response_format='verbose_json',
            timestamp_granularities=["segment"]
        )

    return transcript

    # # creating default output file if not provided
    # if output_location is None:

    #     # using name of video as name for audio
    #     file_name = audio.parts[-1]
    #     file_name = file_name[0:file_name.rfind('.')] + '_transcript.json'

    #     # accessing same path as input and adding file_name
    #     output_location = audio.parent
    #     output_location = output_location / file_name

    # with open(output_location, 'a') as f:
    #     # json_string = json.dumps(transcript.model_dump(), indent=4)
    #     f.write(transcript.model_dump_json(indent=4))