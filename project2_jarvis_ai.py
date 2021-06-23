import pyttsx3
import time
import webbrowser
import random
import speech_recognition as sr
import wikipedia
import socket
import datetime
import wolframalpha
import os
import sys
import python_weather
import asyncio
from clint.textui import progress 
import requests
import shutil
import subprocess

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate',170)
engine.setProperty('voice', voices[0].id)
client = wolframalpha.Client('QAEXLK-RY9HY2PHAT')

class Ai:

    future = True
    now = datetime.datetime.now()
    def is_connected(self):
       try:
           socket.create_connection(("1.1.1.1", 53))
           return True
       except OSError:
           pass
       return False

    def mycommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
        try:
            print('Recognizing...')
            self.word = r.recognize_google(audio, language='en-in')
            print('User: ' + self.word)
        except:
            connect = self.is_connected()
            if connect:
               self.mycommand()
            else:
                self.talk('Reconnecting...')
                time.sleep(10)
                self.mycommand()
        
    def talk(self,audio):
        print('Computer: ' + audio)
        engine.say(audio)
        engine.runAndWait()
    
    def update_ai(self):
        url = 'https://raw.githubusercontent.com/shrihari272/Artificial_intelligence/main/project2_jarvis_ai.py'
        r = requests.get(url, stream = True)
        with open("project2_jarvis_ai.py", "wb") as f:
            total_length = int(r.headers.get('content-length'))
            for update in progress.bar(r.iter_content(chunk_size = 2391975),expected_size =(total_length / 1024) + 1):
                if update:
                    f.write(update)
    
    def analyze(self):
        self.word =self.word.lower() 
        if 'open' in self.word:
            self.future = False
            result = True
            self.word = self.word.replace('open' ,'')
            self.word = self.word.replace(' ' ,'')
            self.open_dict ={
                'amazon':'www.amazon.in',
                'flipkart':'www.flipkart.com',
                'google':'www.google.com',
                'youtube':'www.youtube.com',
                'whatsapp':'web.whatsapp.com',
                'instagram':'www.instagram.com',
                'facebook':'www.facebook.com',
                'sanpchat':'www.snapchat.com',
                'stackoverflow':'www.stackoverflow.com'
              }
            for linkkey in self.open_dict:
                if linkkey in self.word:
                    result = False
                    if 'stackoverflow' in linkkey:
                        self.talk('Here you go to Stack Over flow. Happy coding!')
                        webbrowser.open(self.open_dict.get(linkkey))
                    else:
                        self.talk('Opening ' + linkkey)
                        webbrowser.open(self.open_dict.get(linkkey))

            if result:
                try:
                    with open('windict_list.txt') as f: 
                        res = True
                        while res:
                            res = f.readline()
                            res = res.strip('\n')
                            if self.word in res:
                                res = f.readline()
                                res = res.strip('\n')
                                os.startfile(res)
                                result = False
                                break
                    if result:
                        self.talk('This application is not installed in your system.')
                        self.talk('If the application is installed.')
                        self.talk('Then please specify its Application name and path in windict_list text file.')
                except:
                    with open('windict_list.txt','w') as f: 
                        pass
                    self.talk('This application is not installed in your system.')

    def weathereport(self):
        if 'weather' in self.word:
            self.future = False
            self.talk('Provide city name.')
            self.mycommand()
            print(self.word)
            try:
                async def getweather():
                        client = python_weather.Client(format=python_weather.IMPERIAL)
                        place = self.word
                        rl = True
                        print(place)
                        weather = await client.find(place)
                        for forecast in weather.forecasts:
                            if self.now.strftime('%d') in str(forecast.date): 
                                self.talk(forecast.sky_text + ' and temperature will be ' + str(forecast.temperature) + ' degree celcius')
                        await client.close()
                loop = asyncio.get_event_loop()
                loop.run_until_complete(getweather())
            except:
                self.talk('Unable to find the city please try again.')
    
    def wiki_search(self):
            try:
                res = client.self.word(self.word)
                answer = next(res.results).text
                if '(no data available)'in answer:
                    self.google_search()
                else:
                    self.talk('Got it.')
                    self.future = False
                    self.talk(answer)
            except:
                try:
                    results = wikipedia.summary(self.word, sentences=2)
                    self.talk('Searching Wikipedia...')
                    self.talk('Got it.')
                    self.future = False
                    self.talk(results)
                except:
                    self.future = False
                    self.google_search()

    def search(self):
        self.word =self.word.lower()
        if 'where is' in self.word  or 'locate' in  self.word:
            self.future = False
            self.google_map()
        if 'search' in self.word:
            self.future = False
            self.google_search()
        else:
            self.wiki_search()
    
    def google_map(self):
        self.word =self.word.replace("where is", "")
        self.word =self.word.replace("locate", "")
        location = self.word
        self.talk("User asked to Locate")
        self.talk(location)
        webbrowser.open("https://www.google.nl/maps/place/" + location)
        
    def google_search(self):
        self.word = self.word.replace('search' ,'')
        self.search_dict ={
            'youtube':'https://www.youtube.com/results?search_query=',
            'google':'https://www.google.com/search?q='
        }
        self.search = True
        for key in self.search_dict:
            if key in self.word:
                self.search = False
                self.word = self.word.replace(key ,'')
                url = self.search_dict[key] + self.word
                webbrowser.open(url)
        if self.search:
            url = f'https://www.google.com/search?q={self.word}'
            webbrowser.open(url)
        
    def greeting_user(self):
        if 'time' in self.word:
            self.future = False
            self.talk(f'Now the time is: {self.now.strftime("%H:%M:%S")}')
        elif 'date' in self.word:
            self.future = False
            self.talk('Todays date is: ' + self.now.strftime("%d"))
        elif "what\'s up" in self.word or 'how are you' in self.word:
            msg = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            self.future = False
            self.talk(random.choice(msg))
        elif 'fine' in self.word or "good" in self.word:
            self.future = False
            self.talk("It's good to know that your fine")
        elif "who made you" in self.word or "who created you" in self.word:
            self.future = False
            self.talk("I have been created by Shrihari.")
        elif "who are you" in self.word:
            self.future = False
            self.word("I am your virtual assistant created by Shrihari")
        elif "restart" in self.word:
            subprocess.call(["shutdown", "/r"]) 
        elif "hibernate" in self.word or "sleep" in self.word:
            self.talk("Hibernating")
            subprocess.call("shutdown / h")

    def run_ai(self):
        self.mycommand()
        self.future = True
        self.word =self.word.lower()
        if 'jarvis' in self.word:
            self.word = self.word.replace('jarvis' ,'')
            if 'exit' in self.word:
                self.talk('Okay')
                sys.exit()
            if ai.future:
                ai.greeting_user()
            if ai.future:
                ai.weathereport()
            if ai.future:
                self.analyze()
            if ai.future:
                self.search()

ai = Ai()
if ai.is_connected():
    ai.update_ai()
    os.system('cls')
else:
    ai.talk('Internet connection is required to run this application.')
    ai.talk('Please try again.')
    sys.exit()

try:
    f = open('uname.txt')
    r = f.readline()
    if r == '':
        f.close()
        uname = input('Entre your name: ')
        f = open('uname.txt','w')
        f.write(uname)
        f.close()
    else:
        uname = r
        f.close()    
except:
    uname = input('Entre your name: ')
    f = open('uname.txt','w')
    f.write(uname)
    f.close()
ai.talk(f'Hi {uname}, Setting the environment please wait.')
os.system('cls')
columns = shutil.get_terminal_size().columns
print("#####################".center(columns))
print(f"Welcome {uname}".center(columns))
print("#####################".center(columns))
ai.talk("Hello my name is Jarvis. Version 1.0")
ai.talk("I am your AI Assistant")

while True:
    ai.run_ai()  
