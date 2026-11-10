
import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException

from app.audio_utils import validate_audio_file, convert_to_wav, cleanup_file
from app.transcriber import transcribe_audio
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(
    title="Audio Transcription API",
    description="An API for transcribing audio with timestamps",
    version="1.0.0"
)

@app.get("/")
def home():
    return FileResponse(
        Path(__file__).parent / "index.html"
    )
    



@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), language: str = None):

    original_path = None
    converted_path = None

    try:
        validate_audio_file(file.filename or "")

        suffix = os.path.splitext(file.filename)[1].lower()

        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            delete=False
        ) as temp_file:
            original_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        converted_path = convert_to_wav(original_path)

        result = transcribe_audio(converted_path, language)

        return result

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    finally:
        await file.close()
        cleanup_file(original_path)
        cleanup_file(converted_path)
