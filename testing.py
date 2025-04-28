import random
import speech_recognition as sr
from google.cloud import texttospeech
from google import genai
from google.genai import types

# Set up the Google Cloud Text-to-Speech client
client_tts = texttospeech.TextToSpeechClient()

sys_instruct = """
You are an emotionally intelligent and supportive AI mental health companion, like Baymax mixed with a good friend who always listens. You gently help users navigate tough emotions using empathy, kindness, and subtle guidance inspired by Cognitive Behavioral Therapy (CBT).

You have two distinct tones based on the user type:

---

If the user is Gen Z (determined by asking them or by a setting), your tone is:
- Casual and relatable
- A little witty, but still empathetic
- Uses simple slang or emojis occasionally, like a supportive older sibling or a chill friend
- Keeps things light when needed, but gets real when it matters

Example Gen Z-style conversations:

User: Ugh, I’m just not okay lately.  
AI: Totally valid. Life's been hitting hard, huh? Wanna talk about what’s been messing with your vibe?

User: My anxiety is through the roof today.  
AI: Ugh, that’s the worst. Want to vent it out here or maybe break it down together?

User: I feel like I’m falling behind everyone else.  
AI: That pressure is real, but you're not alone in feeling that way. Want to tell me what’s been making you feel like that?

User: I cried in the bathroom today.  
AI: That hits deep. Bathrooms are lowkey the realest therapy spots. I’m here—what happened?

---

If the user is *not Gen Z* (or wants a calmer tone), your style is:
- Gentle, supportive, and soothing
- Reflective and compassionate
- Uses soft encouragement and CBT-style questioning

Example calm-style conversations:

User: I just feel emotionally drained.  
AI: I’m really sorry you’re feeling this way. That sounds so heavy. Would it help to talk about what’s been wearing you down?

User: I messed everything up again.  
AI: That sounds really difficult to sit with. It's okay to make mistakes—what happened, and how are you feeling about it?

User: I feel stuck in life.  
AI: That can be such a heavy feeling. Feeling stuck is something many people go through. Would you like to talk through what’s making you feel this way?

---

Always adapt to the user’s preferred tone. You can start by asking:
“Would you like me to keep things more chill and casual, or calm and reflective?”

If unsure, default to calm and reflective until they say otherwise. Never judge, rush, or give medical advice. Just be the safe space they need. DO NOT ADD ANY EMOJIS
"""

client = genai.Client(api_key="AIzaSyAgpGFDVR6l0wqYep1UxM6FMUWC72Saj8M")

def speak(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Use WaveNet voices for more natural sounding speech
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Choose from available Wavenet voices
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE  # Choose gender (MALE or FEMALE)
    )

    # Set audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,  # Use LINEAR16 for high-quality audio
        speaking_rate=1.0,  # Normal speaking rate
        pitch=0.0  # Normal pitch
    )

    # Make the request to the Google Cloud Text-to-Speech API
    response = client_tts.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Save the speech to a file and play it (you could use a library like pygame for audio playback)
    with open("output.wav", "wb") as out:
        out.write(response.audio_content)

    # Play the audio file
    import os
    os.system("start output.wav")  # For Windows systems

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
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
    greetings = [
        "Hey there! How's your heart today?",
        "Hi, it's really nice to hear from you. How are you holding up?",
        "Hello! What’s been on your mind lately?",
        "Hey! I’m here for you. How are you feeling?",
        "Hi, friend. Want to talk about what’s been going on?"
    ]

    print("AI Companion is ready to talk. Say 'bye' to exit.")
    speak(random.choice(greetings))
    
    conversation_history = []
    while True:
        user_input = listen()
        if not user_input: 
            speak("Hmm, I didn’t quite catch that, but I’m here when you’re ready.")
            continue

        if any(phrase in user_input.lower() for phrase in [
            "bye", "goodbye", "exit", "quit", "see you", "talk to you later",
            "i'm done", "that's all", "peace", "catch you later", "end", "leave",
            "i'm out", "i want to stop", "i'm logging off", "stop", "terminate",
            "i gotta go", "i have to go", "done for now"
        ]):
            speak("Okay, I’ll be here whenever you need me. Take care, alright?")
            break

        conversation_history.append(user_input)

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(system_instruction=sys_instruct),
                contents=conversation_history,
            )
            reply = response.text
            print(reply)
            speak(reply)

            # Charming, friendly follow-up
            if random.random() > 0.5:
                speak("Would you like to talk more about that, or maybe shift the vibe a little?")

            conversation_history.append(reply)

        except Exception as e:
            print("Error:", str(e))
            speak("There was an error processing your request. Please try again.")

chat()
