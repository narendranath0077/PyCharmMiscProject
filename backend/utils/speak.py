import pyttsx3
import threading

engine = pyttsx3.init()

def _speak(text):
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()

def speak_async(text):
    thread = threading.Thread(target=_speak, args=(text,))
    thread.start()