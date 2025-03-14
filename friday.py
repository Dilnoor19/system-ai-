import requests
import datetime
import time
import pyautogui
import pyttsx3
import speech_recognition as sr
import webbrowser
import os 
import json

# Chat bot
API_KEY = "YOUR_GEMINI_API_KEY"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def chat_with_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            return "Error: Unexpected response format."
    return f"Error {response.status_code}: {response.text}"

# initialization
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate',rate-50)
volume = engine.getProperty('volume')
engine.setProperty('volume', volume+0.25)
 
# speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# fun system
def fun():
    jokes = pyjokes.get_joke()
    speak(jokes)
    

# listing function
def listen_to_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.5)
        print("listening.........", end="",flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=3000
        r.phrase_time_limit=10
        audio = r.listen(source)
    try:
        print("\r", end="",flush=True)
        print("recognizing.......", end="",flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r", end="",flush=True)
        print(f"user said: {query}\n")
    except Exception as e:
        print("say that again please")
        return "none"
    return query

# jarvis day system
def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict ={
        1:"Monday", 
        2:"Tuesday",    
        3:"Wednesday",
        4:"Thirsday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"  
    }
    return day_dict.get(day,"unknown")


# time teller
def show_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Current time: {current_time}")
    speak(f"Current time: {current_time}")

# schdule function
def schedule():
    day = cal_day().lower()
    week = {
        "monday": "hey boss , today you have to attend college from 2pm to 6pm , after 7 pm you to do little workout , then 10pm to 12am you have to study college subject or do homework and at last work on previous project or practice new projects or you can also listen lecture"   ,      
        "tuesday":  "hey boss , today you have to attend college from 2pm to 6pm , after 7 pm you to do little workout , then 10pm to 12am you have to study college subject or do homework and at last work on previous project or practice new projects or you can also listen lecture"   ,      
        "wednesday": "hey boss , today you have to attend college from 2pm to 6pm , after 7 pm you to do little workout , then 10pm to 12am you have to study college subject or do homework and at last work on previous project or practice new projects or you can also listen lecture"  ,
        "thirsday": "hey boss , today you have to attend college from 2pm to 6pm , after 7 pm you to do little workout , then 10pm to 12am you have to study college subject or do homework and at last work on previous project or practice new projects or you can also listen lecture" ,
        "friday": "hey boss , today you have to attend college from 2pm to 6pm , after 7 pm you to do little workout , then 10pm to 12am you have to study college subject or do homework and at last work on previous project or practice new projects or you can also listen lecture" ,
        "saturday": "hey boss today is our college holiday so you have to study atleast 3hrs between 12pm tpo 6pm ,you have to do workout at 7pm  and then after dinner yu have to take language lectures or you can also do coding depend on you, remember not to waste time on laptop and mobile " ,
        "sunday":  " boss today is sunday so today you don't have to workout but don't forget to take proper meal and try to study for atleast few time and remeber to revise your week"      
    }
    if day in week.keys():
        speak(week[day])

# website opener        
def open_website(query):
    websites = {
        "anime": "https://hianime.to/",
        "discord": "https://discord.com/",
        "instagram": "https://www.instagram.com/",
        "gpt" : "https://chatgpt.com/?model=auto" ,
        "type test" : " https://www.typingtest.com/",
        "github" : "https://github.com/"
    }
    query = query.lower()  
    for name, url in websites.items():
        if f"open {name}" in query:
            try:
                webbrowser.open(url)
                speak(f"Opening your {name}")
                print(f"Opening your {name}")
            except Exception as e:
                print(f"Failed to open {name}: {e}")
                speak(f"Sorry, I couldn't open {name}.")
            return True 
    return False

# wishing system 
def wishme():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()
    work = schedule()

    if (hour>=0) and (hour<=12) and ('AM' in t ):
        speak(f"good morning boss ,it's {day} and the time is {t} , task you have to {work} ")
    elif (hour>=12) and (hour<=16) and ('PM' in t ):
        speak(f"good AFternoon boss ,it's {day} and the time is {t}, task you have to do {work} ")
    else:
        speak(f"good evening boss ,it's {day} and the time is {t}, have a good night boss ")
     
# application opener
def open_apps(query):
    apps = { 
       "brave": "C:/Users/dilno/OneDrive/Desktop/Brave.lnk",
        "spotify": "C:/Users/dilno/OneDrive/Desktop/Spotify.lnk" ,
        "calculator": "C:/Users/dilno/OneDrive/Desktop/Calculator.lnk",
        "whatsapp": "C:/Users/dilno/OneDrive/Desktop/WhatsApp.lnk",
        "youtube": "C:/Users/dilno/OneDrive/Desktop/YouTube.lnk" ,
        "vs code" : "C:/Users/dilno/OneDrive/Desktop/Visual Studio Code.lnk" ,
        "store" : "C:/Users/dilno/OneDrive/Desktop/Microsoft Store.lnk" ,
        "classroom" : "C:/Users/dilno/OneDrive/Desktop/Google Classroom.lnk", 
        "chrome" : "C:/Users/Public/Desktop/Google Chrome.lnk" ,
        "microsoft edge" : "C:/Users/Public/Desktop/Microsoft Edge.lnk" ,
        "copilet" : "C:/Users/dilno/OneDrive/Desktop/Copilot.lnk",
        "c drive" : "c:" ,
        "camera" : "C:/Users/dilno/OneDrive/Desktop/Camera.lnk"
    } 
    query = query.lower()
    for name, url in apps.items():
        if f"open {name}" in query: 
            try: 
                os.startfile(url) 
                speak(f"Opening your {name}") 
                print(f"Opening your {name}") 
            except Exception as e:
                print(f"Failed to open {name}: {e}") 
                speak(f"Sorry, I couldn't open {name}.") 
            return True
    return False

# main commands recever and decison maker
def personal_assistant(): 
    wishme()
    speak("Friday rebooting.........!!")
    while True: 
        command = listen_to_command()
        if command:
            command = command.lower() 
            if "open " in command:
                if not open_website(command):
                    if not open_apps(command):
                        speak("Website or application not found.")
            elif"something funny" in command:
                fun()
            elif "time" in command:
                show_time() 
            elif "schedule" in command:
                schedule()
            elif("volume up" in command) or ("increase volume" in command):
                pyautogui.press("volumeup")
                speak("volume increased")
            elif("volume down" in command) or ("decrease volume" in command):
                pyautogui.press("volumedown")
                speak("volume decreased")
            elif("volume mute" in command) or ("mute the sound" in command):
                pyautogui.press("volumemute")
                speak("volume muted")
            elif "exit" in command or "stop" in command:
                print("Goodbye!")
                speak("Goodbye!")
                break
            else:
                response = chat_with_gemini(command)
                speak(response)

personal_assistant()
