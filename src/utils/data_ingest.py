import zipfile
import tempfile
from pathlib import Path
from tkinter import Tk, filedialog
from pydub import AudioSegment
from src.utils.audio_convert import convert_audio, SUPPORTED_FORMATS, get_export_args
from src.utils.clean_name import clean_file_name

def upload_file():
    """
    Open a file dialog to select a file.

    Returns:
        str: Selected file path.
    """
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def select_folder():
    """
    Open a folder dialog to select a folder.

    Returns:
        str: Selected folder path.
    """
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path

def save_uploaded_file(file) -> Path:
    """
    Cleans the file name and saves it to a temp folder.
    Returns the path of the saved file.
    """
    temp_dir = Path(tempfile.mkdtemp())
    base_name = clean_file_name(file.filename)
    saved_path = temp_dir / base_name
    
    # Avoid overwriting if filename already exists
    counter = 1
    while saved_path.exists():
        saved_path = temp_dir / f"{saved_path.stem}_{counter}{saved_path.suffix}"
        counter += 1

    file.save(saved_path)
    return saved_path