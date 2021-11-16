import smtplib
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage


listener = sr.Recognizer()
engine = pyttsx3.init()

# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

def talk(text):
    voices = engine.getProperty('voices')
    #for voice in voices:
    #print(voice, voice.id)
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    #engine.stop()


def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('youremail@mail.com', 'YourPassword') #requires to switch to OFF less secure apps in google security settings
    email = EmailMessage()
    email['From'] = 'youremail@mail.com' # from whom email is sent
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)
    talk('Your message is sent')
    talk('Do you have another message?')
    send_more = get_info()
    if 'yes' in send_more:
        get_email_info()

def get_info():
    try:
        with sr.Microphone() as source:
            print('listening')
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(info)
            return info.lower()
    except:
        pass

email_list = {
    'contact': 'contactemail@mail.com'  #use key: email (speak onle the key word when asked
}

def get_email_info():
    talk("To whom would you like to send an email")
    name = get_info()
    receiver = email_list[name]
    print(receiver)
    talk("What is the subject of the email")
    subject = get_info()
    talk("What is your message")
    message = get_info()

    send_email(receiver, subject, message)

get_email_info()
