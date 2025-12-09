import pathlib as pl
import time

from process_video import extract_audio, create_audio_chunks
from transcribe_ai import transcribe_audio
from utils import create_file_in_same_dir

def transcribe_video(video_location: pl.Path,
                     chunk_duration: int = 900,
                     output_location: pl.Path | None = None
                     ) -> None:
    '''
    Transcribes the input video. By default this function creates a .txt file that contains the transcript of the provided video
    Args:
        video_location (Path):          path to the input video.
        chunk_duration (int):           size of the audio chunks in seconds. The function will split the input video's audio
                                        into chunks. Split points will be set after the first <chunk_size> seconds, after the
                                        second <chunk_size> seconds etc. These chunks will be send to the openai API for transcription.
                                        This splitting is necessary since the API cannot deal with files that are larger
                                        than 25MB. Therefore, you must make sure that the resulting parts (chunks) do not exceed
                                        this size. The default of 900 seconds equals 15 minutes and most often ensures that the
                                        resulting chunks are below 25 MB.
        output_location (Path | None):  path to the output file to save the transcription in. If None, transcription will be saved
                                        in the same directory as the input video under the same name in the .txt format.
    '''
    # creating file and directory names
    audio_file_location = create_file_in_same_dir(input_file_location=video_location, file_ending='_audio.mp3')
    file_name = video_location.parts[-1]
    chunk_file_folder = audio_file_location.parent / file_name[0:file_name.rfind('.')]
    chunk_file_folder.mkdir()

    if output_location is None:
        output_location = create_file_in_same_dir(input_file_location=video_location, file_ending='_transcript.txt')

    extract_audio(video_location=video_location, output_location=audio_file_location)
    create_audio_chunks(audio_location = audio_file_location, chunk_duration = chunk_duration, output_location = chunk_file_folder)

    # iterate over all mp3 files in the chunk folder. Each file is a single chunk
    for audio_chunk_number, audio_chunk in enumerate(list(chunk_file_folder.glob('**/*.mp3'))):

        print('Creating transcription for chunk ' + str(audio_chunk_number))
        chunk_transcription = transcribe_audio(audio_location=audio_chunk)

        with open(output_location, 'a') as f:
            f.write('PART ' + str(audio_chunk_number) + '\n')

        current_time_offset = audio_chunk_number * chunk_duration
        for segment in chunk_transcription.segments: # type: ignore
            # we need to add the current time offset to get the actual time of the original video
            # if we do not do this, the resulting timestamps will start counting at the beginning
            # of each chunk
            print_time = time.strftime("%H:%M:%S", time.gmtime(segment.start + current_time_offset))
            with open(output_location, 'a') as f:
                f.write(print_time + ' ' + segment.text + '\n')

if __name__ == '__main__':
    transcribe_video(video_location=pl.Path("PATH/TO/YOUR/VIDEO.mp4"))
