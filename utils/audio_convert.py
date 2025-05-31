import tempfile
import pandas as pd
from pydub import AudioSegment
from pydub.effects import normalize as norm
from pathlib import Path


# Supported output formats and bitrate presets
LOSSY_FORMATS = ["mp3", "aac", "ogg", "wma", "m4a", "opus","mp4"]
LOSSLESS_FORMATS = ["wav", "flac", "alac", "aiff"]
SUPPORTED_FORMATS = LOSSY_FORMATS + LOSSLESS_FORMATS

BITRATES = [
    "32k", "48k", "64k", "96k", "112k", "128k", "160k", "192k", "224k", "256k", "320k", "384k"
]

def get_export_args(output_format: str, bitrate: str) -> dict:
    """
    Return export arguments based on output format and bitrate.
    """
    return {"format": output_format, "bitrate": bitrate} if output_format in LOSSY_FORMATS else {"format": output_format}

def convert_audio(input_path: str, output_format: str, bitrate: str = "192k", normalize=False, output_name: str = None) -> Path:
    """
    Convert audio file to a different format using pydub.

    Args:
        input_path (str): Path to the input audio file.
        output_format (str): Desired output format (e.g., 'mp3', 'wav').
        bitrate (str): Bitrate for the output audio file.
        normalize (bool): Whether to normalize audio volume.
        output_name (str): Optional output filename (without extension).

    Returns:
        Path: Path to the converted audio file.
    """
    
    audio = AudioSegment.from_file(input_path)
    if normalize:
        audio = norm(audio)
   
    if output_name is None:
        output_name = Path(input_path).stem
    
    temp_dir = tempfile.mkdtemp()    
    output_path = Path(temp_dir) / f"{output_name}.{output_format}"
    export_args = {"format": output_format}
    if output_format in LOSSY_FORMATS:
        export_args["bitrate"] = bitrate
        
    audio.export(output_path, **export_args)
    return output_path
