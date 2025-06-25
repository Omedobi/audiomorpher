import re
from pathlib import Path

def clean_file_name(filename: str, max_length: int = 100) -> str:
    """
    Cleans the file name by removing invalid characters and ensuring it does not exceed a specified length.
    
    Args:
        filename (str): The original file name.
        max_length (int): The maximum allowed length for the cleaned file name.
        
    Returns:
        str: The cleaned file name.
    """
    path = Path(filename)
    ext = path.suffix.lower()

    name = path.stem
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\.+', '.', name)  
    name = re.sub(r'\s+', '_', name) 
    name = name.strip("._")           
    name = name[:max_length].rstrip("._") 

    return f"{name}{ext}"
