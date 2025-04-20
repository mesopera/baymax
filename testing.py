import speech_recognition as sr
import pyttsx3
from google import genai
from google.genai import types

sys_instruct = "Act like an AI companion and a friend. Keep the conversation engaging, remember past discussions, and respond naturally."

client = genai.Client(api_key="AIzaSyAgpGFDVR6l0wqYep1UxM6FMUWC72Saj8M")

engine = pyttsx3.init()
engine.setProperty('rate', 200)

def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def chat():
    print("AI Companion is ready to talk. Say 'bye' to exit.")
    speak("Hello! How are you feeling today?")
    
    conversation_history = []  

    while True:
        user_input = listen()
        if not user_input:  
            speak("I couldn't understand. Could you repeat that?")
            continue

        if user_input.lower() in ["bye", "exit", "quit"]:
            speak("Goodbye! Take care.")
            break

        conversation_history.append(f"User: {user_input}")

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(system_instruction=sys_instruct),
                contents=conversation_history,
            )

            reply = response.text
            print(reply)
            speak(reply)

            conversation_history.append(f"AI: {reply}") 

        except Exception as e:
            print("Error:", str(e))
            speak("Sorry, there was an error.")

chat()
