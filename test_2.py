import random

import playsound
from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import os

import speech_recognition as sr
from gtts import gTTS


class Assist:
    def __init__(self):

        self.task()


    def speak(self, audio_string):
        tts = gTTS(text=audio_string, lang='en')
        r = random.randint(1, 1000000)
        audio_file = 'audio-' + str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        os.remove(audio_file)



    def record_audio(self, ask = False):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            if ask:
                self.speak(ask)

            audio = r.listen(source)
            voice_data = ''
            try:
                voice_data = r.recognize_google(audio)
            except sr.UnknowmValueError:
                self.speak('did not get that can you try again for me please ?')

            except sr.RequestError:
                self.speak('server is down')
            return voice_data


    def respond(self, voice_data):
        if 'name' in voice_data:
            self.speak('my name is alexa , i was made by Yassine Baghdadi')



    def task(self):
        self.speak('Hello dear how can i help you sur ?')
        voice_data = self.record_audio()
        self.respond(voice_data)


assist = Assist()