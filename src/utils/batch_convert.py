import zipfile
import tempfile
from pydub.effects import normalize as norm
from pathlib import Path
from pydub import AudioSegment
from src.utils.audio_convert import SUPPORTED_FORMATS, get_export_args
from src.utils.clean_name import clean_file_name


def batch_convert(folder_path: str, output_format: str, bitrate: str = "192k", normalize: bool = False, progress_callback=None) -> Path:
    """
    Convert all supported audio files in the specified folder to a target format and bitrate.
    
    Args:
        folder_path (str): Path to the folder containing audio files.
        output_format (str): Desired output format.
        bitrate (str): Bitrate for conversion (ignored for lossless).
        
    Returns:
        Path: Path to the ZIP archive containing converted files.
    """
    
    input_dir = Path(folder_path)
    temp_out_dir = Path(tempfile.mkdtemp())
    files = list(input_dir.glob("*"))
    converted_files = []

    for idx, file in enumerate(files):
        if file.suffix.lower().lstrip(".") in SUPPORTED_FORMATS:
            try:
                audio = AudioSegment.from_file(file)
                if normalize:
                    audio = norm(audio)
                output_name = clean_file_name(file.stem).rsplit(".", 1)[0] 
                output_file = temp_out_dir / f"{output_name}.{output_format}"
                export_args = get_export_args(output_format, bitrate)
                audio.export(output_file, **export_args)
                converted_files.append(output_file)
            except Exception as e:
                print(f"❌ Skipping {file.name}: {e}")
        if progress_callback:
            progress_callback((idx + 1) / len(files))

    zip_path = temp_out_dir.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for f in converted_files:
            zipf.write(f, arcname=f.name)

    return zip_path
