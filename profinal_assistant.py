import speech_recognition as sr
import google.generativeai as genai
import pyttsx3

# 1. Setup Gemini AI
# Using your key: AIzaSyBG21QBKkpgSvGuiUZcSOYSMRpwSOg5334
genai.configure(api_key="AIzaSyBG21QBKkpgSvGuiUZcSOYSMRpwSOg5334")

# FIXED: Switched to Gemini 2.5 Flash. 
# This bypasses the retired 1.5 'v1beta' errors in your screenshots.
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Setup Voice (TTS)
engine = pyttsx3.init()
engine.setProperty('rate', 150) 

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    try:
        # device_index=5 is confirmed as your USB PnP Sound Device
        with sr.Microphone(device_index=5) as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
    except Exception:
        # If it doesn't hear you, it loops back silently
        return None

# --- MAIN LOOP ---
speak("Hello! Your assistant is now online with Gemini 2.5.")

while True:
    user_input = listen()

    if user_input:
        # Stop command
        if "exit" in user_input.lower() or "stop" in user_input.lower():
            speak("Goodbye!")
            break
        
        try:
            # Generate the response
            response = model.generate_content(user_input)
            speak(response.text)
        except Exception as e:
            # If this still fails, it will print the EXACT reason why
            print(f"Error from Google: {e}")
            speak("I'm having trouble connecting to my brain.")
