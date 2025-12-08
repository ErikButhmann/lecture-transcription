from openai import OpenAI
from moviepy import AudioFileClip
from dotenv import load_dotenv
import pathlib as pl
import os

def extract_audio(video: pl.Path, output_location: pl.Path | None = None) -> None:
    '''
    Extract the audio of an input video and save it.
    
    Args:
        video (Path):                   path to the input video. The function will extract this video's audio.
        output_location (Path | None):  output file to save the video's audio in. If None, audio will be saved
                                        in the same directory as the video under the same name in the .wav format.
    '''
    # reading video as audio file
    # this will automatically transform it into a wave file
    clip = AudioFileClip(video)

    # creating default output file if not provided
    if output_location is None:

        # using name of video as name for audio
        file_name = video.parts[-1]
        file_name = file_name[0:file_name.rfind('.')] + '_audio.wav'

        # accessing same path as input and adding file_name
        output_location = video.parent
        output_location = output_location / file_name

    # writing audio to file
    clip.write_audiofile(output_location)
    clip.close()


def clip_audio(audio: pl.Path, start: int = 0, end:int =60, output_location: pl.Path | None = None) -> None:
    '''
    Clip an input audio file to the seconds between the parameters start and end. Save the resulting
    audio clip in the provided output_location or a default folder.
    
    audio (Path):                    path to the input audio.
    start (int):                        start time to cut in seconds
    end (int):                          end time to cut in seconds
    output_location (Path | None):   output file to save the clipped audio in. If None, it will be saved
                                        in the same directory as the input under the same name in the .wav format.
    '''
    clip = AudioFileClip(audio)
    sub_clip = clip.subclipped(start_time=start, end_time=end)

    # creating default output file if not provided
    if output_location is None:

        # using name of video as name for audio
        file_name = audio.parts[-1]
        file_name = file_name[0:file_name.rfind('.')] + '_clipped.wav'

        # accessing same path as input and adding file_name
        output_location = audio.parent
        output_location = output_location / file_name

    # writing audio to file
    sub_clip.write_audiofile(output_location)
    sub_clip.close()
    clip.close()


def create_audio_chunks(audio: pl.Path, chunk_duration: int, output_location: pl.Path | None = None) -> None:
    '''
    Splits input audio file in smaller files. This is often necessary since the openai API cannot deal with
    audio files that are larger than 25MB.

    Args:
        audio (Path):                   input audio file to split in chunks.
        chunk_duration (int):           size of the audio chunks in seconds. The function will split the input audio file
                                        into chunks after the first <chunk_size> seconds, after the second <chunk_size>
                                        seconds etc.
        output_location (Path | None):  output directory to save the chunks in. If values is None, a new sub-directory
                                        will be created in the directory of the input audio file. This sub-directory is
                                        named after the input audio file. The resulting audio files will be .mp3 files.
    '''
    clip = AudioFileClip(audio)
    overall_duration = clip.duration
    clip.close()

    # creating sub-directory for chunks
    if output_location is None:
        subdir_name = audio.parts[-1]
        subdir_name = subdir_name[0:subdir_name.rfind('.')]
        output_location = audio.parent / subdir_name
        output_location.mkdir()
    if not output_location.is_dir():
        raise ValueError('Output location must be a directory.')

    # setting up number of chunks and start and end time
    chunk_number = int((overall_duration // chunk_duration)) + 1
    current_start = 0
    current_end = chunk_duration

    # cutting out each chunk and saving it in the subdirectory
    for current_chunk in range(chunk_number):
        if current_end > overall_duration:
            # if the increased end is higher than the overall duration
            # this means that we reached the end of the main file.
            # Therefore, the end time is set to the overall duration since the main
            # audio cannot be clipped to an end behind this duration
            current_end = overall_duration

        # creating a file name for each chunk
        # file names are numbered based on the chunk number
        file_name = audio.parts[-1]
        file_name = file_name[0:file_name.rfind('.')] + '_part' + str(current_chunk) + '.mp3'

        # clipping the main audio file
        clip_audio(audio=audio, start=current_start, end=current_end, output_location = output_location / file_name)

        # increase start and end time of the next chunk
        current_start += chunk_duration
        current_end += chunk_duration


def transcribe_audio(audio: pl.Path, output_location: pl.Path | None = None) -> None:
    '''
    Transcribes the content of an audio file and saves the transcription. This function uses the openai API.
    Therefore, an openai API key is necessary. This key should be saved in a .env-file in the root folder.
    This file must contain a variable called OPENAI_API_KEY that is associated with a working key.

    Args:
        audio (Path):                   input audio file to transcribe
        output_location (Path | None):  output file to save the transcription in. If None, it will be saved
                                        in the same directory as the input audio under the same name in the .json format.
    '''
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with open(audio, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="text"
        )

    # creating default output file if not provided
    if output_location is None:

        # using name of video as name for audio
        file_name = audio.parts[-1]
        file_name = file_name[0:file_name.rfind('.')] + '_transcript.txt'

        # accessing same path as input and adding file_name
        output_location = audio.parent
        output_location = output_location / file_name

    with open(output_location, "a") as f:
        f.write(transcript)


if __name__ == '__main__':
    transcribe_audio(audio = pl.Path("D:/Studium/SHK/Prof_Geoinfo/transkript/lecture-transcription/data/test_data/L-GDI-2-SDSS_audio_clipped.wav"))
