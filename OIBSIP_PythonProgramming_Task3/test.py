import pyttsx3

engine = pyttsx3.init('sapi5')
engine.say("Hello, your voice assistant is working")
engine.runAndWait()