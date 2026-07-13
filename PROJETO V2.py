import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import os
import time

# 1. Setup Gemini AI
genai.configure(api_key="AIzaSyCq6t0u99uJAWOuCTOa_Qp-fDpY3uhKwEM")
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Setup Voice (TTS)
engine = pyttsx3.init()
engine.setProperty('rate', 160) 

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    # We use a try block here to catch hardware 'busy' errors
    try:
        with sr.Microphone(device_index=5) as source:
            print("\nListening...")
            # Reduced duration to 0.5 for faster response
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Google Speech could not understand audio")
            return None
        except sr.RequestError:
            print("Could not request results; check internet")
            return None
    except Exception as e:
        print(f"Microphone Error: {e}")
        return None

# --- MAIN LOOP ---
speak("Hello! I am your Pi Assistant. How can I help you today?")

while True:
    user_input = listen()
    
    if user_input:
        user_input_lower = user_input.lower()
        if "exit" in user_input_lower or "stop" in user_input_lower:
            speak("Goodbye!")
            break
            
        # Send text to Gemini
        try:
            response = model.generate_content(user_input)
            speak(response.text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            speak("I'm having trouble thinking right now.")
    
    # Small pause to let the CPU breathe
    time.sleep(0.1)