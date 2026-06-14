# Voice Assistant using Python

## Overview

This project is a Python-based Voice Assistant that listens to user voice commands, processes them using speech recognition, and performs various tasks such as opening websites, searching the web, sending emails, providing date and time information, and responding with voice output.

The assistant uses Speech Recognition for voice input and Text-to-Speech (TTS) for voice responses, creating a hands-free interactive experience.

## Features

- Voice-based interaction
- Text-to-Speech responses
- Speech Recognition using Google Speech API
- Tell current date and time
- Open Google, YouTube, and WhatsApp Web
- Search the web using voice commands
- Play songs on YouTube
- Send emails using Gmail SMTP
- Respond to greetings and thank-you messages
- Error handling for speech recognition and network issues

## Technologies Used

- Python
- SpeechRecognition
- pyttsx3
- smtplib
- Webbrowser
- Datetime

## Installation

1. Clone or download the project.

2. Install the required libraries:

```bash
pip install SpeechRecognition
pip install pyttsx3
pip install pyaudio
pip install wikipedia
```

3. Run the application:

```bash
python main.py
```

## Available Voice Commands

### Greetings

- hello
- hi

### Date and Time

- what is the time
- what is the date

### Open Websites

- open google
- open youtube
- open whatsapp

### Web Search

- search for python programming
- search for machine learning

### Play Music

- play shape of you
- play alan walker songs

### Email

- send email
- email

### Exit

- stop
- exit

## Project Workflow

1. User speaks a command.
2. SpeechRecognition converts speech into text.
3. The assistant analyzes the command.
4. Corresponding action is performed.
5. pyttsx3 converts the response into speech.

## Future Enhancements

- Weather updates using APIs
- News headlines
- AI-powered question answering
- Dynamic reminders and alarms
- Smart home device integration
- Calendar and event management
- Voice authentication

## Author

Chandana Aravelli

## License

This project is developed for learning and educational purposes.
