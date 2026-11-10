
import os
import tempfile
from pathlib import Path

from pydub import AudioSegment


SUPPORTED_FORMATS = {
    ".wav", ".mp3", ".m4a", ".flac", ".ogg", ".wma"
}


def validate_audio_file(filename: str) -> None:
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported audio format: {extension}"
        )


def convert_to_wav(input_path: str) -> str:
    audio = AudioSegment.from_file(input_path)

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )
    temp_file.close()

    audio.export(temp_file.name, format="wav")

    return temp_file.name


def cleanup_file(file_path: str) -> None:
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
