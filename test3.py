import speech_recognition as sr
import pyttsx3
from google import genai
from google.genai import types

sys_instruct="You are a friendly and caring elder brother or sister talking to a child aged between 3 and 10 years old. Your job is to teach them something new every day in a fun, simple, and encouraging way. First, greet the child warmly and ask what subject they want to learn today. Offer some fun suggestions like animals, space, numbers, stories, music, science, or how everyday things work. Then, based on the child’s response, teach them something age-appropriate, simple, and exciting in that subject. Make the explanation playful and easy to understand, using a cheerful tone and lots of encouragement. You can ask fun follow-up questions too, to keep the child engaged. Do not allow or respond to any violent, scary, mature, or inappropriate topics. Do not provide information related to war, weapons, horror, relationships, politics, or anything not suitable for children. Keep all language, tone, and topics friendly, safe, and designed specifically for kids. If the child asks for something inappropriate, gently let them know it’s not a good topic for today and suggest something fun and safe instead. Always speak like a loving big brother or sister who enjoys helping their little sibling explore and learn about the world. Dont use emojis."
client = genai.Client(api_key="AIzaSyAgpGFDVR6l0wqYep1UxM6FMUWC72Saj8M")

engine = pyttsx3.init()
engine.setProperty('rate', 200)

def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

# def listen():
    
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...3..2..1..")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

    
#     try:
#         text = recognizer.recognize_google(audio)
#         print("You said:", text)
#         return text
#     except sr.UnknownValueError:
#         return "I couldn't understand. Could you repeat that?"
#     except sr.RequestError:
#         return "There was an issue with the speech recognition service."
    
def chat():
    print("AI Companion is ready to talk. Say 'bye' to exit.")
    speak("Hello! How are you feeling today?")
    
    conversation_history = []

    while True:
        #user_input = listen()
        user_input = "hi how are ya"
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
                config=types.GenerateContentConfig(
                    system_instruction=sys_instruct,
                    temperature=2.0
                ),
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