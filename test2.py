import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

speak("Hello! How are you feeling today?")