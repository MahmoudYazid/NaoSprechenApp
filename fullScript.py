# -*- coding: utf-8 -*-
import requests
import speech_recognition as sr
from naoqi import ALProxy 



def ask_gpt(prompt):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyC7uO2DyDrB7HWUFXxLZ5ZxE7NNvtrbHIE"
        headers = {
            "Content-Type": "application/json"
        }
        prompt = prompt + " "+"Bitte antworten Sie kurz und ohne ö oder ü oder ä "
        data = {"contents": [{"parts": [{"text": "{}".format(prompt)}]}]}
        
        response = requests.post(url, headers=headers, json=data)
       
        
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def recognize_speech():
        with sr.Microphone() as source:
            tts = ALProxy("ALTextToSpeech", "172.16.1.110", 9559)

            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source) 
            text = u"stell sie ein frage"  # Prefix the string with 'u' to make it Unicode
            text_encoded = text.encode('utf-8')  # Encode it to UTF-8

            # Now pass it to tts.say
            tts.say("{}".format(text_encoded))
           
            audio = recognizer.listen(source)  # Listen for audio

            try:
                # Recognize speech using Google Web Speech API
                text = recognizer.recognize_google(audio, language='de-DE')
                
                print(text)
                if(text is not list or tuple):
                    return str(text).encode('utf-8') 
                else:
                     return "das ist ein list"
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                return None
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return None
def connect_to_nao():
    try:
        
        tts = ALProxy("ALTextToSpeech", "172.16.1.110", 9559)
        ourSpeak = recognize_speech()
        AskAi = ask_gpt(ourSpeak)
        print(AskAi)
        response = CleanResponse(AskAi )
         # Print debug information
        print("Response before encoding: ", response)  # Check the response
        print("Type of response:", type(response))  # Should be str or unicode

        # Ensure response is a Unicode string (Python 3 does this by default)
        text_encoded = response.encode('utf-8')  # Encode to UTF-8
        
        print("Encoded response:", text_encoded)  # Print the encoded response for debugging

        # Use the correct format for NAO TTS
        tts.say(text_encoded)  # Directly use the encoded bytes
    except Exception as e:
        print("Could not connect to NAO: {}".format(e))


def CleanResponse (text):
     return text.replace('*', ' ').replace('\n', ' ').replace('...', ' ').replace('_', ' ').strip().encode('utf-8')



def AntwortNichtMehrAls3Liene():
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyC7uO2DyDrB7HWUFXxLZ5ZxE7NNvtrbHIE"
        headers = {
            "Content-Type": "application/json"
        }
        data = {"contents": [{"parts": [{"text": "{}".format("Bitte antworten Sie kurz")}]}]}
        
        requests.post(url, headers=headers, json=data)
       
        
while(True) :
    AntwortNichtMehrAls3Liene()
    connect_to_nao()