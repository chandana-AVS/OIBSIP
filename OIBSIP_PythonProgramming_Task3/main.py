
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import smtplib
import requests


def web_search(query):
    speak(f"Searching for {query}")
    webbrowser.open(
        f"https://www.google.com/search?q={query}"
    )


def speak(text):
    print("Assistant:", text)
    
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

def take_command():
    listener = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)

            audio = listener.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            print("Recognizing...")
            command = listener.recognize_google(audio, language="en-US")
            command = command.lower()

            print("You said:", command)
            return command

        except sr.WaitTimeoutError:
            print("No speech detected")
            return ""

        except sr.UnknownValueError:
            print("Could not understand")
            return ""

        except sr.RequestError:
            print("Network issue. Check internet.")
            speak("Internet connection issue")
            return ""

        except KeyboardInterrupt:
            print("Stopped manually")
            return "stop"

        except Exception as e:
            print("Error:", e)
            return ""
        
def send_email(to, subject, message):
    sender_email = "avschandana@gmail.com"
    app_password = "YOUR_APP_PASSWORD"  # NOT normal password

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)

        email = f"Subject: {subject}\n\n{message}"

        server.sendmail(sender_email, to, email)
        server.quit()

        speak("Email sent successfully")

    except Exception as e:
        print("Email Error:", e)
        speak("Sorry, I was not able to send the email")


def run_assistant():        
    speak("Voice assistant started")

    while True:
        command = take_command()
        print("DEBUG COMMAND:", repr(command))  

        if not command:
            continue

        if "hello" in command:
            speak("Hello, how can I help you?")

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")

        elif "date" in command:
            today = datetime.datetime.now().strftime("%B %d %Y")
            speak(f"Today's date is {today}")

        elif "google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "whatsapp" in command:
            speak("Opening WhatsApp")
            webbrowser.open("https://web.whatsapp.com")
        
        elif "search for" in command:
            query = command.replace("search for", "").strip()
            web_search(query)
            
    
        elif "weather" in command:
            speak("Opening weather report")
            webbrowser.open("https://www.google.com/search?q=weather")
        
        elif "motivate me" in command:
            speak("Success comes to those who keep learning and never give up")
        
        elif "play" in command:
            song = command.replace("play", "")
            speak(f"Playing {song}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        
        elif "send email" in command or "email" in command or "mail" in command:
            speak("Starting email process") 
            speak("Who should I send it to?")
            username = take_command().replace(" ", "")

            to = username + "@gmail.com"

            print("Recipient:", to)
            speak(f"Sending email to {username}")
            speak("What is the subject?")
            subject = take_command()

            speak("What is the message?")
            message = take_command()
            send_email(to, subject, message)
        
        elif "stop" in command:
            speak("Goodbye! reach out if you need anything else.")
            break

        elif "thank you" in command or "thanks" in command or "thank" in command:
            speak("You're welcome. Happy to help.")
        
        else:
            print("ELSE BLOCK HIT")
            print("COMMAND WAS:", repr(command))
            speak("Sorry, I did not understand that command")
        


run_assistant()