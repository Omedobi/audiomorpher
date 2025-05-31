import os, argparse
from pathlib import Path
import pandas as pd
from pydub import AudioSegment
from mutagen import File as MutagenFile

SUPPORTED_FORMATS = ['mp3', 'wav', 'flac', 'ogg', 'wma', 'aac', 'm4a', 'opus']


def convert_audio(input_path, output_format, output_dir=None, bitrate=None):
    input_path = Path(input_path)
    if input_path.suffix[1:].lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported input format: {input_path.suffix}")
    
    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported output format: {output_format}")
    
    audio = AudioSegment.from_file(input_path)
    
    if output_dir:
        output_path = Path(output_dir) / f"{input_path.stem}.{output_format}"
    else:
        output_path = input_path.with_suffix(f".{output_format}")
  
    export_args = {}
    if bitrate:
            export_args['bitrate'] = bitrate
            
    audio.export(output_path, format=output_format, **export_args)
        
        
    # get metadata
    try:
        original_metadata = MutagenFile(str(input_path), easy=True)
        if original_metadata:
            converted_metadata = MutagenFile(str(output_path), easy=True)
            if converted_metadata:
                for tag in original_metadata:
                    converted_metadata[tag] = original_metadata[tag]
                converted_metadata.save() 
    except Exception:
        pass
    print(f"Converted {input_path} to {output_path} with bitrate {bitrate}.")
    
def batch_convert(input_dir, output_format, output_dir=None, bitrate=None):
    input_dir = Path(input_dir)
    for file in input_dir.rglob("*"):
        if file.suffix[1:].lower() in SUPPORTED_FORMATS:
            try:
                convert_audio(file, output_format, output_dir, bitrate)
            except Exception as e:
                print(f"Failed to convert {file.name}: {e}")                
  
          
def main():
    parser = argparse.ArgumentParser(description="AudioMorpher: Convert audio formats via CLI")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("output_format", help="Desired output format (e.g., mp3, wav, flac, wma,ogg)")
    parser.add_argument("--output_dir", help="Directory to save converted files")
    parser.add_argument("--bitrate", help="Bitrate for output audio (e.g., 128k)")

    args = parser.parse_args()

    input_path = Path(args.input)
    if input_path.is_file():
        convert_audio(args.input, args.output_format, args.output_dir, args.bitrate)
    elif input_path.is_dir():
        batch_convert(args.input, args.output_format, args.output_dir, args.bitrate)
    else:
        print("Error: Invalid input path")


if __name__ == "__main__":
    main()