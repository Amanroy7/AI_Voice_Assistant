import tkinter as tk
from tkinter import scrolledtext
import threading

# ---- Your existing code ----
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()

def talk(text):
    output_box.insert(tk.END, "Assistant: " + text + "\n")
    output_box.see(tk.END)
    
    # ✅ Reinitialize engine every time (fixes voice issue)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)   # female voice
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            output_box.insert(tk.END, "Listening...\n")
            output_box.see(tk.END)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'mira' in command:
                command = command.replace('alexa', '').strip()
    except sr.UnknownValueError:
        talk("Sorry, I did not understand that.")
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
    return command

def run_alexa():
    command = take_command()
    if command:
        output_box.insert(tk.END, "You said: " + command + "\n")
        output_box.see(tk.END)
        if 'play' in command:   
            song = command.replace('play', '').strip()
            talk('Playing ' + song)
            pywhatkit.playonyt(song)

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)

        elif 'search' in command or 'wikipedia' in command:
            query = command.replace('search', '').replace('wikipedia', '').strip()
            try:
                info = wikipedia.summary(query, sentences=2)
                talk("According to Wikipedia " + info)
                output_box.insert(tk.END, "Wikipedia: " + info + "\n")
                output_box.see(tk.END)
            except:
                talk("Sorry, I couldn't find anything on Wikipedia.")
                
        elif 'love' in command:
            talk('Sorry, I am AI, and I am in a relationship with the Internet.')
        elif 'mira' in command:
            talk('Yes, I am here. How can I help you?')
        elif 'how are you' in command:
            talk("I'm doing great, thank you for asking!")
        elif 'hello' in command or 'hi' in command:
            talk("Hello! How can I assist you today?")
        elif 'exit' in command or 'stop' in command or 'bye' in command:
            talk("Goodbye! Have a nice day.")
            return
        
        elif 'joke' in command:
            joke = pyjokes.get_joke()
            talk(joke)

        else:
            talk("This function is not available right now, I am working on it")
    else:
        talk("Please say something.")

# ---- Tkinter UI ----
def start_assistant():
    threading.Thread(target=run_alexa).start()

root = tk.Tk()
root.title("AI Voice Assistant (Mira)")
root.geometry("500x400")

label = tk.Label(root, text="Your AI Voice Assistant", font=("Arial", 16, "bold"))
label.pack(pady=10)

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Arial", 10))
output_box.pack(padx=10, pady=10)

start_button = tk.Button(root, text="🎤 Speak", command=start_assistant, font=("Arial", 12, "bold"), bg="lightblue")
start_button.pack(pady=10)

root.mainloop()
