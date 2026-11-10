
from faster_whisper import WhisperModel


# Load model once when the application starts
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(audio_path: str, language: str = None):
    segments, info = model.transcribe(
        audio_path,
        language=language,
        beam_size=5,
        vad_filter=True,
        word_timestamps=True
    )

    results = []

    for segment in segments:
        words = []

        if segment.words:
            for word in segment.words:
                words.append({
                    "word": word.word,
                    "start": round(word.start, 2),
                    "end": round(word.end, 2)
                })

        results.append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip(),
            "words": words
        })

    return {
        "language": info.language,
        "language_probability": round(info.language_probability, 3),
        "segments": results
    }
