import pathlib as pl

from moviepy import AudioFileClip

from utils import create_file_in_same_dir

def extract_audio(video_location: pl.Path, output_location: pl.Path | None = None) -> None:
    '''
    Extract the audio of an input video and save it.
    
    Args:
        video_location (Path):          path to the input video. The function will extract this video's audio.
        output_location (Path | None):  output file to save the video's audio in. If None, audio will be saved
                                        in the same directory as the video under the same name in the .mp3 format.
    '''
    # reading video as audio file
    clip = AudioFileClip(video_location)

    # creating default output file if not provided
    if output_location is None:
        output_location = create_file_in_same_dir(input_file_location=video_location, file_ending='_audio.mp3')

    # writing audio to file
    clip.write_audiofile(output_location)
    clip.close()


def clip_audio(audio_location: pl.Path, start: int = 0, end:int =60, output_location: pl.Path | None = None) -> None:
    '''
    Clip an input audio file to the seconds between the parameters start and end. Save the resulting
    audio clip in the provided output_location or a default folder.

    audio_location (Path):          path to the input audio.
    start (int):                    start time of the cut in seconds
    end (int):                      end time of the cut in seconds
    output_location (Path | None):  output file to save the clipped audio in. If None, it will be saved
                                    in the same directory as the input under the same name in the .mp3 format.
    '''
    clip = AudioFileClip(audio_location)
    sub_clip = clip.subclipped(start_time=start, end_time=end)

    # creating default output file if not provided
    if output_location is None:
        output_location = create_file_in_same_dir(input_file_location=audio_location, file_ending='_clipped.mp3')

    # writing audio to file
    sub_clip.write_audiofile(output_location)
    sub_clip.close()
    clip.close()


def create_audio_chunks(audio_location: pl.Path, chunk_duration: int, output_location: pl.Path | None = None) -> None:
    '''
    Splits the input audio file in smaller files. This is often necessary since the openai API cannot deal with
    audio files that are larger than 25MB.

    Args:
        audio_location (Path):          input audio file to split in chunks.
        chunk_duration (int):           size of the audio chunks in seconds. The function will split the input audio file
                                        into chunks after the first <chunk_duration> seconds, after the second <chunk_duration>
                                        seconds etc.
        output_location (Path | None):  output directory to save the chunks in. If value is None, a new sub-directory
                                        will be created in the directory of the input audio file. This sub-directory is
                                        named after the input audio file. The resulting audio files will be .mp3 files.
                                        All these chunk files will be named after the input file with additional '_part0',
                                        '_part1' etc. extensions.
    '''
    clip = AudioFileClip(audio_location)
    overall_duration = clip.duration
    clip.close()

    # creating sub-directory for chunks
    if output_location is None:
        subdir_name = audio_location.parts[-1]
        subdir_name = subdir_name[0:subdir_name.rfind('.')]
        output_location = audio_location.parent / subdir_name
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
            # Therefore, the end time is set to the overall duration in
            # this case since the main audio cannot be clipped to an end
            # behind this duration
            current_end = overall_duration

        # creating a file name for each chunk
        # file names are numbered based on the chunk number
        file_name = audio_location.parts[-1]
        file_name = file_name[0:file_name.rfind('.')] + '_part' + str(current_chunk) + '.mp3'

        # clipping the main audio file
        clip_audio(audio_location=audio_location, start=current_start, end=current_end, output_location = output_location / file_name)

        # increase start and end time of the next chunk
        current_start += chunk_duration
        current_end += chunk_duration
