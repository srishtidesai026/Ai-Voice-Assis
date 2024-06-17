import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import sys
import subprocess
import pkg_resources

#Ensure pyaudio is installed
required = {'pyaudio'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

#if package is missing
if missing:
    print("Missing packages: ", missing)
    python = sys.executable
    try:
        subprocess.check_call([python, '-m', 'pip', 'install', *missing])
    except subprocess.CalledProcessError:
        print("Failed to install missing packages.")
        sys.exit(1)

#Initialize recognizer and text-to-speech engine (pyttsx3)
listener = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
    #Convert text to speech
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    #Listen for and recognize spoken instructions
    instruction = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            speech = listener.listen(source)
            instruction = listener.recognize_google(speech)
            print(f"Raw instruction: {instruction}")  # Debug print the raw instruction
            instruction = instruction.lower()
            if "jarvis" in instruction:
                instruction = instruction.replace("jarvis", "").strip()
                print(f"Recognized instruction: {instruction}")
            else:
                instruction = ""
    except sr.UnknownValueError:
        talk("Sorry, I did not catch that.")
        print("UnknownValueError: Could not understand audio")
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
        print("RequestError: Could not request results from Google Speech Recognition service")
    except Exception as e:
        talk("An error occurred.")
        print(f"Exception: {e}")
    return instruction

def play_Jarvis():
    #Main function to process instructions and perform actions
    instruction = input_instruction()
    if instruction:
        print(f"Processing instruction: {instruction}")
        if "play" in instruction:
            song = instruction.replace('play', "").strip()
            talk("Playing " + song)
            pywhatkit.playonyt(song)
        
        elif 'time' in instruction:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk("Current time is " + current_time)
        
        elif 'date' in instruction:
            current_date = datetime.datetime.now().strftime('%d/%m/%Y')
            talk("Today's date is " + current_date)
        
        elif 'how are you' in instruction:
            talk('I am fine, how about you?')
        
        elif 'what is your name' in instruction:
            talk('I am Jarvis, what can I do for you?')
        
        elif 'who is' in instruction:
            person = instruction.replace('who is', "").strip()
            info = wikipedia.summary(person, sentences=1)
            print(info)
            talk(info)
        
        else:
            talk('Please repeat...')
    else:
        talk('No instruction received.')
        print("No instruction received.")

#Start assistant
play_Jarvis()

