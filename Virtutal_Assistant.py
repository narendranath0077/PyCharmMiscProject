import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pyjokes


# Initialize the speaker
engine = pyttsx3.init()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
    return command

def run_assistant():
    command = listen()
    print("You said:", command)

    if 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('The time is ' + time)

    elif 'search' in command:
        search_term = command.replace('search', '')
        url = 'https://www.google.com/search?q=' + search_term
        webbrowser.open(url)
        talk('Here is what I found for ' + search_term)

    elif 'open youtube' in command:
        webbrowser.open('https://www.youtube.com')
        talk('Opening YouTube')

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)

    else:
        talk("Sorry, I didn't understand that.")

run_assistant()
