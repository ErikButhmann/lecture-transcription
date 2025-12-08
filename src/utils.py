import pathlib as pl

def create_file_in_same_dir(input_file: pl.Path, file_ending: str) -> pl.Path:
    '''
    Creates a new Path object that describes a file in the same directory as the input file.
    This new file has the same name as the input file, but its ending and especially its format
    can be changed by the file_ending parameter.

    Args:
        input_file (Path):  the input file that defines the directory to put the new file in.
        file_ending (str):  String that will be added at the ending of the new file. This string
                            should contain a file format specification.
    '''
    file_name = input_file.parts[-1]
    file_name = file_name[0:file_name.rfind('.')] + file_ending
    output_location = input_file.parent
    output_location = output_location / file_name

    return output_location
