import whisper
import sounddevice as sd
import numpy as np

model = whisper.load_model("base")

def listen():
    try:
        samplerate = 16000
        duration = 5

        audio = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype='float32'
        )
        sd.wait()

        audio = np.squeeze(audio)

        # silence check
        if np.max(np.abs(audio)) < 0.01:
            return ""

        result = model.transcribe(audio, fp16=False)
        return result["text"].strip()

    except Exception:
        return ""