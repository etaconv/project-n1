import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import os

# 1. Setup Gemini AI
# Fixed: Added 'models/' prefix to avoid the 404 error
genai.configure(api_key="AIzaSyCq6t0u99uJAW0uCT0a_Qp-fDpY3uhKwEM")
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 2. Setup Voice (TTS)
engine = pyttsx3.init()
engine.setProperty('rate', 150) 

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    # Using device_index=5 from your hardware scan
    with sr.Microphone(device_index=5) as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except Exception:
            return None

# --- MAIN LOOP ---
speak("Hello! I am your Pi Assistant. How can I help you today?")

while True:
    user_input = listen()

    if user_input:
        if "exit" in user_input.lower() or "stop" in user_input.lower():
            speak("Goodbye!")
            break
        
        try:
            # Send text to Gemini
            response = model.generate_content(user_input)
            speak(response.text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            speak("I'm having trouble thinking right now.")
