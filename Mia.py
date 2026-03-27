import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import requests
import pywhatkit
import wikipedia
import json
from twilio.rest import Client

account_sid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# Create a Twilio client object
client = Client(account_sid, auth_token)
# The phone number you want to call (in E.164 format)
to_number = '+91 xxxxxxxxx'
# The Twilio phone number to use as the caller ID (in E.164 format)
from_number = '+16xxxxxxx'
# The URL of the TwiML file that will handle the call
twiml_url = 'http://demo.twilio.com/docs/voice.xml'

engine=pyttsx3.init('sapi5')
voices=engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
message="I am in danger"

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")
    elif hour<=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am Virtual assistant, My name is Juno, Please tell me how may I help you")

def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=10)
        print("Listening....")
        speak("Listening")
        audio=r.listen(source)

    try:
        print("Recognizing")
        speak("Recognizing")
        query=r.recognize_google(audio,language="en-in")
        print(f"User said:{query}")


    except:
        stap="Say that again please...."
        print(stap)
        speak(stap)
        return "None"
    return query

def command_play_music(command):
    song = command.replace('play', '')
    speak('Playing ' + song)
    pywhatkit.playonyt('playing ' + song)

def command_search_wikipedia(command):
    person = command.replace('who is', '')
    info = wikipedia.summary(person, 2)
    print(info)
    speak(info)

def command_tell_joke():
    # Set the API endpoint URL
    url = "https://icanhazdadjoke.com/"

    # Set the headers for the HTTP GET request
    headers = {
        "Accept": "application/json"
    }

    # Make an HTTP GET request to the API endpoint
    response = requests.get(url, headers=headers)

    # Parse the JSON response
    data = json.loads(response.text)

    # Print the joke
    joke = data['joke']
    print(joke)
    speak(joke)

def command_tell_news():
    # Set the API endpoint URL and parameters
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",
        # Insert your api_key here
        "apiKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }

    # Make an HTTP GET request to the API endpoint
    response = requests.get(url, params=params)

    # Parse the JSON response
    data = json.loads(response.text)

    # Print the news headlines
    articles = data['articles']
    for article in articles:
        title = article['title']
        print(title)
        speak(title)

wishme()
while True:
    query=takecommand().lower()
    if "help" in query:
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url=twiml_url)

        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
    elif "who are you" in query:
        speak("I am your virtual assistant sir, my name is Jarvis sir")
    elif "what do you do" in query:
        speak("I can search google, open facebook, tell time, tell joke and tell news")
    elif "open facebook" in query:
        webbrowser.open("facebook.com")
    elif "sleep" in query:
        break
    elif 'play' in query:
        command_play_music(query)
    elif 'who is' in query:
        command_search_wikipedia(query)
    elif 'how are you' in query:
        speak('I am doing great')
        print('I am doing great')
    elif 'news' in query:
        command_tell_news()
    elif 'joke' in query:
        command_tell_joke()
    elif "open google" in query:
        webbrowser.open("google.com")
        speak("What do you want to search")
        print("Do you want to search")
        a = takecommand().lower()
        if "search google" in a:
            while True:
                s=takecommand().lower()
                if "close" in s:
                    speak("Exiting google...")
                    break
                elif "none" not in s:
                    webbrowser.open_new_tab(f"https://www.google.com/search?q={s}")
    elif "time now" in query:
        time_now=datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"time now is{time_now}")





