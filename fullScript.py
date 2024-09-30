import requests
import speech_recognition as sr
from naoqi import ALProxy 

# -*- coding: utf-8 -*-

def ask_gpt(prompt):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyC7uO2DyDrB7HWUFXxLZ5ZxE7NNvtrbHIE"
        headers = {
            "Content-Type": "application/json"
        }
        data = {"contents": [{"parts": [{"text": "{}".format(prompt)}]}]}
        
        response = requests.post(url, headers=headers, json=data)
       
        print(response.json())
        print(response.json()["candidates"][0]["content"]["parts"][0]["text"])
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def recognize_speech():
        with sr.Microphone() as source:
            tts = ALProxy("ALTextToSpeech", "172.16.1.110", 9559)

            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source) 
            text = u"ich kann ihnen horen ?"  # Prefix the string with 'u' to make it Unicode
            text_encoded = text.encode('utf-8')  # Encode it to UTF-8

            # Now pass it to tts.say
            tts.say("{}".format(text_encoded))
            print("start listening") # Adjust for ambient noise
            audio = recognizer.listen(source)  # Listen for audio

            try:
                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio, language='de-DE')
                print("You said: " + text)
                return text
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                return None
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return None
def connect_to_nao():
    try:
        
        tts = ALProxy("ALTextToSpeech", "172.16.1.110", 9559)
        
        response = CleanResponse(ask_gpt(recognize_speech()))
        text_encoded = response.encode('utf-8')

        tts.say("{}".format(text_encoded))
        print(response )
    except Exception as e:
        print("Could not connect to NAO: {}".format(e))


def CleanResponse (text):
     return text.replace('*', '').replace('\n', '').replace('...', '').replace('_', '').strip()




connect_to_nao()
