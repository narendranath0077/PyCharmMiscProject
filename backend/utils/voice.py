import whisper
import sounddevice as sd
import numpy as np

model = whisper.load_model("base")

def listen():
    samplerate = 16000
    duration = 5

    audio = sd.rec(int(duration * samplerate),
                   samplerate=samplerate,
                   channels=1,
                   dtype='float32')
    sd.wait()

    audio = np.squeeze(audio)

    result = model.transcribe(audio)
    return result["text"].strip()