#!/usr/bin/env python3


from tkinter import *
from tkinter.filedialog import askopenfilename
import speech_recognition as sr
from pathlib import Path
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import subprocess
# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,

        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try: 
                text = r.recognize_google(audio_listened, language="de-DE")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
                nonsens = " "
                datei = open("Transscript.txt", "a")
                datei.write("\r\n" + chunk_filename + nonsens + text)
                datei.close()
                exit_code = subprocess.call("./Finish.sh")
                print(exit_code)
                return whole_text

    # return the text for all chunks detected
        
        
    
# def datei soll loadbar aufrufen welche am Ende des Aktion gestoppt werden soll

def datei():
    try:
        filename = askopenfilename()
        get_large_audio_transcription(filename)
    except FileNotFoundError:
        print("Error")
    except AttributeError:
        print("Error2")
def anleitung():
    root2 = Tk()
    root2.geometry("600x200")
    root2.title("Anleitung")
    frame = Frame(root2)
    frame.pack()
    
    sb = Scrollbar(frame, orient=HORIZONTAL)
    sb.pack(fill=X)
    lb = Listbox(frame, width=580, height=180, xscrollcommand=sb.set)
    lb.pack()

    lb.configure(xscrollcommand=sb.set)
    sb.config(command=lb.xview)
    
    lb.insert(0, "1.Anleitung")
    lb.insert(1, "2.Vorinformationen")
    lb.insert(2, "3.Achtung! Das Programm funktioniert nur mit .wav Datein!!!")
    lb.insert(3, "4.Sollten sie andere Audio Formate nutzen könnte es zu Problemen kommen.")
    lb.insert(4, "5.Das Programm benötigt eine Internetverbindung da es auf eine Datenbank zugreift.")
    lb.insert(5, "6.Der Transcripter arbeitet nicht 100% perfekt und hat Probleme mit Dialekten.")
    lb.insert(6, "7.Er kann nicht zwischen Stimmen unterscheiden.")
    lb.insert(7, "8.Nach Nutzung sollte der Text nochmal korrigiert werden.")
    lb.insert(8, "9.Dazu werden während des transkribieren Audio Chunks erstellt, jeweils versähen mit dem Namen des Chunks.")
    lb.insert(9, "10.Diese Chunks werden im selben Ordner in der sich auch das Programm befindet gespeichert.")
    lb.insert(10, "11.Zusätzlich wird der Text in der Datei ""Transscript.txt"" gespeichert welche auch im Ordner des Programms gespeichert wird.")
    lb.insert(11, "12.Begriffserklärung:")
    lb.insert(12, "Error:Eine Stelle wo keine Sprache erkannt worden ist. (Kann bei langem Atmen o.ä auftreten)")
 
    root2.mainloop()

def close():
    root.quit()

root = Tk()
root.title("PYTranscriptor")
root.geometry("200x200")
anleitungb = Button(root, text="Anleitung", command=anleitung)
close = Button(root, text="Close", command=close)
l1 = Label(root, text="Audio Datei:")
b1 = Button(root, text="Öffnen", command=datei)
b1.grid(row=1, column=2, pady=10)
l1.grid(row=1, column=1, padx=10)
close.grid(row=2, column=2)
anleitungb.grid(row=2, column=1)
root.mainloop()
