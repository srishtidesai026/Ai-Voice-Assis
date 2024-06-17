import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

contacts = {
    'srishti' : '+919108733432',
    "amma": '+919900020138',
    "appaji": '+919620702889',
    "pratiksha": '+918722728004'
}



def speak(text):
    machine = pyttsx3.init()
    machine.say(text)
    machine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-India')
            print(f"User said: {query}")
        except Exception as e:
            speak("Sorry, I didn't catch that. Could you say it again please?")
            return None
    return query

def send_whatsapp_message(phone_number, message):
    # Assuming you want to send the message immediately, let's set the time 2 minutes from now.
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute + 2  # Adding 2 minutes to current time to avoid errors
    if minute >= 60:
        hour += 1
        minute -= 60
    speak(f"Sending WhatsApp message to {phone_number}")
    pywhatkit.sendwhatmsg(f"+91{phone_number}", message, hour, minute, 15, True, 5)
    speak("Message sent.")


def handle_query(query):
    if 'play' in query:
        song = query.replace('play', '')
        speak(f'Playing {song}')
        pywhatkit.playonyt(song)
        return 1
    elif 'search for' in query:
        search_query = query.replace('search for', '')
        speak(f'Searching for {search_query}')
        pywhatkit.search(search_query)
        return 1
    elif 'time' in query:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f'The current time is {current_time}')
    elif 'date' in query:
         current_date = datetime.datetime.now().strftime('%d/%m/%Y')
         speak(f'The date today is {current_date}')
    elif 'who is' in query:
        person = query.replace('who is', '')
        info = wikipedia.summary(person, sentences=2)
        print(info)
        speak(info)
        return 1
    elif 'what is your name' in query:
            speak('I am Jarvis, what can I do for you?')
    elif 'stop' in query:
            return 1
    elif 'date' in query:
            current_date = datetime.datetime.now().strftime('%d/%m/%Y')
            speak("Today's date is " + current_date)
    elif 'how is your day' in query:
            speak("Awesome!! How about you ? Hope you had a good day too!!")
    elif 'send message to' in query:
        try:
            contact_name = query.split('send message to')[1].split('saying')[0].strip().lower()
            message = query.split('saying')[1].strip()
            if contact_name in contacts:
                phone_number = contacts[contact_name]
                send_whatsapp_message(phone_number, message)
            else:
                speak(f"Sorry, you don't have a contact named {contact_name}")
        except Exception as e:
            speak("Sorry, I couldn't understand the message details.")
            print(e)
            return 1
    elif 'thank you' in query:
            speak("No Problem!!")
            return 1
    else:
        speak("I can do more if you teach me!")


def main():
    while True:
        query = listen()
        if query:
            if  handle_query(query):
                break

if __name__ == "__main__":
    speak("Hello, I am Jarvis, your AI assistant. How can I help you today?")
    main()

