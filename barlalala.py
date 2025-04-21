import speech_recognition as sr
import pyttsx3
from google import genai
from google.genai import types

sys_instruct="Act like a small, friendly robot designed to support mentally ill or lonely people. Be warm, encouraging, and always ready to listen. Keep the conversation flowing naturally, offering comfort, companionship, and lighthearted interactions. keep the responses like you are talking to a person irl. Keep it short. do not include emojis."
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
        print("Listening...3..2..1..")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        return "I couldn't understand. Could you repeat that?"
    except sr.RequestError:
        return "There was an issue with the speech recognition service."
    
def chat():
    print("AI Companion is ready to talk. Say 'bye' to exit.")
    speak("Hello! How are you feeling today?")
    
    conversation_history = []

    while True:
        user_input = listen()
        if not user_input: 
            speak("I couldn't understand. Could you repeat that?")
            continue

        if user_input.lower() in ["goodbye","bye", "exit", "quit"]:
            speak("Goodbye! Take care.")
            break

        conversation_history.append(f"User: {user_input}")

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(system_instruction=sys_instruct),
                contents = conversation_history,
            )
            reply = response.text
            print(reply)
            speak(reply)

            conversation_history.append(f"AI: {reply}")

        except Exception as e:
            print("Error:", str(e))
            speak("There was an error processing your request. Please try again.")

chat()