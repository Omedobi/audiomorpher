import zipfile
import tempfile
from pathlib import Path
from tkinter import Tk, filedialog
from pydub import AudioSegment
from utils.audio_convert import convert_audio, SUPPORTED_FORMATS, get_export_args

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

